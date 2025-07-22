<template>
    <div class="dashboard-page-wrapper">
        <!-- Navbar (Reused from Dashboard for consistency) -->
        <nav class="navbar">
            <h1>My Dashboard</h1>
            <div class="nav-links">
                <a href="/dashboard">Dashboard <i class="fas fa-tachometer-alt"></i></a>
                <a href="/search">Search <i class="fas fa-search"></i></a>
                <a href="/summary">Summary <i class="fas fa-chart-line"></i></a>
                <a href="/profile">Profile <i class="fas fa-user"></i></a>
                <a href="/login">Logout <i class="fas fa-sign-out-alt"></i></a>
            </div>
        </nav>

        <!-- Main Chapter Content -->
        <div class="dashboard-container">

            <!-- Section 1: Chapter Header and Details -->
            <section class="chapter-header-section">
                <a href="/dashboard" class="btn btn-back"><i class="fas fa-arrow-left"></i> Back to Dashboard</a>
                
                <div class="chapter-details-card">
                    <div class="chapter-details-icon">
                        <i class="fas fa-book-reader"></i>
                    </div>
                    <h2 class="chapter-title">{{ title }}</h2>
                    <p class="chapter-description">{{ discription }}</p>
                </div>
            </section>

            <!-- Section 2: Quizzes for this Chapter -->
            <section class="quizzes-section">
                <h2 class="section-title">Quizzes for this Chapter</h2>
                <div class="table-responsive-wrapper">
                    <table class="quiz-table">
                        <thead>
                            <tr>
                                <th>S. No.</th>
                                <th>Quiz Title</th>
                                <th>Description</th>
                                <th>Max Marks</th>
                                <th>Correct</th>
                                <th>Wrong</th>
                                <th>Date</th>
                                <th>Duration</th>
                                <th>Questions</th>
                                <th>Attempts</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr v-for="(quiz, index) in chapterQuizzes" :key="quiz[0]">
                                <td>{{ index + 1 }}</td>
                                <td>{{ quiz[1] }}</td>
                                <td>{{ quiz[2] }}</td>
                                <td>{{ quiz[3] }}</td>
                                <td>{{ quiz[4] }}</td>
                                <td>{{ quiz[5] }}</td>
                                <td>{{ quiz[6] }}</td>
                                <td>{{ quiz[7] }}</td>
                                <td>{{ quiz[8] }}</td>
                                <td>{{ quiz[9] }}</td>
                                <td class="action-buttons">
                                    <button class="btn btn-start-quiz" v-if="quiz[9] == 0" @click="startQuiz(quiz[0], quiz[9])"> 
                                        <i class="fas fa-play-circle"></i> Start Quiz</button>
                                    <button class="btn btn-reattempt-quiz" v-else
                                        @click="reattemptQuiz(quiz[0], quiz[9])"><i class="fas fa-redo"></i>Reattempt</button>
                                </td>

                            </tr>

                        </tbody>
                    </table>
                </div>
            </section>

        </div> <!-- End of dashboard-container -->

        <!-- Footer  -->
        <footer class="footer">
            <p>© 2025 Ischool. All Rights Reserved.</p>
        </footer>
    </div>
</template>

<script>
import axios from 'axios';
import vuecookies from 'vue-cookies';
export default {
    name: 'User_Chap_Page',
    data() {
        return {
            chapter_id: this.$route.params.chapter_id, 
            title: '',
            discription: '',
            chapterQuizzes: [], 
        };
    },
    methods:{
        async fetchbasicinfo(){
            try {
                const token = vuecookies.get('access_token');
                const response = await axios.get(`http://127.0.0.1:5000/chapter/chapter_det_with_quiz/${this.chapter_id}?token=${token}`);

                // const response = await axios.get('/api/chapter/basicinfo');
                const data = response.data.chapter_info;
                this.title = data[1]
                this.discription = data[2];
                this.chapterQuizzes = data[3];
                // this.title = response.data.chapter_info;
                // this.discription = response.data.description;
            } catch (error) {
                console.error('Error fetching chapter basic info:', error);
            }
        },
        startQuiz(quiz_id, attempt_number){
            this.$router.push(`/dashboard/attempt/${quiz_id}/attempt_=${attempt_number}`)
        },
        reattemptQuiz(quiz_id, attempt_number){
            this.$router.push(`/dashboard/attempt/${quiz_id}/attempt_=${attempt_number}`)
        }
    },
    mounted() {
        this.fetchbasicinfo();
    }
}
</script>

