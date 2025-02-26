<template>
  <div class="filters">
    <div class="filters__section">
      <h3>Категории</h3>
      <div class="filters__categories">
        <button
          v-for="category in categories"
          :key="category.id"
          :class="['filters__category-btn', { active: selectedCategory === category.slug }]"
          @click="selectCategory(category.slug)"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <div class="filters__section">
      <h3>Цена</h3>
      <div class="filters__price">
        <input
          type="number"
          v-model="priceMin"
          placeholder="От"
          @input="updatePriceFilter"
        >
        <span>—</span>
        <input
          type="number"
          v-model="priceMax"
          placeholder="До"
          @input="updatePriceFilter"
        >
      </div>
    </div>

    <div class="filters__section">
      <h3>Особенности</h3>
      <div class="filters__features">
        <label class="filters__checkbox">
          <input
            type="checkbox"
            v-model="isVegetarian"
            @change="updateFeatureFilter"
          >
          Вегетарианское
        </label>
        <label class="filters__checkbox">
          <input
            type="checkbox"
            v-model="isSpicy"
            @change="updateFeatureFilter"
          >
          Острое
        </label>
      </div>
    </div>

    <div class="filters__section">
      <h3>Сортировка</h3>
      <select v-model="sortBy" @change="updateSort">
        <option value="title">По названию</option>
        <option value="price">По цене</option>
      </select>
      <select v-model="sortOrder" @change="updateSort">
        <option value="asc">По возрастанию</option>
        <option value="desc">По убыванию</option>
      </select>
    </div>

    <button class="filters__reset" @click="resetAllFilters">
      Сбросить фильтры
    </button>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useProductsStore } from '@/stores/products';
import { useCategoriesStore } from '@/stores/categories';

export default {
  name: 'ProductFilters',
  setup() {
    const productsStore = useProductsStore();
    const categoriesStore = useCategoriesStore();

    const selectedCategory = ref(null);
    const priceMin = ref('');
    const priceMax = ref('');
    const isVegetarian = ref(false);
    const isSpicy = ref(false);
    const sortBy = ref('title');
    const sortOrder = ref('asc');

    onMounted(async () => {
      await categoriesStore.fetchCategories();
    });

    const selectCategory = (slug) => {
      selectedCategory.value = selectedCategory.value === slug ? null : slug;
      productsStore.setFilter('category', selectedCategory.value);
    };

    const updatePriceFilter = () => {
      productsStore.setFilter('priceRange', {
        min: priceMin.value ? Number(priceMin.value) : null,
        max: priceMax.value ? Number(priceMax.value) : null
      });
    };

    const updateFeatureFilter = () => {
      productsStore.setFilter('isVegetarian', isVegetarian.value);
      productsStore.setFilter('isSpicy', isSpicy.value);
    };

    const updateSort = () => {
      productsStore.setFilter('sortBy', sortBy.value);
      productsStore.setFilter('sortOrder', sortOrder.value);
    };

    const resetAllFilters = () => {
      selectedCategory.value = null;
      priceMin.value = '';
      priceMax.value = '';
      isVegetarian.value = false;
      isSpicy.value = false;
      sortBy.value = 'title';
      sortOrder.value = 'asc';
      productsStore.resetFilters();
    };

    return {
      categories: computed(() => categoriesStore.getAllCategories),
      selectedCategory,
      priceMin,
      priceMax,
      isVegetarian,
      isSpicy,
      sortBy,
      sortOrder,
      selectCategory,
      updatePriceFilter,
      updateFeatureFilter,
      updateSort,
      resetAllFilters
    };
  }
};
</script>

<style lang="scss" scoped>
.filters {
  background: #1c1c1c;
  padding: 20px;
  border-radius: 8px;
  color: #fff;

  &__section {
    margin-bottom: 20px;

    h3 {
      color: #d58c51;
      margin-bottom: 10px;
      font-size: 16px;
    }
  }

  &__categories {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  &__category-btn {
    background: #333;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    color: #fff;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background: #444;
    }

    &.active {
      background: #d58c51;
    }
  }

  &__price {
    display: flex;
    align-items: center;
    gap: 8px;

    input {
      width: 100px;
      padding: 8px;
      background: #333;
      border: 1px solid #444;
      border-radius: 4px;
      color: #fff;

      &:focus {
        outline: none;
        border-color: #d58c51;
      }
    }
  }

  &__features {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  &__checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;

    input {
      cursor: pointer;
    }
  }

  select {
    width: 100%;
    padding: 8px;
    background: #333;
    border: 1px solid #444;
    border-radius: 4px;
    color: #fff;
    margin-bottom: 8px;
    cursor: pointer;

    &:focus {
      outline: none;
      border-color: #d58c51;
    }
  }

  &__reset {
    width: 100%;
    padding: 10px;
    background: #d58c51;
    border: none;
    border-radius: 4px;
    color: #fff;
    cursor: pointer;
    transition: background 0.3s ease;

    &:hover {
      background: #c47b40;
    }
  }
}
</style> 