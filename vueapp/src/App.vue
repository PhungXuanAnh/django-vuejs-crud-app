<template>
<div>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <a class="navbar-brand" href="#">Test sender</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">

          <li class="nav-item">
          <a class="btn btn-primary" href="/">Home</a>
          </li>
          <li class="nav-item">
          <a class="btn btn-primary" href="/product-list">Products</a>
          </li>
          <li class="nav-item">
          <a class="btn btn-primary" href="/product-create">Create</a>
          </li>

        </ul>

      </div>
    </nav>

    <div class="container">
      <router-view></router-view>
    </div>

</div>  
</template>

<script>
/* eslint-disable */
export default {
  name: 'app',
  data () {
    return {}
  },
  methods: {}
}
</script>

<style>
@import './assets/bootstrap.min.css';
body {
  min-height: 75rem;
  padding-top: 4.5rem;
}
.nav-item{
  padding:1px;
  margin-left: 5px;
}
</style>
