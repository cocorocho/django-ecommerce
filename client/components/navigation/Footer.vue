<template>
  <footer class="bg-black">
    <!-- TODO -->
  </footer>
</template>

<script setup lang="ts">
import { useStoreMeta } from "~/store/store";

const storeMeta = useStoreMeta();
const { data: storeMetaData } = await useAsyncData("storeMetaData", async () => storeMeta.store);
</script>