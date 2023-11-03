<template>
  <LayoutContainer>
    <div class="text-center">
      <h1>
        {{ $t('message.thankYouForPurchase') }}
      </h1>
      <div>
        <Icon
          name="ic:baseline-check-circle-outline"
          size="100px"
          color="green"
        />
      </div>
      <div>
        <h4>{{ $t("message.youWillBeRedirected", { n: redirectTimer }) }}</h4>
      </div>
    </div>
  </LayoutContainer>
</template>

<script setup lang="ts">

const redirectTimer = ref<number>(5);

if (process.client) {
  const interval = setInterval(() => redirectTimer.value--, 1000);

  watch(redirectTimer, async (value) => {
    if (value === 0) {
      clearInterval(interval);
      await navigateTo("/");
    }
  });
}
</script>