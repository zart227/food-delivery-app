<template>
    <form class="auth-form" @submit.prevent="handleSubmit">
      <InputField
        v-model="email"
        label="Email"
        placeholder="Введите ваш email"
        :error="emailError"
        autocomplete="email"
      />
      <button class="auth-form__submit">Восстановить пароль</button>
      <span class="auth-form__link" @click="$emit('switch', 'login')">
        Назад ко входу
      </span>
    </form>
  </template>
  
  <script>
  import InputField from '../../ui/InputField.vue';
  import api from '../../../api/axios';
  import { useToast } from 'vue-toastification';
  
  export default {
    name: 'ForgotPasswordForm',
    components: { InputField },
    emits: ['switch'], // Добавляем switch в emits
    data() {
      return {
        email: '',
        emailError: '',
      };
    },
    methods: {
      async handleSubmit() {
        const toast = useToast();

        this.emailError = '';
        try {
          await api.post('/auth/users/reset_password/', { email: this.email });
          toast.success('Инструкция по восстановлению отправлена на вашу почту.');
        } catch (error) {
          if (error.response && error.response.data && error.response.data.detail) {
            this.emailError = error.response.data.detail;
            toast.error(this.emailError);
          } else if (error.response && error.response.data) {
            this.emailError = JSON.stringify(error.response.data);
            toast.error(this.emailError);
          } else if (error instanceof Error) {
            this.emailError = error.message;
            toast.error(this.emailError);
          } else if (typeof error === 'string') {
            this.emailError = error;
            toast.error(this.emailError);
          } else {
            this.emailError = 'Ошибка восстановления пароля';
            toast.error('Произошла ошибка. Попробуйте позже.');
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .auth-form {
    display: flex;
    flex-direction: column;
  }
  
  .auth-form__submit {
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
  
  .auth-form__submit:hover {
    background-color: #b56f43;
  }
  
  .auth-form__link {
    margin-top: 15px;
    font-size: 14px;
    color: #d58c51;
    cursor: pointer;
    text-decoration: underline;
  }
  
  .auth-form__link:hover {
    color: #b56f43;
  }
  </style>
  