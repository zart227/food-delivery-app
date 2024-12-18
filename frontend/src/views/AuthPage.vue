<template>
  <main class="main">
    <!-- <div class="auth-form">
      <h2 class="auth-form__title">{{ mode === 'login' ? 'Авторизация' : 'Регистрация' }}</h2> -->
      <form class="auth-form" @submit.prevent="handleSubmit">
        <span class="auth-form__toggle" @click="toggleMode">{{ mode === 'login' ? 'Зарегистрироваться' : 'Авторизоваться' }}</span>
        <h2 class="auth-form__title">{{ mode === 'login' ? 'Вход' : 'Регистрация' }}</h2>
        <div class="auth-form__body">
          <div class="auth-form__field">
            <!-- <label for="username" class="auth-form__label">Логин:</label> -->
            <input id="username" v-model="username" type="text" placeholder="Логин" class="auth-form__input">
            <span v-if="usernameError" class="auth-form__error">{{ usernameError }}</span>
          </div>
          <div class="auth-form__field">
            <!-- <label for="password" class="auth-form__label">Пароль:</label> -->
            <input id="password" v-model="password" type="password" placeholder="Пароль" class="auth-form__input">
            <span v-if="passwordError" class="auth-form__error">{{ passwordError }}</span>
          </div>
         <div class="auth-form__subscribe">
            <label v-if="mode === 'register'" class="auth-form__subscribe-label">Я согласен получать обновления на почту
              <input id="subscribe" v-model="subscribe" class="auth-form__checkbox" type="checkbox">
              <span class="auth-form__checkmark"></span>
            </label>
          </div>
          <button type="submit" class="auth-form__submit">{{ mode === 'login' ? 'Войти' : 'Зарегистрироваться' }}</button>
        </div>
      </form>
    <!-- </div> -->
  </main>
</template>

<script>
export default {
  name: 'AuthPage',
  data () {
    return {
      mode: 'login',
      username: '',
      password: '',
      subscribe: false,
      isValidUsername: true,
      isValidPassword: true,
      usernameError: '',
      passwordError: ''
    }
  },
  methods: {
    handleSubmit () {
      this.usernameError = ''
      this.passwordError = ''

      this.isValidUsername = this.username.length >= 4
      this.isValidPassword = this.password.length >= 4

      if (!this.isValidUsername) {
        this.usernameError = 'Логин должен содержать не менее 4 символов'
      }

      if (!this.isValidPassword) {
        this.passwordError = 'Пароль должен содержать не менее 4 символов'
      }

      if (this.username.trim() === '') {
        this.usernameError = 'Поле не должно быть пустым'
      }

      if (this.password.trim() === '') {
        this.passwordError = 'Поле не должно быть пустым'
      }

      if (this.isValidUsername && this.isValidPassword && this.username.trim() !== '' && this.password.trim() !== '') {
        try {
          if (this.mode === 'login') {
            // Код авторизации
            const users = JSON.parse(localStorage.getItem('users')) || []
            const user = users.find(u => u.username === this.username && u.password === this.password)
            if (user) {
              localStorage.setItem('currentUser', JSON.stringify(user))
              localStorage.setItem('isAuthenticated', true)
              this.$router.push('/')
            } else {
              alert('Неправильный логин или пароль')
            }
          } else {
            // Код регистрации
            const users = JSON.parse(localStorage.getItem('users')) || []
            if (users.some(u => u.username === this.username)) {
              alert('Пользователь с таким логином уже существует')
            } else {
              users.push({ username: this.username, password: this.password, subscribe: this.subscribe })
              localStorage.setItem('users', JSON.stringify(users))
              alert('Регистрация успешна. Теперь вы можете авторизоваться.')
              this.mode = 'login'
            }
          }
        } catch (error) {
          alert(error.message)
        }
      }
    },
    toggleMode () {
      this.mode = this.mode === 'login' ? 'register' : 'login'
      this.usernameError = ''
      this.passwordError = ''
    }
  }
}
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
.auth-form {
  width: 460px;
  display: flex;
  flex-direction: column;
  position: relative;
  background-color: #fff;
  padding: 9px 20px 20px 20px;
  box-sizing:border-box;

  &__title {
    font-size: 31px;
    font-family: Montserrat;
    font-weight: 700;
    margin: auto;
    margin-bottom: 36px;
  }

  &__body {
    display: flex;
    flex-direction: column;
    align-items: center;
    // margin-bottom: 40px;
  }

  &__field {
    width: 100%;
    // margin-bottom: 10px;
    position: relative;
  }

  &__input {
    border: 1px solid #D58C51;
    border-radius: 60px;
    font-size: 16px;
    // position: relative;
    color: #161516;
    font-family: Montserrat;
    font-weight: 400;
    line-height: 20px;
    margin-bottom: 15px;
    width: 100%;
    height: 39px;
    box-sizing:border-box;
    padding-left: 20px;
  }

  &__subscribe{
    display: flex;
    align-items: center;
    position: absolute;
    // margin-bottom: 28px;
    position: absolute;
    top: 210px;
    left: 20px;
  }

  &__subscribe-label {
    font-size: 11px;
    color: #301411;
    font-family: Montserrat;
    font-weight: 300;

    display: block;
    position: relative;
    padding-left: 30px;
    margin-bottom: 12px;
    cursor: pointer;
    // font-size: 22px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  &__checkbox {
    // box-sizing: border-box;
    //border: 1px solid rgb(213, 140, 81);
    // border-radius: 50%;
    // style
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }

  &__checkmark {
    position: absolute;
    top: -3px;
    left: 0;
    height: 18px;
    width: 18px;
    // background-color: #eee;
    border: 1px solid rgb(213, 140, 81);
    border-radius: 50%;
  }

  /* On mouse-over, add a grey background color */
  &__subscribe-label:hover input ~ &__checkmark {
    background-color: #ccc;
  }

  /* When the checkbox is checked, add a blue background */
  &__subscribe-label input:checked ~ &__checkmark {
    background-color: #2196F3;
  }

  /* Create the checkmark/indicator (hidden when not checked) */
  &__checkmark:after {
    content: "";
    position: absolute;
    display: none;
  }

  /* Show the checkmark when checked */
  &__subscribe-label input:checked ~ &__checkmark:after {
    display: block;
  }

  /* Style the checkmark/indicator */
  &__subscribe-label &__checkmark:after {
    left: 5px;
    top: 1px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 3px 3px 0;
    -webkit-transform: rotate(45deg);
    -ms-transform: rotate(45deg);
    transform: rotate(45deg);
  }

  &__error {
    color: rgb(255, 11, 11);
    font-family: Montserrat;
    font-weight: 300;
    position: absolute;
    font-size: 8px;
    top: 42px;
    left: 20px;
  }

  &__submit {
    width: 200px;
    height: 42px;
    // color: rgb(213, 140, 81);
    background: none;
    border: 1px solid #D58C51;
    background: #D58C51;
    font-family: Montserrat;
    font-size: 14px;
    font-weight: 400;
    line-height: 17px;
    letter-spacing: 0%;
    text-align: center;
    cursor: pointer;
    margin-top: 46px;
    margin-bottom: 14px;
  }

  &__toggle {
    font-size: 11px;
    font-family: Montserrat;
    font-weight: 300;
    cursor: pointer;
    width: max-content;
    margin-left: auto;
    margin-bottom: 15px;
    color: #D58C51;
  }
}
</style>
