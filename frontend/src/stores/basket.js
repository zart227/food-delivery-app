import { defineStore } from 'pinia'
import { useGoodsStore } from './goods'

export const useBasketStore = defineStore('basket', {
  state: () => ({
    goodsInBasket: JSON.parse(localStorage.getItem('basket')) || []
  }),
  getters: {
    getBasketGoods: (state) => state.goodsInBasket
  },
  actions: {
    addGoodInBasket(value) {
      const goodsStore = useGoodsStore()
      const good = goodsStore.getGoodById(value)
      if (good) {
        const itemBasket = {
          id: good.id,
          imageSource: good.imageSource,
          title: good.title,
          price: good.price
        }
        this.goodsInBasket.push(itemBasket)
        localStorage.setItem('basket', JSON.stringify(this.goodsInBasket))
      }
    },
    setStoreBasket() {
      this.goodsInBasket = JSON.parse(localStorage.getItem('basket')) || []
    },
    removeGoodFromBasket(index) {
      this.goodsInBasket.splice(index, 1)
      localStorage.setItem('basket', JSON.stringify(this.goodsInBasket))
    }
  }
})
