<template>
  <div class="product-list">
    <div class="product-list__filters">
      <div class="product-list__search">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск по названию или описанию..."
          @input="updateSearch"
        >
      </div>
      <ProductFilters />
    </div>

    <div class="product-list__content">
      <div v-if="isLoading" class="product-list__loading">
        Загрузка продуктов...
      </div>

      <div v-else-if="error" class="product-list__error">
        {{ error }}
      </div>

      <div v-else-if="!filteredProducts.length" class="product-list__empty">
        <p>По вашему запросу ничего не найдено</p>
        <button @click="resetFilters" class="product-list__reset-btn">
          Сбросить фильтры
        </button>
      </div>

      <div v-else class="product-list__grid">
        <CardProduct
          v-for="product in filteredProducts"
          :key="product.id"
          :product-id="product.id"
          :title="product.title"
          :description="product.description"
          :price="product.price"
          :image-source="product.image"
          @click-main="handleAddToBasket(product.id)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, computed, ref } from 'vue'
import CardProduct from '../elements/CardProduct.vue'
import ProductFilters from './ProductFilters.vue'
import { useBasketStore } from '@/stores/basket'
import { useProductsStore } from '@/stores/products'
import { useToast } from 'vue-toastification'

export default {
  name: 'MainProductList',
  components: {
    CardProduct,
    ProductFilters
  },
  setup() {
    const basketStore = useBasketStore()
    const productsStore = useProductsStore()
    const toast = useToast()
    const searchQuery = ref('')

    onMounted(async () => {
      try {
        await productsStore.fetchAllProducts()
      } catch (error) {
        toast.error('Ошибка загрузки товаров!')
      }
    })

    const updateSearch = () => {
      productsStore.setFilter('searchQuery', searchQuery.value)
    }

    const resetFilters = () => {
      searchQuery.value = ''
      productsStore.resetFilters()
    }

    const handleAddToBasket = async (productId) => {
      try {
        await basketStore.addGoodInBasket(productId)
        toast.success('Товар добавлен в корзину!')
      } catch (error) {
        toast.error('Ошибка добавления товара в корзину!')
      }
    }

    return {
      filteredProducts: computed(() => productsStore.getFilteredProducts),
      isLoading: computed(() => productsStore.isLoading),
      error: computed(() => productsStore.error),
      searchQuery,
      handleAddToBasket,
      updateSearch,
      resetFilters,
      toast
    }
  }
}
</script>

<style lang="scss" scoped>
.product-list {
  display: flex;
  gap: 20px;
  padding: 20px;

  &__filters {
    width: 300px;
    flex-shrink: 0;
  }

  &__search {
    margin-bottom: 20px;

    input {
      width: 100%;
      padding: 12px;
      background: #1c1c1c;
      border: 1px solid #333;
      border-radius: 8px;
      color: #fff;
      font-size: 16px;

      &:focus {
        outline: none;
        border-color: #d58c51;
      }

      &::placeholder {
        color: #666;
      }
    }
  }

  &__content {
    flex-grow: 1;
  }

  &__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }

  &__loading,
  &__error,
  &__empty {
    text-align: center;
    padding: 40px;
    background: #1c1c1c;
    border-radius: 8px;
    color: #fff;
  }

  &__error {
    color: #e53e3e;
  }

  &__reset-btn {
    margin-top: 16px;
    padding: 8px 16px;
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
