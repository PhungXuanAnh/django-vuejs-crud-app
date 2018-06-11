
/* eslint-disable */

import Vue from 'vue'
import Router from 'vue-router'
import ProductList from '@/components/ProductList'
import ProductCreate from '@/components/ProductCreate'
import Callback from '@/components/Callback'
import Home from '@/components/Home'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/product-list',
    name: 'ProductList',
    component: ProductList,
  },
  {
    path: '/product-create',
    name: 'ProductCreate',
    component: ProductCreate,
  },
  {
    path: '/product-update/:pk',
    name: 'ProductUpdate',
    component: ProductCreate
  },
  {
    path: '/callback',
    name: 'Callback',
    component: Callback
  }
]

const router = new Router({
  mode: 'history',
  routes
})

export default router
