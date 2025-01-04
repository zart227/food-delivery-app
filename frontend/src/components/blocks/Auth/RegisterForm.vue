<template>
  <form class="register-form" @submit.prevent="handleRegister">
    <!-- <span class="register-form__toggle" @click="$emit('switch', 'register')"
      >Авторизоваться</span
    > -->
    <h2 class="register-form__title">Регистрация</h2>
    <InputField
      v-model="form.username"
      label="Имя пользователя"
      :error="errors.username"
    />
    <InputField
      v-model="form.email"
      label="Электронная почта"
      type="email"
      :error="errors.email"
    />
    <InputField
      v-model="form.password"
      label="Пароль"
      type="password"
      :error="errors.password"
    />
    <InputField
      v-model="form.confirmPassword"
      label="Подтвердите пароль"
      type="password"
      :error="errors.confirmPassword"
    />
    <CheckboxField
      v-model="form.subscribe"
      label="Я согласен получать обновления на почту"
    />
    <button type="submit" class="register-form__submit">
      Зарегистрироваться
    </button>
    <span class="register-form__switch" @click="$emit('switch', 'login')">
      Уже есть аккаунт? Войти
    </span>
  </form>
</template>

<script>
import InputField from '../../ui/InputField.vue'
import CheckboxField from '../../ui/CheckboxField.vue'
import api from '../../../api/axios'
import { useToast } from 'vue-toastification'

export default {
  name: 'RegisterForm',
  components: { InputField, CheckboxField },
  props: {
    initialForm: {
      type: Object,
      default: () => ({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        subscribe: false,
      }),
    },
  },
  emits: ['switch', 'success'],
  setup() {
    const toast = useToast()
    return {
      toast,
    }
  },
  data() {
    return {
      form: { ...this.initialForm },
      errors: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
      },
    }
  },
  methods: {
    async handleRegister() {
      this.clearErrors()

      if (!this.validateForm()) {
        return
      }

      try {
        await api.post('/auth/users/', {
          username: this.form.username,
          email: this.form.email,
          password: this.form.password,
          re_password: this.form.confirmPassword,
        })

        this.toast.success('Регистрация успешна! Проверьте почту для подтверждения аккаунта.')
        this.$emit(
          'success',
          'Регистрация успешна! Проверьте почту для подтверждения аккаунта.',
        )
      } catch (error) {
        if (error.response && error.response.data) {
          this.processBackendErrors(error.response.data)
        } else {
          this.toast.error('Произошла ошибка при регистрации.')
          console.error('Ошибка регистрации:', error)
        }
      }
    },
    validateForm() {
      let isValid = true

      if (this.form.username.length < 4) {
        this.toast.error('Имя пользователя должно содержать не менее 4 символов.')
        this.errors.username =
          'Имя пользователя должно содержать не менее 4 символов.'
        isValid = false
      }

      if (!this.form.email.includes('@')) {
        this.toast.error('Введите корректный адрес электронной почты.')
        this.errors.email = 'Введите корректный адрес электронной почты.'
        isValid = false
      }

      if (this.form.password.length < 8) {
        this.toast.error('Пароль должен содержать не менее 8 символов.')
        this.errors.password = 'Пароль должен содержать не менее 8 символов.'
        isValid = false
      }

      if (this.form.password !== this.form.confirmPassword) {
        this.toast.error('Пароли не совпадают.')
        this.errors.confirmPassword = 'Пароли не совпадают.'
        isValid = false
      }

      return isValid
    },
    clearErrors() {
      this.errors = {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
      }
    },
    processBackendErrors(errors) {
      for (const key in errors) {
        if (key === 'email') {
          this.toast.error('Пользователь с такой электронной почтой уже существует.')
          this.errors.email =
            'Пользователь с такой электронной почтой уже существует.'
        } else if (key === 'username') {
          this.toast.error('Пользователь с таким именем уже существует.')
          this.errors.username = 'Пользователь с таким именем уже существует.'
        } else if (this.errors[key] !== undefined) {
          this.toast.error(errors[key].join('; '))
          this.errors[key] = errors[key].join('; ')
        }
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.register-form {
  display: flex;
  flex-direction: column;

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

    &:hover {
      background-color: #b56f43;
    }
  }

  &__switch {
    margin-top: 15px;
    font-size: 14px;
    color: #d58c51;
    cursor: pointer;
    text-decoration: underline;

    &:hover {
      color: #b56f43;
    }
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
