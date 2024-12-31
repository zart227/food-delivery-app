import { defineStore } from 'pinia';
import { fetchProducts, fetchProductById } from '../services/productsService';

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [], // Список всех продуктов
    productItem: null, // Текущий продукт
  }),
  getters: {
    getProductList: (state) => state.products,
    getProductItem: (state) => state.productItem,
  },
  actions: {
    async fetchAllProducts() {
      try {
        const products = await fetchProducts();
        this.products = products;
      } catch (error) {
        console.error('Ошибка при загрузке списка продуктов:', error);
        throw error;
      }
    },
    async fetchProductItem(productId) {
      try {
        const product = this.products.find((item) => item.id === parseInt(productId, 10));
        if (product) {
          this.productItem = product;
        } else {
          console.warn('Продукт с указанным ID не найден в загруженных данных. Загружаем из API.');
          const productFromApi = await fetchProductById(productId);
          this.productItem = productFromApi;
        }
      } catch (error) {
        console.error('Ошибка при загрузке данных продукта:', error);
        throw error;
      }
    },
    setProductItem(productId) {
      this.productItem = this.products.find((item) => item.id === parseInt(productId, 10)) || null;
    },
  },
});
