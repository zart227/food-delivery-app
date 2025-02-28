# ER-диаграмма Food Delivery Service

```mermaid
erDiagram
    User ||--o{ UserRole : has
    User ||--o{ Order : places
    User ||--o{ Basket : has
    Role ||--o{ UserRole : has
    
    Category ||--o{ Product : contains
    Category ||--o{ Category : has_parent
    
    Product ||--o{ OrderItem : included_in
    Product ||--o{ Basket : added_to
    
    Order ||--o{ OrderItem : contains

    User {
        int id PK
        string username
        string email UK
        string password
        boolean is_verified
        string phone
        text address
        string avatar
        json notification_preferences
    }

    Role {
        int id PK
        string name UK
        text description
    }

    UserRole {
        int id PK
        int user_id FK
        int role_id FK
        datetime assigned_at
    }

    Category {
        int id PK
        string name
        string slug UK
        text description
        string image
        int parent_id FK
        datetime created_at
        datetime updated_at
    }

    Product {
        int id PK
        string title
        text description
        decimal price
        string image
        int category_id FK
        boolean is_available
        datetime created_at
        datetime updated_at
        decimal weight
        int calories
        boolean is_vegetarian
        boolean is_spicy
    }

    Order {
        int id PK
        int user_id FK
        datetime created_at
        string status
        decimal total_price
        string address
        string phone
        text notes
    }

    OrderItem {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price
    }

    Basket {
        int id PK
        int user_id FK
        int product_id FK
        int quantity
    }
```

## Описание основных сущностей

### Пользователи и роли
- `User`: Расширенная модель пользователя с дополнительными полями для доставки
- `Role`: Роли пользователей в системе
- `UserRole`: Связующая таблица для реализации many-to-many связи

### Каталог товаров
- `Category`: Иерархическая структура категорий с возможностью вложенности
- `Product`: Детальная информация о продуктах с дополнительными атрибутами

### Заказы и корзина
- `Order`: Основная информация о заказе
- `OrderItem`: Позиции заказа с количеством и ценой
- `Basket`: Временное хранение выбранных товаров

## Основные связи

1. Пользователь может:
   - Иметь несколько ролей
   - Создавать множество заказов
   - Иметь одну корзину с несколькими товарами

2. Категории:
   - Могут иметь подкатегории (self-referential)
   - Содержат множество продуктов

3. Продукты:
   - Принадлежат к одной категории
   - Могут быть в нескольких заказах
   - Могут быть в нескольких корзинах

4. Заказы:
   - Принадлежат одному пользователю
   - Содержат несколько позиций (OrderItem) 