import { ref } from "vue";
import authService from './authService.js';
import { API_BASE_URL } from '../config/api.js';

class FavouriteService {
  constructor() {
    this.baseUrl = API_BASE_URL;
    this.favourites = ref([]);
    this.isLoading = ref(false);
  }

  getAuthHeaders() {
    return authService.getAuthHeaders();
  }

  async getFavourites() {
    this.isLoading.value = true;
    try {
      if (!authService.authenticated) {
        throw new Error("No auth token found");
      }
      const response = await fetch(`${this.baseUrl}/api/favourites`, {
        headers: this.getAuthHeaders(),
      });
      if (!response.ok) {
        throw new Error("Failed to fetch favourites");
      }

      const data = await response.json();
      this.favourites.value = data.favourites;
      return this.favourites.value;
    } catch (error) {
      console.error("Error fetching favourites:", error);
      this.favourites.value = [];
      throw error;
    } finally {
      this.isLoading.value = false;
    }
  }

  async saveFavourite(topicData, notes = "") {
    this.isLoading.value = true;
    try {
      if (!authService.authenticated) {
        throw new Error("No auth token found");
      }
      
      // Map frontend topic structure to backend expected structure
      const mappedTopicData = {
        title: topicData.title,
        description: topicData.description,
        difficulty: topicData.difficulty,
        timeline: topicData.duration || topicData.timeline, // Map duration to timeline
        tags: topicData.tags || [],
        resources: topicData.resources || []
      };
      
      console.log("Sending request to:", `${this.baseUrl}/api/favourites`);
      console.log("With headers:", this.getAuthHeaders());
      console.log("With body:", JSON.stringify({ topicData: mappedTopicData, notes }));
      
      const response = await fetch(`${this.baseUrl}/api/favourites`, {
        method: "POST",
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ topicData: mappedTopicData, notes }),
      });
      
      if (!response.ok) {
        let errorMessage = "Failed to save favourite";
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (e) {
          errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        }
        console.error("Backend error details:", errorMessage);
        throw new Error(errorMessage);
      }

      const data = await response.json();

      // Refresh favourites list
      await this.getFavourites();

      return data;
    } catch (error) {
      console.error("Error saving favourite:", error);
      throw error;
    } finally {
      this.isLoading.value = false;
    }
  }

  async removeFavourite(favouriteId) {
    this.isLoading.value = true;
    try {
      if (!authService.authenticated) {
        throw new Error("No auth token found");
      }
      const response = await fetch(
        `${this.baseUrl}/api/favourites/${favouriteId}`,
        {
          method: "DELETE",
          headers: this.getAuthHeaders(),
        }
      );
      if (!response.ok) {
        throw new Error("Failed to remove favourite");
      }

      // Update local state
      this.favourites.value = this.favourites.value.filter(
        (fav) => fav.id !== favouriteId
      );

      return await response.json();
    } catch (error) {
      console.error("Remove Favourite Error:", error);
      throw error;
    } finally {
      this.isLoading.value = false;
    }
  }

  async updateNotes(favouriteId, notes, progressStatus = null) {
    this.isLoading.value = true;
    try {
      if (!authService.authenticated) {
        throw new Error("No auth token found");
      }

      const body = { notes };
      if (progressStatus) {
        body.progress_status = progressStatus;
      }

      const response = await fetch(
        `${this.baseUrl}/api/favourites/${favouriteId}/notes`,
        {
          method: "PUT",
          headers: this.getAuthHeaders(),
          body: JSON.stringify(body),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update notes");
      }

      // Update local favourites list
      const favouriteIndex = this.favourites.value.findIndex(
        (fav) => fav.id === favouriteId
      );
      if (favouriteIndex !== -1) {
        this.favourites.value[favouriteIndex].user_notes = notes;
        if (progressStatus) {
          this.favourites.value[favouriteIndex].status = progressStatus;
        }
      }

      return await response.json();
    } catch (error) {
      console.error("Update Notes Error:", error);
      throw error;
    } finally {
      this.isLoading.value = false;
    }
  }

  async checkFavouriteStatus(topicTitle) {
    try {
      if (!authService.authenticated) {
        return { is_favourite: false };
      }
      
      const encodedTitle = encodeURIComponent(topicTitle);
      const response = await fetch(
        `${this.baseUrl}/api/favourites/check/${encodedTitle}`,
        {
          headers: this.getAuthHeaders(),
        }
      );
      
      if (response.ok) {
        return await response.json();
      }
      
      return { is_favourite: false };
    } catch (error) {
      console.error("Check favourite status error:", error);
      return { is_favourite: false };
    }
  }

  isFavourite(topicTitle) {
    return this.favourites.value.some(
      (fav) => fav.project_topic && fav.project_topic.title === topicTitle
    );
  }

  getFavouriteByTitle(topicTitle) {
    return this.favourites.value.find(
      (fav) => fav.project_topic && fav.project_topic.title === topicTitle
    );
  }
}

// Export singleton instance
export default new FavouriteService();
