
<template>
    <div v-for="(order, i) in orders">
        <div class="card xl:flex xl:justify-content-center">
            <OrderList v-model="orders[i].plates" listStyle="height:auto" dataKey="i">
                <template #header>
                    <div class="flex gap-5">
                        <span># {{ orders[i].order_id }}</span>
                        <span>{{ parseTimeToString(orders[i].order_time) }}</span>
                        <span>Total: {{ getOrderTotal(orders[i].order_id) }} €</span>
                        <span>Status: {{ orders[i].state }} </span>
                    </div>

                </template>
                <template #item="slotProps">
                    <div class="flex flex-wrap p-2 align-items-center gap-3">
                        <img class="w-4rem shadow-2 flex-shrink-0 border-round" :src="plateImage(slotProps.item.plate_id)" :alt="slotProps.item.name" />
                        <div class="flex-1 flex flex-column gap-2">
                            <span class="font-bold w-10rem">{{ slotProps.item.quantity }} x {{ slotProps.item.plate_name }}</span>
                        </div>
                        <span class="font-bold text-900">{{ platePrice(slotProps.item.plate_id) * slotProps.item.quantity }} €</span>
                    </div>
                </template>
            </OrderList>
          <div class="flex flex-column">
            <button @click="changeState(order.order_id, 'APPROVE')">APPROVE</button>
            <button @click="changeState(order.order_id,'REJECT')">REJECT</button>
            <button @click="changeState(order.order_id,'CANCEL')">CANCEL</button>
            <button @click="changeState(order.order_id, 'PREPARE')">PREPARE</button>
            <button @click="changeState(order.order_id, 'SERVE')">SERVE</button>
            <button @click="changeState(order.order_id, 'DELIVER')">DELIVER</button>
          </div>
        </div>
    </div>
</template>

<script setup>
import OrderList from 'primevue/orderlist';
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import {useRouter} from "vue-router";

const orders = ref(null);
const plates = ref();

const store = useStore(); // Access the Vuex store
const router = useRouter(); // Access the Vue router

onMounted(async () => {
    // fetch plates from server
    const URL = "https://localhost:8443/api/plates"
    const response = await fetch(URL);
    const data = await response.json();
    plates.value = data;

    // fetch orders from server
  const URL_ORDERS = "https://localhost:8443/api/orders"
  const token = store.getters.token
  const response_orders = await fetch(URL_ORDERS, {
    method: 'GET', headers: {
      'Content-type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  });
    const data_orders = await response_orders.json();
    orders.value = data_orders;
});


function platePrice(itemId) {
    return plates.value.find(plate => plate.plate_id === itemId).price
}

function plateImage(itemId) {
    return plates.value.find(plate => plate.plate_id === itemId).picture
}

function parseTimeToString(timestamp) {
    const regex = /(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})/;
    let matches = timestamp.match(regex);
    if (matches) {
        return matches[1] + " " + matches[2];
    }
}

function getOrderTotal(orderId) {
    let total = 0;
    orders.value.find(order => order.order_id === orderId).plates.forEach(plate => {
        total += platePrice(plate.plate_id) * plate.quantity;
    });
    return total.toFixed(2);
}

async function changeState(order_id, transition) {
  let data = {
    "order_id": order_id,
    "transition": transition
  }

  const URL_TRANSITION = 'http://localhost:8000/api/orders/change-state'
  const response = await fetch(URL_TRANSITION, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      'Authorization': `Bearer ${store.getters.token}`
    }
  });

  if (response.status === 200) {
    alert('TRANSITION TRIGGERED! IF VALID, CHANGES WILL BE REFLECTED IN THE UI.');
    // change state
    // fetch plates from server
    const URL = "https://localhost:8443/api/plates"
    const response = await fetch(URL);
    const data = await response.json();
    plates.value = data;

    // fetch orders from server
    const URL_ORDERS = "https://localhost:8443/api/orders"
    const token = store.getters.token
    const response_orders = await fetch(URL_ORDERS, {
      method: 'GET', headers: {
        'Content-type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    });
    const data_orders = await response_orders.json();
    orders.value = data_orders;
  } else {
    alert('ERROR')
  }

}
</script>