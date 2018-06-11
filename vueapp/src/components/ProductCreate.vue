<template>
        <div id="container" class="container">

            <!-- <b-container fluid>
              <b-row class="my-1" v-for="type in types" :key="type">
                <b-col sm="3"><label :for="`type-${type}`">Type {{ type }}:</label></b-col>
                <b-col sm="9"><b-form-input :id="`type-${type}`" :type="type"></b-form-input></b-col>
              </b-row>
            </b-container> -->
      
            <div class="row">
            
                <div class="col-sm-8 offset-sm-2">
                <div class="alert alert-warning" v-show="showCreateMessage"  >
                  <button type="button" class="close" @click="hideMessage()">X</button>
                  <strong>Send message successfully !</strong>
                </div>
                <div class="alert alert-warning" v-show="showUpdateMessage"  >
                  <button type="button" class="close" @click="hideMessage()">X</button>
                  <strong>Product successfully updated!</strong>
                </div>
                
                <div class="alert alert-warning" v-show="showError"  >
                  <button type="button" class="close" @click="hideMessage()">X</button>
                  <strong>Error!</strong>
                </div>                
                    <h1>Application test sigma sender</h1>
                    <br/>
                    <div class="info-form">
                      <form>
                        <div class="form-group">
                          <label for="sku">Channel</label>
                          <br/>
                          <!-- <input v-model="product.channel" type="text" class="form-control" id="sku" aria-describedby="skuHelp" placeholder="mail/push/sms"> -->
                          <!-- <small id="skuHelp" class="form-text text-muted">Enter channel you want to test</small> -->
                          
                          <!-- <input type="radio" id="mail" value="mail" v-model="product.channel">
                          <label for="one">mail</label>
                          <input type="radio" id="sms" value="sms" v-model="product.channel">
                          <label for="one">sms</label>
                          <input type="radio" id="push" value="push" v-model="product.channel">
                          <label for="one">push</label> -->
                          <select v-model="product.channel">
                            <option disabled value="">Please select channel: </option>
                            <option>mail</option>
                            <option>sms</option>
                            <option>push</option>
                          </select>
                          <br/>
                          <small id="skuHelp" class="form-text text-muted">Choose channel you want to test</small>
                          <br/>

                          <label for="description">Users</label>
                          <textarea v-model="product.users" class="form-control" id="description" aria-describedby="descHelp" placeholder="Enter list of mail/sms/token ex: addr1@domain.com addr2@damin.com addr3@domain.com"></textarea>
                          <small id="descHelp" class="form-text text-muted"> {{ userDescription }} </small>
                          <br/>

                          <label for="buyPrice">Template Name</label>
                          <input v-model="product.templateName" type="text" class="form-control" id="buyPrice" aria-describedby="buyPriceHelp" placeholder="Enter template name, ex: templates.template">
                          <small id="buyPriceHelp" class="form-text text-muted">Enter your template name</small>
                          <br/>

                          <label for="description">Template Parametters</label>
                          <textarea v-model="product.templateParams" class="form-control" id="description" aria-describedby="descHelp" placeholder='{"param1": "value1", "param2": "value2"}'></textarea>
                          <small id="descHelp" class="form-text text-muted">Enter params in json string format</small>
                          <br/>

                          <!--  <label for="sellPrice">Send time</label>
                           <input v-model="product.sendTime" type="text" class="form-control" id="sellPrice" aria-describedby="sellPriceHelp" placeholder="Enter time to send message">
                           <small id="sellPriceHelp" class="form-text text-muted">Enter time when you want to send message</small> -->

                          <!-- <label for="unit">Expire time</label>
                          <input v-model="product.expireTime" type="text" class="form-control" id="unit" aria-describedby="unitHelp" placeholder="Enter expire time">
                          <small id="unitHelp" class="form-text text-muted">Enter the time that expire </small> -->

                          <!-- <b-col sm="3"><label for="type-date">Send Date:</label></b-col>
                          <b-col sm="9"><b-form-input id="type-date" type="date"></b-form-input></b-col>

                          <b-col sm="3"><label for="type-time">Send Time:</label></b-col>
                          <b-col sm="9"><b-form-input id="type-time" type="time"></b-form-input></b-col> -->
                          
                          <label for="unit">Send Message Datetime</label>
                          <datetime type="datetime" v-model="product.datetimeSendMessage"></datetime>
                          <small id="sellPriceHelp" class="form-text text-muted">Choose time when you want to send message</small>
                          <br/>

                          <label for="unit">Expire Datetime</label>
                          <datetime type="datetime" v-model="product.datetimeExpire"></datetime>
                          <small id="unitHelp" class="form-text text-muted">Enter the time that expire </small> 

                        </div>
                      </form>
                       <button class="btn btn-primary" v-if="!this.product.pk" @click="createProduct()" ><span v-if="!creating">Create</span><span v-if="creating">Creating... Please wait </span></button>
                       <button class="btn btn-primary" v-if="this.product.pk" @click="updateProduct()" ><span v-if="!updating">Update</span><span v-if="updating">Updating... Please wait </span></button>
                       <!-- <button class="btn btn-primary"  @click="newProduct()" >New..</button> -->
                       <!-- <button class="btn btn-primary" v-if="!this.product.pk" @click="sendMessage()" ><span v-if="!creating">Send</span><span v-if="creating">Sending... Please wait </span></button> -->

                    </div>
                </div>
            </div>
        </div>

