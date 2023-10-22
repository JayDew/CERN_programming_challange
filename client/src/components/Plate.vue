<template>
  <div v-if="plate">
    <div class="p-2 border-round-xl"
         style="background: var(--style-cards-bg); border: 1px solid rgba(255, 255, 255, 0.1); backgroundBlendMode: normal, color-dodge; width: 300px;">
      <div class="content bg-white h-full p-2">
        <div class="flex align-items-center gap-2 py-2 px-3">
          <h1 class="font-medium text-gray-900">{{ plate.plate_name }}</h1>
        </div>
        <div
            class="mt-3 content-image-wrapper relative text-center w-full flex align-items-center justify-content-center">
          <img class="shadow-2 flex-shrink-0 border-round" :src="plate.picture"/>
        </div>
        <div class="rating mt-2 mb-2 flex align-items-center justify-content-center gap-2 w-full ">
          <i class="pi pi-star-fill text-gray-900" v-for="n in (plate.rating) ? Math.round(parseInt(plate.rating)) : 0"
             :key="n"></i>
          <i class="pi pi-star-fill text-gray-600"
             v-for="n in (5 - ((plate.rating) ? Math.round(parseInt(plate.rating)) : 0))" :key="n"></i>
        </div>
        <div class="flex align-items-center justify-content-between py-2 px-3 gap-2">
          <div class="flex align-items-center justify-content-center gap-1 border-right-1 surface-border pr-2">
            <i class="pi pi-euro"></i>
            <span class="font-small text-gray-900 white-space-nowrap">{{ plate.price }}</span>
          </div>
          <div class="flex align-items-center gap-1 justify-content-center gap-1 border-right-1 surface-border px-2">
            <i class="pi pi-check"></i>
            <span class="font-small text-gray-900 white-space-nowrap">Delicious</span>
          </div>
          <div class="flex align-items-center gap-1 justify-content-center gap-1 pl-2">
            <i class="pi pi-clock"></i>
            <span class="font-small text-gray-900 white-space-nowrap">15 mins</span>
          </div>
        </div>


        <div v-if="plate.rating" class="card">
          <h4>What others say:</h4>
          <div v-for="rev in reviews" class="content-info mt-2 border-round-sm bg-white-alpha-10 shadow-1 py-1"
               style="backdropFilter: blur(27px);">
            <div class="rating mt-2 mb-2 flex align-items-center justify-content-center gap-2 w-full ">
              <i class="pi pi-star-fill text-gray-900" v-for="n in (rev.rating) ? Math.round(parseInt(rev.rating)) : 0"
                 :key="n"></i>
              <i class="pi pi-star-fill text-gray-600"
                 v-for="n in (5 - ((rev.rating) ? Math.round(parseInt(rev.rating)) : 0))" :key="n"></i>
            </div>
            <div class="flex align-items-center justify-content-between py-2 px-3">
              <span class="font-medium text-black">{{ rev.review }}</span>
            </div>
          </div>
        </div>


        <form @submit.prevent="submitForm">
          <div class="card">
            <h5>Leave a review!</h5>
            <div class="field">
              <label for="rating">Rating</label>
              <input type="number" id="rating" v-model="rating"
                     class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary w-full">
            </div>
            <div class="field">
              <label for="Review">Review</label>
              <input id="review" type="text" v-model="review"
                     class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary w-full">
            </div>
          </div>

          <div class="flex align-items-center justify-content-center pt-2 px-3 gap-2">
            <button
                type="button" mode="flat"
                @click="submitForm"
                class="p-3 flex align-items-center justify-content-center w-5 gap-2 bg-gray-900 shadow-1 border-none cursor-pointer hover:bg-gray-800 transition-duration-200"
                style="border-radius: 50px;">
              <span class="font-medium text-white white-space-nowrap">Review</span>
              <i class="pi pi-thumbs-up-fill text-white"></i>
            </button>
          </div>
        </form>


      </div>
    </div>
  </div>
  <div v-else>Loading...</div>

</template>


<script setup>
import {useStore} from 'vuex';
import {onMounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";

const route = useRoute();
const router = useRouter();
const store = useStore(); // Access the Vuex store

const plate = ref();
const reviews = ref();
const review = ref();
const rating = ref();


onMounted(async () => {
  // retrieve data from vuex store
  const plate_id = route.params.plate_id;
  let plates = store.getters.menu
  plate.value = filterById(plates, plate_id)

  // get the reviews comments from server
  let token = store.getters.token;
  const URL_comments = `https://localhost:8443/api/review/${plate_id}`
  const response = await fetch(URL_comments, {
    method: 'GET', headers: {
      'Content-type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  });
  reviews.value = await response.json();
});

function filterById(plates, plate_id) {
  for (let i = 0; i < plates.length; i++) {
    if (plates[i].plate_id === parseInt(plate_id)) {
      return plates[i];
    }
  }
}

async function submitForm() {
  if (rating < 1 || rating > 5) {
    alert('RATING SHOULD BE BETWEEN 1 AND 5!')
    return;
  }

  const URL_ADD_REVIEW = "https://localhost:8443/api/review/add";
  const token = store.getters.token;

  let response = await fetch(URL_ADD_REVIEW, {
    method: 'POST',
    body: JSON.stringify({
      plate_id: plate.value.plate_id,
      review: review.value,
      rating: rating.value
    }),
    headers: {
      "Content-Type": "application/json; charset=utf-8", 'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json()

  if (response.status !== 200) {
    alert(data.detail);
  } else {
    alert('Comment added!')
    router.push('/') // navigate to home page
  }
}

</script>