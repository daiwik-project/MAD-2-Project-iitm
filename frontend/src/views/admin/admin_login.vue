<template>
    <div class="login-wrapper">
      <div class="login-container">
        <!-- The background image section is kept for visual consistency -->
        <div class="background-section"></div>
        
        <div class="form-section">
          <div class="card-login">
            <div class="logo-container">
              <img src="../../assets/logo.png" alt="iSchool Logo" class="logo" />
            </div>
  
            <!-- STEP 1: Email Input -->
            <div v-if="step === 1">
              <h2 class="login-title">Admin Login</h2>
              <p class="login-subtitle">Enter your email to receive an OTP</p>
    
              <form class="login-form" @submit.prevent="requestOtp">
                  <div class='form-group'>
                    <label for="email">Admin Email</label>
                    <input 
                      type="email" 
                      id="email" 
                      required 
                      v-model="email"
                      placeholder="Enter your admin email address" 
                    />
                  </div>
    
                <button type="submit" class="btn-login">Send OTP</button>
              </form>
            </div>

            <!-- STEP 2: OTP Input -->
            <div v-if="step === 2">
              <h2 class="login-title">Enter OTP</h2>
              <p class="login-subtitle">An OTP has been sent to <strong>{{ email }}</strong></p>

              <form class="login-form" @submit.prevent="verifyOtpAndLogin">
                  <div class='form-group'>
                    <label for="otp">One-Time Password</label>
                    <input 
                      type="text" 
                      id="otp" 
                      required 
                      placeholder="Enter the 6-digit OTP"
                      v-model="otp"
                      maxlength="6"
                      pattern="\d{6}"
                    />
                  </div>
    
                <button type="submit" class="btn-login">Verify & Login</button>
              </form>

              <p class="change-email-link">
                Wrong email? <a href="#" @click.prevent="goBack">Go Back</a>
              </p>
            </div>
  
            <p class="register-link">
              Not an admin? <router-link to="/login">Go to User Login</router-link>
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
  name: "AdminLogin",
  data() {
    return {
      step: 1, // 1 for email input, 2 for OTP input
      email: "",
      otp: "",
    };
  },
  methods: {
    async requestOtp() {
      if (!this.email) {
        alert("Please enter your admin email.");
        return;
      }

      const formData = new FormData();
      formData.append("email", this.email);

      try {
        // --- API CALL 1: Request OTP ---
        console.log("Requesting OTP for:", this.email);
        const response = await axios.post(`http://127.0.0.1:5000/api/request_otp`, formData);
        
        // --- SIMULATED SUCCESS ---
        alert(`An OTP has been sent to ${this.email}.`);
        this.step = 2; // Move to the next step
        // --- END SIMULATION ---

      } catch (error) {
        console.error("OTP Request failed:", error.response ? error.response.data : error.message);
        alert(`Failed to send OTP. Please check the email and try again.`);
      }
    },
    async verifyOtpAndLogin() {
      if (!this.otp || this.otp.length !== 6) {
        alert("Please enter a valid 6-digit OTP.");
        return;
      }

      const loginData = new FormData();
      loginData.append("email", this.email);
      loginData.append("otp", this.otp);

      try {
        const response = await axios.post(`http://127.0.0.1:5000/api/verify_otp`, loginData);
        
        // On success, set the cookie and redirect
        VueCookies.set('admin_token', response.data.admin_token, {
            expires: '1d', // Admin sessions might be shorter
            path: '/',
            samesite: 'Lax',
            secure: false, // Use secure cookies in production
        });
        
        alert('Admin login successful!');
        this.$router.push(`/admindashboard`);

      } catch (error) {
        console.error("Admin login failed:", error.response ? error.response.data : error.message);
        alert(`Login failed! Invalid OTP or server error.`);
      }
    },
    goBack() {
      this.step = 1;
      this.otp = ""; // Clear the OTP field
    }
  }
};
</script>
  
<style scoped>
  /* --- Re-using the exact same styles from your login page for consistency --- */
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
    background-color: #f4f4f4;
    font-family: 'Inter', sans-serif;
  }
  
  .login-container {
    width: 90%;
    max-width: 1200px;
    height: 90vh;
    display: flex;
    overflow: hidden;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  }
  
  .background-section {
    flex: 1;
    /* Using a different image for admin login can be a nice touch */
    background: url('../../assets/login1.jpg') no-repeat center center; 
    background-size: cover;
  }
  
  .form-section {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: white;
    padding: 2rem;
  }
  
  .card-login {
    width: 100%;
    max-width: 450px;
    padding: 2.5rem;
    background-color: white;
    border-radius: 15px;
  }
  
  .logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
  }
  
  .logo {
    max-height: 80px;
    object-fit: contain;
  }
  
  .login-title {
    text-align: center;
    color: #333;
    margin-bottom: 0.5rem; /* Reduced margin */
    font-size: 1.8rem;
    font-weight: 600;
  }

  .login-subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1.25rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
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
    border-color: #00ff88;
    box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.2);
  }
  
  .btn-login {
    width: 100%;
    padding: 0.875rem;
    background-color: #00ff88;
    color: #2b134b;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 1rem;
  }
  
  .btn-login:hover {
    background-color: #00cc77;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 204, 119, 0.4);
  }

  .change-email-link {
    text-align: center;
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #666;
  }
  
  .change-email-link a {
    color: #007bff;
    text-decoration: none;
    font-weight: 500;
  }
  
  .register-link {
    text-align: center;
    margin-top: 1.5rem;
    color: #666;
  }
  
  .register-link a {
    color: #00ff88;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s ease;
  }
  
  .register-link a:hover {
    color: #00cc77;
  }
  
  /* Responsive styles are unchanged */
  @media screen and (max-width: 1024px) {
    .login-container { width: 95%; height: 95vh; }
  }
  
  @media screen and (max-width: 768px) {
    .login-container { flex-direction: column; height: auto; min-height: 100vh; width: 100%; border-radius: 0; }
    .background-section { display: none; }
    .form-section { background-color: #f4f4f4; padding: 1rem; }
    .card-login { width: 90%; padding: 2rem; margin-top: 2rem; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); }
  }
  
  @media screen and (max-width: 480px) {
    .card-login { padding: 1.5rem; }
    .login-title { font-size: 1.5rem; }
  }
</style>