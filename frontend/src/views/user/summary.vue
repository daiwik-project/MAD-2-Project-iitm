<template>
    <div class="summary-page-wrapper">
        <!-- Navbar -->
        <nav class="navbar">
            <h1>Performance Summary</h1>
            <div class="nav-links">
                <a href="/dashboard">Dashboard <i class="fas fa-tachometer-alt"></i></a>
                <a href="/search">Search <i class="fas fa-search"></i></a>
                <a href="/profile">Profile <i class="fas fa-user"></i></a>
                <a href="/">Logout <i class="fas fa-sign-out-alt"></i></a>
            </div>
        </nav>

        <!-- Main Summary Content -->
        <div class="summary-content-container">
            <!-- Top Stats Cards -->
            <div class="stats-overview-grid">
                <div class="stat-card card-animated">
                    <div class="stat-icon-wrapper" style="background-color: rgba(52, 152, 219, 0.1);"><i
                            class="fas fa-list-check" style="color: #3498db;"></i></div>
                    <div class="stat-content">
                        <p class="stat-value">{{ summary.total_quiz_attempts }}</p>
                        <p class="stat-label">Total Unique Quiz Attempts</p>
                    </div>
                </div>
                <div class="stat-card card-animated">
                    <div class="stat-icon-wrapper" style="background-color: rgba(46, 204, 113, 0.1);"><i
                            class="fas fa-bullseye" style="color: #2ecc71;"></i></div>
                    <div class="stat-content">
                        <p class="stat-value">{{ summary.avg_percentage }}%</p>
                        <p class="stat-label">Overall Average Score</p>
                    </div>
                </div>

            </div>


            <!-- Charts Grid -->
            <h2 class="section-title main-charts-title"><i class="fas fa-chart-area"></i> Detailed Analytics</h2>
            <div class="charts-grid">
                <div class="chart-container card-animated">
                    <h3 class="chart-header"><i class="fas fa-pie-chart"></i> Subject-Wise Quiz Attempts</h3>
                    <canvas id="subjectWiseAttemptsChart"></canvas>

                    <!-- <div class="chart-placeholder">Chart: Subject-Wise Attempts</div> -->
                </div>
                <div class="chart-container card-animated">
                    <h3 class="chart-header"><i class="fas fa-percentage"></i> Highest Score Quiz-Wise (%)</h3>
                    <canvas id="highestScoreQuizwiseChart"></canvas>

                    <!-- <div class="chart-placeholder">Chart: Highest Scores</div> -->
                </div>
                <div class="chart-container card-animated">
                    <h3 class="chart-header"><i class="fas fa-chart-line"></i> Month-Wise Quiz Attempts</h3>
                    <canvas id="monthWiseAttemptsChart"></canvas>

                    <!-- <div class="chart-placeholder">Chart: Monthly Attempts</div> -->
                </div>
                <div class="chart-container card-animated">
                    <h3 class="chart-header"><i class="fas fa-graduation-cap"></i> Average Score per Subject (%)</h3>
                    <canvas id="averageScoreChart"></canvas>

                    <!-- <div class="chart-placeholder">Chart: Avg Score/Subject</div> -->
                </div>
                <div class="chart-container card-animated">
                    <h3 class="chart-header"><i class="fas fa-book-open"></i> Quizzes Attempted Chapter-Wise</h3>
                    <canvas id="quizzesAttemptedChart"></canvas>

                    <!-- <div class="chart-placeholder">Chart: Chapter Attempts</div> -->
                </div>
                <div class="chart-container card-animated">
                    <h3 class="chart-header"><i class="fas fa-trophy"></i> Best Score in Each Subject (%)</h3>
                    <canvas id="bestScoresubjectwiseChart"></canvas>

                    <!-- <div class="chart-placeholder">Chart: Best Score/Subject</div> -->
                </div>
                <div class="chart-container card-animated">
                    <h3 class="chart-header"><i class="fas fa-trophy"></i> Number of Attempts per Quiz</h3>
                    <canvas id="attemptsPerQuizChart"></canvas>

                    <!-- <div class="chart-placeholder">Chart: Best Score/Subject</div> -->
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
    name: 'SummaryPage',
    data() {
        return {
            summary: {}
        }
    },
    methods: {
        async initfunction() {
            try {
                const token = vuecookies.get('access_token');
                const req = await axios.get(`http://127.0.0.1:5000/u_summary_page?token=${token}`)
                this.summary = req.data.summary
            } catch (err) {
                console.log(err);
            }
        },
        async graphfunct() {
            // --- Chart 1: Subject-Wise Quiz Attempts ---
            const subjectWiseAttemptsData = this.summary.subject_wise_quiz_attempts;
            const subjectWiseAttemptsLabels = Object.keys(subjectWiseAttemptsData);
            const subjectWiseAttemptsValues = Object.values(subjectWiseAttemptsData);

            new Chart(document.getElementById('subjectWiseAttemptsChart').getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: subjectWiseAttemptsLabels,
                    datasets: [{
                        data: subjectWiseAttemptsValues,
                        backgroundColor: ['#ff6f61', '#3b82f6', '#34d399', '#fbbf24', '#9932cc', '#65000b', '#fa8072', '#556b2f'],
                        borderColor: ['#ff5733', '#0081c9', '#28a745', '#f59e0b', '#800080', '#8b0000', '#e9967a', '#6b8e23'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: "#000" } }
                    }
                }
            });

            // --- Chart 2: Highest Score Quiz-Wise ---
            const highestScoreData = this.summary.highest_score_quiz_wise;
            const highestScoreLabels = Object.keys(highestScoreData);
            const highestScoreValues = Object.values(highestScoreData);

            new Chart(document.getElementById('highestScoreQuizwiseChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: highestScoreLabels,
                    datasets: [{
                        label: 'Highest Score (%)',
                        data: highestScoreValues,
                        backgroundColor: '#4e54c8',
                        borderColor: '#8f94fb',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, ticks: { color: '#000' } },
                        x: { ticks: { color: '#000' } }
                    },
                    plugins: {
                        legend: { labels: { color: "#000" } }
                    }
                }
            });

            // --- Chart 3: Month-Wise Quiz Attempts ---
            const monthWiseAttemptsData = this.summary.month_wise_quiz_attempts;
            const monthWiseAttemptsLabels = Object.keys(monthWiseAttemptsData).sort(); // Sort months chronologically
            const monthWiseAttemptsValues = monthWiseAttemptsLabels.map(label => monthWiseAttemptsData[label]);

            new Chart(document.getElementById('monthWiseAttemptsChart').getContext('2d'), {
                type: 'line',
                data: {
                    labels: monthWiseAttemptsLabels,
                    datasets: [{
                        label: 'Quiz Attempts',
                        data: monthWiseAttemptsValues,
                        borderColor: '#b3e5fc',
                        backgroundColor: 'rgba(179, 229, 252, 0.2)',
                        borderWidth: 2,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, ticks: { color: '#000' } },
                        x: { ticks: { color: '#000' } }
                    },
                    plugins: {
                        legend: { labels: { color: "#000" } }
                    }
                }
            });

            // --- Chart 4: Average Score per Subject ---
            const averageScoreData = this.summary.average_score_per_subject;
            const averageScoreLabels = Object.keys(averageScoreData);
            const averageScoreValues = Object.values(averageScoreData);

            new Chart(document.getElementById('averageScoreChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: averageScoreLabels,
                    datasets: [{
                        label: 'Average Score (%)',
                        data: averageScoreValues,
                        backgroundColor: '#2ecc71',
                        borderColor: '#58d68d',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, ticks: { color: '#000' } },
                        x: { ticks: { color: '#000' } }
                    },
                    plugins: {
                        legend: { labels: { color: "#000" } }
                    }
                }
            });

            // --- Chart 5: Quizzes Attempted Chapter-Wise ---
            const quizzesAttemptedData = this.summary.quizzes_attempted_per_chapter;
            const quizzesAttemptedLabels = Object.keys(quizzesAttemptedData);
            const quizzesAttemptedValues = Object.values(quizzesAttemptedData);

            new Chart(document.getElementById('quizzesAttemptedChart').getContext('2d'), {
                type: 'pie',
                data: {
                    labels: quizzesAttemptedLabels,
                    datasets: [{
                        data: quizzesAttemptedValues,
                        backgroundColor: ['#ff6f61', '#3b82f6', '#34d399', '#fbbf24', '#9932cc', '#65000b', '#fa8072', '#556b2f'],
                        borderColor: ['#ff5733', '#0081c9', '#28a745', '#f59e0b', '#800080', '#8b0000', '#e9967a', '#6b8e23'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: "#000" } }
                    }
                }
            });

            // --- Chart 6: Best Score in Each Subject ---
            const bestScoreData = this.summary.best_score_in_each_subject;
            const bestScoreLabels = Object.keys(bestScoreData);
            const bestScoreValues = Object.values(bestScoreData);

            new Chart(document.getElementById('bestScoresubjectwiseChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: bestScoreLabels,
                    datasets: [{
                        label: 'Best Score (%)',
                        data: bestScoreValues,
                        backgroundColor: '#f1c40f',
                        borderColor: '#f39c12',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, ticks: { color: '#000' } },
                        x: { ticks: { color: '#000' } }
                    },
                    plugins: {
                        legend: { labels: { color: "#000" } }
                    }
                }
            });

            // --- Chart 7: Number of Attempts per Quiz ---
            const attemptsPerQuizData = this.summary.number_of_attempts_per_quiz;
            const attemptsPerQuizLabels = Object.keys(attemptsPerQuizData);
            const attemptsPerQuizValues = Object.values(attemptsPerQuizData);

            new Chart(document.getElementById('attemptsPerQuizChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: attemptsPerQuizLabels,
                    datasets: [{
                        label: 'Number of Attempts',
                        data: attemptsPerQuizValues,
                        backgroundColor: '#e74c3c',
                        borderColor: '#c0392b',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, ticks: { color: '#000' } },
                        x: { ticks: { color: '#000' } }
                    },
                    plugins: {
                        legend: { labels: { color: "#000" } }
                    }
                }
            });




        }
    },
    async mounted() {
        await this.initfunction();
        await this.graphfunct();

    }
}

