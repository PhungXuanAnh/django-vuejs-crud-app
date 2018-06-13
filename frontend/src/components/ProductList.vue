<template>
<div>
<h1>Products ()</h1>
<table class="table table-bordered table-hover">
  <thead>
    <tr>
      <th>#</th>
      <th>SKU</th>
      <th>Name</th>
      <th>Quantity</th>
      <th>Price</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr   v-for="product in products" v-bind:key="product.pk" @click="selectProduct(product)">
      <th></th>
      <th></th>
      <td></td>
      <td> </td>
      <td></td>
      <td>
        <button class="btn btn-danger" @click="deleteProduct(product)"> X</button>
        <a class="btn btn-primary" v-bind:href="'/product-update/' + product.pk"> &#9998; </a>

      </td>
    </tr>
  </tbody>
</table>
<div>
<ul class="list-horizontal">
  <li><button class="btn btn-primary" @click="getPreviousPage()">Previous</button></li>
  <li v-for="page in pages" v-bind:key="page.link">
    <a class="btn btn-primary" @click="getPage(page.link)"></a>
  </li>
  <li><button class="btn btn-primary" @click="getNextPage()">Next</button></li>
</ul>


</div>

<div class="card text-center" v-if="selectedProduct">
  <div class="card-header">
    # -- 
  </div>
  <div class="card-block">
    <h4 class="card-title"></h4>
    <p class="card-text">

    </p>
    <a class="btn btn-primary" v-bind:href="'/product-update/' + selectedProduct.pk"> &#9998; </a>
    <button class="btn btn-danger" @click="deleteProduct(selectedProduct)"> X</button>

  </div>

</div>
</div>
</template>

<script>
import {APIService} from '../http/APIService';
import Loading from './Loading';
const API_URL = 'http://localhost:8000';
const apiService = new APIService();

export default {
  name: 'ProductList',
  data() {
    return {
      selectedProduct:null,
      products: [],
      numberOfPages:0,
      pages : [],
      numberOfProducts:0,
      loading: false,
      nextPageURL:'',
      previousPageURL:''
    };
  }, 
  methods: {
    getProducts(){

      this.loading = true;
      apiService.getProducts().then((page) => {
        this.products = page.data;
        console.log(page);
        console.log(page.nextlink);
        this.numberOfProducts = page.count;
        this.numberOfPages = page.numpages;
        this.nextPageURL = page.nextlink;
        this.previousPageURL = page.prevlink;
        if(this.numberOfPages)
        {
          for(var i = 1 ; i <= this.numberOfPages ; i++)
          {
            const link = `/api/products/?page=${i}`;
            this.pages.push({pageNumber: i , link: link})
          }
        }
        this.loading = false;
      });
    },
    getPage(link){
      this.loading = true;  
      apiService.getProductsByURL(link).then((page) => {
        this.products = page.data;
        this.nextPageURL = page.nextlink;
        this.previousPageURL = page.prevlink;
        this.loading = false;
      });
    },
    getNextPage(){
      console.log('next' + this.nextPageURL);
      this.loading = true;  
      apiService.getProductsByURL(this.nextPageURL).then((page) => {
        this.products = page.data;
        this.nextPageURL = page.nextlink;
        this.previousPageURL = page.prevlink;
        this.loading = false;
      });

    },
    getPreviousPage(){
      this.loading = true;  
      apiService.getProductsByURL(this.previousPageURL).then((page) => {
        this.products = page.data;
        this.nextPageURL = page.nextlink;
        this.previousPageURL = page.prevlink;
        this.loading = false;
      });

    },
    deleteProduct(product){
      console.log("deleting product: " + JSON.stringify(product))
      apiService.deleteProduct(product).then((r)=>{
        console.log(r);
        if(r.status === 204)
        {
          alert("Product deleted");
          this.$router.go()

        }
      })
    },
    selectProduct(product){
      this.selectedProduct = product;
    }
  },
  mounted() {

    this.getProducts();

  },
}
</script>

<style scoped>
.list-horizontal li {
    display:inline-block;
}
.list-horizontal li:before {
    content: '\00a0\2022\00a0\00a0';
    color:#999;
    color:rgba(0,0,0,0.5);
    font-size:11px;
}
.list-horizontal li:first-child:before {
    content: '';
}
</style>