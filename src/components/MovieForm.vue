<template>
  <div class="container mt-5">
    <form id="movieForm" @submit.prevent="saveMovie" enctype="multipart/form-data">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" v-model="title" />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea name="description" class="form-control" v-model="description"></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" name="poster" class="form-control" accept="image/jpeg,image/png" />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>

    <!-- Error Messages -->
    <div v-if="errors.length > 0" class="alert alert-danger mt-3">
      <ul>
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const title = ref("");
const description = ref("");
const csrf_token = ref("");
const successMessage = ref("");
const errors = ref([]);

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
}

function saveMovie() {
  const movieForm = document.getElementById('movieForm');
  const form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
  .then(function (response) {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(function (data) {
    if (data.errors) {
      errors.value = data.errors;
      successMessage.value = "";
    } else {
      successMessage.value = data.message;
      errors.value = [];
      // Clear form
      title.value = "";
      description.value = "";
      movieForm.reset();
    }
  })
  .catch(function (error) {
    console.error('Error:', error);
    errors.value = [`An error occurred: ${error.message}`];
    successMessage.value = "";
  });
}

onMounted(() => {
  getCsrfToken();
});
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style> 