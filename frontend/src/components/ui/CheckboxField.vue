<template>
    <div class="checkbox-field">
      <label :for="id" class="checkbox-field__label">
        <input
          :id="id"
          type="checkbox"
          class="checkbox-field__input"
          :checked="modelValue"
          @change="$emit('update:modelValue', $event.target.checked)"
        />
        <span class="checkbox-field__custom"></span>
        {{ label }}
      </label>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CheckboxField',
    props: {
      modelValue: {
        type: Boolean,
        required: true,
      },
      label: {
        type: String,
        required: true,
      },
      id: {
        type: String,
        default: () => `checkbox-${Math.random().toString(36).substr(2, 9)}`,
      },
    },
    emits: ['update:modelValue'], // Явно объявляем событие
  };
  </script>
  
  <style lang="scss" scoped>
  .checkbox-field {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
  
    &__label {
      font-family: Montserrat;
      font-size: 14px;
      font-weight: 400;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
    }
  
    &__input {
      display: none;
    }
  
    &__custom {
      width: 18px;
      height: 18px;
      border: 1px solid #d58c51;
      border-radius: 3px;
      background-color: #fff;
      position: relative;
    }
  
    &__input:checked + .checkbox-field__custom {
      background-color: #d58c51;
      border-color: #d58c51;
    }
  
    &__input:checked + .checkbox-field__custom:after {
      content: '';
      position: absolute;
      top: 3px;
      left: 6px;
      width: 4px;
      height: 8px;
      border: solid #fff;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
    }
  }
  </style>
  