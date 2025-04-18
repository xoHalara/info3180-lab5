<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<template>
  <AppHeader />

  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/movies">Movies</router-link> |
    <router-link to="/movies/create">Add Movie</router-link>
  </nav>

  <main>
    <RouterView />
  </main>
  
  <AppFooter />
</template>

<style>
body {
  padding-top: 75px;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  margin: 0 10px;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>