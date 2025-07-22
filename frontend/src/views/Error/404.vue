<template>
  <div class="not-found-page-wrapper">
    <div class="error-card card-animated">
      <div class="error-icon-wrapper">
        <i class="fas fa-compass"></i>
      </div>
      <h1 class="error-code">404</h1>
      <h2 class="error-title">Page Not Found</h2>
      <p class="error-message">
        Oops! The page you are looking for does not exist. It might have been moved, deleted, or you may have typed the
        address incorrectly.
      </p>
      <router-link to="/" class="btn btn-primary btn-go-home">
        <i class="fas fa-home"></i> Go to Root Page
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
};
</script>

<style scoped>
/* --- 1. Main Page Wrapper --- */
/* This creates the overall page layout and background */
.not-found-page-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  /* Same background as other pages */
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* --- 2. The Main Error Card --- */
/* This is the central white card, styled like profile.vue */
.error-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  padding: 40px 50px;
  text-align: center;
  max-width: 550px;
  width: 100%;
}

/* Add the hover effect from other pages */
.card-animated {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-animated:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

/* --- 3. Card Content: Icon and Typography --- */
.error-icon-wrapper {
  font-size: 60px;
  color: #3498db;
  /* A friendly, professional blue */
  margin-bottom: 25px;
}

.error-code {
  font-size: 6.5rem;
  font-weight: 700;
  color: #2c3e50;
  /* Dark, serious color for the code */
  margin: 0;
  line-height: 1;
}

.error-title {
  font-size: 2.2rem;
  font-weight: 600;
  color: #34495e;
  margin-top: 15px;
  margin-bottom: 15px;
}

.error-message {
  font-size: 1rem;
  color: #7f8c8d;
  /* Softer color for helper text */
  margin-bottom: 35px;
  line-height: 1.6;
}

/* --- 4. Button Styling --- */
/* This reuses the exact button style from your other components */
.btn {
  color: #fff;
  padding: 12px 25px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 6px 15px rgba(54, 101, 255, 0.4);
}

.btn-primary {
  background: linear-gradient(to right, #3665ff, #2548cc);
}

/* --- 5. Responsive Design --- */
@media (max-width: 576px) {
  .error-card {
    padding: 30px 25px;
  }

  .error-icon-wrapper {
    font-size: 50px;
  }

  .error-code {
    font-size: 5rem;
  }

  .error-title {
    font-size: 1.8rem;
  }

  .error-message {
    font-size: 0.9rem;
  }

  .btn {
    width: 100%;
    padding: 12px;
    font-size: 15px;
  }
}
</style>