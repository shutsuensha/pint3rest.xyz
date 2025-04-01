import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const authUserStore = defineStore("authUserStore", () => {
  const authUsername = ref(null);

  const setUsername = async (username) => {
    authUsername.value = username
  };

  return { authUsername, setUsername };
});