</template>

</template>

<script>
/* eslint-disable */
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

import Datetime from 'vue-datetime';
import 'vue-datetime/dist/vue-datetime.css';
import Vue from 'vue';
Vue.use(Datetime);

// import { FormInput } from 'bootstrap-vue/es/components';
// import Vue from 'vue'
// Vue.use(FormInput);

import {APIService} from '../http/APIService';
const apiService = new APIService();

export default {
  name: 'ProductCreate',
  components: {
    // FormInput
  },
  data() {
    return {
      showCreateMessage: false,
      showUpdateMessage: false,
      showError: false,
      product: {
        // channel: "mail",
        // users: ["addr1@domain.com", "phungxuananh1991@gmail.com"],
        // templateName: "templates.template",
        // templateParams: {
        //     subject: "Email from sigma sender service",
        //     from_emai: "sender@sigma.com",
        //     var1: "value of var1",
        //     var2: "value of var2"
        // },

      },
      products: '',
      creating: false,
      updating: false,
      userDescription: "Enter list of users where you want to send message",
      // types: [
      //   'text', 'password', 'email', 'number', 'url',
      //   'tel', 'date', `time`, 'range', 'color'
      // ]
    };
  }, 
  methods: {
    hideMessage(){
      this.showCreateMessage = false;
      this.showUpdateMessage = false;
      this.showError = false;
    },
    createProduct(){
      console.log('create product' + JSON.stringify(this.product));
      this.product.templateParams = JSON.parse(this.product.templateParams)
      
      this.creating = true;
      apiService.createProduct(this.product).then((result)=>{
          console.log(result);
          // success 
          if(result.status === 201){
            this.product = result.data;
            this.showCreateMessage = true;
            
            
          }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        this.showError = true;
            sleep(1000).then(() => {
               this.creating = false;
            })
      });
    },
    updateProduct(){
      this.updating = true;
      console.log('update product' + JSON.stringify(this.product));
      apiService.updateProduct(this.product).then((result)=>{
          console.log(result);
          // success 
          if(result.status === 200){
            //this.product = {};
            this.showUpdateMessage = true;
            sleep(1000).then(() => {
               this.updating = false;
            })
            
          }
          
      },(error)=>{
        this.showError = true;
        sleep(1000).then(() => {
               this.updating = false;
        })        
      });
    },
    newProduct(){
      this.product = {};
    },

    sendMessage(){
      console.log('Send message' + JSON.stringify(this.product));
      this.creating = true;
      apiService.sendMessage(this.product).then((result)=>{
          console.log(result);
          // success 
          if(result.status === 201){
            this.product = result.data;
            this.showCreateMessage = true;
          }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        this.showError = true;
            sleep(1000).then(() => {
               this.creating = false;
            })
      });
    },
    
  },
  mounted() {
    
    if(this.$route.params.pk){
      console.log(this.$route.params.pk)
      apiService.getProduct(this.$route.params.pk).then((product)=>{
        this.product = product;
      })
    }
  },
}
</script>
<style scoped>
.aform{
  margin-left:  auto;
  width: 60%;
}
</style>