</script>

<style scoped>
/* Navbar and Footer styles */
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

.nav-links a:hover {
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

/* Summary Page Specific Styles */
.summary-page-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    padding-bottom: 1px;
}

.summary-content-container {
    max-width: 1300px;
    margin: 30px auto;
    padding: 0 20px;
}

.card-animated {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-animated:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

/* Stats Overview Grid */
.stats-overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 25px;
    margin-bottom: 30px;
}

.stat-card {
    padding: 25px;
    display: flex;
    align-items: center;
}

.stat-icon-wrapper {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20px;
    flex-shrink: 0;
}

.stat-icon-wrapper i {
    font-size: 26px;
}

.stat-content .stat-value {
    font-size: 26px;
    font-weight: 700;
    color: #2c3e50;
    margin: 0 0 5px 0;
    line-height: 1.2;
}

.stat-content .stat-label {
    font-size: 14px;
    color: #7f8c8d;
    margin: 0;
}

/* Report Download Section */
.report-download-section {
    padding: 30px;
    margin-bottom: 40px;
    text-align: center;
}

.section-title-alt {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.section-title-alt i {
    margin-right: 10px;
    color: #3498db;
}

.report-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}

.report-buttons .btn {
    min-width: 280px;
}

/* Charts Grid */
.main-charts-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
    display: flex;
    align-items: center;
}

