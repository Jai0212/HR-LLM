<template>
  <div id="app">
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
body {
  background-color: #eaf4e7;
}
#app {
  font-family: 'Arial', sans-serif;
  text-align: center;
  margin: 20px;
}

main {
  margin-top: 20px;
}
</style>
