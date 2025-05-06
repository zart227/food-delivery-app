import { defineStore } from 'pinia';
import { websocketService } from '@/services/websocketService';
import { createOrder } from '@/services/orderService';
import { useToast } from 'vue-toastification';

export const useOrdersStore = defineStore('orders', {
    state: () => ({
        orders: [],
        currentOrder: null,
        isLoading: false,
        error: null,
        wsConnected: false
    }),

    getters: {
        getOrderById: (state) => (id) => {
            return state.orders.find(order => order.id === id);
        },
        getOrderStatus: (state) => (id) => {
            const order = state.orders.find(order => order.id === id);
            return order ? order.status : null;
        }
    },

    actions: {
        // Инициализация WebSocket соединения
        initWebSocket() {
            websocketService.connect();
            websocketService.subscribeToOrderUpdates(this.handleOrderUpdate);
            this.wsConnected = true;
        },

        // Обработка обновлений от WebSocket
        handleOrderUpdate(data) {
            const toast = useToast();
            
            if (data.type === 'orders_statuses') {
                this.orders = data.statuses;
            } else if (data.type === 'order_status_update') {
                const orderIndex = this.orders.findIndex(o => o.id === data.order_id);
                if (orderIndex !== -1) {
                    this.orders[orderIndex].status = data.status;
                    toast.info(`Статус заказа #${data.order_id} обновлен: ${data.status}`);
                }
            }
        },

        // Создание нового заказа
        async createNewOrder(orderData) {
            this.isLoading = true;
            this.error = null;
            const toast = useToast();

            try {
                const response = await createOrder(orderData);
                this.currentOrder = response;
                
                // Запрашиваем статус созданного заказа через WebSocket
                if (this.wsConnected) {
                    websocketService.requestOrderStatus(response.id);
                }

                toast.success('Заказ успешно создан!');
                return response;
            } catch (error) {
                this.error = error.message;
                toast.error('Ошибка при создании заказа');
                throw error;
            } finally {
                this.isLoading = false;
            }
        },

        // Очистка данных при выходе
        clearOrdersData() {
            this.orders = [];
            this.currentOrder = null;
            this.error = null;
            if (this.wsConnected) {
                websocketService.disconnect();
                this.wsConnected = false;
            }
        }
    }
}); 