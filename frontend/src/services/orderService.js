import api from '@/api/axios'

export const createOrder = async (orderData) => {
  try {
    const response = await api.post('/orders/create/', orderData)
    return response.data
  } catch (error) {
    console.error('Ошибка при создании заказа:', error)
    throw error
  }
}
