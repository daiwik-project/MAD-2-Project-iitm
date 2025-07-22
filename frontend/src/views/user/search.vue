<template>
    <div class="search-page-wrapper">
        <!-- Navbar -->
        <nav class="navbar">
            <h1>Search Quizzes & Content</h1>
            <div class="nav-links">
                <a href="/dashboard">Dashboard <i class="fas fa-tachometer-alt"></i></a>
                <a href="/summary">Summary <i class="fas fa-chart-line"></i></a>
                <a href="/profile">Profile <i class="fas fa-user"></i></a>
                <a href="/login">Logout <i class="fas fa-sign-out-alt"></i></a>
            </div>
        </nav>

        <!-- Main Search Content -->
        <div class="search-content-container">
            <div class="search-form-card card-animated">
                <form class="search-form-flex" @submit.prevent="performSearch(parameter, querry)">
                    <div class="form-group select-group">
                        <label for="searchParameter"><i class="fas fa-filter"></i> Search By:</label>
                        <select id="searchParameter" v-model="parameter">
                            <!-- FIX #2: Use the standard 'value' attribute for options -->
                            <option value="quiz_title">Quiz Title</option>
                            <option value="date">Date (YYYY-MM-DD)</option>
                            <option value="chapter_name">Chapter Name</option>
                            <option value="subject_name">Subject Name</option>
                            <option value="score">Your Score (e.g., >80)</option>
                        </select>
                    </div>
                    <div class="form-group query-group">
                        <label for="searchQuery"><i class="fas fa-keyboard"></i> Your Query:</label>
                        <input type="text" id="searchQuery" v-model="querry" placeholder="e.g., Introduction to Stoichiometry" required>
                    </div>
                    <button type="submit"   class="btn btn-primary btn-search-action">
                        <i class="fas fa-search"></i> Search
                    </button>
                </form>
            </div>

            <div class="search-results-area">
                <h2 class="section-title">Search Results</h2>

                <!-- The three states below would be shown conditionally. -->
                <!-- By default, the results table is shown. -->

                <!-- State 1: Loading Indicator (The fa-spin class provides the animation) -->
                
                <div v-if="isLoading" class="loading-indicator">
                    <i class="fas fa-spinner fa-spin"></i> Loading results...
                </div>
               

                <!-- State 2: Results Found (Displayed by default as a placeholder) -->
                <div v-else-if="result.length > 0" class="results-table-wrapper card-animated">
                    <table class="quiz-table">
                        <thead>
                            <tr>
                                <th>S. No.</th>
                                <th>Quiz Title</th>
                                <th>Chapter</th>
                                <th>Subject</th>
                                <th>Date</th>
                                <th>Max Marks</th>
                                <th>Your Score</th>
                                <th>Percentage</th>
                                <th>Attempt Number</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(r, index) in result" :key="index">
                                <td>{{ index + 1 }}</td>
                                <td>{{ r.quiz_title }}</td>
                                <td>{{ r.chapter_name }}</td>
                                <td>{{ r.subject_name }}</td>
                                <td>{{ r.date }}</td>
                                <td>{{ r.max_marks }}</td>
                                <td>{{ r.your_score }}</td>
                                <td>{{ r.percentage }}%</td>
                                <td>{{ r.attempt_number }}</td>
                                <td class="action-buttons">
                                    <button @click="gotoquiz_result(r.quiz_id, r.attempt_number)" class="btn btn-view-quiz">
                                        <i class="fas fa-eye"></i> View
                                    </button>
                                </td>
                            </tr>

                        </tbody>
                    </table>
                </div>

                <!-- State 3: No Results Found -->
                
                <div v-else class="no-results-found card-animated">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>No results found for your query.</p>
                    <p>Try different keywords or broaden your search criteria.</p>
                </div>
               

            </div>
        </div>

        <!-- Footer -->
        <footer class="footer">
            <p>© 2025 Ischool. All Rights Reserved.</p>
        </footer>
    </div>
</template>

<script>
import axios from 'axios';
import vuecookies from 'vue-cookies';

export default {
    name: 'Search',
    data() {
        return {
            parameter: 'quiz_title',
            querry: '',
            isLoading: false,
            result: [],
            loadingTimeout: null 

        };
    },
    methods: {
        async performSearch(value, querry) {
            this.isLoading = true;
            this.result = []; 
            const searchdata = new FormData;
            searchdata.append("parameter", value)
            searchdata.append("querry", querry)

            try {
                const token = vuecookies.get('access_token')
                const req = await axios.post(`http://127.0.0.1:5000/u/search?token=${token}`, searchdata)
                this.result = req.data.search_result
                console.log(this.result)

            } catch (error) {
                console.log(error)
            } finally {
                this.isLoading = false;
            }
        },
        gotoquiz_result(quiz_id, attempt_number) {
            this.$router.push(`/dashboard/summary/${quiz_id}/attempt_=${attempt_number}`)
        },

    },
    mounted(){
    }
}
</script>

