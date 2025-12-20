# Composables

Reusable composition functions for the FYP Guidance System.

## Available Composables

### `useAdminApi`
Centralized admin API operations with consistent error handling.

**Usage:**
```javascript
import { useAdminApi } from '@/composables/useAdminApi'

const { loading, error, fetchOverviewStats, fetchUsers } = useAdminApi()

// Fetch stats
const stats = await fetchOverviewStats()

// Fetch users with filters
const users = await fetchUsers({ page: 1, per_page: 20, role: 'student' })
```

**Available Methods:**
- `fetchOverviewStats()` - Get system overview statistics
- `fetchUsageStats()` - Get usage analytics
- `fetchUsers(params)` - Get users with pagination/filters
- `updateUserRole(userId, role)` - Update user role
- `fetchTopics(params)` - Get topics with pagination/filters
- `deleteTopic(topicId)` - Delete a topic
- `fetchAISettings()` - Get AI provider settings

### `useErrorHandler`
Consistent error handling and user-friendly error messages.

**Usage:**
```javascript
import { useErrorHandler } from '@/composables/useErrorHandler'

const { error, isError, handleError, clearError, withErrorHandling } = useErrorHandler()

// Manual error handling
try {
  await someAsyncOperation()
} catch (err) {
  handleError(err, 'Custom fallback message')
}

// Automatic error handling
const safeOperation = withErrorHandling(
  async () => await someAsyncOperation(),
  'Operation failed'
)
await safeOperation()
```

### `useLoading`
Loading state management with optional messages.

**Usage:**
```javascript
import { useLoading } from '@/composables/useLoading'

const { isLoading, loadingMessage, startLoading, stopLoading, withLoading } = useLoading()

// Manual loading control
startLoading('Fetching data...')
await fetchData()
stopLoading()

// Automatic loading control
const fetchWithLoading = withLoading(
  async () => await fetchData(),
  'Fetching data...'
)
await fetchWithLoading()
```

## Best Practices

1. **Combine composables** for comprehensive state management:
```javascript
const { isLoading, withLoading } = useLoading()
const { error, withErrorHandling } = useErrorHandler()
const { fetchOverviewStats } = useAdminApi()

const loadStats = withLoading(
  withErrorHandling(
    async () => await fetchOverviewStats(),
    'Failed to load statistics'
  ),
  'Loading statistics...'
)
```

2. **Use destructuring** to only import what you need
3. **Handle errors appropriately** - use fallback messages for better UX
4. **Provide loading feedback** for all async operations