.main-charts-title i {
    margin-right: 12px;
    color: #3498db;
}

.charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
}

.chart-container {
    padding: 25px;
    min-height: 350px;
    display: flex;
    flex-direction: column;
}

.chart-header {
    font-size: 17px;
    font-weight: 600;
    color: #34495e;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    align-items: center;
}

.chart-header i {
    margin-right: 10px;
    color: #5dade2;
}

.chart-placeholder {
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f8f9fa;
    border-radius: 8px;
    color: #adb5bd;
    font-style: italic;
    font-size: 16px;
    text-align: center;
    padding: 20px;
}

/* General Button Styles */
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

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background: #5a6268;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* Responsive adjustments */
@media (max-width: 992px) {
    .charts-grid {
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    }
}

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

    .summary-content-container {
        margin: 20px auto;
        padding: 0 15px;
    }

    .stats-overview-grid {
        grid-template-columns: 1fr;
    }

    .stat-card {
        flex-direction: column;
        text-align: center;
    }

    .stat-icon-wrapper {
        margin-right: 0;
        margin-bottom: 15px;
    }

    .report-buttons .btn {
        min-width: 100%;
        margin-bottom: 10px;
    }

    .report-buttons .btn:last-child {
        margin-bottom: 0;
    }

    .charts-grid {
        grid-template-columns: 1fr;
    }

    .card-animated,
    .report-download-section,
    .chart-container {
        padding: 20px;
    }
}

@media (max-width: 576px) {
    .navbar h1 {
        font-size: 22px;
    }

    .stat-content .stat-value {
        font-size: 22px;
    }

    .stat-content .stat-label {
        font-size: 13px;
    }

    .chart-header {
        font-size: 16px;
    }
}
</style>