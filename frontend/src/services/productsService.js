import api from '../api/axios';

export async function fetchProducts() {
  try {
    const response = await api.get('/products/');
    return response.data.map((product) => ({
      ...product,
      price: parseFloat(product.price), // Преобразуем цену в число
      // image: new URL(product.image, api.defaults.baseURL).href, // Создаем полный URL для картинки
    }));
  } catch (error) {
    console.error('Ошибка при получении продуктов:', error);
    throw error;
  }
}

export async function fetchProductById(productId) {
  try {
    const response = await api.get(`/products/${productId}/`);
    return {
      ...response.data,
      price: parseFloat(response.data.price), // Преобразуем цену в число
      // image: new URL(response.data.image, api.defaults.baseURL).href, // Создаем полный URL для картинки
    };
  } catch (error) {
    console.error('Ошибка при получении данных продукта:', error);
    throw error;
  }
}
