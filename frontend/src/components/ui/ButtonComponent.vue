<template>
  <div class="main">
    <button :class="buttonClass">
      <!-- {{ buttonText }} -->
      <div v-if="iconShow"><i :class="fontIcon"></i></div>
      <div v-if="textShow">{{ buttonText }}</div>
    </button>
  </div>
</template>
<script>
// import { ref } from 'vue'

export default {
  name: 'ButtonComponent',
  components: {
  },
  props: {
    fontIcon: {
      type: String,
      default: ''
    },

    isBasketCard: {
      type: Boolean,
      default: false
    },

    isBasketMain: {
      type: Boolean,
      default: false
    },

    isMain: {
      type: Boolean,
      default: false
    },

    iconShow: {
      type: Boolean,
      default: false
    },

    textShow: {
      type: Boolean,
      default: false
    },

    isBasketFooter: {
      type: Boolean,
      default: false
    },

    buttonText: {
      type: String,
      default: ''
    },

    isRotated: {
      type: Boolean,
      default: false
    },
    isGoodFooter: {
      type: Boolean,
      default: false
    }
  },

  // data () {

  // },

  // определяет вычисляемое свойство buttonClass, которое возвращает объект с классами CSS
  // в зависимости от значений определенных свойств.
  computed: {
    buttonClass: function () {
      return {
        buttonMainCard: this.isMain,
        buttonBasketCard: this.isBasketCard,
        buttonBasketFooter: this.isBasketFooter,
        buttonBasketMain: this.isBasketMain,
        buttonRotate: this.isRotated,
        buttonGoodFooter: this.isGoodFooter
      }
    }
  }

  // methods: {

  // }
}
</script>

<style lang="scss" scoped>
.buttonMainCard {
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  background: none;
  border: 1px solid #FFFFFF;
  color: #FFFFFF;
  font-size: 25px;
}

.buttonBasketCard {
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  background: none;
  border: 1px solid #D58C51;
  color: #D58C51;
  font-size: 25px;
}
.buttonBasketMain {
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  flex-shrink: 0;
  // background: none;
  background-color: #D58C51;
  border: 1px solid #D58C51;
  color: #ffffff;
  font-size: 25px;
}
.buttonBasketFooter {
  width: 200px;
  height: 42px;
  color: rgb(213, 140, 81);
  background: none;
  border: 1px solid #D58C51;
  font-family: Montserrat;
  font-size: 14px;
  font-weight: 400;
  line-height: 17px;
  letter-spacing: 0%;
  text-align: center;
}

.buttonGoodFooter {
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
}

.buttonRotate {
  rotate: 45deg;
}

.buttonBasketCard:hover {
  background: #D58C51;
  color: rgb(19, 19, 19);
}

.buttonBasketMain:hover {
  background: #ffffff;
  color: #D58C51;
}

.buttonMainCard:hover {
  background: #D58C51;
  border: 1px solid #D58C51;
}

.buttonBasketFooter:hover {
  background: #D58C51;
  color: rgb(19, 19, 19);
}

.buttonGoodFooter:hover {
  background: none;
  color: rgb(213, 140, 81);
}
</style>
