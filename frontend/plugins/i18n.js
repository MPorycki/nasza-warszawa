/**
 * plugins/i18n.js
 * Плагин nuxtjs для переводов
 * назначает приложению объект для переводов,
 * добавляет функцию для создания url с учетом языка
 * @see https://nuxtjs.org/examples/i18n/
 */

import Vue from 'vue'
import VueI18n from 'vue-i18n'
import PL from '~/locales/pl.json'
import EN from '~/locales/en.json'

Vue.use(VueI18n)

export default ({ app, store, params }) => {
  // Set i18n instance on app
  // This way we can use it in middleware and pages asyncData/fetch
  app.i18n = new VueI18n({
    locale: store.state.locale,
    fallbackLocale: 'pl',
    messages: {
      'pl': PL,
      'en': EN
    }
  })

  // app.i18n.path = (link) => {
  //   if (link[0] === '/') link = link.substr(1)
  //   return `/${app.i18n.locale}/${link}`
  // }
}
