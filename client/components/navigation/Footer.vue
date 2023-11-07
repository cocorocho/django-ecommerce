<template>
  <footer class="bg-black text-[var(--text-color)] p-8">
    <LayoutContainer>
      <div class="grid grid-cols-3 h-full">
        <div class="col-span-2 grid lg:grid-cols-2">
          <div v-if="Object.keys(policies).length">
            <div
              v-for="policy in Object.keys(policies)"
              :key="policy"
            >
              <NuxtLink
                class="capitalize"
                :to="{
                  name: 'storePolicies',
                  params: { policyName: policy }
                }"
              >
                {{ normalize(policy) }}
              </NuxtLink>
            </div>
          </div>
          <div>
            <!-- socials -->
            <div class="socials flex flex-wrap"
              v-if="socials"
            >
              <NuxtLink
                v-for="social in Object.entries(socials)"
                :to="social[1]"
                class="px-1"
              >
                <Icon
                  :name="socialIcons[social[0]]"
                  class="hover:brightness-150 duration-200 transition-filter"
                />
              </NuxtLink>
            </div>
          </div>
        </div>
        <div class="flex flex-col">
          <div class="mt-auto" v-if="storeMetaData && storeMetaData.name">
            <Icon name=ph:copyright size="16px"/>
            {{ storeMetaData.name }}
          </div>
        </div>
      </div>
    </LayoutContainer>
  </footer>
</template>

<script setup lang="ts">
import { useStoreMeta } from "~/store/store";

const storeMeta = useStoreMeta();
const { data: storeMetaData } = await useAsyncData("storeMetaData", async () => storeMeta.store);
const policies = computed(() => (
  lodashPickBy(storeMetaData.value?.policies, (value: string) => value !== ""))
);
const socials = computed(() => (
  lodashPickBy(storeMetaData.value?.socials, (value: string) => value !== ""))
);
const socialIcons: {[key: string]: string} = {
  facebook: "logos:facebook",
  instagram: "skill-icons:instagram",
  twitter: "skill-icons:twitter",
  youtube: "logos:youtube-icon",
  tiktok: "logos:tiktok-icon",
  pinterest: "logos:pinterest"
};
</script>

<style scoped>
footer:deep(a) {
  @apply no-underline text-[var(--text-color)] hover:text-white;
}
</style>