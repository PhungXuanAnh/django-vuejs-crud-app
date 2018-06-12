// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

// import BootstrapVue from 'bootstrap-vue'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
// Vue.use(BootstrapVue)

// import Datetime from 'vue-datetime'
// import 'vue-datetime/dist/vue-datetime.css'
// Vue.use(Datetime)

// Vue.extend({
//   template: '...',
//   components: {
//     datetime: Datetime
//   }
// })

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})

Vue.filter('currency', function (value) {
  return '$' + parseFloat(value).toFixed(2)
})
