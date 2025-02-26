import { defineStore } from 'pinia';
import api from '@/api/axios';

export const useCategoriesStore = defineStore('categories', {
  state: () => ({
    categories: [],
    isLoading: false,
    error: null
  }),

  getters: {
    getAllCategories: (state) => state.categories,
    getCategoryBySlug: (state) => (slug) => state.categories.find(cat => cat.slug === slug)
  },

  actions: {
    async fetchCategories() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.get('/categories/');
        this.categories = response.data;
      } catch (error) {
        this.error = 'Ошибка при загрузке категорий';
        console.error('Ошибка при загрузке категорий:', error);
      } finally {
        this.isLoading = false;
      }
    }
  }
}); 