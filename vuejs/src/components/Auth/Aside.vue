<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue';
import axios from 'axios'
import { RouterLink, useRoute } from 'vue-router';
import { useUnreadMessagesStore } from "@/stores/unreadMessages";

const unreadMessagesStore = useUnreadMessagesStore();


import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import "dayjs/locale/en"; // Используем английскую локаль

dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.locale("en"); // Устанавливаем английскую локаль

const formatTime = (createdAt) => {
  const now = dayjs();
  const createdTime = dayjs.utc(createdAt).local();
  const diffMinutes = now.diff(createdTime, "minute");

  return diffMinutes < 30 ? "just now" : createdTime.fromNow();
};

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};

const emit = defineEmits(['logout'])

const props = defineProps({
  me: Object,
  meImage: String
})


async function logout() {
  try {
    await axios.post('/api/users/logout')
    emit('logout')
  } catch (error) {
    console.log(error)
  }
}

const cntUnreadMessages = ref(null)

const showModal = ref(false)

function openModal() {
  showModal.value = true
  loadUpdates()
}

function closeModal() {
  showModal.value = false
  updates.value = []
  offset.value = 0
  limit.value = 7
  isPinsLoading.value = false
}

const updates = ref([])
const tempUpdates = ref([])

const offset = ref(0);
const limit = ref(7);

const isPinsLoading = ref(false);

const canLoad = ref(true)


