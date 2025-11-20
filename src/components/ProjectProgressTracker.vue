<template>
  <div class="progress-tracker">
    <!-- Header Section -->
    <div class="tracker-header">
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Project Timeline</h2>
          <p class="text-gray-600">Track your progress through each phase of development</p>
        </div>
        <div class="text-right">
          <div class="text-3xl font-bold text-primary-600">{{ overallProgress }}%</div>
          <div class="text-sm text-gray-500">Overall Progress</div>
        </div>
      </div>
      
      <!-- Overall Progress Bar -->
      <div class="mt-6">
        <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div 
            class="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full transition-all duration-500"
            :style="{ width: overallProgress + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600">Loading timeline...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
      {{ error }}
    </div>

    <!-- Timeline Display -->
    <div v-else-if="phases.length > 0" class="timeline-container">
      <div 
        v-for="(phase, index) in phases" 
        :key="phase.id"
        class="phase-card"
        :class="getPhaseStatusClass(phase.status)"
      >
        <!-- Phase Header -->
        <div class="phase-header" @click="togglePhase(phase.id)">
          <div class="flex items-center gap-4 flex-1">
            <!-- Phase Number Badge -->
            <div class="phase-badge" :class="getPhaseBadgeClass(phase.status)">
              <span v-if="phase.status === 'completed'" class="text-white text-lg">✓</span>
              <span v-else class="text-white font-semibold">{{ index + 1 }}</span>
            </div>

            <!-- Phase Info -->
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-1">
                <h3 class="text-lg font-semibold text-gray-800">{{ phase.phase_name }}</h3>
                <span class="status-badge" :class="getStatusBadgeClass(phase.status)">
                  {{ formatStatus(phase.status) }}
                </span>
              </div>
              <p class="text-sm text-gray-600">{{ phase.description }}</p>
              <div class="flex items-center gap-4 mt-2 text-sm text-gray-500">
                <span>⏱️ {{ phase.estimated_duration_weeks }} weeks</span>
                <span>📋 {{ phase.tasks?.length || 0 }} tasks</span>
                <span>✅ {{ getCompletedTaskCount(phase) }} completed</span>
              </div>
            </div>

            <!-- Expand Icon -->
            <div class="text-gray-400 transition-transform" :class="{ 'rotate-180': expandedPhases.has(phase.id) }">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </div>
          </div>
        </div>

        <!-- Phase Progress Bar -->
        <div class="px-6 pb-4">
          <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="getProgressBarClass(phase.status)"
              :style="{ width: phase.progress_percentage + '%' }"
            ></div>
          </div>
          <div class="text-xs text-gray-500 mt-1 text-right">{{ phase.progress_percentage }}%</div>
        </div>

        <!-- Tasks List (Expandable) -->
        <div v-if="expandedPhases.has(phase.id)" class="phase-tasks">
          <div class="px-6 pb-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="font-semibold text-gray-700">Tasks</h4>
              <button 
                @click="showAddTask(phase.id)"
                class="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1"
              >
                <span>+</span> Add Task
              </button>
            </div>

            <!-- Add Task Form -->
            <div v-if="addingTaskToPhase === phase.id" class="mb-4 p-3 bg-gray-50 rounded-lg">
              <input 
                v-model="newTaskTitle"
                @keyup.enter="addTask(phase.id)"
                @keyup.esc="cancelAddTask"
                type="text"
                placeholder="Enter task title..."
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
                autofocus
              />
              <div class="flex gap-2 mt-2">
                <button 
                  @click="addTask(phase.id)"
                  class="px-3 py-1 bg-primary-600 text-white rounded text-sm hover:bg-primary-700"
                >
                  Add
                </button>
                <button 
                  @click="cancelAddTask"
                  class="px-3 py-1 bg-gray-300 text-gray-700 rounded text-sm hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>

            <!-- Task Items -->
            <div v-if="phase.tasks && phase.tasks.length > 0" class="space-y-2">
              <div 
                v-for="task in phase.tasks" 
                :key="task.id"
                class="task-item group"
                :class="{ 'completed': task.is_completed }"
              >
                <label class="flex items-center gap-3 cursor-pointer flex-1">
                  <input 
                    type="checkbox"
                    :checked="task.is_completed"
                    @change="toggleTask(phase.id, task.id)"
                    class="w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500 cursor-pointer"
                  />
                  <span class="flex-1" :class="{ 'line-through text-gray-400': task.is_completed }">
                    {{ task.task_name }}
                  </span>
                </label>
                <button 
                  @click="deleteTask(phase.id, task.id)"
                  class="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 transition-opacity text-sm"
                >
                  Delete
                </button>
              </div>
            </div>
            <div v-else class="text-center py-4 text-gray-400 text-sm">
              No tasks yet. Click "Add Task" to get started!
            </div>
          </div>
        </div>

        <!-- Phase Actions -->
        <div class="phase-actions">
          <button 
            v-if="phase.status === 'not_started'"
            @click="updatePhaseStatus(phase.id, 'in_progress')"
            class="btn-action bg-primary-600 hover:bg-primary-700 text-white"
          >
            Start Phase
          </button>
          <button 
            v-else-if="phase.status === 'in_progress'"
            @click="updatePhaseStatus(phase.id, 'completed')"
            class="btn-action bg-green-600 hover:bg-green-700 text-white"
          >
            Mark Complete
          </button>
          <button 
            v-else-if="phase.status === 'completed'"
            @click="updatePhaseStatus(phase.id, 'in_progress')"
            class="btn-action bg-gray-500 hover:bg-gray-600 text-white"
          >
            Reopen Phase
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="text-6xl mb-4">📋</div>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">No Timeline Yet</h3>
      <p class="text-gray-500">Progress tracking hasn't been initialized for this project.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import progressService from '../services/progressService.js';

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
});

