import { ref } from "vue";

class FavouriteService {
  constructor() {
    this.baseUrl = "http://localhost:5000";
    this.favourites = ref([]);
    this.isLoading = ref(false);
  }

  async getFavourites() {
    this.isLoading.value = true;
    try {
      const token = localStorage.getItem("auth.token");
      if (!token) {
        throw new Error("No auth token found");
      }
      const response = await fetch(`${this.baseUrl}/api/favourites`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
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
    try {
      const token = localStorage.getItem("auth.token");
      if (!token) {
        throw new Error("No auth token found");
      }
      const response = await fetch(`${this.baseUrl}/api/favourites`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topicData, notes }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to save favourite");
      }

      const data = await response.json();

      await this.getFavourites();

      return result;
    } catch (error) {
      console.error("Error saving favourite:", error);
      throw error;
    } finally {
      this.isLoading.value = false;
    }
  }

  async removeFavourtie(favouriteId) {
    try {
      const token = localStorage.getItem("auth.token");
      if (!token) {
        throw new Error("No auth token found");
      }
      const response = await fetch(
        `${this.baseUrl}/api/favourites/${favouriteId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error("Failed to remove favourite");
      }

      this.favourites.value = this.favourites.value.filter(
        (fav) => fav.id !== favouriteId
      );

      return await response.json();
    } catch (error) {
      console.error("Remove Favourite Error:", error);
      throw error;
    }
  }

  async updateNotes(favouriteId, notes) {
    try {
      const token = localStorage.getItem("auth.token");
      if (!token) {
        throw new Error("No auth token found");
      }

      const response = await fetch(
        `${this.baseURL}/api/favorites/${favoriteId}/notes`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            notes: notes,
            progress_status: progressStatus,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update notes");
      }

      // Update local favorites list
      const favoriteIndex = this.favorites.value.findIndex(
        (fav) => fav.id === favoriteId
      );
      if (favoriteIndex !== -1) {
        this.favorites.value[favoriteIndex].notes = notes;
        this.favorites.value[favoriteIndex].progress_status = progressStatus;
      }

      return await response.json();
    } catch (error) {
      console.error("Update Notes Error:", error);
      throw error;
    }
  }

  isFavourite(topicTitle) {
    return this.favourites.value.some((fav) => fav.title === topicTitle);
  }

  getFavouriteByTitle(topicTitle) {
    return this.favourites.value.find((fav) => fav.title === topicTitle);
  }
}