<style scoped>
/* --- IMPORTANT --- */
/* This CSS is copied directly from your DashboardPage.vue to ensure the design is identical. */
/* I have only added a few new styles for the chapter header section at the bottom. */

/* Navbar (Styles from your example, slightly adapted) */
.navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar h1 {
    font-size: 28px;
    font-weight: 700;
    color: #fff;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    margin: 0;
}

.nav-links {
    display: flex;
    gap: 25px;
}

.nav-links a {
    color: #e0e0e0;
    font-size: 15px;
    text-decoration: none;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 6px;
    transition: color 0.3s ease, background-color 0.3s ease, transform 0.2s ease;
}

.nav-links a:hover,
.nav-links a.router-link-active {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

.nav-links a i {
    margin-right: 5px;
}

/* Main Dashboard Wrapper & Container */
.dashboard-page-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
}

.dashboard-container {
    background-color: #ffffff;
    color: #333333;
    max-width: 1400px;
    margin: 30px auto;
    padding: 30px 40px;
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-in-out;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
    display: flex;
    align-items: center;
}

.section-title::before {
    content: '';
    display: inline-block;
    width: 5px;
    height: 24px;
    background-color: #3498db;
    margin-right: 10px;
    border-radius: 3px;
}

/* Quizzes Section (Identical to Dashboard) */
.quizzes-section {
    margin-top: 50px;
}

.table-responsive-wrapper {
    overflow-x: auto;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    padding: 10px;
}

.quiz-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 14px;
    color: #333;
}

.quiz-table th,
.quiz-table td {
    padding: 15px 12px;
    text-align: left;
    border-bottom: 1px solid #e8ebee;
    vertical-align: middle;
}

.quiz-table th {
    background-color: #f8f9fa;
    font-weight: 600;
    color: #555;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 0.5px;
}

.quiz-table thead th:first-child {
    border-top-left-radius: 8px;
}

.quiz-table thead th:last-child {
    border-top-right-radius: 8px;
}

.quiz-table tbody tr:hover {
    background-color: #f1f5f8;
}

.quiz-table tbody tr:last-child td {
    border-bottom: none;
}

.quiz-table td:nth-child(2) {
    font-weight: 500;
    color: #2c3e50;
}

.action-buttons {
    display: flex;
    gap: 8px;
    align-items: center;
}

.action-buttons .btn {
    padding: 6px 12px;
    font-size: 13px;
    border-radius: 5px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

/* General Button Styles (Identical to Dashboard) */
.btn {
    background: linear-gradient(to right, #ff6ec4, #0800ff);
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    font-size: 15px;
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
    box-shadow: 0 6px 15px rgba(128, 0, 128, 0.3);
}

.btn-start-quiz {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.btn-start-quiz:hover {
    box-shadow: 0 6px 15px rgba(39, 174, 96, 0.3);
}

.btn-reattempt-quiz {
    background: linear-gradient(135deg, #e67e22, #d35400);
}

.btn-reattempt-quiz:hover {
    box-shadow: 0 6px 15px rgba(230, 126, 34, 0.3);
}

/* Footer (Identical to Dashboard) */
.footer {
    margin-top: 40px;
    text-align: center;
    padding: 25px;
    background: #121212;
    color: #888;
    font-size: 14px;
    border-top: 1px solid #2a2a2a;
}

/* --- NEW STYLES FOR THIS PAGE --- */

.chapter-header-section {
    margin-bottom: 40px;
}

.btn-back {
    background: #6c757d; /* A neutral gray */
    color: white;
    margin-bottom: 25px;
    padding: 8px 16px;
    font-size: 14px;
}

.btn-back:hover {
    background: #5a6268;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.chapter-details-card {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border: 1px solid #dee2e6;
    border-radius: 10px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.chapter-details-icon {
    font-size: 40px;
    color: #3498db;
    margin-bottom: 15px;
}

.chapter-title {
    font-size: 28px;
    font-weight: 700;
    color: #34495e;
    margin-bottom: 10px;
}

.chapter-description {
    font-size: 16px;
    color: #7f8c8d;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto; /* Center the description text block */
}

/* Responsive adjustments (Identical to Dashboard) */
@media (max-width: 768px) {
    .dashboard-container {
        margin: 20px 15px;
        padding: 20px;
    }
    .navbar {
        padding: 15px 20px;
        flex-direction: column;
        gap: 10px;
    }
    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }
    .section-title {
        font-size: 20px;
    }
    .chapter-title {
        font-size: 24px;
    }
    .chapter-description {
        font-size: 15px;
    }
}
</style>