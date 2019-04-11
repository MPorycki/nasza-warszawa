import axios from 'axios'
import api from '../constants/api'

export const state = () => ({
  locales: ['pl', 'en'],
  locale: 'pl'
})

export const mutations = {
  SET_LANG(state, locale) {
    if (state.locales.indexOf(locale) !== -1) {
      state.locale = locale
    }
  }
}

export const actions = {
  nuxtServerInit({ dispatch, state }, { params }) {

  },

  register({ state }, data) {
    console.log('data in store')
    console.log(data)
    const form = new FormData()

    form.append('email', data.email)
    form.append('raw_password', data.password)

    axios.post(api.register, form)
      .then(res => console.log(res))
      .catch(e => console.log(e))
  },

  test() {
    axios.get('/')
      .then(console.log)
      .catch(console.log)
  }
}
