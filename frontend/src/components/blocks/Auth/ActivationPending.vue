<template>
  <div class="activation-pending">
    <h2 class="activation-pending__title">Подтверждение аккаунта</h2>
    <p class="activation-pending__text">
      Ссылка для подтверждения аккаунта была отправлена на вашу почту:
      <b>{{ email }}</b
      >.
    </p>
    <p class="activation-pending__text">
      Если вы не получили письмо, вы можете отправить его повторно.
    </p>
    <div class="activation-pending__actions">
      <button class="activation-pending__button" @click="resendActivation">
        Отправить письмо повторно
      </button>
      <button
        class="activation-pending__button activation-pending__button--secondary"
        @click="$emit('switch', 'login')"
      >
        Назад ко входу
      </button>
    </div>
    <p v-if="successMessage" class="activation-pending__success">
      {{ successMessage }}
    </p>
    <p v-if="errorMessage" class="activation-pending__error">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import api from '../../../api/axios'

export default {
  name: 'ActivationPending',
  emits: ['switch'], // Добавляем switch в emits
  data() {
    return {
      email: localStorage.getItem('activationEmail') || '',
      successMessage: '',
      errorMessage: '',
    }
  },
  methods: {
    async resendActivation() {
      this.successMessage = ''
      this.errorMessage = ''
      try {
        await api.post('/auth/users/resend_activation/', { email: this.email })
        this.successMessage = 'Письмо успешно отправлено. Проверьте вашу почту.'
      } catch {
        this.errorMessage = 'Не удалось отправить письмо. Попробуйте позже.'
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.activation-pending {
  //text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-family: Montserrat, sans-serif;
//   align-items: center;

  &__title {
    font-size: 31px;
    font-family: Montserrat;
    font-weight: 700;
    margin: auto;
    margin-bottom: 36px;
  }

  &__text {
    margin-bottom: 15px;
    font-size: 16px;
    //color: #555;
  }

  &__actions {
    margin-top: 20px;
    display: flex;
    gap: 10px;
    justify-content: space-between;
  }

  &__button {
    padding: 10px 10px;
    border: none;
    background-color: #d58c51;
    color: #fff;
    font-family: Montserrat, sans-serif;
    font-size: 16px;
    font-weight: 500;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  &__button--secondary {
    background-color: #f0f0f0;
    color: #333;
  }

  &__button:hover {
    background-color: #b56f43;
  }

  &__button--secondary:hover {
    background-color: #e0e0e0;
  }

  &__success {
    margin-top: 20px;
    color: green;
  }

  &__error {
    margin-top: 20px;
    color: red;
  }
}
</style>
