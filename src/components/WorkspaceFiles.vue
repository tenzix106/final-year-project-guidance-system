<template>
  <div class="flex flex-col h-full bg-white rounded-lg border border-gray-200">
    <!-- Files Header -->
    <div class="px-4 py-3 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900 flex items-center space-x-2">
        <FolderOpen class="w-5 h-5" />
        <span>Shared Files</span>
      </h3>
      <button
        @click="showUploadModal = true"
        :disabled="!canUpload"
        class="px-3 py-1.5 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-1.5 text-sm"
      >
        <Upload class="w-4 h-4" />
        <span>Upload</span>
      </button>
    </div>

    <!-- Files List -->
    <div class="flex-1 overflow-y-auto p-4" style="max-height: 400px;">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-8">
        <Loader2 class="w-6 h-6 animate-spin text-primary-600" />
      </div>

      <!-- Empty State -->
      <div v-else-if="files.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500">
        <FolderOpen class="w-12 h-12 mb-2 text-gray-400" />
        <p>No files uploaded yet</p>
        <button
          v-if="canUpload"
          @click="showUploadModal = true"
          class="mt-3 text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          Upload your first file
        </button>
      </div>

      <!-- Files Grid -->
      <div v-else class="space-y-2">
        <div
          v-for="file in files"
          :key="file.id"
          class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <div class="flex items-center space-x-3 flex-1 min-w-0">
            <!-- File Icon -->
            <component
              :is="getFileIconComponent(file.file_type)"
              class="w-8 h-8 text-primary-600 flex-shrink-0"
            />
            
            <!-- File Info -->
            <div class="flex-1 min-w-0">
              <h4 class="text-sm font-medium text-gray-900 truncate">
                {{ file.original_filename }}
              </h4>
              <div class="flex items-center space-x-2 text-xs text-gray-500 mt-0.5">
                <span>{{ formatFileSize(file.file_size) }}</span>
                <span>•</span>
                <span>{{ file.uploader_name || file.uploader_email }}</span>
                <span>•</span>
                <span>{{ formatDate(file.created_at) }}</span>
              </div>
              <p v-if="file.description" class="text-xs text-gray-600 mt-1 truncate">
                {{ file.description }}
              </p>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center space-x-2 ml-3">
            <button
              @click="handleDownload(file)"
              class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Download"
            >
              <Download class="w-4 h-4 text-gray-600" />
            </button>
            <button
              v-if="canDelete(file)"
              @click="handleDelete(file.id)"
              class="p-2 hover:bg-red-50 rounded-lg transition-colors"
              title="Delete"
            >
              <Trash2 class="w-4 h-4 text-red-600" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Modal -->
    <transition name="modal">
      <div
        v-if="showUploadModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
        @click.self="closeUploadModal"
      >
        <div class="bg-white rounded-xl shadow-2xl max-w-lg w-full p-6" @click.stop>
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-semibold text-gray-900">Upload File</h3>
            <button @click="closeUploadModal" class="p-1 hover:bg-gray-100 rounded-lg transition-colors">
              <X class="w-5 h-5 text-gray-600" />
            </button>
          </div>

          <form @submit.prevent="handleUpload">
            <!-- File Input -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Select File <span class="text-red-500">*</span>
              </label>
              <div
                class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors cursor-pointer"
                @click="$refs.fileInput.click()"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
                :class="{ 'border-primary-500 bg-primary-50': isDragging }"
              >
                <input
                  ref="fileInput"
                  type="file"
                  @change="handleFileSelect"
                  class="hidden"
                />
                <Upload class="w-10 h-10 mx-auto mb-2 text-gray-400" />
                <p v-if="!selectedFile" class="text-sm text-gray-600">
                  Click to select or drag and drop
                </p>
                <p v-else class="text-sm text-gray-900 font-medium">
                  {{ selectedFile.name }}
                </p>
                <p class="text-xs text-gray-500 mt-1">
                  Max size: 50MB
                </p>
              </div>
            </div>

            <!-- Description -->
            <div class="mb-6">
              <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
                Description (Optional)
              </label>
              <textarea
                id="description"
                v-model="uploadDescription"
                rows="3"
                placeholder="Add a description for this file..."
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              ></textarea>
            </div>

            <!-- Error Message -->
            <div v-if="uploadError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-sm text-red-700">{{ uploadError }}</p>
            </div>

            <!-- Actions -->
            <div class="flex space-x-3">
              <button
                type="button"
                @click="closeUploadModal"
                class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="!selectedFile || uploading"
                class="flex-1 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                <Loader2 v-if="uploading" class="w-4 h-4 animate-spin" />
                <Upload v-else class="w-4 h-4" />
                <span>{{ uploading ? 'Uploading...' : 'Upload' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  FolderOpen, Upload, Download, Trash2, X, Loader2,
  FileText, Image, Video, File, Archive, Sheet
} from 'lucide-vue-next'
import fileService from '../services/fileService.js'
import { currentUser } from '../services/authService.js'

const props = defineProps({
  workspace: {
    type: Object,
    required: true
  }
})

const files = ref([])
const loading = ref(false)
const showUploadModal = ref(false)
const selectedFile = ref(null)
const uploadDescription = ref('')
const uploading = ref(false)
const uploadError = ref('')
const isDragging = ref(false)

const currentUserId = computed(() => currentUser.value?.id)
const canUpload = computed(() => {
  if (!currentUser.value) return false
  if (props.workspace.owner_id === currentUserId.value) return true
  // Check if user has edit permission
  const member = props.workspace.members?.find(m => m.user_id === currentUserId.value)
  return member?.can_edit || false
})

const canDelete = (file) => {
  if (!currentUser.value) return false
  // Owner, admin, or file uploader can delete
  if (props.workspace.owner_id === currentUserId.value) return true
  if (file.uploaded_by === currentUserId.value) return true
  const member = props.workspace.members?.find(m => m.user_id === currentUserId.value)
  return member?.role === 'admin' || member?.role === 'owner'
}

onMounted(async () => {
  await loadFiles()
})

const loadFiles = async () => {
  loading.value = true
  try {
    files.value = await fileService.getFiles(props.workspace.id)
  } catch (error) {
    console.error('Failed to load files:', error)
  } finally {
    loading.value = false
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    uploadError.value = ''
  }
}

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) {
    selectedFile.value = file
    uploadError.value = ''
  }
}

