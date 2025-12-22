const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

class FileService {
  getAuthHeaders() {
    const token = localStorage.getItem('auth_token')
    const headers = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    return headers
  }

  async getFiles(workspaceId) {
    const response = await fetch(`${API_BASE_URL}/api/files/${workspaceId}/files`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to fetch files')
    }

    const data = await response.json()
    return data.files
  }

  async uploadFile(workspaceId, file, description = '') {
    const formData = new FormData()
    formData.append('file', file)
    if (description) {
      formData.append('description', description)
    }

    const response = await fetch(`${API_BASE_URL}/api/files/${workspaceId}/files`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: formData
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to upload file')
    }

    return await response.json()
  }

  getDownloadUrl(workspaceId, fileId) {
    const token = localStorage.getItem('auth_token')
    return `${API_BASE_URL}/api/files/${workspaceId}/files/${fileId}/download?token=${token}`
  }

  async downloadFile(workspaceId, fileId, filename) {
    const response = await fetch(`${API_BASE_URL}/api/files/${workspaceId}/files/${fileId}/download`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to download file')
    }

    // Create blob and trigger download
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  async deleteFile(workspaceId, fileId) {
    const response = await fetch(`${API_BASE_URL}/api/files/${workspaceId}/files/${fileId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to delete file')
    }

    return await response.json()
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  getFileIcon(fileType) {
    if (!fileType) return 'File'
    
    if (fileType.startsWith('image/')) return 'Image'
    if (fileType.startsWith('video/')) return 'Video'
    if (fileType === 'application/pdf') return 'FileText'
    if (fileType.includes('zip') || fileType.includes('rar') || fileType.includes('7z')) return 'Archive'
    if (fileType.includes('word') || fileType.includes('document')) return 'FileText'
    if (fileType.includes('excel') || fileType.includes('spreadsheet')) return 'Sheet'
    if (fileType.includes('powerpoint') || fileType.includes('presentation')) return 'Presentation'
    
    return 'File'
  }
}

const fileService = new FileService()
export default fileService
