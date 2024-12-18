import globals from "globals";
import pluginJs from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import eslintConfigPrettier from "eslint-config-prettier";

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    // Указываем к каким файлам применяются правила
    files: ["**/*.{js,mjs,cjs,vue}"],
    languageOptions: {
      // Аналог env: { browser: true, es2021: true }
      globals: {
        ...globals.node,
      },
      ecmaVersion: "latest",
      sourceType: "module",
    },
    rules: {
      // Добавьте тут любые дополнительные правила, если они были в .eslintrc
      // Пример:
      // "no-unused-vars": "warn",
    },
  },
  // Аналог "eslint:recommended"
  pluginJs.configs.recommended,
  // Аналог "plugin:vue/vue3-recommended"
  ...pluginVue.configs["flat/recommended"],
  // Аналог "@vue/eslint-config-prettier"
  eslintConfigPrettier,
];
