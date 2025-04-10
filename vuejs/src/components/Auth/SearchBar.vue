<template>
	<nav :class="[
		'fixed top-0 left-20 w-full z-40 bg-white',
		showSearchSection ? '' : 'bg-opacity-20 backdrop-blur-sm'
	]">
		<div class="flex items-center justify-between px-6 mt-2">
			<div class="relative flex-1 mr-20">
				<input v-model="searchValue" type="text" placeholder="Search" class="transition-all duration-300 cursor-text
             bg-white bg-opacity-20 backdrop-blur-lg text-black
             text-md rounded-3xl block w-full py-3 pl-12 pr-12
             outline-none border border-black
             focus:shadow-2xl focus:shadow-blue-500/50" @click="onClick" @keydown.enter="onEnter" />
				<!-- Иконка поиска слева -->
				<div class="absolute left-1 top-4 pl-3 flex items-center pointer-events-none">
					<i class="pi pi-search text-black"></i>
				</div>
				<!-- Кнопка-крестик справа -->
				<button v-if="showSearchSection" @click="showSearchSection = false"
					class="absolute right-3 top-1/2 transform -translate-y-1/2 px-3 py-1 rounded-full text-lg text-white bg-black">
					✕
				</button>
			</div>
		</div>
	</nav>

	<transition name="slide-down" appear>
		<!-- Оверлей на весь экран -->
		<section v-if="showSearchSection"
			class="fixed inset-0 z-30 bg-black flex items-start justify-center transition-opacity duration-700 ease-in-out"
			:class="{ 'bg-opacity-50': showSearchSection, 'bg-opacity-0': !showSearchSection }"
			@click.self="showSearchSection = false">
			<!-- Белый блок с контентом (не занимает всю область) -->
			<div class="mt-14 ml-20 mr-20 bg-white px-8 py-2 w-full rounded-b-2xl shadow">
				<h1 v-if="latestSearch && latestSearch.length > 0" class="text-xl mb-4  mt-2">Recently Search</h1>
				<div v-if="latestSearch" class="grid grid-cols-8 gap-4">
					<div v-for="(query, index) in latestSearch" :key="index" @click="searchValue = query;onEnter()"
						class="flex items-center bg-gray-100 hover:bg-gray-200 px-4 rounded-full py-2 cursor-pointer">
						<button @click.stop="deleteSearch(query)" class="mr-2 text-white bg-black rounded-full px-2">&times;</button>
						<span class="text-nowrap truncate">{{ query }}</span>
					</div>
				</div>
				<h1 class="text-xl mb-4  mt-4">Popular on Pinterest</h1>
				<div class="grid grid-cols-4 gap-4 mb-4">
					<div v-for="tag in available_tags" :key="tag.id" @click="showTagsPin(tag)"
						:class="[tag.color, 'hover:' + tag.color.replace('200', '400'), 'cursor-pointer rounded-3xl flex flex-row items-center']">
						<div v-if="tag.isImage">
							<img :src="tag.file" :alt="tag.name" class="w-32 h-32 object-cover rounded-l-3xl flex-shrink-0" />
						</div>
						<div v-else>
							<video :src="tag.file" class="w-32 h-32 object-cover rounded-l-3xl flex-shrink-0" autoplay loop
								muted></video>
						</div>
						<!-- Текст занимает оставшееся пространство и обрезается, если слишком длинный -->
						<p class="flex-1 text-md ml-4 truncate whitespace-nowrap">{{ tag.name }}</p>
					</div>
				</div>
			</div>
		</section>
	</transition>


</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import axios from 'axios'

const searchValue = ref('')
const showSearchSection = ref(false)

const router = useRouter();

const beforeShowSearchSection = ref(null)

const onClick = async () => {
	beforeShowSearchSection.value = showSearchSection.value
	showSearchSection.value = true

	if (beforeShowSearchSection.value == showSearchSection.value) {
		return;
	}
	try {
		const response = await axios.get('/api/search/latest', { withCredentials: true })
		latestSearch.value = response.data
	} catch (error) {
		console.error(error)
	}
	try {
		const response = await axios.get('/api/tags/', { withCredentials: true });
		// Берем только первые 10 элементов
		available_tags.value = response.data.slice(12, 24);

		// Обновляем прогресс после получения списка тегов
		available_tags.value.forEach(tag => {
			tag.color = randomBgColor();
		});
	} catch (error) {
		console.log(error);
	}

	for (let i = 0; i < available_tags.value.length; i++) {
		try {
			const response = await axios.get(`/api/pins/tag/${available_tags.value[i].name}`, {
				params: { offset: 0, limit: 1 },
				withCredentials: true,
			});

			if (response.data.length === 1) {
				const pin_id = response.data[0].id;
				try {
					const pinResponse = await axios.get(`/api/pins/upload/${pin_id}`, { responseType: 'blob' });
					const blobUrl = URL.createObjectURL(pinResponse.data);
					const contentType = pinResponse.headers['content-type'];
					if (contentType.startsWith('image/')) {
						available_tags.value[i].file = blobUrl;
						available_tags.value[i].isImage = true;
					} else {
						available_tags.value[i].file = blobUrl;
						available_tags.value[i].isImage = false;
						available_tags.value[i].videoPlayer = null;
					}
				} catch (error) {
					console.error(error);
				}
			} else {
				available_tags.value[i].file = 'https://i.pinimg.com/736x/40/f1/b0/40f1b01bf3df9bc24bdbad4589125023.jpg';
				available_tags.value[i].isImage = true;
			}
		} catch (error) {
			console.error(error);
		}
	}
}

const available_tags = ref(null)
const bgColors = ref(['bg-red-200', 'bg-orange-200', 'bg-amber-200', 'bg-lime-200', 'bg-green-200', 'bg-emerald-200', 'bg-teal-200', 'bg-sky-200', 'bg-blue-200', 'bg-indigo-200', 'bg-violet-200', 'bg-purple-200', 'bg-fuchsia-200', 'bg-pink-200', 'bg-rose-200', 'bg-cyan-200', 'bg-slate-200', 'bg-stone-200'])

const randomBgColor = () => {
	const randomIndex = Math.floor(Math.random() * bgColors.value.length);
	return bgColors.value[randomIndex];
};

async function deleteSearch(query) {
	try {
		await axios.delete("/api/search/", {
			data: { query: query.trim() },  // Передаём данные в `data`
			withCredentials: true
		})
		latestSearch.value = latestSearch.value.filter(item => item !== query.trim());
	} catch (error) {
		console.error(error)
	}
}

const latestSearch = ref(null)


function showTagsPin(tag) {
	showSearchSection.value = false
	router.push(`/?tag=${tag.name}`);
}

async function onEnter() {
	if (!searchValue.value.trim()) {
		return
	}
	try {
		await axios.post("/api/search/", {
			query: searchValue.value.trim()
		}, { withCredentials: true })
		latestSearch.value.unshift(searchValue.value.trim());
	} catch (error) {
		console.error(error)
	}
	let tempSearch = searchValue.value.trim()
	searchValue.value = ''
	showSearchSection.value = false
	router.push(`/?search=${tempSearch}`);
}

</script>

<style scoped>
/* Анимация для появления секции */
.slide-down-enter-active,
.slide-down-leave-active {
	transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
	transform: translateY(-20px);
	opacity: 0;
}

.slide-down-enter-to,
.slide-down-leave-from {
	transform: translateY(0);
	opacity: 1;
}
</style>
