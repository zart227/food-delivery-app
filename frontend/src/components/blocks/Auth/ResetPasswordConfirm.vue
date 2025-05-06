<template>
    <div class="reset-password-confirm">
      <h2 class="reset-password-confirm__title">Сброс пароля</h2>
      <form @submit.prevent="submitForm">
        <input
          type="password"
          v-model="newPassword"
          placeholder="Новый пароль"
          required
          autocomplete="new-password"
        />
        <input
          type="password"
          v-model="reNewPassword"
          placeholder="Повторите новый пароль"
          required
          autocomplete="new-password"
        />
        <button type="submit">Подтвердить</button>
      </form>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import api from '../../../api/axios';
  import { useToast } from 'vue-toastification';
  
  export default {
    name: 'ResetPasswordConfirm',
    props: {
      uid: {
        type: String,
        required: true,
      },
      token: {
        type: String,
        required: true,
      },
    },
    emits: ['switch'], // Добавляем switch в emits
    data() {
      return {
        newPassword: '',
        reNewPassword: '',
        successMessage: '',
        errorMessage: '',
      };
    },
    methods: {
      async submitForm() {
        const toast = useToast()

        try {
          await api.post('/auth/users/reset_password_confirm/', {
            uid: this.uid,
            token: this.token,
            new_password: this.newPassword,
            re_new_password: this.reNewPassword,
          });
          toast.success('Пароль успешно изменен!');
          this.successMessage = 'Пароль успешно изменен!';
          this.errorMessage = '';
          this.$emit('switch', 'login')

        } catch (error) {
          if (error.response && error.response.data && error.response.data.detail) {
            toast.error(error.response.data.detail);
            this.errorMessage = error.response.data.detail;
          } else if (error.response && error.response.data) {
            toast.error(JSON.stringify(error.response.data));
            this.errorMessage = JSON.stringify(error.response.data);
          } else if (error instanceof Error) {
            toast.error(error.message);
            this.errorMessage = error.message;
          } else if (typeof error === 'string') {
            toast.error(error);
            this.errorMessage = error;
          } else {
            toast.error('Произошла ошибка. Попробуйте позже.');
            this.errorMessage = 'Ошибка при сбросе пароля. Проверьте данные или попробуйте позже.';
          }
          this.successMessage = '';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Стили для компонента */
  .reset-password-confirm {
    /* Ваши стили */
  }
  .success-message {
    color: green;
  }
  .error-message {
    color: red;
  }
  </style>
  