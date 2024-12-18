<template>
  <div class="main">
    <div class="main__header">
      <HeaderProductList />
    </div>
    <MainProductList />
  </div>
</template>

<script>
// import { ref } from 'vue'
import HeaderProductList from '@/components/blocks/HeaderProductList.vue'
import MainProductList from '@/components/blocks/MainProductList.vue'

export default {
  name: 'MainPage',
  components: {
    HeaderProductList,
    MainProductList
  },
  props: {
  },
  setup () {
  }
}
</script>

<style lang="scss" scoped>
.main {
  background: #161516;
  padding-bottom: 45px;
}

.main__header {
  z-index: 1;
  background-color: #161516;
  position: fixed;
  width: 100%;
  padding-top: 54px;
  padding-bottom: 50px;
}
</style>
