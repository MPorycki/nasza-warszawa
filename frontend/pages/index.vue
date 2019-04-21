<template>
  <v-layout
    column
    justify-center
    align-center
  >
    <v-flex
      xs12
      sm8
      md6
    >
      <v-card class="main-text">
        <!--TODO: Edit it properly and maintainably, maybe using some content-management system-->
        <h1>{{ $t('main.content.header') }}</h1>

        <h2>{{ $t('main.content.subheader') }}</h2>
        <br>
        <p>
          <b>{{ $t('main.content.list_header') }}</b>
        </p>
        <ul>
          <li v-for="index in LIST_ITEM_AMOUNT" :key="`main_list_item${index}`">
            {{ $t(`main.content.list_item_${index}`) }}
          </li>
        </ul>
        <br>
        <p v-for="index in DESCRIPTION_AMOUNT" :key="`main_description${index}`">
          {{ $t(`main.content.description_${index}`) }}
        </p>
      </v-card>
      <v-btn @click="$store.dispatch('test')">
        Test
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  components: {
  },
  data() {
    return {
      LIST_ITEM_AMOUNT: 7,
      DESCRIPTION_AMOUNT: 2
    }
  }
}
</script>

<style scoped>
  .main-text {
    padding: 15px
  }
</style>
