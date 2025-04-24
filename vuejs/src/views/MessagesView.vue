<script setup>
import { onMounted, ref, nextTick, watch, computed, onBeforeUnmount, onActivated, reactive } from 'vue';
import axios from 'axios'
import UserChat from '@/components/Auth/UserChat.vue';
import WebsocketChat from '@/components/Auth/WebsocketChat.vue';
import { useRoute, useRouter } from 'vue-router';
import { useUnreadMessagesStore } from "@/stores/unreadMessages";

import { useChatStore } from "@/stores/useChatStore";

import NewMessageToastWebsocket from '@/components/Auth/NewMessageToastWebsocket.vue';
import NewMessageToast from '@/components/Auth/NewMessageToast.vue';

import { useToast } from "vue-toastification";

import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();


const toast = useToast();

const chatStore = useChatStore();

const unreadMessagesStore = useUnreadMessagesStore();

import ClipLoader from 'vue-spinner/src/ClipLoader.vue'


const searchValue = ref('')

const filteredChats = computed(() => {
  if (!searchValue.value.trim()) {
    return sortedChats.value; // Если строка пустая, показываем все чаты
  }
  return sortedChats.value.filter(chat =>
    chat.user.username.toLowerCase().includes(searchValue.value.trim().toLowerCase())
  );
});


const colorMap = {
  red: { track: "#fca5a5", thumb: "#ef4444" }, // bg-red-300 / bg-red-500
  blue: { track: "#93c5fd", thumb: "#3b82f6" }, // bg-blue-300 / bg-blue-500
  lime: { track: "#bef264", thumb: "#84cc16" }, // bg-lime-300 / bg-lime-500
  yellow: { track: "#fde047", thumb: "#eab308" }, // bg-yellow-300 / bg-yellow-500
  purple: { track: "#d8b4fe", thumb: "#a855f7" } // bg-purple-300 / bg-purple-500
};

watch(() => chatStore.bgColor, (newColor) => {
  if (colorMap[newColor]) {
    document.documentElement.style.setProperty("--scrollbar-thumb-bg-chats", colorMap[newColor].thumb);
  }
}, { immediate: true });

const color = ref('red')
const size = ref('100px')

const route = useRoute();
const router = useRouter()

const chats = ref(null)
const auth_user_id = ref(null)


const sortedChats = computed(() => {
  return chats.value ? [...chats.value].sort((a, b) => b.last_message.id - a.last_message.id) : [];
});


const clearQuery = () => {
  router.replace({ path: route.path, query: {} });
};


watch(
  () => route.name,
  async (newName, oldName) => {
    if (newName === "messages") {
      let unreadMessagesCount = unreadMessagesStore.count;
      let unreadUpdatesCount = unreadUpdatesStore.count;
      let totalUnread = unreadMessagesCount + unreadUpdatesCount;

      if (totalUnread > 0) {
        document.title = `(${totalUnread}) Pinterest`; // Если есть непрочитанные уведомления
      } else {
        document.title = 'Pinterest'; // Если уведомлений нет
      }
      const chat_id_redirect = route.query.chat_id || null;
      const new_chat = route.query.new_chat || null;
      if (new_chat !== null && !userConnected.value) {
        await addChat(chat_id_redirect)
      }
      if (chat_id_redirect !== null && !userConnected.value) {
        let index = 0;
        let chatObj = null;
        for (let i = 0; i < sortedChats.value.length; i++) {
          if (sortedChats.value[i].id == chat_id_redirect) {
            index = i;
            chatObj = sortedChats.value[i]
            break;
          }
        }
        if (new_chat !== null) {
          loadChat2(chatObj, index)
        } else {
          loadChat(chatObj, index)
        }
      }
      clearQuery()
    }
  }
);


