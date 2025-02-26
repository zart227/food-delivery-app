class WebSocketService {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectTimeout = 3000;
    }

    connect() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            console.error('No access token found');
            return;
        }

        const wsUrl = `ws://${window.location.host}/ws/orders/`;
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.isConnected = true;
            this.reconnectAttempts = 0;
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.isConnected = false;
            this.reconnect();
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            setTimeout(() => this.connect(), this.reconnectTimeout);
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }

    // Подписка на обновления статуса заказа
    subscribeToOrderUpdates(callback) {
        if (this.ws) {
            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === 'order_status_update' || data.type === 'orders_statuses') {
                    callback(data);
                }
            };
        }
    }

    // Запрос статуса конкретного заказа
    requestOrderStatus(orderId) {
        if (this.ws && this.isConnected) {
            this.ws.send(JSON.stringify({
                type: 'get_order_status',
                order_id: orderId
            }));
        }
    }
}

export const websocketService = new WebSocketService(); 