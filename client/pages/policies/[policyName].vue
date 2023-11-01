<template>
  <LayoutContainer
    :label="normalize(policyName)"
  >
    <div v-html="policyData" />
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useStoreMeta } from "~/store/store";

definePageMeta({
  name: "storePolicies",
})

const route = useRoute();
const storeMeta = useStoreMeta();
const { policyName } = route.params;
const { data: policies } = await useAsyncData("policies", async () => storeMeta.store.policies);

// As html, route to page if there is no policy
const policyData: string | undefined = lodashGet(policies.value, policyName, undefined);
if (!policyData) await navigateTo("/");
</script>