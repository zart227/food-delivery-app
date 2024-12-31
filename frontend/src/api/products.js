import api from './axios';

export const fetchProducts = async () => {
  const response = await api.get('/products/');
  return response.data;
};

export const addToCart = async (productId) => {
  const response = await api.post('/cart/', { product_id: productId });
  return response.data;
};

export const fetchCart = async () => {
  const response = await api.get('/cart/');
  return response.data;
};

export const fetchOrders = async () => {
  const response = await api.get('/orders/');
  return response.data;
};