<style scoped>
/* Navbar and Footer styles (Same as DashboardPage.vue) */
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
    color: #fff;
}

.navbar h1 {
    font-size: 28px;
    font-weight: 700;
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

.footer {
    margin-top: 40px;
    text-align: center;
    padding: 25px;
    background: #121212;
    color: #888;
    font-size: 14px;
    border-top: 1px solid #2a2a2a;
}

/* Search Page Specific Styles */
.search-page-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    padding-bottom: 1px;
}

.search-content-container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 0 20px;
}

.card-animated {
    /* Reusable animation class */
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    padding: 30px;
    margin-bottom: 30px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-animated:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.search-form-card {
    margin-bottom: 30px;
}

.search-form-flex {
    display: flex;
    align-items: flex-end;
    /* Align items to bottom for label consistency */
    gap: 20px;
    flex-wrap: wrap;
    /* Allow wrapping on smaller screens */
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    font-weight: 500;
    margin-bottom: 8px;
    color: #495057;
    font-size: 14px;
    display: flex;
    align-items: center;
}

.form-group label i {
    margin-right: 8px;
    color: #3498db;
}

.form-group select,
.form-group input[type="text"] {
    padding: 12px 15px;
    border: 1px solid #ced4da;
    border-radius: 6px;
    font-size: 15px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    height: 46px;
    /* Consistent height */
}

.form-group select {
    min-width: 200px;
    /* Ensure select is not too small */
}

.form-group.query-group {
    flex-grow: 1;
    /* Allow query input to take remaining space */
}

.form-group input[type="text"] {
    width: 100%;
}

.form-group select:focus,
.form-group input[type="text"]:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    outline: none;
}

.btn-search-action {
    padding: 12px 25px;
    height: 46px;
    /* Match input height */
    align-self: flex-end;
    /* Align with bottom of inputs */
}

.search-results-area .section-title {
    font-size: 22px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}

.loading-indicator,
.no-results-found,
.search-prompt {
    text-align: center;
    padding: 40px 20px;
    font-size: 18px;
    color: #555;
}

.loading-indicator i,
.no-results-found i,
.search-prompt i {
    font-size: 40px;
    color: #3498db;
    margin-bottom: 15px;
    display: block;
}

.no-results-found p,
.search-prompt p {
    margin-bottom: 5px;
    line-height: 1.6;
}

.no-results-found p:last-child,
.search-prompt p:last-child {
    font-size: 15px;
    color: #7f8c8d;
}


/* Table styles (similar to DashboardPage.vue quiz-table) */
.results-table-wrapper {
    overflow-x: auto;
    padding: 10px;
    /* Reduced padding as card already has padding */
}

.quiz-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 14px;
}

.quiz-table th,
.quiz-table td {
    padding: 14px 12px;
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

.quiz-table tbody tr:last-child td:first-child {
    border-bottom-left-radius: 8px;
}

.quiz-table tbody tr:last-child td:last-child {
    border-bottom-right-radius: 8px;
}

.quiz-table td {
    color: #555;
}

.quiz-table td:nth-child(2) {
    font-weight: 500;
    color: #2c3e50;
}

/* Quiz Title */

.action-buttons {
    display: flex;
    gap: 8px;
}

.btn-view-quiz {
    background: linear-gradient(135deg, #5dade2, #2e86c1);
    color: white;
    padding: 6px 12px;
    font-size: 13px;
    border-radius: 5px;
}

.btn-view-quiz:hover {
    background: linear-gradient(135deg, #2e86c1, #2874a6);
    transform: scale(1.05);
}

/* General Button Styles (Copied for consistency) */
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

.btn-primary {
    background: linear-gradient(to right, #3665ff, #2548cc);
}

.btn-primary:hover {
    box-shadow: 0 6px 15px rgba(54, 101, 255, 0.4);
}

/* Responsive adjustments */
@media (max-width: 768px) {
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

    .search-content-container {
        margin: 20px auto;
        padding: 0 15px;
    }

    .search-form-flex {
        flex-direction: column;
        align-items: stretch;
    }

    .form-group select,
    .form-group input[type="text"],
    .btn-search-action {
        width: 100%;
    }

    .form-group.select-group {
        min-width: auto;
    }

    .btn-search-action {
        margin-top: 10px;
    }

    .card-animated,
    .search-form-card {
        padding: 20px;
    }
}

@media (max-width: 576px) {
    .navbar h1 {
        font-size: 22px;
    }

    .form-group select,
    .form-group input[type="text"] {
        font-size: 14px;
        padding: 10px 12px;
        height: 42px;
    }

    .btn-search-action {
        height: 42px;
        font-size: 14px;
    }

    .quiz-table th,
    .quiz-table td {
        padding: 10px 8px;
        font-size: 13px;
    }
}
</style>