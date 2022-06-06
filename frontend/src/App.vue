<template>
  <v-app>
    <v-main  class="appbackground">
      <Detector/>
    </v-main>
  </v-app>
</template>

<script>
import Detector from './components/Detector';

export default {
  name: 'App',

  components: {
    Detector,
  },

  data: () => ({
    //
  }),
};
</script>

<style scoped>
.appbackground{
  background-color: #FFF2C2;
}
</style>