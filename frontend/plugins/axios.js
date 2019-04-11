import axios from 'axios'
import api from '../constants/api'

axios.defaults.baseURL = api.BASE_URL

// export default function ({ $axios, redirect }) {
//   // Modify it in case some global changes to axios
//   $axios.onRequest((config) => {
//     console.log('Making request to ' + config.url)
//   })
//
//   $axios.onError((error) => {
//     const code = parseInt(error.response && error.response.status)
//     if (code === 400) {
//       redirect('/400')
//     }
//   })
// }
