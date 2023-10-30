<template>
  <LayoutContainer>

    <div class="text-center">
      <h1>
        Thank you for your purchase!
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

setInterval(async () => {
  redirectTimer.value--;

  if (redirectTimer.value === 0) {
    await navigateTo("/");
  }
}, 1000);
</script>