<template>
  <div class="login-container p-d-flex p-jc-center p-ai-center">
    <div class="login-card p-p-4" style="width: auto">
      <div class="p-d-flex p-jc-center p-mb-4">
        <i class="pi pi-user p-mr-2"></i>
        <h3>{{ submitButtonCaption }}</h3>
      </div>

      <form @submit.prevent="submitForm">
        <div class="p-fluid">
          <div class="p-field">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" class="p-inputtext">
          </div>

          <div class="p-field">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" class="p-inputtext">
          </div>
        </div>

        <p v-if="!formIsValid">Please enter a valid email and password (must be at least 4 chars long).</p>


        <div class="p-d-flex p-jc-center p-mt-2">
          <button class="p-button p-button-primary">{{ submitButtonCaption }}</button>
        </div>
        <div class="p-d-flex p-jc-center p-mt-2">
          <button type="button" class="p-button p-button-secondary" @click="switchAuthMode">{{ switchModeButtonCaption }}</button>
        </div>
      </form>


    </div>
  </div>

</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      formIsValid: true,
      mode: 'login',
      isLoading: false,
      error: ''
    }
  },
  computed: {
    submitButtonCaption() {
      if (this.mode === 'login') {
        return 'Log in'
      } else {
        return 'Sign Up'
      }
    },
    switchModeButtonCaption() {
      if (this.mode === 'login') {
        return 'Sign Up Instead'
      } else {
        return 'Log In Instead'
      }
    }
  },
  methods: {
    async submitForm() {
      if (this.email === "" || !this.email.includes('@') || this.password.length < 4) {
        this.formIsValid = false;
        return;
      }
      this.isLoading = true;
      try {
        if (this.mode === 'login') {
          await this.$store.dispatch('login', {
            email: this.email,
            password: this.password,
          })
        } else {
          await this.$store.dispatch('signup', {
            email: this.email,
            password: this.password,
            username: 'test'
          })
          this.$router.replace('/');
        }
      } catch (err) {
        console.log(this.error)
      }
      this.isLoading = false;
      this.$router.replace('/'); // navigate to home page
    },
    switchAuthMode() {
      if (this.mode === 'login') {
        this.mode = 'signup'
      } else {
        this.mode = 'login'
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  width: 300px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.p-mr-2 {
  margin-right: 0.5rem;
}

.p-mb-4 {
  margin-bottom: 1rem;
}

.p-mt-2 {
  margin-top: 0.5rem;
}

.p-button-primary {
  background-color: rebeccapurple;
  color: #fff;
  border: none;
}
</style>