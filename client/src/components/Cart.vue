<template>
  <div>
    <div v-if="cart.length === 0">
      <p>Your cart is empty. Please add some products.</p>
    </div>
    <div v-else>
      <div v-for="product in cart">
        <div class="flex flex-wrap p-2 align-items-center gap-3">
          <img class="w-4rem shadow-2 flex-shrink-0 border-round" :src="product.picture" :alt="product.plate_name"/>
          <div class="flex-1 flex flex-column gap-2">
            <span class="font-bold w-10rem">{{ product.quantity }} x {{ product.plate_name }}</span>
          </div>
          <span class="font-bold text-900">{{ product.quantity * product.price }} EUR-</span>
        </div>
        <Button icon="pi pi-plus" rounded @click="incrementProduct(product.plate_id)"></Button>
        <Button icon="pi pi-minus" rounded @click="decrementProduct(product.plate_id)"></Button>
      </div>
      <button @click="submitOrder">SEND ORDER!</button>
    </div>
  </div>
</template>

<script>
import OrderList from "primevue/orderlist";
import Button from "primevue/button";

export default {
  components: {Button, OrderList},
  data() {
    return {
      products: [],
      menu: []
    }
  },
  methods: {
    async submitOrder() {
      await this.$store.dispatch('submitOrder', {products: this.products})
      this.$router.replace('/'); // navigate to home page
    },
    incrementProduct(id) {
      this.$store.commit('addToOrder', id);
    },
    decrementProduct(id){
      this.$store.commit('removeFromOrder', id);
    }
  },
  mounted() {
    this.products = this.$store.getters.products
    this.menu = this.$store.getters.menu
  },
  computed: {
    cart: function () {
      return this.products.map(item1 => {
        const correspondingItem = this.menu.find(item2 => item1.plate_id === item2.plate_id);
        if (correspondingItem) {
          return {...item1, ...correspondingItem};
        }
      });
    }
  }

}
</script>