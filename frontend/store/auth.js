import axios from 'axios'

import api from '../constants/api'
import cookie from '../constants/cookie'

export const state = () => ({
  userId: '',
  session: ''
})

export const getters = {
  getUserId(state) {
    return state.userId
  }
}

export const mutations = {
  set(state, { data, value }) {
    state[data] = value
  }
}

export const actions = {

  authenticate({ state, commit }, { action, email, password }) {
    const form = new FormData()

    form.append('email', email)
    form.append('raw_password', password)

    axios.post(api[action], form)
      .then((res) => {
        const { user_id, session_id } = res.data

        commit('set', { data: 'session', value: session_id })
        commit('set', { data: 'userId', value: user_id })

        this.$cookies.set(cookie.session, session_id)
        this.$cookies.set(cookie.user, user_id)
        this.$router.push(`/profile`)
      })
      .catch(e => console.log(e))
  },

  logout({ state, commit }) {
    const form = new FormData()
    form.append('user_id', state.userId)

    return axios.delete(api.logout, form)
      .then(() => {
        commit('set', { data: 'session', value: '' })
        commit('set', { data: 'userId', value: '' })
        this.$cookies.remove(cookie.session)
        this.$cookies.remove(cookie.user)
        this.$router.push('/')
      })
      .catch(console.log)
  }

  // getUser({ state, commit }) {
  //   return this.$axios.get('/user', {
  //     headers: {
  //       Authorization: this.$cookies.get(cookie)
  //     }
  //   })
  //     .then((res) => {
  //       commit('set', { data: 'user', value: res.data })
  //     })
  //     .catch((e) => {
  //       console.log(e)
  //     })
  // }
}
