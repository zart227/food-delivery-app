<template>
  <div class="profile-page">
    <HeaderComponent
      title="Личный кабинет"
      show-back-button
      back-route="/"
      is-basket-cart
    />
    
    <div class="profile-page__content">
      <!-- Навигация по разделам -->
      <div class="profile-page__nav">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['profile-page__tab', { active: currentTab === tab.id }]"
          @click="currentTab = tab.id"
        >
          {{ tab.name }}
        </button>
      </div>

      <!-- Контент текущего раздела -->
      <div class="profile-page__tab-content">
        <!-- Настройки профиля -->
        <div v-if="currentTab === 'settings'" class="profile-settings">
          <h3>Настройки профиля</h3>
          <form @submit.prevent="updateProfile" class="profile-settings__form">
            <InputField
              v-model="profile.username"
              label="Имя пользователя"
              :disabled="true"
            />
            <InputField
              v-model="profile.email"
              label="Email"
              type="email"
              :error="errors.email"
            />
            <InputField
              v-model="profile.firstName"
              label="Имя"
              :error="errors.firstName"
            />
            <InputField
              v-model="profile.lastName"
              label="Фамилия"
              :error="errors.lastName"
            />
            <button type="submit" class="profile-settings__submit">
              Сохранить изменения
            </button>
          </form>
        </div>

        <!-- История заказов -->
        <div v-if="currentTab === 'orders'" class="order-history">
          <h3>История заказов</h3>
          <div v-if="orders.length" class="order-history__list">
            <div v-for="order in orders" :key="order.id" class="order-card">
              <div class="order-card__header">
                <span class="order-card__number">Заказ #{{ order.id }}</span>
                <span :class="['order-card__status', order.status]">
                  {{ getStatusText(order.status) }}
                </span>
              </div>
              <div class="order-card__date">
                {{ formatDate(order.created_at) }}
              </div>
              <div class="order-card__items">
                <div v-for="item in order.items" :key="item.product.id || item.product_detail.id" class="order-card__item">
                  <img v-if="item.product_detail && item.product_detail.image" :src="item.product_detail.image" :alt="item.product_detail.title" style="width: 40px; height: 40px; object-fit: cover; margin-right: 10px; border-radius: 4px; display: inline-block; vertical-align: middle;" />
                  <span style="vertical-align: middle;">{{ item.product_detail ? item.product_detail.title : '' }} × {{ item.quantity }}</span>
                </div>
              </div>
              <div class="order-card__total">
                Итого: {{ order.total_price }} ₽
              </div>
            </div>
          </div>
          <div v-else class="order-history__empty">
            У вас пока нет заказов
          </div>
        </div>

        <!-- Текущие заказы -->
        <div v-if="currentTab === 'active'" class="active-orders">
          <h3>Текущие заказы</h3>
          <div v-if="activeOrders.length" class="active-orders__list">
            <div v-for="order in activeOrders" :key="order.id" class="order-card">
              <div class="order-card__header">
                <span class="order-card__number">Заказ #{{ order.id }}</span>
                <span :class="['order-card__status', order.status]">
                  {{ getStatusText(order.status) }}
                </span>
              </div>
              <div class="order-card__progress">
                <div 
                  :class="['progress-step', { completed: isStepCompleted(order.status, step) }]"
                  v-for="step in orderSteps" 
                  :key="step"
                >
                  {{ getStepText(step) }}
                </div>
              </div>
              <div class="order-card__items">
                <div v-for="item in order.items" :key="item.product.id || item.product_detail.id" class="order-card__item">
                  <img v-if="item.product_detail && item.product_detail.image" :src="item.product_detail.image" :alt="item.product_detail.title" style="width: 40px; height: 40px; object-fit: cover; margin-right: 10px; border-radius: 4px; display: inline-block; vertical-align: middle;" />
                  <span style="vertical-align: middle;">{{ item.product_detail ? item.product_detail.title : '' }} × {{ item.quantity }}</span>
                </div>
              </div>
              <div class="order-card__total">
                Итого: {{ order.total_price }} ₽
              </div>
            </div>
          </div>
          <div v-else class="active-orders__empty">
            У вас нет активных заказов
          </div>
        </div>

        <!-- Управление аккаунтом -->
        <div v-if="currentTab === 'account'" class="account-management">
          <h3>Управление аккаунтом</h3>
          
          <!-- Смена пароля -->
          <div class="account-section">
            <h4>Смена пароля</h4>
            <form @submit.prevent="changePassword" class="account-form">
              <InputField
                v-model="passwordForm.current_password"
                label="Текущий пароль"
                type="password"
                :error="errors.current_password"
              />
              <InputField
                v-model="passwordForm.new_password"
                label="Новый пароль"
                type="password"
                :error="errors.new_password"
              />
              <InputField
                v-model="passwordForm.re_new_password"
                label="Подтверждение нового пароля"
                type="password"
                :error="errors.re_new_password"
              />
              <button type="submit" class="account-button">
                Сменить пароль
              </button>
            </form>
          </div>

          <!-- Смена логина -->
          <div class="account-section">
            <h4>Смена логина</h4>
            <form @submit.prevent="changeUsername" class="account-form">
              <InputField
                v-model="usernameForm.current_password"
                label="Текущий пароль"
                type="password"
                :error="errors.username_current_password"
              />
              <InputField
                v-model="usernameForm.new_username"
                label="Новый логин"
                :error="errors.new_username"
              />
              <InputField
                v-model="usernameForm.re_new_username"
                label="Подтверждение нового логина"
                :error="errors.re_new_username"
              />
              <button type="submit" class="account-button">
                Сменить логин
              </button>
            </form>
          </div>

          <!-- Смена email -->
          <div class="account-section">
            <h4>Смена email</h4>
            <form @submit.prevent="requestEmailChange" class="account-form">
              <InputField
                v-model="emailForm.email"
                label="Новый email"
                type="email"
                :error="errors.email_change"
              />
              <button type="submit" class="account-button">
                Запросить смену email
              </button>
            </form>
          </div>

          <!-- Удаление аккаунта -->
          <div class="account-section account-section--danger">
            <h4>Удаление аккаунта</h4>
            <form @submit.prevent="deleteAccount" class="account-form">
              <InputField
                v-model="deleteForm.current_password"
                label="Введите пароль для подтверждения"
                type="password"
                :error="errors.delete_password"
              />
              <button type="submit" class="account-button account-button--danger">
                Удалить аккаунт
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import HeaderComponent from '../components/blocks/HeaderComponent.vue'
import InputField from '../components/ui/InputField.vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import api from '@/api/axios'
import { useRouter } from 'vue-router'

