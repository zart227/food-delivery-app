<template>
    <div class="input-field">
      <label v-if="label" :for="id" class="input-field__label">{{ label }}</label>
      <input
        :id="id"
        :type="type"
        :placeholder="placeholder"
        class="input-field__input"
        :class="{ 'input-field__input--error': error }"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :autocomplete="autocomplete"
      />
      <span v-if="error" class="input-field__error">{{ error }}</span>
    </div>
  </template>
  
  <script>
  export default {
    name: 'InputField',
    props: {
      modelValue: {
        type: String,
        required: true,
      },
      label: {
        type: String,
        default: '',
      },
      type: {
        type: String,
        default: 'text',
      },
      placeholder: {
        type: String,
        default: '',
      },
      error: {
        type: String,
        default: '',
      },
      id: {
        type: String,
        default: () => `input-${Math.random().toString(36).substr(2, 9)}`,
      },
      autocomplete: {
        type: String,
        default: '',
      },
    },
    emits: ['update:modelValue'], // Явно объявляем событие
  };
  </script>
  
  <style lang="scss" scoped>
  .input-field {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
  
    &__label {
      font-family: Montserrat;
      font-size: 14px;
      font-weight: 500;
      margin-bottom: 5px;
    }
  
    &__input {
      border: 1px solid #d58c51;
      border-radius: 6px;
      font-size: 16px;
      padding: 10px;
      font-family: Montserrat;
      outline: none;
      transition: border-color 0.2s;
  
      &--error {
        border-color: #ff4d4f;
      }
    }
  
    &__error {
      color: #ff4d4f;
      font-size: 12px;
      margin-top: 5px;
    }
  }
  </style>
  