<template>
  <section>

    <h4>Chat with us!</h4>
    <div v-for="(message, idx) in messages" :key="idx">
      <div v-if="message.author === 'client'" class="bg-green-100 content-info mt-2 border-round-sm shadow-1 py-1">
        <span><i class="pi pi-user p-mr-2"></i></span>
        <p>{{ message.text }}</p>
      </div>
      <div v-else class="bg-blue-100 content-info mt-2 border-round-sm shadow-1 py-1">
        <span><i class="pi pi-server p-mr-2"></i><p>{{ message.text }}</p></span>
      </div>
    </div>


    <div class="card">
      <div class="field">
        <label for="rating">Message</label>
        <input type="text" v-model="message" @keyup.enter="sendMessage"
               class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary w-full">
      </div>
    </div>

    <div class="flex align-items-center justify-content-center pt-2 px-3 gap-2">
      <button
          type="button" mode="flat"
          @click="sendMessage"
          class="p-3 flex align-items-center justify-content-center w-5 gap-2 bg-gray-900 shadow-1 border-none cursor-pointer hover:bg-gray-800 transition-duration-200"
          style="border-radius: 50px;">
        <span class="font-medium text-white white-space-nowrap">Send</span>
        <i class="pi pi-telegram text-white"></i>
      </button>

      <button
          type="button" mode="flat"
          @click="stop"
          class="p-3 flex align-items-center justify-content-center w-5 gap-2 bg-gray-900 shadow-1 border-none cursor-pointer hover:bg-gray-800 transition-duration-200"
          style="border-radius: 50px;">
        <span class="font-medium text-white white-space-nowrap">Stop</span>
        <i class="pi pi-stop-circle text-white"></i>
      </button>
    </div>
    <p v-if="isWaiting">Wait for response...</p>
  </section>
</template>

<script>
export default {
  name: 'Chat',
  data: () => ({
    message: '',
    messages: [],
    isWaiting: false,
    userActivityThrottlerTimeout: null,
    userActivityTimeout: null,
    USER_INACTIVE_TIMEOUT: 10000
  }),
  beforeMount() {
    this.activateActivityTracker();
  },
  beforeDestroy() {
    window.removeEventListener("mousemove", this.userActivityThrottler);
    window.removeEventListener("scroll", this.userActivityThrottler);
    window.removeEventListener("keydown", this.userActivityThrottler);
    window.removeEventListener("resize", this.userActivityThrottler);

    clearTimeout(this.userActivityTimeout);
    clearTimeout(this.userActivityThrottlerTimeout);
  },
  methods: {
    async sendMessage() {
      const message = this.message

      if (message === '') {
        alert('Please add a message!');
        return;
      }

      this.messages.push({
        text: message,
        author: 'client'
      });

      this.isWaiting = true;
      setTimeout(() => {
        this.isWaiting = false

        let responses = [
          'Can we go to the park.',
          'Where is the orange cat? Said the big black dog.',
          'We can make the bird fly away.',
          'We can go down to the store with the dog.',
          'My big yellow cat ate the little black bird.',
          'I like to read my book at school.',
          'We are going to swim at the park.'
        ];

        const randomIndex = Math.floor(Math.random() * responses.length);

        this.message = '';
        this.messages.push({
          text: responses[randomIndex],
          author: 'server'
        });
      }, 3000);
    },
    stop() {
      this.$router.replace('/');
    },

    activateActivityTracker() {
      window.addEventListener("mousemove", this.resetUserActivityTimeout);
      window.addEventListener("scroll", this.resetUserActivityTimeout);
      window.addEventListener("keydown", this.resetUserActivityTimeout);
      window.addEventListener("resize", this.resetUserActivityTimeout);
      window.addEventListener("mousemove", this.userActivityThrottler);
    },

    resetUserActivityTimeout() {
      clearTimeout(this.userActivityTimeout);
      this.userActivityTimeout = setTimeout(() => {
        alert('TIMEOUT! YOU WILL BE REDIRECTED TO THE MENU PAGE')
        this.$router.replace('/');
      }, this.USER_INACTIVE_TIMEOUT);
    },

    userActivityThrottler() {
      if (!this.userActivityThrottlerTimeout) {
        this.userActivityThrottlerTimeout = setTimeout(() => {
          this.resetUserActivityTimeout();

          clearTimeout(this.userActivityThrottlerTimeout);
          this.userActivityThrottlerTimeout = null;
        }, this.USER_INACTIVE_TIMEOUT);
      }
    },
  }
}
</script>
