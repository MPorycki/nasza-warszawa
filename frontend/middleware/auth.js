import cookie from '@/constants/cookie'

export default function ({ store, route, redirect, app }) {
  const session = app.$cookies.get(cookie.session)

  if (route.path !== '/') {
    if (!session) redirect('/')
  } else if (route.path === '/' && session) {
    redirect(`/profile`)
  }
}
