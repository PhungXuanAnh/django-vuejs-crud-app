import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ProductList from '@/components/ProductList'
import ProductCreate from '@/components/ProductCreate'
import Home from '@/components/Home'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/product-create',
      name: 'ProductCreate',
      component: ProductCreate
    },
    {
      path: '/product-update/:pk',
      name: 'ProductUpdate',
      component: ProductCreate
    }
  ]
})
