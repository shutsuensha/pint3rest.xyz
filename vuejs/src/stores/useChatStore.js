import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useChatStore = defineStore("chat", () => {
  const bgColor = ref(null); // Дефолтный цвет
  const size = ref(null);
  const side = ref(null)

  const fetchSide = async () => {
    try {
      const response = await axios.get("/api/chats/side", { withCredentials: true });
      side.value = response.data
    } catch (error) {
      console.error("Ошибка загрузки цвета чата:", error);
    }
  };

  const setSide = (side) => {
    side.value = side;
  };

  const fetchChatColor = async () => {
    try {
      const response = await axios.get("/api/chats/color", { withCredentials: true });
      bgColor.value = response.data
    } catch (error) {
      console.error("Ошибка загрузки цвета чата:", error);
    }
  };

  const setChatColor = (color) => {
    bgColor.value = color;
  };

  const fetchChatSize = async () => {
    try {
      const response = await axios.get("/api/chats/size", { withCredentials: true });
      size.value = response.data
    } catch (error) {
      console.error("Ошибка загрузки цвета чата:", error);
    }
  };

  const setChatSize = (size) => {
    size.value = size;
  };

  return { bgColor, fetchChatColor, setChatColor, size, fetchChatSize, setChatSize, fetchSide, setSide, side };
});