// State
const phases = ref([]);
const isLoading = ref(false);
const error = ref(null);
const expandedPhases = ref(new Set());
const addingTaskToPhase = ref(null);
const newTaskTitle = ref('');

// Computed
const overallProgress = computed(() => {
  if (phases.value.length === 0) return 0;
  const total = phases.value.reduce((sum, phase) => sum + phase.progress_percentage, 0);
  return Math.round(total / phases.value.length);
});

// Methods
const loadProgress = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const data = await progressService.getProgress(props.projectId);
    phases.value = data.phases || [];
    // Auto-expand the first in-progress or not-started phase
    const activePhase = phases.value.find(p => p.status === 'in_progress' || p.status === 'not_started');
    if (activePhase) {
      expandedPhases.value.add(activePhase.id);
    }
  } catch (err) {
    error.value = err.message || 'Failed to load progress timeline';
    console.error('Error loading progress:', err);
  } finally {
    isLoading.value = false;
  }
};

const togglePhase = (phaseId) => {
  if (expandedPhases.value.has(phaseId)) {
    expandedPhases.value.delete(phaseId);
  } else {
    expandedPhases.value.add(phaseId);
  }
};

const updatePhaseStatus = async (phaseId, newStatus) => {
  try {
    await progressService.updatePhaseStatus(props.projectId, phaseId, newStatus);
    await loadProgress();
  } catch (err) {
    console.error('Error updating phase status:', err);
    error.value = 'Failed to update phase status';
  }
};

const toggleTask = async (phaseId, taskId) => {
  try {
    await progressService.toggleTask(props.projectId, phaseId, taskId);
    await loadProgress();
  } catch (err) {
    console.error('Error toggling task:', err);
    error.value = 'Failed to update task';
  }
};

const showAddTask = (phaseId) => {
  addingTaskToPhase.value = phaseId;
  newTaskTitle.value = '';
};

const cancelAddTask = () => {
  addingTaskToPhase.value = null;
  newTaskTitle.value = '';
};