const handleUpload = async () => {
  if (!selectedFile.value) return
  
  uploadError.value = ''
  uploading.value = true
  
  try {
    await fileService.uploadFile(
      props.workspace.id,
      selectedFile.value,
      uploadDescription.value
    )
    
    await loadFiles()
    closeUploadModal()
  } catch (error) {
    uploadError.value = error.message || 'Failed to upload file'
  } finally {
    uploading.value = false
  }
}

const handleDownload = async (file) => {
  try {
    await fileService.downloadFile(props.workspace.id, file.id, file.original_filename)
  } catch (error) {
    console.error('Failed to download file:', error)
    alert('Failed to download file')
  }
}

const handleDelete = async (fileId) => {
  if (!confirm('Are you sure you want to delete this file?')) return
  
  try {
    await fileService.deleteFile(props.workspace.id, fileId)
    await loadFiles()
  } catch (error) {
    console.error('Failed to delete file:', error)
    alert(error.message || 'Failed to delete file')
  }
}

const closeUploadModal = () => {
  showUploadModal.value = false
  selectedFile.value = null
  uploadDescription.value = ''
  uploadError.value = ''
  isDragging.value = false
}

const getFileIconComponent = (fileType) => {
  if (!fileType) return File
  
  if (fileType.startsWith('image/')) return Image
  if (fileType.startsWith('video/')) return Video
  if (fileType === 'application/pdf') return FileText
  if (fileType.includes('zip') || fileType.includes('rar') || fileType.includes('7z')) return Archive
  if (fileType.includes('word') || fileType.includes('document')) return FileText
  if (fileType.includes('excel') || fileType.includes('spreadsheet')) return Sheet
  if (fileType.includes('powerpoint') || fileType.includes('presentation')) return FileText
  
  return File
}

const formatFileSize = (bytes) => {
  return fileService.formatFileSize(bytes)
}

const formatDate = (dateString) => {
  const date = new Date(dateString + 'Z')
  const now = new Date()
  const diff = now - date
  
  // Less than 1 hour
  if (diff < 3600000) {
    const mins = Math.floor(diff / 60000)
    return mins < 1 ? 'Just now' : `${mins}m ago`
  }
  
  // Today
  if (date.toDateString() === now.toDateString()) {
    return 'Today at ' + date.toLocaleTimeString('en-MY', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true
    })
  }
  
  // Yesterday
  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)
  if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday'
  }
  
  // This year
  if (date.getFullYear() === now.getFullYear()) {
    return date.toLocaleDateString('en-MY', { month: 'short', day: 'numeric' })
  }
  
  // Different year
  return date.toLocaleDateString('en-MY', { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