async function loadUpdates() {
  if (isPinsLoading.value) {
    return;
  }

  if (!canLoad.value) {
    return
  }

  isPinsLoading.value = true;
  try {
    const response = await axios.get(`/api/updates/`, { params: { offset: offset.value, limit: limit.value } })
    const data = response.data

    for (let i = 0; i < data.length; i++) {

      if (!data[i].is_read) {
        try {
          await axios.put(`/api/updates/read/${data[i].id}`)
          unreadUpdatesStore.decrement()
        } catch (error) {
          console.error(error)
        }
      }

      if (data[i].update_type == "recommendations") {
        const response = await axios.get(`/api/recommendations/${data[i].id}`, {
          params: { offset: 0, limit: 1 },
          withCredentials: true,
        });

        const pin_id = response.data[0].id
        try {
          const pinResponse = await axios.get(`/api/pins/upload/${pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            data[i].file = blobUrl;
            data[i].isImage = true;
          } else {
            data[i].file = blobUrl;
            data[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }
      }

      if (data[i].update_type == "follow") {
        try {
          const response = await axios.get(`/api/users/user_id/${data[i].user_id}`);
          data[i].user = response.data;

          try {
            const userResponse = await axios.get(`/api/users/upload/${data[i].user.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(userResponse.data);
            data[i].image = blobUrl;

          } catch (error) {
            console.error(error);
          }
        } catch (error) {
          console.error(error)
        }
      }

      if (data[i].update_type == "like_pin") {
        try {
          const response = await axios.get(`/api/users/user_id/${data[i].user_id}`);
          data[i].user = response.data;

          try {
            const userResponse = await axios.get(`/api/users/upload/${data[i].user.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(userResponse.data);
            data[i].image = blobUrl;

          } catch (error) {
            console.error(error);
          }
        } catch (error) {
          console.error(error)
        }

        try {
          const pinResponse = await axios.get(`/api/pins/upload/${data[i].pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            data[i].file = blobUrl;
            data[i].isImage = true;
          } else {
            data[i].file = blobUrl;
            data[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }
      }

      if (data[i].update_type == "save_pin") {
        try {
          const response = await axios.get(`/api/users/user_id/${data[i].user_id}`);
          data[i].user = response.data;

          try {
            const userResponse = await axios.get(`/api/users/upload/${data[i].user.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(userResponse.data);
            data[i].image = blobUrl;

          } catch (error) {
            console.error(error);
          }
        } catch (error) {
          console.error(error)
        }

        try {
          const pinResponse = await axios.get(`/api/pins/upload/${data[i].pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            data[i].file = blobUrl;
            data[i].isImage = true;
          } else {
            data[i].file = blobUrl;
            data[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }
      }

      if (data[i].update_type == "comment_pin") {
        try {
          const response = await axios.get(`/api/users/user_id/${data[i].user_id}`);
          data[i].user = response.data;

          try {
            const userResponse = await axios.get(`/api/users/upload/${data[i].user.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(userResponse.data);
            data[i].image = blobUrl;

          } catch (error) {
            console.error(error);
          }
        } catch (error) {
          console.error(error)
        }

        try {
          const pinResponse = await axios.get(`/api/pins/upload/${data[i].pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            data[i].file = blobUrl;
            data[i].isImage = true;
          } else {
            data[i].file = blobUrl;
            data[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }

        try {
          const response = await axios.get(`/api/comments/get-by-id/${data[i].comment_id}`, { withCredentials: true })
          data[i].comment = response.data

          if (data[i].comment.image) {
            try {
              const response = await axios.get(`/api/comments/upload/${data[i].comment.id}`, { responseType: 'blob' });
              const blobUrl = URL.createObjectURL(response.data);
              const contentType = response.headers['content-type'];
              data[i].commentFile = blobUrl;
              if (contentType.startsWith('image/')) {
                data[i].commentIsIamge = true;
              } else {
                data[i].commentIsIamge = false;
              }
            } catch (error) {
              console.error(error);
            }
          }
        } catch (error) {
          console.error(error)
        }
      }

      if (data[i].update_type == "like_comment") {
        try {
          const response = await axios.get(`/api/users/user_id/${data[i].user_id}`);
          data[i].user = response.data;

          try {
            const userResponse = await axios.get(`/api/users/upload/${data[i].user.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(userResponse.data);
            data[i].image = blobUrl;

          } catch (error) {
            console.error(error);
          }
        } catch (error) {
          console.error(error)
        }

        try {
          const pinResponse = await axios.get(`/api/pins/upload/${data[i].pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            data[i].file = blobUrl;
            data[i].isImage = true;
          } else {
            data[i].file = blobUrl;
            data[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }

        try {
          const response = await axios.get(`/api/comments/get-by-id/${data[i].comment_id}`, { withCredentials: true })
          data[i].comment = response.data

          if (data[i].comment.image) {
            try {
              const response = await axios.get(`/api/comments/upload/${data[i].comment.id}`, { responseType: 'blob' });
              const blobUrl = URL.createObjectURL(response.data);
              const contentType = response.headers['content-type'];
              data[i].commentFile = blobUrl;
              if (contentType.startsWith('image/')) {
                data[i].commentIsIamge = true;
              } else {
                data[i].commentIsIamge = false;
              }
            } catch (error) {
              console.error(error);
            }
          }
        } catch (error) {
          console.error(error)
        }
      }

      if (data[i].update_type == "reply_comment") {
        try {
          const response = await axios.get(`/api/users/user_id/${data[i].user_id}`);
          data[i].user = response.data;

          try {
            const userResponse = await axios.get(`/api/users/upload/${data[i].user.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(userResponse.data);
            data[i].image = blobUrl;

          } catch (error) {
            console.error(error);
          }
        } catch (error) {
          console.error(error)
        }

        try {
          const pinResponse = await axios.get(`/api/pins/upload/${data[i].pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            data[i].file = blobUrl;
            data[i].isImage = true;
          } else {
            data[i].file = blobUrl;
            data[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }

        try {
          const response = await axios.get(`/api/comments/get-by-id/${data[i].comment_id}`, { withCredentials: true })
          data[i].comment = response.data

          if (data[i].comment.image) {
            try {
              const response = await axios.get(`/api/comments/upload/${data[i].comment.id}`, { responseType: 'blob' });
              const blobUrl = URL.createObjectURL(response.data);
              const contentType = response.headers['content-type'];
              data[i].commentFile = blobUrl;
              if (contentType.startsWith('image/')) {
                data[i].commentIsIamge = true;
              } else {
                data[i].commentIsIamge = false;
              }
            } catch (error) {
              console.error(error);
            }
          }
        } catch (error) {
          console.error(error)
        }


        try {
          const response = await axios.get(`/api/comments/get-by-id/${data[i].reply_id}`, { withCredentials: true })
          data[i].reply = response.data

          if (data[i].reply.image) {
            try {
              const response = await axios.get(`/api/comments/upload/${data[i].reply.id}`, { responseType: 'blob' });
              const blobUrl = URL.createObjectURL(response.data);
              const contentType = response.headers['content-type'];
              data[i].replyFile = blobUrl;
              if (contentType.startsWith('image/')) {
                data[i].replyIsIamge = true;
              } else {
                data[i].replyIsIamge = false;
              }
            } catch (error) {
              console.error(error);
            }
          }
        } catch (error) {
          console.error(error)
        }
      }

      if (data[i].update_type == "like_reply") {
        try {
          const response = await axios.get(`/api/users/user_id/${data[i].user_id}`);
          data[i].user = response.data;

          try {
            const userResponse = await axios.get(`/api/users/upload/${data[i].user.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(userResponse.data);
            data[i].image = blobUrl;

          } catch (error) {
            console.error(error);
          }
        } catch (error) {
          console.error(error)
        }

        try {
          const pinResponse = await axios.get(`/api/pins/upload/${data[i].pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            data[i].file = blobUrl;
            data[i].isImage = true;
          } else {
            data[i].file = blobUrl;
            data[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }

        try {
          const response = await axios.get(`/api/comments/get-by-id/${data[i].comment_id}`, { withCredentials: true })
          data[i].comment = response.data

          if (data[i].comment.image) {
            try {
              const response = await axios.get(`/api/comments/upload/${data[i].comment.id}`, { responseType: 'blob' });
              const blobUrl = URL.createObjectURL(response.data);
              const contentType = response.headers['content-type'];
              data[i].commentFile = blobUrl;
              if (contentType.startsWith('image/')) {
                data[i].commentIsIamge = true;
              } else {
                data[i].commentIsIamge = false;
              }
            } catch (error) {
              console.error(error);
            }
          }
        } catch (error) {
          console.error(error)
        }


        try {
          const response = await axios.get(`/api/comments/get-by-id/${data[i].reply_id}`, { withCredentials: true })
          data[i].reply = response.data

          if (data[i].reply.image) {
            try {
              const response = await axios.get(`/api/comments/upload/${data[i].reply.id}`, { responseType: 'blob' });
              const blobUrl = URL.createObjectURL(response.data);
              const contentType = response.headers['content-type'];
              data[i].replyFile = blobUrl;
              if (contentType.startsWith('image/')) {
                data[i].replyIsIamge = true;
              } else {
                data[i].replyIsIamge = false;
              }
            } catch (error) {
              console.error(error);
            }
          }
        } catch (error) {
          console.error(error)
        }
      }

      if (data[i].update_type == "pin_created_for_followers") {
        try {
          const response = await axios.get(`/api/users/user_id/${data[i].user_id}`);
          data[i].user = response.data;

          try {
            const userResponse = await axios.get(`/api/users/upload/${data[i].user.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(userResponse.data);
            data[i].image = blobUrl;

          } catch (error) {
            console.error(error);
          }
        } catch (error) {
          console.error(error)
        }

        try {
          const pinResponse = await axios.get(`/api/pins/upload/${data[i].pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            data[i].file = blobUrl;
            data[i].isImage = true;
          } else {
            data[i].file = blobUrl;
            data[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }
      }
      tempUpdates.value.push(data[i])
    }
  } catch (error) {
    console.error(error)
  }


  offset.value += limit.value;

  updates.value.push(...tempUpdates.value)

  if (tempUpdates.value.length < limit.value) {
    canLoad.value = false
  }

  tempUpdates.value = []

  isPinsLoading.value = false;

  if (limit.value == 7) {
    limit.value = 5
  }
}

const handleScroll = (event) => {
  const container = event.target;
  if (container.scrollTop + container.clientHeight >= container.scrollHeight - 10) {
    loadUpdates();
  }
};


let eventSource = null;

function connectSSE() {
  eventSource = new EventSource(`/api/sse/updates/stream/${props.me.id}`);

  eventSource.onmessage = (event) => {
    const rawData = JSON.parse(event.data);  // Парсим первый раз
    const new_update = JSON.parse(rawData.message); // Парсим вложенный JSON
    addNewUpdate(new_update)
  };

  eventSource.onerror = () => {
    console.warn("🔌 Updates SSE отключен. Попытка переподключения...");
    eventSource.close();
    setTimeout(() => {
      connectSSE(); // повторное подключение
    }, 5000); // через 5 сек
  };
}

async function addNewUpdate(update) {
  if (showModal.value === false) {
    unreadUpdatesStore.increment()
  } else {

    try {
      await axios.put(`/api/updates/read/${update.id}`)
    } catch (error) {
      console.error(error)
    }

    if (update.update_type == "recommendations") {
      const response = await axios.get(`/api/recommendations/${update.id}`, {
        params: { offset: 0, limit: 1 },
        withCredentials: true,
      });

      const pin_id = response.data[0].id
      try {
        const pinResponse = await axios.get(`/api/pins/upload/${pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          update.file = blobUrl;
          update.isImage = true;
        } else {
          update.file = blobUrl;
          update.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (update.update_type == "follow") {
      try {
        const response = await axios.get(`/api/users/user_id/${update.user_id}`);
        update.user = response.data;

        try {
          const userResponse = await axios.get(`/api/users/upload/${update.user.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          update.image = blobUrl;

        } catch (error) {
          console.error(error);
        }
      } catch (error) {
        console.error(error)
      }
    }

    if (update.update_type == "like_pin") {
      try {
        const response = await axios.get(`/api/users/user_id/${update.user_id}`);
        update.user = response.data;

        try {
          const userResponse = await axios.get(`/api/users/upload/${update.user.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          update.image = blobUrl;
        } catch (error) {
          console.error(error);
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const pinResponse = await axios.get(`/api/pins/upload/${update.pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          update.file = blobUrl;
          update.isImage = true;
        } else {
          update.file = blobUrl;
          update.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (update.update_type == "save_pin") {
      try {
        const response = await axios.get(`/api/users/user_id/${update.user_id}`);
        update.user = response.data;

        try {
          const userResponse = await axios.get(`/api/users/upload/${update.user.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          update.image = blobUrl;
        } catch (error) {
          console.error(error);
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const pinResponse = await axios.get(`/api/pins/upload/${update.pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          update.file = blobUrl;
          update.isImage = true;
        } else {
          update.file = blobUrl;
          update.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (update.update_type == "comment_pin") {
      try {
        const response = await axios.get(`/api/users/user_id/${update.user_id}`);
        update.user = response.data;

        try {
          const userResponse = await axios.get(`/api/users/upload/${update.user.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          update.image = blobUrl;
        } catch (error) {
          console.error(error);
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const pinResponse = await axios.get(`/api/pins/upload/${update.pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          update.file = blobUrl;
          update.isImage = true;
        } else {
          update.file = blobUrl;
          update.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const response = await axios.get(`/api/comments/get-by-id/${update.comment_id}`, { withCredentials: true });
        update.comment = response.data;

        if (update.comment.image) {
          try {
            const response = await axios.get(`/api/comments/upload/${update.comment.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(response.data);
            const contentType = response.headers['content-type'];
            update.commentFile = blobUrl;
            if (contentType.startsWith('image/')) {
              update.commentIsIamge = true;
            } else {
              update.commentIsIamge = false;
            }
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error);
      }
    }



    if (update.update_type == "like_comment") {
      try {
        const response = await axios.get(`/api/users/user_id/${update.user_id}`);
        update.user = response.data;

        try {
          const userResponse = await axios.get(`/api/users/upload/${update.user.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          update.image = blobUrl;
        } catch (error) {
          console.error(error);
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const pinResponse = await axios.get(`/api/pins/upload/${update.pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          update.file = blobUrl;
          update.isImage = true;
        } else {
          update.file = blobUrl;
          update.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const response = await axios.get(`/api/comments/get-by-id/${update.comment_id}`, { withCredentials: true });
        update.comment = response.data;

        if (update.comment.image) {
          try {
            const response = await axios.get(`/api/comments/upload/${update.comment.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(response.data);
            const contentType = response.headers['content-type'];
            update.commentFile = blobUrl;
            if (contentType.startsWith('image/')) {
              update.commentIsIamge = true;
            } else {
              update.commentIsIamge = false;
            }
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (update.update_type == "reply_comment") {
      try {
        const response = await axios.get(`/api/users/user_id/${update.user_id}`);
        update.user = response.data;

        try {
          const userResponse = await axios.get(`/api/users/upload/${update.user.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          update.image = blobUrl;
        } catch (error) {
          console.error(error);
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const pinResponse = await axios.get(`/api/pins/upload/${update.pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          update.file = blobUrl;
          update.isImage = true;
        } else {
          update.file = blobUrl;
          update.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const response = await axios.get(`/api/comments/get-by-id/${update.comment_id}`, { withCredentials: true });
        update.comment = response.data;

        if (update.comment.image) {
          try {
            const response = await axios.get(`/api/comments/upload/${update.comment.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(response.data);
            const contentType = response.headers['content-type'];
            update.commentFile = blobUrl;
            if (contentType.startsWith('image/')) {
              update.commentIsIamge = true;
            } else {
              update.commentIsIamge = false;
            }
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const response = await axios.get(`/api/comments/get-by-id/${update.reply_id}`, { withCredentials: true });
        update.reply = response.data;

        if (update.reply.image) {
          try {
            const response = await axios.get(`/api/comments/upload/${update.reply.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(response.data);
            const contentType = response.headers['content-type'];
            update.replyFile = blobUrl;
            if (contentType.startsWith('image/')) {
              update.replyIsIamge = true;
            } else {
              update.replyIsIamge = false;
            }
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error);
      }
    }


    if (update.update_type == "like_reply") {
      try {
        const response = await axios.get(`/api/users/user_id/${update.user_id}`);
        update.user = response.data;

        try {
          const userResponse = await axios.get(`/api/users/upload/${update.user.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          update.image = blobUrl;
        } catch (error) {
          console.error(error);
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const pinResponse = await axios.get(`/api/pins/upload/${update.pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          update.file = blobUrl;
          update.isImage = true;
        } else {
          update.file = blobUrl;
          update.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const response = await axios.get(`/api/comments/get-by-id/${update.comment_id}`, { withCredentials: true });
        update.comment = response.data;

        if (update.comment.image) {
          try {
            const response = await axios.get(`/api/comments/upload/${update.comment.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(response.data);
            const contentType = response.headers['content-type'];
            update.commentFile = blobUrl;
            if (contentType.startsWith('image/')) {
              update.commentIsIamge = true;
            } else {
              update.commentIsIamge = false;
            }
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error);
      }

      try {
        const response = await axios.get(`/api/comments/get-by-id/${update.reply_id}`, { withCredentials: true });
        update.reply = response.data;

        if (update.reply.image) {
          try {
            const response = await axios.get(`/api/comments/upload/${update.reply.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(response.data);
            const contentType = response.headers['content-type'];
            update.replyFile = blobUrl;
            if (contentType.startsWith('image/')) {
              update.replyIsIamge = true;
            } else {
              update.replyIsIamge = false;
            }
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (update.update_type == "pin_created_for_followers") {
      try {
        const response = await axios.get(`/api/users/user_id/${update.user_id}`);
        update.user = response.data;

        try {
          const userResponse = await axios.get(`/api/users/upload/${update.user.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          update.image = blobUrl;

        } catch (error) {
          console.error(error);
        }
      } catch (error) {
        console.error(error)
      }

      try {
        const pinResponse = await axios.get(`/api/pins/upload/${update.pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          update.file = blobUrl;
          update.isImage = true;
        } else {
          update.file = blobUrl;
          update.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }
    }

    updates.value.unshift(update);
  }
}

onMounted(async () => {
  connectSSE()
})

onBeforeUnmount(() => {
  if (eventSource) {
    eventSource.close();
  }
})
</script>


<template>
  <nav
    class="fixed top-0 left-0 h-full w-20 flex flex-col justify-between items-center z-30 border-r border-gray-300 py-4 ">
    <!-- Icons -->
    <div class="flex flex-col items-center text-xl space-y-6">
      <RouterLink to="/"
        :class="[isActiveLink('/') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i :class="['pi', 'pi-home', ]"></i>
      </RouterLink>
      <RouterLink :to="`/user/${me.username}`"
        :class="[isActiveLink(`/user/${me.username}`) ? '' : 'transition-transform duration-100 transform hover:scale-125 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <img :src="meImage" alt="me profile"
          :class="[isActiveLink(`/user/${me.username}`) ? 'border-black' : 'border-gray-400', 'w-10', 'h-10', 'object-cover', 'rounded-full', 'border-2']" />
      </RouterLink>
      <RouterLink to="/create-pin"
        :class="[isActiveLink('/create-pin') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i :class="['pi', 'pi-plus-circle']"></i>
      </RouterLink>
      <div @click="openModal" class="relative"
        :class="[showModal ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i class="pi pi-bell"></i>
        <div v-if="unreadUpdatesStore.count"
          class="absolute top-0 right-0 py-0.5 px-2 bg-red-600 rounded-full flex align-center items-center">
          <span class="text-xs text-white"> {{ unreadUpdatesStore.count }}</span>
        </div>
      </div>
      <RouterLink to="/messages" class="relative"
        :class="[isActiveLink('/messages') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i class="pi pi-envelope"></i>
        <div v-if="unreadMessagesStore.count"
          class="absolute top-0 right-0 py-0.5 px-2 bg-red-600 rounded-full flex align-center items-center">
          <span class="text-xs text-white"> {{ unreadMessagesStore.count }}</span>
        </div>
      </RouterLink>
      <div @click="logout"
        class="cursor-pointer rounded-md transition-transform duration-100 transform hover:scale-150 p-5 text-xl flex items-center">
        <i class="pi pi-sign-out"></i>
      </div>
    </div>
  </nav>

  <Transition name="fade">
    <div v-if="showModal" class="fixed top-4 left-24 bottom-4 w-1/4 bg-white shadow-2xl z-[60] rounded-3xl">
      <!-- Заголовок и кнопка закрытия -->
      <div class="flex justify-between items-center p-4">
        <h2 class="text-xl font-bold text-black">Updates</h2>
        <button @click="closeModal"
          class="text-black text-4xl transition duration-300 transform hover:scale-125 hover:bg-gray-200 rounded-full px-2 items-center justify-center flex">
          ×
        </button>
      </div>

      <!-- Список обновлений -->
      <div class="space-y-4 overflow-y-auto h-[600px]" @scroll="handleScroll">
        <div class="pl-4 space-y-2" v-auto-animate>
          <div v-for="update in updates" :key="update.id">
            <RouterLink @click="closeModal" v-if="update.update_type == 'recommendations'"
              :to="`/recommendations/${update.id}`" :class="[
                'rounded-lg flex items-center space-x-4 w-full h-24 relative hover:bg-purple-300 transition',
                !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
              ]">
              <!-- Файл (изображение/видео) слева -->
              <div class="w-20 h-24 flex-shrink-0">
                <template v-if="update.isImage">
                  <img :src="update.file" alt="Update Image" class="w-full h-full object-cover rounded-lg" />
                </template>
                <template v-else>
                  <video :src="update.file" autoplay muted loop class="w-full h-full object-cover rounded-lg"></video>
                </template>
              </div>

              <!-- Сообщение в центре -->
              <p class="text-black text-md font-medium flex items-center justify-center">
                {{ update.content }}
              </p>

              <!-- Дата в верхнем правом углу -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- NEW метка в нижнем правом углу -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </RouterLink>

            <RouterLink @click="closeModal" v-if="update.update_type == 'follow'" :to="`/user/${update.user.username}`"
              :class="[
                'rounded-lg flex items-center w-full h-24 relative hover:bg-purple-300 transition',
                !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
              ]">
              <!-- Увеличенный аватар -->
              <div class="mx-2 w-20 h-24 flex-shrink-0 flex justify-center items-center">
                <img :src="update.image" alt="Update Image" class="w-20 h-20 object-cover rounded-full" />
              </div>

              <!-- Колонка с текстом -->
              <div class="flex flex-col justify-center overflow-hidden mr-auto max-w-[180px]">
                <span class="text-black text-md font-bold truncate">
                  {{ update.user.username }}
                </span>
                <span class="text-black text-md font-medium">started following you</span>
              </div>

              <!-- Дата -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- Метка New -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </RouterLink>

            <div v-if="update.update_type == 'like_pin'" :class="[
              'rounded-lg flex items-center w-full h-24 relative hover:bg-purple-300 transition',
              !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
            ]">
              <!-- Аватар пользователя -->
              <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                class="mx-2 w-20 h-24 flex-shrink-0 flex justify-center items-center">
                <img :src="update.image" alt="User Avatar" class="w-20 h-20 object-cover rounded-full" />
              </RouterLink>

              <!-- Колонка с текстом -->
              <div class="flex flex-col justify-center overflow-hidden mr-auto max-w-[180px]">
                <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                  class="text-black text-md font-bold truncate hover:underline">
                  {{ update.user.username }}
                </RouterLink>
                <span class="text-black text-md font-medium">
                  ❤️ liked your pin
                </span>
              </div>

              <!-- Превью пина -->
              <RouterLink @click="closeModal" :to="`/pin/${update.pin_id}`" class="mr-4 flex-shrink-0">
                <img v-if="update.isImage" :src="update.file" alt="Liked Pin" class="w-10 h-10 object-cover rounded" />
                <video v-else :src="update.file" autoplay loop muted class="w-10 h-10 object-cover rounded"></video>
              </RouterLink>

              <!-- Дата -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- Метка New -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </div>

            <div v-if="update.update_type == 'save_pin'" :class="[
              'rounded-lg flex items-center w-full h-24 relative hover:bg-purple-300 transition',
              !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
            ]">
              <!-- Аватар пользователя -->
              <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                class="mx-2 w-20 h-24 flex-shrink-0 flex justify-center items-center">
                <img :src="update.image" alt="User Avatar" class="w-20 h-20 object-cover rounded-full" />
              </RouterLink>

              <!-- Колонка с текстом -->
              <div class="flex flex-col justify-center overflow-hidden mr-auto max-w-[180px]">
                <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                  class="text-black text-md font-bold truncate hover:underline">
                  {{ update.user.username }}
                </RouterLink>
                <span class="text-black text-md font-medium">
                  💾 saved your pin to {{ update.content }}
                </span>
              </div>

              <!-- Превью пина -->
              <RouterLink @click="closeModal" :to="`/pin/${update.pin_id}`" class="mr-4 flex-shrink-0">
                <img v-if="update.isImage" :src="update.file" alt="Liked Pin" class="w-10 h-10 object-cover rounded" />
                <video v-else :src="update.file" autoplay loop muted class="w-10 h-10 object-cover rounded"></video>
              </RouterLink>

              <!-- Дата -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- Метка New -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </div>

            <div v-if="update.update_type == 'comment_pin'" :class="[
              'rounded-lg flex items-center w-full h-24 relative hover:bg-purple-300 transition',
              !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
            ]">
              <!-- Аватар пользователя -->
              <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                class="mx-2 w-20 h-24 flex-shrink-0 flex justify-center items-center">
                <img :src="update.image" alt="User Avatar" class="w-20 h-20 object-cover rounded-full" />
              </RouterLink>

              <!-- Колонка с текстом -->
              <div class="flex flex-col justify-center overflow-hidden mr-auto max-w-[180px]">
                <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                  class="text-black text-md font-bold truncate hover:underline">
                  {{ update.user.username }}
                </RouterLink>
                <span class="text-black text-md font-medium flex flex-wrap gap-0.5">
                  💬 commented on
                  <span class="text-gray-700 italic truncate max-w-[50px]" v-if="update.comment.content">{{
                    update.comment.content
                    }}</span>
                  <div v-if="update.commentFile" class="">
                    <img v-if="update.commentIsIamge" :src="update.commentFile" alt="Comment media"
                      class="w-7 h-7 object-cover rounded-lg" />
                    <video v-else :src="update.commentFile" autoplay loop muted
                      class="w-7 h-7 object-cover rounded-lg"></video>
                  </div>
                  on your pin
                </span>
              </div>

              <!-- Превью пина -->
              <RouterLink @click="closeModal" :to="`/pin/${update.pin_id}`" class="mr-4 flex-shrink-0">
                <img v-if="update.isImage" :src="update.file" alt="Liked Pin" class="w-10 h-10 object-cover rounded" />
                <video v-else :src="update.file" autoplay loop muted class="w-10 h-10 object-cover rounded"></video>
              </RouterLink>

              <!-- Дата -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- Метка New -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </div>

            <div v-if="update.update_type == 'like_comment'" :class="[
              'rounded-lg flex items-center w-full h-24 relative hover:bg-purple-300 transition',
              !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
            ]">
              <!-- Аватар пользователя -->
              <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                class="mx-2 w-20 h-24 flex-shrink-0 flex justify-center items-center">
                <img :src="update.image" alt="User Avatar" class="w-20 h-20 object-cover rounded-full" />
              </RouterLink>

              <!-- Колонка с текстом -->
              <div class="flex flex-col justify-center overflow-hidden mr-auto max-w-[190px]">
                <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                  class="text-black text-md font-bold truncate hover:underline">
                  {{ update.user.username }}
                </RouterLink>
                <span class="text-black text-sm font-medium flex flex-wrap gap-0.5">
                  ❤️liked your 💬comment
                  <span class="text-gray-700 italic truncate max-w-[50px]" v-if="update.comment.content">{{
                    update.comment.content
                    }}</span>
                  <div v-if="update.commentFile" class="">
                    <img v-if="update.commentIsIamge" :src="update.commentFile" alt="Comment media"
                      class="w-7 h-7 object-cover rounded-lg" />
                    <video v-else :src="update.commentFile" autoplay loop muted
                      class="w-7 h-7 object-cover rounded-lg"></video>
                  </div>
                  on pin
                </span>
              </div>

              <!-- Превью пина -->
              <RouterLink @click="closeModal" :to="`/pin/${update.pin_id}`" class="mr-4 flex-shrink-0">
                <img v-if="update.isImage" :src="update.file" alt="Liked Pin" class="w-10 h-10 object-cover rounded" />
                <video v-else :src="update.file" autoplay loop muted class="w-10 h-10 object-cover rounded"></video>
              </RouterLink>

              <!-- Дата -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- Метка New -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </div>


            <div v-if="update.update_type == 'reply_comment'" :class="[
              'rounded-lg flex items-center w-full h-24 relative hover:bg-purple-300 transition',
              !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
            ]">
              <!-- Аватар пользователя -->
              <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                class="mx-2 w-20 h-24 flex-shrink-0 flex justify-center items-center">
                <img :src="update.image" alt="User Avatar" class="w-20 h-20 object-cover rounded-full" />
              </RouterLink>

              <!-- Колонка с текстом -->
              <div class="flex flex-col justify-center overflow-hidden mr-auto max-w-[180px]">
                <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                  class="text-black text-md font-bold truncate hover:underline">
                  {{ update.user.username }}
                </RouterLink>
                <span class="text-black text-sm font-medium flex flex-wrap gap-0.5">
                  💬 reply on
                  <span class="text-gray-700 italic truncate max-w-[50px]" v-if="update.comment.content">{{
                    update.comment.content
                    }}</span>
                  <div v-if="update.commentFile" class="">
                    <img v-if="update.commentIsIamge" :src="update.commentFile" alt="Comment media"
                      class="w-7 h-7 object-cover rounded-lg" />
                    <video v-else :src="update.commentFile" autoplay loop muted
                      class="w-7 h-7 object-cover rounded-lg"></video>
                  </div>
                  with
                  <span class="text-gray-700 italic truncate max-w-[50px]" v-if="update.reply.content">{{
                    update.reply.content
                    }}</span>
                  <div v-if="update.replyFile" class="">
                    <img v-if="update.replyIsIamge" :src="update.replyFile" alt="Comment media"
                      class="w-7 h-7 object-cover rounded-lg" />
                    <video v-else :src="update.replyFile" autoplay loop muted
                      class="w-7 h-7 object-cover rounded-lg"></video>
                  </div>
                  on pin
                </span>
              </div>

              <!-- Превью пина -->
              <RouterLink @click="closeModal" :to="`/pin/${update.pin_id}`" class="mr-4 flex-shrink-0">
                <img v-if="update.isImage" :src="update.file" alt="Liked Pin" class="w-10 h-10 object-cover rounded" />
                <video v-else :src="update.file" autoplay loop muted class="w-10 h-10 object-cover rounded"></video>
              </RouterLink>

              <!-- Дата -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- Метка New -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </div>

            <div v-if="update.update_type == 'like_reply'" :class="[
              'rounded-lg flex items-center w-full h-24 relative hover:bg-purple-300 transition',
              !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
            ]">
              <!-- Аватар пользователя -->
              <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                class="mr-2 w-16 h-16 flex-shrink-0 flex justify-center items-center">
                <img :src="update.image" alt="User Avatar" class="w-16 h-16 object-cover rounded-full" />
              </RouterLink>

              <!-- Колонка с текстом -->
              <div class="flex flex-col justify-center overflow-hidden mr-auto max-w-[220px]">
                <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                  class="text-black text-md font-bold truncate hover:underline">
                  {{ update.user.username }}
                </RouterLink>
                <span class="text-black text-sm font-medium flex flex-wrap gap-0.5">
                  ❤️liked your reply
                  <span class="text-gray-700 italic truncate max-w-[50px]" v-if="update.reply.content">{{
                    update.reply.content
                    }}</span>
                  <div v-if="update.replyFile" class="">
                    <img v-if="update.replyIsIamge" :src="update.replyFile" alt="Comment media"
                      class="w-7 h-7 object-cover rounded-lg" />
                    <video v-else :src="update.replyFile" autoplay loop muted
                      class="w-7 h-7 object-cover rounded-lg"></video>
                  </div>
                  on comment
                  <span class="text-gray-700 italic truncate max-w-[50px]" v-if="update.comment.content">{{
                    update.comment.content
                    }}</span>
                  <div v-if="update.commentFile" class="">
                    <img v-if="update.commentIsIamge" :src="update.commentFile" alt="Comment media"
                      class="w-7 h-7 object-cover rounded-lg" />
                    <video v-else :src="update.commentFile" autoplay loop muted
                      class="w-7 h-7 object-cover rounded-lg"></video>
                  </div>
                  on pin
                </span>
              </div>

              <!-- Превью пина -->
              <RouterLink @click="closeModal" :to="`/pin/${update.pin_id}`" class="mr-4 flex-shrink-0">
                <img v-if="update.isImage" :src="update.file" alt="Liked Pin" class="w-10 h-10 object-cover rounded" />
                <video v-else :src="update.file" autoplay loop muted class="w-10 h-10 object-cover rounded"></video>
              </RouterLink>

              <!-- Дата -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- Метка New -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </div>

            <div v-if="update.update_type == 'pin_created_for_followers'" :class="[
              'rounded-lg flex items-center w-full h-24 relative hover:bg-purple-300 transition',
              !update.is_read ? 'border-l-4 border-blue-500 bg-blue-50' : ''
            ]">
              <!-- Аватар пользователя -->
              <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                class="mx-2 w-20 h-24 flex-shrink-0 flex justify-center items-center">
                <img :src="update.image" alt="User Avatar" class="w-20 h-20 object-cover rounded-full" />
              </RouterLink>

              <!-- Колонка с текстом -->
              <div class="flex flex-col justify-center overflow-hidden mr-auto max-w-[180px]">
                <RouterLink @click="closeModal" :to="`/user/${update.user.username}`"
                  class="text-black text-md font-bold truncate hover:underline">
                  {{ update.user.username }}
                </RouterLink>
                <span class="text-black text-md font-medium">
                  whom you follow, published a new pin
                </span>
              </div>

              <!-- Превью пина -->
              <RouterLink @click="closeModal" :to="`/pin/${update.pin_id}`" class="mr-4 flex-shrink-0">
                <img v-if="update.isImage" :src="update.file" alt="Liked Pin" class="w-10 h-10 object-cover rounded" />
                <video v-else :src="update.file" autoplay loop muted class="w-10 h-10 object-cover rounded"></video>
              </RouterLink>

              <!-- Дата -->
              <span class="absolute top-2 right-2 font-medium text-gray-600 text-xs">
                {{ formatTime(update.created_at) }}
              </span>

              <!-- Метка New -->
              <span v-if="!update.is_read" class="absolute bottom-2 right-2 text-xs text-blue-600 font-semibold">
                ● New
              </span>
            </div>

          </div>

          <div v-if="isPinsLoading" class="flex item-center justify-center">
            <span class="loader2"></span>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>


<style>
/* Анимация плавного появления (fade) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.loader2 {
  width: 48px;
  height: 48px;
  background: #FFF;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

.loader2::after {
  content: '';
  box-sizing: border-box;
  position: absolute;
  left: 6px;
  top: 10px;
  width: 12px;
  height: 12px;
  color: #FF3D00;
  background: currentColor;
  border-radius: 50%;
  box-shadow: 25px 2px, 10px 22px;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>