<template>
  <v-app>
    <v-toolbar>
      <v-toolbar-title>
        {{ title }}
      </v-toolbar-title>
      <v-spacer />
      <v-toolbar-items class="hidden-sm-and-down">
        <Modal action="feedback" />
        <Modal action="sign-in" />
        <!--<v-btn color="success" flat>Register</v-btn>-->
        <!--<v-btn color="primary" flat>Login</v-btn>-->
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer
      :fixed="fixed"
      app
    >
      <span>&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
import Modal from '@/components/index-modal'
export default {
  components: {
    Modal
  },
  data() {
    return {
      fixed: false,
      items: [
        {
          icon: 'apps',
          title: 'Welcome',
          to: '/'
        },
        {
          icon: 'bubble_chart',
          title: 'Inspire',
          to: '/inspire'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Nasza Warszawa'
    }
  }
}
</script>