export default {
  name: 'ProfilePage',
  components: {
    HeaderComponent,
    InputField
  },
  setup() {
    const authStore = useAuthStore()
    const toast = useToast()
    const router = useRouter()
    const currentTab = ref('active')
    const orders = ref([])
    const profile = ref({
      username: '',
      email: '',
      firstName: '',
      lastName: ''
    })
    const errors = ref({
      email: '',
      firstName: '',
      lastName: '',
      current_password: '',
      new_password: '',
      re_new_password: '',
      username_current_password: '',
      new_username: '',
      re_new_username: '',
      email_change: '',
      delete_password: ''
    })

    const tabs = [
      { id: 'active', name: 'Текущие заказы' },
      { id: 'orders', name: 'История заказов' },
      { id: 'settings', name: 'Настройки профиля' },
      { id: 'account', name: 'Управление аккаунтом' }
    ]

    const orderSteps = ['pending', 'processing', 'shipping', 'delivered']

    const getStepText = (step) => {
      const texts = {
        pending: 'Ожидает обработки',
        processing: 'Готовится',
        shipping: 'В доставке',
        delivered: 'Доставлен'
      }
      return texts[step]
    }

    const getStatusText = (status) => {
      const texts = {
        pending: 'Ожидает обработки',
        processing: 'Готовится',
        shipping: 'В доставке',
        delivered: 'Доставлен',
        cancelled: 'Отменён'
      }
      return texts[status]
    }

    const isStepCompleted = (currentStatus, step) => {
      const stepOrder = {
        pending: 0,
        processing: 1,
        shipping: 2,
        delivered: 3
      }
      return stepOrder[currentStatus] >= stepOrder[step]
    }

    const activeOrders = computed(() => {
      return orders.value.filter(order => 
        ['pending', 'processing', 'shipping'].includes(order.status)
      )
    })

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }

    const loadProfile = async () => {
      try {
        const response = await api.get('/auth/users/me/')
        profile.value = {
          username: response.data.username,
          email: response.data.email,
          firstName: response.data.first_name || '',
          lastName: response.data.last_name || ''
        }
      } catch (error) {
        toast.error('Ошибка при загрузке профиля')
        console.error('Ошибка загрузки профиля:', error)
      }
    }

    const loadOrders = async () => {
      try {
        const response = await api.get('/orders/')
        orders.value = response.data
      } catch (error) {
        toast.error('Ошибка при загрузке заказов')
        console.error('Ошибка загрузки заказов:', error)
      }
    }

    const updateProfile = async () => {
      try {
        await api.patch('/auth/users/me/', {
          email: profile.value.email,
          first_name: profile.value.firstName,
          last_name: profile.value.lastName
        })
        toast.success('Профиль успешно обновлен')
      } catch (error) {
        toast.error('Ошибка при обновлении профиля')
        console.error('Ошибка обновления профиля:', error)
        if (error.response?.data) {
          errors.value = {
            email: error.response.data.email?.[0] || '',
            firstName: error.response.data.first_name?.[0] || '',
            lastName: error.response.data.last_name?.[0] || ''
          }
        }
      }
    }

    // Формы для управления аккаунтом
    const passwordForm = ref({
      current_password: '',
      new_password: '',
      re_new_password: ''
    })

    const usernameForm = ref({
      current_password: '',
      new_username: '',
      re_new_username: ''
    })

    const emailForm = ref({
      email: ''
    })

    const deleteForm = ref({
      current_password: ''
    })

    // Функция очистки ошибок
    const clearErrors = () => {
      Object.keys(errors.value).forEach(key => {
        errors.value[key] = ''
      })
    }

    // Смена пароля
    const changePassword = async () => {
      clearErrors()
      try {
        await api.post('/auth/users/set_password/', {
          new_password: passwordForm.value.new_password,
          re_new_password: passwordForm.value.re_new_password,
          current_password: passwordForm.value.current_password
        })
        toast.success('Пароль успешно изменен')
        passwordForm.value = {
          current_password: '',
          new_password: '',
          re_new_password: ''
        }
      } catch (error) {
        if (error.response?.data) {
          errors.value = {
            ...errors.value,
            current_password: error.response.data.current_password?.[0] || '',
            new_password: error.response.data.new_password?.[0] || '',
            re_new_password: error.response.data.re_new_password?.[0] || ''
          }
        }
        toast.error('Ошибка при смене пароля')
      }
    }

    // Смена логина
    const changeUsername = async () => {
      clearErrors()
      try {
        await api.post('/auth/users/set_username/', {
          current_password: usernameForm.value.current_password,
          new_username: usernameForm.value.new_username,
          re_new_username: usernameForm.value.re_new_username
        })
        toast.success('Логин успешно изменен')
        await authStore.logoutUser()
        router.push('/auth')
      } catch (error) {
        if (error.response?.data) {
          errors.value = {
            ...errors.value,
            username_current_password: error.response.data.current_password?.[0] || '',
            new_username: error.response.data.new_username?.[0] || '',
            re_new_username: error.response.data.re_new_username?.[0] || ''
          }
        }
        toast.error('Ошибка при смене логина')
      }
    }

    // Запрос на смену email
    const requestEmailChange = async () => {
      clearErrors()
      try {
        await api.post('/auth/users/reset_email/', {
          email: emailForm.value.email
        })
        toast.success('На указанный email отправлено письмо для подтверждения')
        emailForm.value.email = ''
      } catch (error) {
        if (error.response?.data) {
          errors.value = {
            ...errors.value,
            email_change: error.response.data.email?.[0] || ''
          }
        }
        toast.error('Ошибка при запросе смены email')
      }
    }

    // Удаление аккаунта
    const deleteAccount = async () => {
      clearErrors()
      if (!confirm('Вы уверены, что хотите удалить свой аккаунт? Это действие необратимо.')) {
        return
      }
      try {
        await api.delete('/auth/users/me/', {
          data: { current_password: deleteForm.value.current_password }
        })
        toast.success('Аккаунт успешно удален')
        await authStore.logoutUser()
        router.push('/auth')
      } catch (error) {
        if (error.response?.data) {
          errors.value = {
            ...errors.value,
            delete_password: error.response.data.current_password?.[0] || ''
          }
        }
        toast.error('Ошибка при удалении аккаунта')
      }
    }

    onMounted(async () => {
      await loadProfile()
      await loadOrders()
    })

    return {
      currentTab,
      tabs,
      orders,
      activeOrders,
      profile,
      errors,
      orderSteps,
      getStepText,
      getStatusText,
      isStepCompleted,
      formatDate,
      updateProfile,
      // Новые поля и методы
      passwordForm,
      usernameForm,
      emailForm,
      deleteForm,
      changePassword,
      changeUsername,
      requestEmailChange,
      deleteAccount
    }
  }
}
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
  background-color: #1c1c1c;
  color: #fff;

  &__content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  &__nav {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
  }

  &__tab {
    padding: 10px 20px;
    background: none;
    border: 2px solid #d58c51;
    color: #d58c51;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s ease;

    &:hover {
      background: #d58c51;
      color: #fff;
    }

    &.active {
      background: #d58c51;
      color: #fff;
    }
  }
}

