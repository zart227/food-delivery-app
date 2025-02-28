<template>
  <div class="reset-email">
    <h2 class="reset-email__title">Смена Email</h2>
    <form @submit.prevent="handleSubmit" class="reset-email__form">
      <InputField
        v-model="form.new_email"
        label="Новый Email"
        type="email"
        :error="errors.new_email"
      />
      <InputField
        v-model="form.re_new_email"
        label="Подтверждение нового Email"
        type="email"
        :error="errors.re_new_email"
      />
      <button type="submit" class="reset-email__submit">
        Подтвердить смену Email
      </button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import InputField from '../../ui/InputField.vue'
import api from '@/api/axios'

export default {
  name: 'ResetEmailConfirm',
  components: {
    InputField
  },
  props: {
    uid: {
      type: String,
      required: true
    },
    token: {
      type: String,
      required: true
    }
  },
  setup(props, { emit }) {
    const router = useRouter()
    const toast = useToast()
    
    const form = ref({
      new_email: '',
      re_new_email: ''
    })
    
    const errors = ref({
      new_email: '',
      re_new_email: ''
    })

    const handleSubmit = async () => {
      try {
        await api.post('/auth/users/reset_email_confirm/', {
          uid: props.uid,
          token: props.token,
          new_email: form.value.new_email,
          re_new_email: form.value.re_new_email
        })
        
        toast.success('Email успешно изменен')
        emit('success')
        router.push('/profile')
      } catch (error) {
        if (error.response?.data) {
          errors.value = {
            new_email: error.response.data.new_email?.[0] || '',
            re_new_email: error.response.data.re_new_email?.[0] || ''
          }
          
          if (error.response.data.token) {
            toast.error('Ссылка для смены email недействительна или устарела')
            router.push('/profile')
          } else {
            toast.error('Ошибка при смене email')
          }
        }
      }
    }

    return {
      form,
      errors,
      handleSubmit
    }
  }
}
</script>

<style lang="scss" scoped>
.reset-email {
  &__title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: center;
  }

  &__form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  &__submit {
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
  }
}
</style> 