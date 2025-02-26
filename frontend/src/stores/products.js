import { defineStore } from 'pinia';
import { fetchProducts, fetchProductById } from '../services/productsService';

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [], // Список всех продуктов
    productItem: null, // Текущий продукт
    isLoading: false,
    error: null,
    filters: {
      category: null,
      priceRange: { min: null, max: null },
      isVegetarian: null,
      isSpicy: null,
      searchQuery: '',
      sortBy: 'title',
      sortOrder: 'asc'
    }
  }),
  getters: {
    getProductList: (state) => state.products,
    getProductItem: (state) => state.productItem,
    getFilteredProducts: (state) => {
      let filtered = [...state.products];

      // Фильтрация по категории
      if (state.filters.category) {
        filtered = filtered.filter(product => 
          product.category.slug === state.filters.category
        );
      }

      // Фильтрация по цене
      if (state.filters.priceRange.min !== null) {
        filtered = filtered.filter(product => 
          product.price >= state.filters.priceRange.min
        );
      }
      if (state.filters.priceRange.max !== null) {
        filtered = filtered.filter(product => 
          product.price <= state.filters.priceRange.max
        );
      }

      // Фильтрация по вегетарианским блюдам
      if (state.filters.isVegetarian !== null) {
        filtered = filtered.filter(product => 
          product.is_vegetarian === state.filters.isVegetarian
        );
      }

      // Фильтрация по острым блюдам
      if (state.filters.isSpicy !== null) {
        filtered = filtered.filter(product => 
          product.is_spicy === state.filters.isSpicy
        );
      }

      // Поиск по названию и описанию
      if (state.filters.searchQuery) {
        const query = state.filters.searchQuery.toLowerCase();
        filtered = filtered.filter(product => 
          product.title.toLowerCase().includes(query) ||
          product.description.toLowerCase().includes(query)
        );
      }

      // Сортировка
      filtered.sort((a, b) => {
        const modifier = state.filters.sortOrder === 'asc' ? 1 : -1;
        if (state.filters.sortBy === 'price') {
          return (a.price - b.price) * modifier;
        }
        return a.title.localeCompare(b.title) * modifier;
      });

      return filtered;
    }
  },
  actions: {
    async fetchAllProducts() {
      this.isLoading = true;
      this.error = null;
      try {
        const products = await fetchProducts();
        this.products = products;
      } catch (error) {
        this.error = 'Ошибка при загрузке списка продуктов';
        console.error('Ошибка при загрузке списка продуктов:', error);
      } finally {
        this.isLoading = false;
      }
    },
    async fetchProductItem(productId) {
      this.isLoading = true;
      this.error = null;
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
        this.error = 'Ошибка при загрузке данных продукта';
        console.error('Ошибка при загрузке данных продукта:', error);
      } finally {
        this.isLoading = false;
      }
    },
    setProductItem(productId) {
      this.productItem = this.products.find((item) => item.id === parseInt(productId, 10)) || null;
    },
    setFilter(filterName, value) {
      this.filters[filterName] = value;
    },
    resetFilters() {
      this.filters = {
        category: null,
        priceRange: { min: null, max: null },
        isVegetarian: null,
        isSpicy: null,
        searchQuery: '',
        sortBy: 'title',
        sortOrder: 'asc'
      };
    }
  },
});