async function addChat(chat_id) {
  try {
    const response = await axios.get(`/api/messages/get_chat_by_id/${chat_id}`, { withCredentials: true });
    const chat = response.data

    const userId = auth_user_id.value === chat.user_1_id ? chat.user_2_id : chat.user_1_id
    try {
      const response = await axios.get(`/api/users/user_id/${userId}`, { withCredentials: true })
      chat.user = response.data
    } catch (error) {
      console.error(error)
    }

    try {
      const userResponse = await axios.get(`/api/users/upload/${userId}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(userResponse.data);
      chat.userImage = blobUrl;
    } catch (error) {
      console.error(error);
    }

    chat.online = false

    chat.socket = new WebSocket(`/ws/${chat.id}/${auth_user_id.value}?chat_connection=true`);
    chat.socket.onmessage = async (event) => {
      const message = JSON.parse(event.data);
      if ("online" in message) {
        if (message.online == true) {
          chat.online = true
        } else {
          chat.online = false
        }
        chats.value = [...chats.value];
        return
      }
      if ("user_start_sending_media" in message) {
        chat.isSendingMedia = true
        chats.value = [...chats.value];
        return
      }
      if ("user_stop_sending_media" in message) {
        chat.isSendingMedia = false
        chats.value = [...chats.value];
        return
      }
      if ("user_read_messages" in message) {
        chat.last_message.is_read = true
        chats.value = [...chats.value];
        return
      }
      if ("user_start_typing" in message) {
        chat.typing = true
        chats.value = [...chats.value];
        return
      }
      if ("user_stop_typing" in message) {
        chat.typing = false
        chats.value = [...chats.value];
        return
      }
      unreadMessagesStore.increment()
      updateChat2(message.chat_id)
    }

    try {
      const response = await axios.get(`/api/messages/last/${chat.id}`, { withCredentials: true })
      chat.last_message = response.data
      if (chat.last_message.image !== null) {
        try {
          const response = await axios.get(`/api/messages/upload/${chat.last_message.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(response.data);
          chat.last_message.media = blobUrl
          const contentType = response.headers['content-type'];
          if (contentType.startsWith('image/')) {
            chat.last_message.isImage = true;
          } else {
            chat.last_message.isImage = false;
          }
        } catch (error) {
          console.error(error);
        }
      }
    } catch (error) {
      console.error(error)
    }

    try {
      const response = await axios.get(`/api/messages/unread/cnt/${chat.id}`, { withCredentials: true })
      chat.cntUnreadMessages = response.data
    } catch (error) {
      console.log(error)
    }

    chats.value.push(reactive(chat));

    if (route.name !== 'messages') {
      toast({
        component: NewMessageToast,
        props: { chat: JSON.parse(JSON.stringify(chat)) },
        listeners: {
          MyClick: () => router.push(`/messages?chat_id=${chat.id}`)
        }
      }, {
        position: "bottom-left",
        timeout: 5041,
        closeOnClick: true,
        pauseOnFocusLoss: true,
        pauseOnHover: true,
        draggable: true,
        draggablePercent: 0.6,
        showCloseButtonOnHover: false,
        hideProgressBar: false,
        closeButton: false,
        icon: false,
        rtl: false,
        toastClassName: "my-custom-toast-class",
      });
    }

  } catch (error) {
    console.error(error);
  }

}


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

const chat_id_redirect = ref(null)

const showLoading = ref(null)

onBeforeUnmount(() => {
  if (eventSource) {
    eventSource.close();
  }

  for (let i = 0; i < chats.value.length; i++) {
    if (chats.value[i].socket) {
      chats.value[i].socket.close()
    }
  }
});


const userConnected = ref(null)

let eventSource = null;

function connectSSE() {
  eventSource = new EventSource(`/api/sse/messages/stream/${auth_user_id.value}`);

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    addChat(data.message.chat_id);
    unreadMessagesStore.increment();
    chat_selected.value += 1;
  };

  eventSource.onerror = () => {
    console.warn("🔌 Messages SSE отключен. Попытка переподключения...");
    eventSource.close();
    setTimeout(() => {
      connectSSE(); // повторное подключение
    }, 5000); // через 5 сек
  };
}



