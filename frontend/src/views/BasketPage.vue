<template>
    <div class="main">
        <div class="main__header">
            <HeaderBasket />
        </div>
        <div class="main__goods">
            <MainBasket />
        </div>
        <hr class="separator">
        <div class="main__footer">
            <FooterBasket />
        </div>
    </div>
</template>

<script>
// import { ref } from 'vue'
import HeaderBasket from '@/components/blocks/HeaderBasket.vue'
import MainBasket from '@/components/blocks/MainBasket.vue'
import FooterBasket from '@/components/blocks/FooterBasket.vue'
export default {
  name: 'BasketPage',
  components: {
    HeaderBasket,
    MainBasket,
    FooterBasket
  },
  props: {
  },
  setup () {
  }
}
</script>

<style lang="scss" scoped>
.main__header {
    padding-top: 54px;
    padding-bottom: 81px;
}

.main__footer {
    width: 100%;
    // position: fixed;
    height: 20%;
    bottom: 0;
    left: 0;
}

.separator {
    margin-top: 100px;
    margin-bottom: 28px;
    border: 1px solid rgb(213, 140, 81);
}
</style>
