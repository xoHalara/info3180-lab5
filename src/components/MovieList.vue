<template>
  <div class="container mt-5">
    <h2 class="mb-4">Movie Collection</h2>
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else class="row">
      <div v-for="movie in movies" :key="movie.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-header d-flex justify-content-end">
            <div class="dropdown">
              <button class="btn btn-link text-dark" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="bi bi-three-dots-vertical"></i>
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item text-danger" href="#" @click="deleteMovie(movie.id)">Delete Movie</a></li>
              </ul>
            </div>
          </div>
          <img :src="movie.poster" class="card-img-top" :alt="movie.title">
          <div class="card-body">
            <h5 class="card-title fw-bold">{{ movie.title }}</h5>
            <p class="card-text small">{{ movie.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>

    <!-- Error Messages -->
    <div v-if="deleteError" class="alert alert-danger mt-3">
      {{ deleteError }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const movies = ref([]);
const loading = ref(true);
const error = ref(null);
const successMessage = ref("");
const deleteError = ref("");

async function fetchMovies() {
  try {
    const response = await fetch('/api/v1/movies');
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || `HTTP error! status: ${response.status}`);
    }
    
    movies.value = data.movies;
  } catch (e) {
    error.value = `Error loading movies: ${e.message}`;
    console.error('Error details:', e);
  } finally {
    loading.value = false;
  }
}

async function deleteMovie(movieId) {
  if (!confirm('Are you sure you want to delete this movie?')) {
    return;
  }

  try {
    const response = await fetch(`/api/v1/movies/${movieId}`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrf_token.value
      }
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || `HTTP error! status: ${response.status}`);
    }

    // Remove the movie from the list
    movies.value = movies.value.filter(movie => movie.id !== movieId);
    successMessage.value = "Movie successfully deleted";
    deleteError.value = "";
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = "";
    }, 3000);
  } catch (e) {
    deleteError.value = `Error deleting movie: ${e.message}`;
    successMessage.value = "";
  }
}

onMounted(() => {
  fetchMovies();
});
</script>

<style scoped>
.card-img-top {
  height: 400px;
  object-fit: cover;
}

.card-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.card-text {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
}

.card-header {
  background: none;
  border: none;
  padding: 0.5rem;
}

.dropdown-toggle::after {
  display: none;
}

.btn-link {
  padding: 0.25rem;
}

.bi-three-dots-vertical {
  font-size: 1.25rem;
}
</style> 