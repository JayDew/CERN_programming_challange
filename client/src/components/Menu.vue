
<template>
    <div class="card">
        <DataView :value="plates" :layout="layout">
            <template #header>
              <h2>CERN R1 MENU</h2>
              <h5>(I wish...)</h5>
                <div class="flex justify-content-end">
                    <DataViewLayoutOptions v-model="layout" />
                </div>
            </template>

            <template #list="slotProps">
                <div class="col-12">
                    <div class="flex flex-column xl:flex-row xl:align-items-start p-4 gap-4"
                         @click="$router.push(`/plate/${slotProps.data.plate_id}`)">
                        <img class="w-9 sm:w-16rem xl:w-10rem shadow-2 block xl:block mx-auto border-round" :src="slotProps.data.picture" :alt="slotProps.data.plate_name" />
                        <div class="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-4">
                            <div class="flex flex-column align-items-center sm:align-items-start gap-3">
                                <div class="text-2xl font-bold text-900">{{ slotProps.data.plate_name }}</div>
                            </div>
                            <div>
                              <i class="pi pi-star-fill text-gray-900" v-for="n in (slotProps.data.rating ) ? Math.round(parseInt(slotProps.data.rating )) : 0" :key="n"></i>
                              <i class="pi pi-star-fill text-gray-600" v-for="n in (5 - ((slotProps.data.rating ) ? Math.round(parseInt(slotProps.data.rating )) : 0))" :key="n"></i>
                            </div>
                            <div class="flex sm:flex-column align-items-center sm:align-items-end gap-3 sm:gap-2">
                                <span class="text-2xl font-semibold">{{ slotProps.data.price }} € </span>
                                <Button icon="pi pi-shopping-cart" rounded></Button>
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <template #grid="slotProps">
                <div class="col-12 sm:col-6 lg:col-12 xl:col-4 p-2">
                    <div class="p-4 border-1 surface-border surface-card border-round">
                      <div class="flex flex-column align-items-center gap-3 py-5"
                           @click="$router.push(`/plate/${slotProps.data.plate_id}`)">
                      <img class="w-9 shadow-2 border-round" :src="slotProps.data.picture" :alt="slotProps.data.plate_name" />
                            <div class="text-2xl font-bold">{{ slotProps.data.plate_name }}</div>
                        </div>
                        <div class="flex align-items-center justify-content-between">
                            <span class="text-2xl font-semibold">{{ slotProps.data.price }} €</span>
                          <div>
                            <i class="pi pi-star-fill text-gray-900" v-for="n in (slotProps.data.rating ) ? Math.round(parseInt(slotProps.data.rating )) : 0" :key="n"></i>
                            <i class="pi pi-star-fill text-gray-600" v-for="n in (5 - ((slotProps.data.rating ) ? Math.round(parseInt(slotProps.data.rating )) : 0))" :key="n"></i>
                          </div>
                            <Button icon="pi pi-shopping-cart" rounded @click="addToCart(slotProps.data.plate_id)"></Button>
                        </div>
                    </div>
                </div>
            </template>
        </DataView>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Button from 'primevue/button';

import DataView from 'primevue/dataview';
import DataViewLayoutOptions from 'primevue/dataviewlayoutoptions'
import {useStore} from "vuex";

const plates = ref();
const layout = ref('grid');

const store = useStore();

onMounted(async () => {
    // fetch data from server
    const URL = "https://localhost:8443/api/plates"
    const response = await fetch(URL);
    const data = await response.json();
    plates.value = data;

    // fetch the reviews form the server
    let token = store.getters.token;
    for (let i=0; i< data.length; i++) {
      const URL_reviews = `https://localhost:8443/api/review/${data[i].plate_id}/average`
      const response = await fetch(URL_reviews, {
        method: 'GET', headers: {
          'Content-type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });
      plates.value[i]['rating'] = await response.json();
    }
    //save the menu in vuex
    store.commit('setMenu', {menu: data});
});

function addToCart(id) {
  store.commit('addToOrder', id);
  alert('Item added to cart!')
}
</script>

<style scoped>
div.flex:hover {
  cursor: pointer;
}
</style>
