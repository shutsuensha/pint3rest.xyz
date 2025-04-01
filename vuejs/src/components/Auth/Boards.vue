<script setup>
import { onMounted, ref, onBeforeUnmount, onActivated, onDeactivated, nextTick } from 'vue';
import axios from 'axios';
import PinsByBoard from '@/components/Auth/PinsByBoard.vue';

import { useSelectedBoard } from "@/stores/userSelectedBoard";

const userSelectedBoardStore = useSelectedBoard();


const props = defineProps({
  user_id: Number,
  auth_user_id: Number
})

const loading = ref(true)

const boards = ref([])

const canEdit = ref(false)

const selectedBoardId = ref(null)
const selectedBoardname = ref(null)

const pinsSectionWrapper = ref(null)

onMounted(async () => {
  canEdit.value = props.user_id === props.auth_user_id
  try {
    const response = await axios.get(`/api/boards/user/${props.user_id}`, { withCredentials: true });
    boards.value = response.data;
  } catch (error) {
    console.error(error)
  }

  for (let i = 0; i < boards.value.length; i++) {
    try {
      const response = await axios.get(`/api/boards/${boards.value[i].id}`, {
        params: { offset: 0, limit: 10 },
        withCredentials: true,
      });
      boards.value[i].pins = response.data
      for (let j = 0; j < boards.value[i].pins.length; j++) {
        try {
          const pinResponse = await axios.get(`/api/pins/upload/${boards.value[i].pins[j].id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            boards.value[i].pins[j].file = blobUrl;
            boards.value[i].pins[j].isImage = true;
          } else {
            boards.value[i].pins[j].file = blobUrl;
            boards.value[i].pins[j].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }
      }
    } catch (error) {
      console.error(error)
    }
  }

  loading.value = false
})

const showAddBoard = ref(false);

const boardName = ref('');

const closeModal = () => {
  showAddBoard.value = false;
  boardName.value = '';
};

const createBoard = async () => {
  if (!boardName.value.trim()) return;
  try {
    const response = await axios.post(`/api/boards/`, {
      title: boardName.value.trim()
    }, {
      withCredentials: true
    });
    const new_board = response.data
    boards.value.push(new_board)
  } catch (error) {
    console.error(error)
  }
  closeModal();
};


const deleteBoard = async (boardId) => {
  try {
    const response = await axios.delete(`/api/boards/${boardId}`, { withCredentials: true });
    // Удаляем доску из массива после успешного удаления
    boards.value = boards.value.filter(board => board.id !== boardId);
  } catch (error) {
    console.error('Error deleting board:', error);
  }
  if (userSelectedBoardStore.selectedBoard.id === boardId) {
    userSelectedBoardStore.setBoard(null)
  }
  if (selectedBoardId.value === boardId) {
    selectedBoardId.value = null
    selectedBoardname.value = null
    await nextTick()
  }
};

async function laodPinsByBoard(boardId, boardName) {
  // Сбрасываем значение выбранного борда
  selectedBoardId.value = null
  selectedBoardname.value = null
  await nextTick()

  // Обновляем выбранный борд
  selectedBoardId.value = boardId
  selectedBoardname.value = boardName
  await nextTick()

  if (pinsSectionWrapper.value) {
    pinsSectionWrapper.value.scrollIntoView({ behavior: 'smooth' })
  }


}


</script>

<template>
  <div class="mt-10 ml-20">
    <div v-if="loading" class="flex items-center justify-center h-full p-2">
      <span class="text-center loader2"></span>
    </div>
    <div v-else class="">
      <div v-if="canEdit" class="flex justify-center items-center w-full mb-6">
        <button @click="showAddBoard = true"
          class="bg-white bg-opacity-80 rounded-full p-3 shadow-md focus:outline-none flex justify-center items-center hover:bg-gray-100 transition">
          Add Board
        </button>
      </div>
      <div class="grid grid-cols-5 gap-2 mx-2">
        <div v-for="board in boards" :key="board.id" @click="laodPinsByBoard(board.id, board.title)"
          class="shadow-md rounded-2xl p-4 hover:shadow-lg transition cursor-pointer hover:bg-gray-200"
          :class="[board.id === selectedBoardId ? 'bg-gray-200' : 'bg-white']">
          <!-- Коллаж превью борда -->
          <div class="w-full h-44 grid grid-cols-2 gap-1">
            <!-- Левая часть (большая картинка) -->
            <div class="relative col-span-1 row-span-2">
              <img v-if="board.pins && board.pins.length && board.pins[0].isImage" :src="board.pins[0].file"
                alt="Board preview" class="object-cover w-full h-full rounded-md" />
              <video v-if="board.pins && board.pins.length && !board.pins[0].isImage" :src="board.pins[0].file"
                alt="Board preview" class="object-cover w-full h-full rounded-md" autoplay loop muted></video>
            </div>

            <!-- Правая часть (4 ячейки в сетке 2x2) -->
            <div class="col-span-1 grid grid-cols-2 grid-rows-2 gap-1">
              <div v-if="board.pins" v-for="(pin, index) in board.pins.slice(1, 5)" :key="index" class="relative">
                <img v-if="pin.isImage" :src="pin.file" alt="Pin" class="object-cover w-full h-full rounded-md" />
                <video autoplay loop muted v-if="!pin.isImage" :src="pin.file" alt="Pin"
                  class="object-cover w-full h-full rounded-md"></video>

                <!-- Если это последняя ячейка (index === 3) и есть больше 5 пинов, показываем оверлей "+N" -->
                <div v-if="board.pins && index === 3 && board.pins.length > 5"
                  class="absolute inset-0 bg-black/50 flex items-center justify-center text-white text-lg font-semibold">
                  +{{ board.pins.length - 5 }}
                </div>
              </div>
            </div>
          </div>

          <!-- Заголовок борда и какая-то информация -->
          <h3 class="text-xl text-center  text-bkack font-bold dark:text-white mt-12">
            {{ board.title }}
          </h3>

          <!-- Кнопка Delete (если canEdit == true) -->
          <div v-if="canEdit" class="mt-2 flex justify-end">
            <button @click.stop="deleteBoard(board.id)"
              class="px-3 py-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition">
              Delete
            </button>
          </div>
        </div>
      </div>
      <div v-if="boards.length === 0">
        <section class="text-center flex flex-col justify-center items-center relative">
          <h1 class="text-2xl font-bold mb-4">no boards</h1>
          <img class="h-72 rounded-xl" src="https://i.pinimg.com/736x/40/f1/b0/40f1b01bf3df9bc24bdbad4589125023.jpg"
            alt="not found image">
        </section>
      </div>

      <div ref="pinsSectionWrapper" class="mt-10 min-h-[500px]">
        <PinsByBoard v-if="selectedBoardId" :user_id="user_id" :auth_user_id="auth_user_id" :boardId="selectedBoardId"
          :canEdit="canEdit" :boardName="selectedBoardname" />
      </div>


    </div>
    <div v-if="showAddBoard"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-40 backdrop-blur-sm"
      @click.self="closeModal">
      <div class="bg-white p-6 rounded-2xl shadow-lg w-96 max-w-full z-50">
        <h2 class="text-xl font-bold mb-4 text-gray-800">Create Board</h2>

        <!-- Поле ввода -->
        <input type="text" v-model="boardName" placeholder="Board name"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 text-gray-700">

        <!-- Кнопки -->
        <div class="flex justify-end gap-3 mt-5">
          <button @click="closeModal"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition">Cancel</button>
          <button @click="createBoard"
            class="px-5 py-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
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