const addTask = async (phaseId) => {
  if (!newTaskTitle.value.trim()) return;
  
  try {
    await progressService.addTask(props.projectId, phaseId, newTaskTitle.value.trim());
    await loadProgress();
    cancelAddTask();
  } catch (err) {
    console.error('Error adding task:', err);
    error.value = 'Failed to add task';
  }
};

const deleteTask = async (phaseId, taskId) => {
  if (!confirm('Are you sure you want to delete this task?')) return;
  
  try {
    await progressService.deleteTask(props.projectId, phaseId, taskId);
    await loadProgress();
  } catch (err) {
    console.error('Error deleting task:', err);
    error.value = 'Failed to delete task';
  }
};

// Helper functions
const getPhaseStatusClass = (status) => {
  return {
    'completed': status === 'completed',
    'in-progress': status === 'in_progress',
    'blocked': status === 'blocked'
  };
};

const getPhaseBadgeClass = (status) => {
  const classes = {
    'not_started': 'bg-gray-400',
    'in_progress': 'bg-primary-600',
    'completed': 'bg-green-600',
    'blocked': 'bg-red-600'
  };
  return classes[status] || 'bg-gray-400';
};

const getStatusBadgeClass = (status) => {
  const classes = {
    'not_started': 'bg-gray-100 text-gray-700',
    'in_progress': 'bg-blue-100 text-blue-700',
    'completed': 'bg-green-100 text-green-700',
    'blocked': 'bg-red-100 text-red-700'
  };
  return classes[status] || 'bg-gray-100 text-gray-700';
};

const getProgressBarClass = (status) => {
  const classes = {
    'not_started': 'bg-gray-400',
    'in_progress': 'bg-gradient-to-r from-primary-500 to-primary-600',
    'completed': 'bg-green-500',
    'blocked': 'bg-red-500'
  };
  return classes[status] || 'bg-gray-400';
};

const formatStatus = (status) => {
  const labels = {
    'not_started': 'Not Started',
    'in_progress': 'In Progress',
    'completed': 'Completed',
    'blocked': 'Blocked'
  };
  return labels[status] || status;
};

const getCompletedTaskCount = (phase) => {
  if (!phase.tasks) return 0;
  return phase.tasks.filter(task => task.is_completed).length;
};

// Lifecycle
onMounted(() => {
  loadProgress();
});

// Watch for project changes
watch(() => props.projectId, () => {
  loadProgress();
});
</script>

<style scoped>
.progress-tracker {
  max-width: 1200px;
  margin: 0 auto;
}

.tracker-header {
  background: #E67E22;
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(230, 126, 34, 0.3);
}

.timeline-container {
  position: relative;
  padding-left: 2rem;
}

.timeline-container::before {
  content: '';
  position: absolute;
  left: 1.875rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, #e5e7eb, #d1d5db);
}

.phase-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  margin-left: 2rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
}

.phase-card::before {
  content: '';
  position: absolute;
  left: -2.875rem;
  top: 2rem;
  width: 1rem;
  height: 1rem;
  background: white;
  border: 3px solid #e5e7eb;
  border-radius: 50%;
  z-index: 1;
}

.phase-card.in-progress {
  border-color: rgba(230, 126, 34, 0.3);
  box-shadow: 0 4px 20px rgba(230, 126, 34, 0.15);
}

.phase-card.in-progress::before {
  border-color: #E67E22;
  background: #E67E22;
  box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.2);
}

.phase-card.completed {
  border-color: rgba(16, 185, 129, 0.3);
}

.phase-card.completed::before {
  border-color: #10b981;
  background: #10b981;
}

.phase-header {
  padding: 1.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.phase-header:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.phase-badge {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.phase-tasks {
  border-top: 1px solid #e5e7eb;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.task-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s;
}

.task-item:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.task-item.completed {
  opacity: 0.7;
}

.phase-actions {
  padding: 0 1.5rem 1.5rem;
  display: flex;
  gap: 0.75rem;
}

.btn-action {
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.btn-action:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.rotate-180 {
  transform: rotate(180deg);
}
</style>
