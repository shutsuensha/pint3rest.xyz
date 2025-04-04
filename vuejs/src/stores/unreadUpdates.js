import { defineStore } from "pinia";
import axios from "axios";

export const useUnreadUpdatesStore = defineStore("unread_updates", {
  state: () => ({
    count: 0, // Unread messages count
  }),
  actions: {
    async fetchUnreadUpdates() {
      try {
        const response = await axios.get("/api/updates/count", {
          withCredentials: true,
        });
        this.count = response.data; // Update store state
      } catch (error) {
        console.error("Error fetching unread messages:", error);
      }
    },
    increment() {
      this.count++;
    },
    decrement() {
      this.count--;
    },
  },
});
