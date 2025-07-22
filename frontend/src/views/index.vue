<template>
    <div class="landing-page-wrapper">
        <!-- 1. Abstract Animated Shapes in the Background -->
        <div class="shape-container">
            <div class="shape shape-1"></div>
            <div class="shape shape-2"></div>
            <div class="shape shape-3"></div>
        </div>

        <!-- 2. Clean Header -->
        <header class="header">
            <img src="../assets/logo.png" alt="iSchool Logo" class="logo" />
            <div class="header-buttons">
                <span>For Teachers Only</span>
                <a href="/admindashboard" class="btn-admin">
                    <i class="fas fa-arrow-right-to-bracket"></i> Admin Dashboard
                </a>
            </div>
        </header>

        <!-- 3. Main Content Grid -->
        <main class="main-grid">
            <!-- Left Side: The Big, Bold Text -->
            <div class="hero-text-section">
                <h1 class="hero-title-main">ONLINE</h1>
                <p class="hero-title-sub">EXAMINATION</p>
            </div>

            <!-- Right Side: The Glassmorphism Login Card -->
            <div class="login-card-section">
                <div class="glass-card">
                    <h2>Welcome to iSchool</h2>
                    <h3>Start success with iSchool Tests and Quizes</h3>
                    <div class="cta-buttons">
                        <a href="/login" class="btn btn-login">Login</a>
                        <a href="/register" class="btn btn-register">Register</a>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import axios from 'axios';
import VueCookies from 'vue-cookies'; 
export default {
    name: 'home',
    data() {
        return {
        };
    },
    methods: {
        root(){
            axios.get('http://127.0.0.1:5000/')
        }
    },
    mounted() {
        if (VueCookies.get('admin_token')) {
            // 3. If it exists, remove it
            VueCookies.remove('admin_token');
            console.log('Access token found and removed on home page. User has been logged out.');
        }

        this.root();
    },
};
</script>

<style scoped>


/* 1. Foundational Setup & Page Wrapper */
.landing-page-wrapper {
    height: 100vh;
    width: 100%;
    background-color: #ffffff;
    font-family: 'Poppins', sans-serif;
    color: #1e2125;
    overflow: hidden; /* Prevents scrollbars from shapes */
    position: relative;
    display: flex;
    flex-direction: column;
}

/* 2. Static Background Shapes (Animation Removed) */
.shape-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
}

.shape {
    position: absolute;
    background: linear-gradient(45deg, #eef2ff, #dbe4ff);
    border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; /* Creates organic blob shapes */
    opacity: 0.7;
    /* The 'animation' property was removed from here to make the shapes static */
}

.shape-1 {
    width: 500px;
    height: 500px;
    top: -150px;
    right: -150px;
}

.shape-2 {
    width: 600px;
    height: 600px;
    bottom: -200px;
    left: -250px;
}

.shape-3 {
    width: 350px;
    height: 350px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* The @keyframes 'float' animation block has been removed */


/* 3. Header Styling */
.header {
    padding: 20px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
    flex-shrink: 0;
}

.logo {
    height: 40px;
}

.header-buttons {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.header-buttons span {
    font-size: 0.9rem;
    color: #555;
}

.btn-admin {
    background-color: #343a40;
    color: #fff;
    text-decoration: none;
    padding: 10px 22px;
    border-radius: 50px; /* Pill shape */
    font-weight: 600;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.btn-admin:hover {
    transform: translateY(-2px);
    background-color: #000;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

/* 4. Main Content Grid Layout */
.main-grid {
    flex-grow: 1;
    display: grid;
    grid-template-columns: 45% 55%;
    align-items: center;
    padding: 0 5%;
    z-index: 5;
}

/* 5. Hero Text Section (Left) */
.hero-text-section {
    padding-right: 2rem;
}

.hero-title-main {
    font-size: 7rem;
    font-weight: 800;
    line-height: 1;
    margin: 0;
    color: #2c3e50;
}

.hero-title-sub {
    font-size: 3rem;
    font-weight: 600;
    letter-spacing: 12px; /* The wide tracking effect */
    margin: 0;
    color: #34495e;
}

/* 6. Glassmorphism Card (Right) */
.login-card-section {
    display: flex;
    justify-content: center;
    align-items: center;
}

.glass-card {
    width: 100%;
    max-width: 500px;
    padding: 3rem;
    text-align: center;
    /* The Glassmorphism Effect */
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    /* Entrance Animation */
    opacity: 0;
    transform: translateY(20px);
    animation: card-fade-in 1s 0.5s ease-out forwards;
}

@keyframes card-fade-in {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.glass-card h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    /* The orange/red gradient from the image */
    background: linear-gradient(45deg, #FF8C42, #FF5C5C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.glass-card h3 {
    font-size: 1.1rem;
    font-weight: 400;
    margin: 0 0 2.5rem 0;
    color: #583D72; /* The dark purple from the image */
}

/* 7. Call to Action Buttons */
.cta-buttons {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
}

.btn {
    flex-grow: 1;
    padding: 14px 20px;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    color: #fff;
    border: none;
    border-radius: 50px; /* Pill shape */
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 20px -5px rgba(0, 0, 0, 0.3);
}

.btn:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.4);
}

.btn-login {
    background: linear-gradient(45deg, #0052D4, #4364F7, #6FB1FC);
}

.btn-register {
    background: linear-gradient(45deg, #9D50BB, #D250BB, #FE50BB);
}

/* 8. Responsive Design */
@media (max-width: 1024px) {
    .main-grid {
        grid-template-columns: 1fr; /* Stack the columns */
        text-align: center;
        padding-top: 2rem;
    }
    .hero-text-section {
        padding-right: 0;
        margin-bottom: 3rem;
    }
    .hero-title-main { font-size: 5rem; }
    .hero-title-sub { font-size: 2rem; letter-spacing: 8px; }
    .glass-card { padding: 2rem; }
}

@media (max-width: 768px) {
    .header { flex-direction: column; gap: 1rem; }
    .hero-title-main { font-size: 3.5rem; }
    .hero-title-sub { font-size: 1.2rem; letter-spacing: 6px; }
    .glass-card h2 { font-size: 2rem; }
    .glass-card h3 { font-size: 1rem; }
    .cta-buttons { flex-direction: column; gap: 1rem; }
}
</style>