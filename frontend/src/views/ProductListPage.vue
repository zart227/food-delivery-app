<template>
  <div class="wrapper container">
    <div class="header__wrapper">
      <HeaderComponent
        is-main
        title="Наша продукция"
        show-cart-info
      />
    </div>
    <MainProductList />
  </div>
</template>

<script>
// import { ref } from 'vue'
import HeaderComponent from '@/components/blocks/HeaderComponent.vue'
import MainProductList from '@/components/blocks/MainProductList.vue'

export default {
  name: 'ProductListPage',
  components: {
    HeaderComponent,
    MainProductList
  },
  props: {
  },
  setup () {
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    height: calc(100vh);
}

// .product_list {
//     flex: 1;
//     overflow-y: auto;
//     padding: 10px;
// }
.header__wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
