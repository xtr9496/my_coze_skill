<template>
  <div class="{{kebabCase componentName}}">
    <h1>{{ title }}</h1>
  </div>
</template>

<script setup lang="ts">
/**
 * {{componentName}} 组件
 * {{description}}
 */
interface Props {
  title: string;
}

const props = defineProps<Props>();
</script>

<style scoped>
.{{kebabCase componentName}} {
  padding: 20px;
}
</style>
