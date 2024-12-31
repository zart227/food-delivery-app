<template>
  <main class="main">
    <div class="auth-page">
      <!-- <h2 class="auth-page__title">{{ getTitle }}</h2> -->
      <component
        :is="currentComponent"
        @switch="handleSwitch"
        @success="handleSuccess"
        :uid="uid"
        :token="token"
      />
    </div>
  </main>
</template>

<script>
import LoginForm from '../components/blocks/Auth/LoginForm.vue';
import RegisterForm from '../components/blocks/Auth/RegisterForm.vue';
import ForgotPasswordForm from '../components/blocks/Auth/ForgotPasswordForm.vue';
import ActivationPending from '../components/blocks/Auth/ActivationPending.vue';
import ActivateAccount from '../components/blocks/Auth/ActivateAccount.vue';

export default {
  name: 'AuthPage',
  props: {
    mode: {
      type: String,
      default: 'login',
    },
    uid: {
      type: String,
      default: null,
    },
    token: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      currentMode: this.mode, // Устанавливаем начальный режим из props
    };
  },
  computed: {
    currentComponent() {
      switch (this.currentMode) {
        case 'register':
          return RegisterForm;
        case 'forgotPassword':
          return ForgotPasswordForm;
        case 'activationPending':
          return ActivationPending;
        case 'activateAccount':
          return ActivateAccount;
        default:
          return LoginForm;
      }
    },
    getTitle() {
      return {
        login: 'Вход',
        register: 'Регистрация',
        forgotPassword: 'Восстановление пароля',
        activationPending: 'Активация аккаунта',
        activateAccount: 'Подтверждение аккаунта',
      }[this.currentMode];
    },
  },
  watch: {
    // Обновляем currentMode при изменении props.mode
    mode(newMode) {
      this.currentMode = newMode;
    },
  },
  methods: {
    handleSwitch(mode) {
      this.currentMode = mode;
    },
    handleSuccess() {
      this.currentMode = 'login';
    },
  },
};
</script>

<style lang="scss" scoped>
.main {
  height: 100vh;
  background-image: url(../assets/img/bgAuth.png);
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-page {
  width: 460px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

  &__title {
    font-size: 31px;
    font-family: Montserrat;
    font-weight: 700;
    margin: auto;
    margin-bottom: 36px;
    text-align: center;
  }
}
</style>
