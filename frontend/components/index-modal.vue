<template>
  <v-dialog max-width="350">
    <template v-slot:activator="{ on }">
      <v-btn :color="isFeedback ? 'blue' : 'primary'" :flat="isFeedback" dark v-on="on">
        {{ action }}
      </v-btn>
    </template>
    <v-card class="modal">
      <v-card-title class="headline">
        <div v-if="!isFeedback">
          <v-btn flat color="blue" @click="isRegister = false">
            {{ $t('main.sign-in') }}
          </v-btn>
          <v-btn flat color="blue" @click="isRegister = true">
            {{ $t('main.register') }}
          </v-btn>
        </div>
        <div v-else>
          {{ $t('main.modal.feedback-title') }}
        </div>
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="form.email"
          :label="$t('main.modal.email')"
          :rules="!isFeedback ? [rules.required, rules.email] : []"
          :validate-on-blur="true"
          autofocus
        />
        <v-text-field
          v-if="!isFeedback"
          v-model="form.password"
          :label="$t('main.modal.password')"
          :rules="[rules.required, rules.password]"
          :validate-on-blur="true"
          required
        />
        <v-textarea
          v-if="isFeedback"
          name="input-7-1"
          label="Message"
          hint="Write your message"
        />
        <v-text-field
          v-if="isRegister"
          v-model="form.repeatPassword"
          :label="$t('main.modal.password-repeat')"
          :rules="[rules.required, rules.password, rules.passwordRepeat]"
          :validate-on-blur="true"
          required
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="blue" class="submit-btn" @click="sendForm">
          {{ $t('main.modal.submit') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    action: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isRegister: false,
      form: {
        email: '',
        password: '',
        repeatPassword: ''
      },
      rules: {
        required: value => !!value || this.$t('main.modal.error.required'),
        password: value => value.length > 5 || this.$t('main.modal.error.length'),
        email: (value) => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || this.$t('main.modal.error.email')
        },
        passwordRepeat: value => value === this.form.password || this.$t('main.modal.error.password-repeat')
      }
    }
  },
  computed: {
    isFeedback() {
      return this.action === 'feedback'
    }
  },
  methods: {
    sendForm() {
      this.$store.dispatch('register', this.form)
    }
  }
}
</script>

<style scoped>
  .modal {
    transition: .3s;
  }
  .headline {
    display: flex;
    justify-content: center;
  }
  .submit-btn {
    color: white !important
  }
</style>
