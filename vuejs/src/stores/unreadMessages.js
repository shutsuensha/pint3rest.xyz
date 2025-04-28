import { defineStore } from "pinia";
import axios from "axios";

export const useUnreadMessagesStore = defineStore("unread_messages", {
  state: () => ({
    count: 0, // Unread messages count
  }),
  actions: {
    async fetchUnreadMessages() {
      try {
        const response = await axios.get("/api/messages/unread/all_chats/cnt", {
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



