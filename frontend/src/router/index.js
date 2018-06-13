import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Home from '@/components/Home'
import ProductList from '@/components/ProductList'
import ProductCreate from '@/components/ProductCreate'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/hello-world',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/product-list',
      name: 'ProductList',
      component: ProductList
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
      },
  ]
})
