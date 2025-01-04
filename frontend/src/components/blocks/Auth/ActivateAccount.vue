<template>
  <div class="activate-account">
    <h2 class="activate-account__title">Подтверждение аккаунта</h2>
    <p 
      v-if="!successMessage && !errorMessage"
      class="activate-account__message"
    >
      Подтверждаем ваш аккаунт...
    </p>
    <p
      v-if="successMessage"
      class="activate-account__message activate-account__message--success"
    >
      {{ successMessage }}
    </p>
    <p
      v-if="errorMessage"
      class="activate-account__message activate-account__message--error"
    >
      {{ errorMessage }}
    </p>
    <div
      v-if="successMessage || errorMessage"
      class="activate-account__redirect"
    >
      <p class="activate-account__text">
        Вы будете автоматически перенаправлены на страницу входа через
        <span class="activate-account__countdown">{{ redirectCountdown }}</span>
        секунд.
      </p>
      <p class="activate-account__text">
        Если перенаправление не произошло, нажмите
        <span class="activate-account__link" @click="redirectToLogin"
          >здесь</span
        >.
      </p>
    </div>
    <div
      v-if="errorMessage && !successMessage"
      class="activate-account__actions"
    >
      <button class="activate-account__button" @click="resendActivation">
        Отправить письмо повторно
      </button>
    </div>
  </div>
</template>

<script>
import api from '../../../api/axios'
import { useToast } from 'vue-toastification'

export default {
  name: 'ActivateAccount',
  props: {
    uid: {
      type: String,
      required: true,
      default: '',
    },
    token: {
      type: String,
      required: true,
      default: '',
    },
  },
  emits: ['switch'], // Добавляем switch в emits
  setup() {
    const toast = useToast()
    return {
      toast,
    }
  },
  data() {
    return {
      successMessage: '',
      errorMessage: '',
      redirectCountdown: 5,
    }
  },
  mounted() {
    this.activateAccount()
  },
  methods: {
    async activateAccount() {
      try {
        await api.post('/auth/users/activation/', {
          uid: this.uid,
          token: this.token,
        })
        this.successMessage = 'Аккаунт успешно активирован!'
        this.toast.success('Аккаунт успешно активирован!')
        this.errorMessage = ''
        this.startRedirectCountdown()
      } catch (error) {
        if (error.response && error.response.status === 403) {
          this.errorMessage = 'Аккаунт уже активирован. Вы можете войти.'
          this.toast.error('Аккаунт уже активирован. Вы можете войти.')
          this.startRedirectCountdown()
        } else {
          this.toast.error('Произошла ошибка. Попробуйте позже.')
          this.errorMessage = 'Ошибка активации аккаунта. Попробуйте позже.'
        }
        this.successMessage = ''
      }
    },
    async resendActivation() {
      this.successMessage = ''
      this.errorMessage = ''
      try {
        await api.post('/auth/users/resend_activation/', {
          email: localStorage.getItem('email'),
        })
        this.toast.success('Письмо успешно отправлено. Проверьте вашу почту.')
        this.successMessage = 'Письмо успешно отправлено. Проверьте вашу почту.'
      } catch {
        this.toast.error('Произошла ошибка. Попробуйте позже.')
        this.errorMessage =
          'Не удалось отправить письмо повторно. Попробуйте позже.'
      }
    },

    startRedirectCountdown() {
      const interval = setInterval(() => {
        if (this.redirectCountdown > 1) {
          this.redirectCountdown -= 1
        } else {
          clearInterval(interval)
          this.redirectToLogin()
        }
      }, 1000)
    },
    redirectToLogin() {
      this.$emit('switch', 'login')
    },
  },
}
</script>

<style lang="scss" scoped>
.activate-account {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-family: Montserrat, sans-serif;

  &__title {
    font-size: 31px;
    font-family: Montserrat;
    font-weight: 700;
    margin: auto;
    margin-bottom: 36px;
  }

  &__message {
    font-size: 16px;
    margin: 10px 0;

    &--success {
      color: green;
    }

    &--error {
      color: red;
    }
  }

  &__redirect {
    margin-top: 20px;

    &__countdown {
      font-weight: bold;
      color: #d58c51;
    }

    &__link {
      color: #d58c51;
      cursor: pointer;
      text-decoration: underline;

      &:hover {
        color: #b56f43;
      }
    }
  }

  &__actions {
    margin-top: 20px;
    margin: auto;

  }

  &__text {
    margin-bottom: 15px;
    font-size: 16px;
    // color: #555;
  }

  &__button {
    margin-top: 10px;
    
    padding: 10px 20px;
    border: none;
    background-color: #d58c51;
    color: #fff;
    font-size: 16px;
    font-weight: 500;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
      background-color: #b56f43;
    }
  }
}
</style>
