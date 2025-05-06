import { defineStore } from 'pinia';
import {
  fetchBasket,
  addToBasket,
  removeFromBasket,
  updateBasketItemQuantity,
} from '../services/basketService';
import { getErrorMessage } from '../utils/cookies';

export const useBasketStore = defineStore('basket', {
  state: () => ({
    basket: [], // Состояние корзины
  }),
  getters: {
    getBasketGoods: (state) => state.basket || [],

    // Получить общее количество товаров в корзине
    getCountProductsInBasket: (state) =>
      state.basket.reduce((total, item) => total + item.quantity, 0),

    // Получить общую стоимость товаров в корзине
    getAllPriceProductsInBasket: (state) =>
      state.basket.reduce(
        (total, item) => total + item.quantity * item.product_data.price,
        0
      ),
  },
  actions: {
    setBasket(data) {
      this.basket = data || [];
    },

    async fetchUserBasket() {
      try {
        const basketData = await fetchBasket();
        this.setBasket(basketData);
      } catch (error) {
        const message = getErrorMessage(error, 'Ошибка загрузки корзины!');
        console.error('Ошибка загрузки корзины:', message);
      }
    },

    async addGoodInBasket(productId, quantity = 1) {
      try {
        const basketItem = await addToBasket(productId, quantity);
    
        // Преобразуем значение price в число
        basketItem.product_data.price = parseFloat(basketItem.product_data.price);
    
        // Проверяем, есть ли уже этот товар в корзине
        const existingItem = this.basket.find((item) => item.product_data.id === productId);
    
        if (existingItem) {
          // Если товар уже в корзине, обновляем его количество
          existingItem.quantity += quantity;
        } else {
          // Если товара нет, добавляем его в корзину
          this.basket.push(basketItem);
        }
      } catch (error) {
        const message = getErrorMessage(error, 'Ошибка добавления в корзину!');
        console.error('Ошибка добавления в корзину:', message);
      }
    }, 

    async removeGoodFromBasket(basketItemId) {
      try {
        await removeFromBasket(basketItemId);
        this.basket = this.basket.filter((item) => item.id !== basketItemId);
      } catch (error) {
        const message = getErrorMessage(error, 'Ошибка удаления из корзины!');
        console.error('Ошибка удаления из корзины:', message);
      }
    },

    async updateBasketItemQuantity(basketItemId, quantity) {
      try {
        const updatedItem = await updateBasketItemQuantity(basketItemId, quantity);
        const itemIndex = this.basket.findIndex((item) => item.id === basketItemId);
        if (itemIndex !== -1) {
          this.basket[itemIndex] = updatedItem;
        }
      } catch (error) {
        const message = getErrorMessage(error, 'Ошибка обновления количества товара!');
        console.error('Ошибка обновления количества товара:', message);
      }
    },
  },
});
