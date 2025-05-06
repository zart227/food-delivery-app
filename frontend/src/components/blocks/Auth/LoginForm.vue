<template>
  <form class="auth-form" @submit.prevent="handleSubmit">
    <h2 class="auth-form__title">Вход</h2>
    <InputField
      v-model="username"
      label="Имя пользователя"
      placeholder="Введите ваш username"
      :error="usernameError"
      autocomplete="username"
    />
    <InputField
      v-model="password"
      label="Пароль"
      type="password"
      placeholder="Введите ваш пароль"
      :error="passwordError"
      autocomplete="current-password"
    />
    <button class="auth-form__submit" type="submit">Войти</button>
    <span class="auth-form__link" @click="$emit('switch', 'forgotPassword')">
      Забыли пароль?
    </span>
    <span class="auth-form__link" @click="$emit('switch', 'register')">
      Зарегистрироваться
    </span>
  </form>
</template>

<script>
import InputField from '../../ui/InputField.vue'
import { useBasketStore } from '@/stores/basket'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification';


export default {
  name: 'LoginForm',
  components: { InputField },
  emits: ['switch'], // Добавляем switch в emits
  data() {
    return {
      username: '',
      password: '',
      usernameError: '',
      passwordError: '',
    }
  },
  methods: {
    async handleSubmit() {
      this.usernameError = ''
      this.passwordError = ''

      const authStore = useAuthStore()
      const basketStore = useBasketStore()
      const toast = useToast()

      try {
        // Авторизация пользователя
        await authStore.loginUser(this.username, this.password)

        // Загрузка корзины после успешной авторизации
        await basketStore.fetchUserBasket()
        toast.success('Вы успешно вошли в аккаунт!')
        // Перенаправляем на главную страницу
        await this.$router.push('/')
      } catch (error) {
        console.error('Полный объект ошибки:', error, error.response?.data);
        if (error.response && error.response.data && error.response.data.detail) {
          const message = error.response.data.detail;
          toast.error(message);
          this.usernameError = message;
        } else if (error.response && error.response.data) {
          const message = JSON.stringify(error.response.data);
          toast.error(message);
          this.usernameError = message;
        } else if (error instanceof Error) {
          toast.error(error.message);
          this.usernameError = error.message;
        } else if (typeof error === 'string') {
          toast.error(error);
          this.usernameError = error;
        } else {
          toast.error('Произошла ошибка. Попробуйте позже.');
          this.usernameError = 'Произошла ошибка. Попробуйте позже.';
        }
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  position: relative;
  box-sizing: border-box;

  &__title {
    font-size: 31px;
    font-family: Montserrat;
    font-weight: 700;
    margin: auto;
    margin-bottom: 36px;
  }

  &__submit {
    margin-top: 20px;
    padding: 10px 20px;
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

  &__submit:hover {
    background-color: #b56f43;
  }

  &__link {
    margin-top: 15px;
    font-size: 14px;
    color: #d58c51;
    cursor: pointer;
    text-decoration: underline;
  }

  &__link:hover {
    color: #b56f43;
  }

  &__toggle {
    font-size: 14px;
    font-family: Montserrat;
    font-weight: 300;
    cursor: pointer;
    width: max-content;
    margin-left: auto;
    margin-bottom: 15px;
    color: #d58c51;
    text-decoration: underline;
  }

  &__toggle:hover {
    color: #b56f43;
  }
}
</style>