onMounted(async () => {
  showLoading.value = true
  chatStore.fetchChatColor();
  chatStore.fetchChatSize();
  chatStore.fetchSide()
  const accessToken = getCookie('access_token');
  // Decode the JWT (assuming the access_token is a JWT)
  const base64Url = accessToken.split('.')[1]; // Get the payload part
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );

  const payload = JSON.parse(jsonPayload);

  // Log user_id to the console
  auth_user_id.value = payload.user_id;

  try {
    const response = await axios.get('/api/messages/user_chats', { withCredentials: true })
    chats.value = response.data
    if (Array.isArray(chats.value) && chats.value.length > 0) {
      try {
        const response = await axios.get(`/api/chats/check_connection/${chats.value[0].id}/${auth_user_id.value}`);

        if (response.data.active) {
          userConnected.value = true
        } else {
          userConnected.value = false
        }
      } catch (error) {
        console.error("Error checking connection:", error);
      }
    }

    if (!userConnected.value) {
      connectSSE();
    }


    for (let i = 0; i < chats.value.length; i++) {
      const userId = auth_user_id.value === chats.value[i].user_1_id ? chats.value[i].user_2_id : chats.value[i].user_1_id
      try {
        const response = await axios.get(`/api/users/user_id/${userId}`, { withCredentials: true })
        chats.value[i].user = response.data
      } catch (error) {
        console.error(error)
      }
      try {
        const userResponse = await axios.get(`/api/users/upload/${userId}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(userResponse.data);
        chats.value[i].userImage = blobUrl;
      } catch (error) {
        console.error(error);
      }
      chats.value[i].online = false
      if (!userConnected.value) {
        chats.value[i].socket = new WebSocket(`/ws/${chats.value[i].id}/${auth_user_id.value}?chat_connection=true`);
        chats.value[i].socket.onmessage = async (event) => {
          const message = JSON.parse(event.data);
          if ("online" in message) {
            if (message.online == true) {
              chats.value[i].online = true
            } else {
              chats.value[i].online = false
            }
            return
          }
          if ("user_start_sending_media" in message) {
            chats.value[i].isSendingMedia = true
            return
          }
          if ("user_stop_sending_media" in message) {
            chats.value[i].isSendingMedia = false
            return
          }
          if ("user_read_messages" in message) {
            chats.value[i].last_message.is_read = true
            return
          }
          if ("user_start_typing" in message) {
            chats.value[i].typing = true
            return
          }
          if ("user_stop_typing" in message) {
            chats.value[i].typing = false
            return
          }
          unreadMessagesStore.increment()
          updateChat2(message.chat_id)
        }
      }
      try {
        const response = await axios.get(`/api/messages/last/${chats.value[i].id}`, { withCredentials: true })
        chats.value[i].last_message = response.data
        if (chats.value[i].last_message.image !== null) {
          try {
            const response = await axios.get(`/api/messages/upload/${chats.value[i].last_message.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(response.data);
            chats.value[i].last_message.media = blobUrl
            const contentType = response.headers['content-type'];
            if (contentType.startsWith('image/')) {
              chats.value[i].last_message.isImage = true;
            } else {
              chats.value[i].last_message.isImage = false;
            }
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error)
      }
      try {
        const response = await axios.get(`/api/messages/unread/cnt/${chats.value[i].id}`, { withCredentials: true })
        chats.value[i].cntUnreadMessages = response.data
      } catch (error) {
        console.log(error)
      }
    }
  } catch (error) {
    console.error(error)
  }

  showLoading.value = false
})

const showChat = ref(false)
const chat_id = ref(null)
const chat_selected = ref(null)
const user_to_load = ref(null)
const chatObject = ref(null)


async function loadChat(chat, index) {
  if (searchValue.value.trim()) {
    searchValue.value = ''
    index = sortedChats.value.findIndex(c => c.id === chat.id);
  }
  let id = chat.id
  if (id !== chat_id.value) {
    if (chat_selected.value !== null) {
      sortedChats.value[chat_selected.value].selected = false
    }
    chatObject.value = chat
    chat.selected = true
    chat_selected.value = index
    showChat.value = false
    await nextTick()
    chat_id.value = id
    user_to_load.value = chat.user_1_id === auth_user_id.value ? chat.user_2_id : chat.user_1_id
    showChat.value = true
  }
}

async function loadChat2(chat, index) {
  if (searchValue.value.trim()) {
    searchValue.value = ''
    index = sortedChats.value.findIndex(c => c.id === chat.id);
  }
  let id = chat.id
  if (id !== chat_id.value) {
    if (chat_selected.value !== null) {
      sortedChats.value[chat_selected.value + 1].selected = false
    }
    chatObject.value = chat
    chat.selected = true
    chat_selected.value = index
    showChat.value = false
    await nextTick()
    chat_id.value = id
    user_to_load.value = chat.user_1_id === auth_user_id.value ? chat.user_2_id : chat.user_1_id
    showChat.value = true
  }
}


const scrollToTop = () => {
  nextTick(() => {
    if (chatsContainer.value) {
      chatsContainer.value.scrollTop = 0;
    }
  });
};

const chatsContainer = ref(null);



