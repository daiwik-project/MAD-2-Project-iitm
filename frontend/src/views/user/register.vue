<template>
    <div class="register-wrapper">
        <div class="register-container">
            <div class="background-section"></div>

            <div class="form-section">
                <div class="card-register">
                    <div class="logo-container">
                        <img src="../../assets/logo.png" alt="iSchool Logo" class="logo" />
                    </div>

                    <h2 class="register-title">Create an Account</h2>

                    <form class="registration-form">
                        <div class='form-group'>
                            <label for="username">Username</label>
                            <input type="text" id="username" required placeholder="Enter your username"
                                v-model="username" />
                        </div>

                        <div class='form-group'>
                            <label for="email">Email Address</label>
                            <input type="email" id="email" required placeholder="Enter your email" v-model="email" />
                        </div>

                        <div class='form-group'>
                            <label for="password">Password</label>
                            <input type="password" id="password" required placeholder="Create a strong password"
                                v-model="password" />
                        </div>

                        <div class='form-group'>
                            <label for="confirmPassword">Confirm Password</label>
                            <input type="password" id="confirmPassword" required placeholder="Confirm your password"
                                v-model="confirmPassword" />
                        </div>

                        <button type="button" @click="register" class="btn-register">Register</button>
                    </form>

                    <p class="login-link">
                        Already have an account? <a href="/login">Login</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'; 
export default {
    name: "Register",
    data() {
        return {
            username: "",
            email: "",
            password: "",
            confirmPassword: ""
        };
    },
    methods: {
        async register() {
            if (!this.username || !this.email || !this.password || !this.confirmPassword) {
                alert("Please fill in all the details: username, email, password, and confirm password.");
                return;
            }


            if (this.password !== this.confirmPassword) {
                alert("Passwords do not match. Please re-enter them.");
                return;
            }


            const reg_data = new FormData();
            reg_data.append("username", this.username)
            reg_data.append("email", this.email)
            reg_data.append("password", this.password)

            try {
                const response = await axios.post(`http://127.0.0.1:5000/register`, reg_data);
                alert(`you are registered bro ${response.data.message}`);
                this.$router.push(`/login`)

            } catch (error) {
                alert(`Error creating level! ${error.response.data.message}`);
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

.register-wrapper {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f4f4f4;
    font-family: 'Inter', sans-serif;
}

.register-container {
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
    background: url('../../assets/register.jpg') no-repeat center center;
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

.card-register {
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

.register-title {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem;
    font-size: 1.8rem;
    font-weight: 600;
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

.btn-register {
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

.btn-register:hover {
    background-color: #00cc77;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 204, 119, 0.4);
}

.login-link {
    text-align: center;
    margin-top: 1.5rem;
    color: #666;
}

.login-link a {
    color: #00ff88;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s ease;
}

.login-link a:hover {
    color: #00cc77;
}

@media screen and (max-width: 1024px) {
    .register-container {
        width: 95%;
        height: 95vh;
    }
}

@media screen and (max-width: 768px) {
    .register-container {
        flex-direction: column;
        height: 100vh;
        width: 100%;
        border-radius: 0;
    }

    .background-section {
        display: none;
    }

    .form-section {
        width: 100%;
        background-color: #f4f4f4;
    }

    .card-register {
        width: 90%;
        padding: 2rem;
        box-shadow: none;
    }
}

@media screen and (max-width: 480px) {
    .card-register {
        padding: 1.5rem;
    }

    .register-title {
        font-size: 1.5rem;
    }
}
</style>