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
    // Use for pre-rendering
  }
}
