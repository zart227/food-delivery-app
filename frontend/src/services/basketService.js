import api from '../api/axios'; // Настроенный axios с базовым URL

export const fetchBasket = async () => {
  try {
    const response = await api.get('/basket/');
    return response.data.map((item) => ({
      ...item,
      product_data: {
        ...item.product_data,
        price: parseFloat(item.product_data.price), // Преобразуем цену в число
      },
    }));
  } catch (error) {
    console.error('Ошибка загрузки корзины:', error);
    throw error;
  }
};


export const addToBasket = async (productId, quantity = 1) => {
  try {
    const response = await api.post('/basket/', { product: productId, quantity });
    //const item = response.data;
    return response.data;
  } catch (error) {
    console.error('Ошибка добавления в корзину:', error);
    throw error;
  }
};

export const removeFromBasket = async (basketItemId) => {
  try {
    await api.delete(`/basket/${basketItemId}/`);
  } catch (error) {
    console.error('Ошибка удаления из корзины:', error);
    throw error;
  }
};

export const updateBasketItemQuantity = async (basketItemId, quantity) => {
  try {
    const response = await api.patch(`/basket/${basketItemId}/`, { quantity });
    const item = response.data;

    return {
      ...item,
      product_data: {
        ...item.product_data,
        price: parseFloat(item.product_data.price), // Преобразуем цену в число
      },
    };
  } catch (error) {
    console.error('Ошибка обновления количества товара:', error);
    throw error;
  }
};


export const clearBasket = async () => {
  try {
    await api.delete('/basket/');
  } catch (error) {
    console.error('Ошибка очистки корзины:', error);
    throw error;
  }
};