async function updateChat2(chat_id) {
  try {
    const response = await axios.get(`/api/messages/last/${chat_id}`, { withCredentials: true })
    const chatObj = sortedChats.value.find(el => el.id === chat_id);
    const chatIndex = sortedChats.value.findIndex(el => el.id === chat_id);
    if (chat_selected.value !== null && chatIndex > chat_selected.value) {
      chat_selected.value += 1
    }
    chatObj.last_message = response.data
    if (chatObj.last_message.image !== null) {
      try {
        const response = await axios.get(`/api/messages/upload/${chatObj.last_message.id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(response.data);
        chatObj.last_message.media = blobUrl
        const contentType = response.headers['content-type'];
        if (contentType.startsWith('image/')) {
          chatObj.last_message.isImage = true;
          if (contentType === 'image/gif') {
            chatObj.last_message.isGif = true;
          }
        } else {
          chatObj.last_message.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }
    }
    try {
      const response = await axios.get(`/api/messages/unread/cnt/${chatObj.id}`, { withCredentials: true })
      chatObj.cntUnreadMessages = response.data
    } catch (error) {
      console.log(error)
    }
    if (route.name !== 'messages') {
      toast({
        component: NewMessageToast,
        props: { chat: JSON.parse(JSON.stringify(chatObj)) },
        listeners: {
          MyClick: () => router.push(`/messages?chat_id=${chatObj.id}`)
        }
      }, {
        position: "bottom-left",
        timeout: 5041,
        closeOnClick: true,
        pauseOnFocusLoss: true,
        pauseOnHover: true,
        draggable: true,
        draggablePercent: 0.6,
        showCloseButtonOnHover: false,
        hideProgressBar: false,
        closeButton: false,
        icon: false,
        rtl: false,
        toastClassName: "my-custom-toast-class",
      });
    }
  } catch (error) {
    console.error(error)
  }
}

async function updateChat(showToast, chat_id, online) {
  scrollToTop()
  try {
    const response = await axios.get(`/api/messages/last/${chat_id}`, { withCredentials: true })
    sortedChats.value[chat_selected.value].last_message = response.data
    sortedChats.value[chat_selected.value].last_message.is_read = online
    chat_selected.value = 0
    if (sortedChats.value[chat_selected.value].last_message.image !== null) {
      try {
        const response = await axios.get(`/api/messages/upload/${sortedChats.value[chat_selected.value].last_message.id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(response.data);
        sortedChats.value[chat_selected.value].last_message.media = blobUrl
        const contentType = response.headers['content-type'];
        if (contentType.startsWith('image/')) {
          sortedChats.value[chat_selected.value].last_message.isImage = true;
          if (contentType === 'image/gif') {
            sortedChats.value[chat_selected.value].last_message.isGif = true;
          }
        } else {
          sortedChats.value[chat_selected.value].last_message.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }
    }
    if (showToast === true) {
      toast({
        component: NewMessageToastWebsocket,
        props: { chat: JSON.parse(JSON.stringify(sortedChats.value[chat_selected.value])) },
        listeners: {
          MyClick: () => router.push('/messages')
        }
      }, {
        position: "bottom-left",
        timeout: 5041,
        closeOnClick: true,
        pauseOnFocusLoss: true,
        pauseOnHover: true,
        draggable: true,
        draggablePercent: 0.6,
        showCloseButtonOnHover: false,
        hideProgressBar: false,
        closeButton: false,
        icon: false,
        rtl: false,
        toastClassName: "my-custom-toast-class",
      });
    }
  } catch (error) {
    console.error(error)
  }
}

const startResize = (event) => {
  const startX = event.clientX;
  const startWidth = chatStore.size;

  // Отключаем выделение текста
  document.body.style.userSelect = "none";

  const onMouseMove = (moveEvent) => {
    let newWidth = startWidth + (moveEvent.clientX - startX);
    newWidth = Math.max(200, Math.min(newWidth, 800));

    if (newWidth === 200) {
      newWidth = 80;
    }

    chatStore.size = newWidth;
  };

  const onMouseUp = async () => {
    try {
      await axios.patch(`/api/chats/size?size=${chatStore.size}`)
    } catch (error) {
      console.log(error)
    }
    window.removeEventListener("mousemove", onMouseMove);
    window.removeEventListener("mouseup", onMouseUp);

    document.body.style.userSelect = "";
  };

  window.addEventListener("mousemove", onMouseMove);
  window.addEventListener("mouseup", onMouseUp);
};

const showimg = ref(false)

const showScroll = ref(false)

function setScrollbarColor(color) {
  document.documentElement.style.setProperty('--scrollbar-thumb-bg-chats', color);
}

</script>

<template>
  <div v-if="userConnected"
    class="left-20 fixed inset-0 flex items-center justify-center bg-indigo-200 z-50 bg-opacity-50">
    <div class="bg-white rounded-2xl shadow-2xl p-8 text-center max-w-md mx-4 animate-fadeInUp">
      <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-4">Oops!</h1>
      <h1 class="text-xl  font-bold text-gray-800 mb-6">
        It looks like you already have an active connection!
      </h1>
      <h1 class="text-xl  font-bold text-gray-800 mb-6">
        Or u have testusername profile account!
      </h1>
      <p class="text-lg md:text-xl text-gray-600 mb-8">
        Check your open tabs
      </p>
      <p class="text-sm text-gray-500">
        If you're sure this is a mistake, try refreshing the page.
      </p>
    </div>
  </div>

  <div v-if="showChat && !userConnected" class="fixed top-0 h-full w-full z-50"
    :style="{ left: `${chatStore.size + 80}px` }">
    <WebsocketChat :chat_id="chat_id" :auth_user_id="auth_user_id" :user_to_load="user_to_load" :chat="chatObject"
      @updateLastMessage="(showToast, chat_id_, online) => updateChat(showToast, chat_id_, online)" />
  </div>
  <div v-if="chatStore.bgColor && chats && !showChat && !(chats.length === 0)" :class="`bg-${chatStore.bgColor}-300`"
    :style="{ left: `${chatStore.size + 80}px`, width: `calc(100vw - ${chatStore.size + 80}px)` }"
    class="fixed top-0 h-full z-20 flex items-center justify-center">
    <span class="text-xs text-white bg-black bg-opacity-20 px-2 py-1 rounded-3xl">
      Select chat to start messaging
    </span>
    <div class="absolute left-[-10px] bottom-0 top-0 w-5 cursor-ew-resize bg-transparen" @mousedown="startResize">
    </div>
  </div>
  <div v-if="chats && chats.length === 0" class="flex flex-col items-center justify-center mt-20">
    <span class="text-3xl">You don't have any chats yet. Start a new conversation!</span>
    <img v-show="showimg === true" src="https://i.pinimg.com/736x/6c/a8/05/6ca805efcc51ff2366298781aecde4ae.jpg"
      class="w-auto h-auto rounded-2xl" @load="showimg = true" />
  </div>
  <div class="ml-20">
    <div v-show="!showLoading && chats && chats.length"
      class="fixed z-30 top-0 left-20 transform h-[50px] flex items-center justify-center shadow-sm"
      :style="{ width: chatStore.size + 'px' }">
      <input v-show="chatStore.size > 200" v-model="searchValue" type="text" placeholder="Search"
        class="w-full mx-5 max-w-[800px] transition-all duration-300 cursor-pointer bg-gray-200 hover:bg-gray-300 text-md rounded-3xl py-2 px-6 outline-none border-none focus:ring-0" />
    </div>
    <div id="chats" ref="chatsContainer" @mouseover="setScrollbarColor(colorMap[chatStore.bgColor].thumb)"
      @mouseleave="setScrollbarColor('white')"
      class="fixed top-0 left-20 h-[675px] flex flex-col overflow-x-hidden mt-[50px]"
      :style="{ width: chatStore.size + 'px' }" v-auto-animate>
      <UserChat v-if="!showLoading" v-for="(chat, index) in filteredChats" :key="chat.id" :chat="chat"
        :auth_user_id="auth_user_id" @click="loadChat(chat, index)" />
      <ClipLoader v-if="showLoading" :color="color" :size="size"
        class="flex items-center justify-center h-96 font-extrabold" />
    </div>
  </div>
</template>

<style scoped>
#chats::-webkit-scrollbar {
  width: 5px;
}

#chats::-webkit-scrollbar-track {
  background: white;
  border-radius: 10px;
}

#chats::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb-bg-chats);
  /* ✅ Работает с Tailwind */
  border-radius: 10px;
}

.my-custom-toast-class {
  background-color: red !important;
  /* ✅ Заменяем цвет */
  box-shadow: none !important;
  /* Убираем тень */
  border: none !important;
  /* Убираем границу */
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(40px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeInUp {
  animation: fadeInUp 1.5s ease-out forwards;
}
</style>