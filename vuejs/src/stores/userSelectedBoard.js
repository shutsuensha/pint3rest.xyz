import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useSelectedBoard = defineStore("selectedBoard", () => {
  const selectedBoard = ref(null);

  const fetchSelectedBoard = async () => {
    try {
      const response = await axios.get("/api/boards/selected", { withCredentials: true });
      selectedBoard.value = response.data
    } catch (error) {
      console.error("Ошибка загрузки цвета чата:", error);
    }
  };

  const setBoard = async (board) => {
    if (board === null) {
      selectedBoard.value = null
      try {
        await axios.patch(`/api/boards/selected/disable`, { withCredentials: true });
      } catch (error) {
        console.error("Ошибка при установке выбранной доски:", error);
      }
      return
    }
    try {
      await axios.patch(`/api/boards/selected?board_id=${board.id}`, { withCredentials: true });
      selectedBoard.value = board;
    } catch (error) {
      console.error("Ошибка при установке выбранной доски:", error);
    }
  };

  return { selectedBoard, fetchSelectedBoard, setBoard };
});