.profile-settings {
  max-width: 600px;

  h3 {
    margin-bottom: 20px;
    font-size: 24px;
  }

  &__form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  &__submit {
    margin-top: 20px;
    padding: 10px 20px;
    background: #d58c51;
    border: none;
    color: #fff;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s ease;

    &:hover {
      background: #c47b40;
    }
  }
}

.order-card {
  background: #2c2c2c;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }

  &__number {
    font-size: 18px;
    font-weight: bold;
  }

  &__status {
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 14px;

    &.pending { background: #ffd700; color: #000; }
    &.processing { background: #ff9800; color: #fff; }
    &.shipping { background: #2196f3; color: #fff; }
    &.delivered { background: #4caf50; color: #fff; }
    &.cancelled { background: #f44336; color: #fff; }
  }

  &__date {
    color: #888;
    font-size: 14px;
    margin-bottom: 15px;
  }

  &__items {
    margin-bottom: 15px;
  }

  &__item {
    padding: 5px 0;
    border-bottom: 1px solid #3c3c3c;
  }

  &__total {
    font-weight: bold;
    color: #d58c51;
  }

  &__progress {
    display: flex;
    justify-content: space-between;
    margin: 20px 0;
    position: relative;

    &::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      height: 2px;
      background: #3c3c3c;
      z-index: 1;
    }
  }
}

.progress-step {
  position: relative;
  background: #2c2c2c;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  z-index: 2;

  &.completed {
    background: #d58c51;
    color: #fff;
  }
}

.order-history, .active-orders {
  h3 {
    margin-bottom: 20px;
    font-size: 24px;
  }

  &__empty {
    text-align: center;
    padding: 40px;
    color: #888;
  }
}

.account-management {
  max-width: 600px;

  h3 {
    margin-bottom: 30px;
    font-size: 24px;
  }

  h4 {
    margin-bottom: 20px;
    font-size: 20px;
    color: #d58c51;
  }
}

.account-section {
  background: #2c2c2c;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;

  &--danger {
    border: 1px solid #f44336;
  }
}

.account-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.account-button {
  margin-top: 10px;
  padding: 10px 20px;
  background: #d58c51;
  border: none;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s ease;

  &:hover {
    background: #c47b40;
  }

  &--danger {
    background: #f44336;

    &:hover {
      background: #d32f2f;
    }
  }
}
</style> 