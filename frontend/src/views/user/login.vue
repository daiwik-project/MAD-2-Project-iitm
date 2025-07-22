<template>
    <div class="login-wrapper">
      <div class="login-container">
        <div class="background-section"></div>
        
        <div class="form-section">
          <div class="card-login">
            <div class="logo-container">
              <img src="../../assets/logo.png" alt="iSchool Logo" class="logo" />
            </div>
  
            <h2 class="login-title">Login to Your Account</h2>
  
            <form class="login-form">
                <div class='form-group'>
                <label for="username">Username or Email</label>
                <input 
                  type="text" 
                  id="username" 
                  required 
                  v-model="username"
                  placeholder="Enter your username or email" 

                />
                </div>

                <div class='form-group'>
                <label for="password">Password</label>
                <input 
                  type="password" 
                  id="password" 
                  required 
                  placeholder="Enter your password"
                  v-model="password"
                />
                </div>
  
              <button type="button" @click="login" class="btn-login">Login</button>
            </form>
  
            <p class="register-link">
              Don't have an account? <a href="/register">Register</a>
            </p>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios'; 
import VueCookies from 'vue-cookies'; 

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      if (!this.username || !this.password) {
        alert("Please fill in both username/email and password.");
        return;
      }

      const login_data = new FormData();
      login_data.append("identifier", this.username);
      login_data.append("password", this.password);

      try {

        const response = await axios.post(`http://127.0.0.1:5000/login`, login_data, 
        );

        VueCookies.set('access_token', response.data.token, {
            expires: '4d', 
            path: '/',
            samesite: 'Lax',
            secure: false  // Set to true in production
          });
        if (response.data.login_attempt === 0){

          this.$router.push(`/dashboard/start`);
        } else {
          this.$router.push(`/dashboard/`);  
        }
        

      } catch (error) {
        alert(`Login failed! Please check your credentials or you are blocked By admin. Pls Contact Admin`); 
      }
    }
  }
};
</script>
  



<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  .login-wrapper {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f4f4f4; /* Same as register page background */
    font-family: 'Inter', sans-serif;
  }
  
  .login-container {
    width: 90%;
    max-width: 1200px; /* Max width for the content area */
    height: 90vh; /* Adjust height as needed */
    display: flex;
    overflow: hidden;
    border-radius: 20px; /* Rounded corners for the container */
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  }
  
  .background-section {
    flex: 1; /* Takes up half the space */
    background: url('../../assets/login1.jpg') no-repeat center center; /* Your login background image */
    background-size: cover;
  }
  
  .form-section {
    flex: 1; /* Takes up the other half */
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: white; /* Form side background */
    padding: 2rem; /* Padding around the form card */
  }
  
  .card-login {
    width: 100%;
    max-width: 450px; /* Max width of the form card */
    padding: 2.5rem; /* Inner padding of the card */
    background-color: white; /* Card background */
    border-radius: 15px; /* Rounded corners for the card */
    /* Removed box-shadow from here as the container has it, but can be added if desired */
  }
  
  .logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem; /* Space below the logo */
  }
  
  .logo {
    max-height: 80px; /* Adjust logo size as needed */
    object-fit: contain;
  }
  
  .login-title {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem; /* Space below the title */
    font-size: 1.8rem; /* Title font size */
    font-weight: 600; /* Title font weight */
  }
  
  .form-group {
    margin-bottom: 1.25rem; /* Space between form fields */
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem; /* Space between label and input */
    color: #555;
    font-weight: 500;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
  }
  
  .form-group input:focus {
    outline: none;
    border-color: #00ff88; /* Highlight color on focus */
    box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.2); /* Glow effect on focus */
  }
  
  .btn-login {
    width: 100%;
    padding: 0.875rem;
    background-color: #00ff88; /* Button background color */
    color: #2b134b; /* Button text color */
    border: none;
    border-radius: 8px;
    font-weight: 600;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 1rem; /* Space above the button */
  }
  
  .btn-login:hover {
    background-color: #00cc77; /* Darker shade on hover */
    transform: translateY(-2px); /* Slight lift on hover */
    box-shadow: 0 5px 15px rgba(0, 204, 119, 0.4); /* Shadow on hover */
  }
  
  .register-link {
    text-align: center;
    margin-top: 1.5rem; /* Space above the link */
    color: #666;
  }
  
  .register-link a {
    color: #00ff88; /* Link color */
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s ease;
  }
  
  .register-link a:hover {
    color: #00cc77; /* Darker link color on hover */
  }
  
  /* Responsive adjustments */
  @media screen and (max-width: 1024px) {
    .login-container {
      width: 95%;
      height: 95vh;
    }
  }
  
  @media screen and (max-width: 768px) {
    .login-container {
      flex-direction: column; /* Stack form below background on small screens */
      height: auto; /* Adjust height for content */
      min-height: 100vh; /* Ensure it takes full viewport height */
      width: 100%;
      border-radius: 0; /* No rounded corners on full width */
    }
  
    .background-section {
      /* Option 1: Hide background section entirely on small screens */
      display: none; 
      
      /* Option 2: Make background section smaller if you want to keep it
      flex: 0.5; 
      min-height: 200px; 
      */
    }
  
    .form-section {
      width: 100%;
      /* If background-section is hidden, form-section takes full space */
      /* If background-section is not hidden, adjust flex or height as needed */
      background-color: #f4f4f4; /* Match wrapper background if card is distinct */
      padding: 1rem; /* Adjust padding for smaller screens */
    }
  
    .card-login {
      width: 90%; /* Card takes most of the width */
      padding: 2rem; /* Adjust card padding */
      margin-top: 2rem; /* Add some margin if background is shown */
      margin-bottom: 2rem;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); /* Add shadow if wrapper is plain */
    }
  }
  
  @media screen and (max-width: 480px) {
    .card-login {
      padding: 1.5rem;
    }
  
    .login-title {
      font-size: 1.5rem;
    }
  }
</style> 