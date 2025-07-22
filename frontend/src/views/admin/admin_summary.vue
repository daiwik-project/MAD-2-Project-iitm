<template>
    <div class="admin-summary-wrapper">
        <!-- Navbar -->
        <nav class="navbar navbar-expand-lg">
            <div class="container-fluid">
                <a class="navbar-brand" href="/admindashboard">Admin Panel</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#adminNavbarNav" aria-controls="adminNavbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <i class="fas fa-bars"></i>
                </button>
                <div class="collapse navbar-collapse" id="adminNavbarNav">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link" href="/admindashboard"><i class="fas fa-book"></i> Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/a/summary"><i class="fas fa-chart-line"></i> Summary</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/a/search"><i class="fas fa-question-circle"></i> Search</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/user-control"><i class="fas fa-users-cog"></i> User control</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/"><i class="fas fa-sign-out-alt"></i> Logout</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="dashboard-container">
            <h2 class="section-title">Dashboard Summary</h2>

            <!-- Summary Cards -->
            <div class="summary-cards-grid">
                <div class="summary-card">
                    <div class="card-icon-wrapper" style="background-color: rgba(52, 152, 219, 0.1); color: #3498db;">
                        <i class="fas fa-layer-group"></i>
                    </div>
                    <div class="card-content">
                        <h3 class="card-title">Total Levels</h3>
                        <p class="card-value">{{ summary?.total_levels || 0 }}</p>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-icon-wrapper" style="background-color: rgba(46, 204, 113, 0.1); color: #2ecc71;">
                        <i class="fas fa-user-graduate"></i>
                    </div>
                    <div class="card-content">
                        <h3 class="card-title">Most Active Student</h3>
                        <div v-if="summary?.student_with_most_attempts?.student_name">
                            <p class="card-value">{{ summary.student_with_most_attempts.student_name }}</p>
                            <p class="card-subtitle">{{ summary.student_with_most_attempts.total_attempts }} attempts</p>
                        </div>
                        <div v-else>
                            <p class="card-value">N/A</p>
                        </div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-icon-wrapper" style="background-color: rgba(241, 196, 15, 0.1); color: #f1c40f;">
                        <i class="fas fa-trophy"></i>
                    </div>
                    <div class="card-content">
                        <h3 class="card-title">Top Scorer</h3>
                        <div v-if="topScorer">
                            <p class="card-value">{{ topScorer.student_name }}</p>
                            <p class="card-subtitle">Score: {{ topScorer.score }}</p>
                        </div>
                        <div v-else>
                            <p class="card-value">N/A</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Chart Grid -->
            <div v-if="!loading && summary" class="charts-grid">
                <div class="chart-card">
                    <h5>Subjects per Level</h5>
                    <div class="chart-wrapper">
                        <canvas id="levelSubjectsChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h5>Quizzes per Subject</h5>
                    <div class="chart-wrapper">
                        <canvas id="subjectQuizzesChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h5>Quiz Max Attempts</h5>
                    <div class="chart-wrapper">
                        <canvas id="quizAttemptsChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h5>Quiz Top Scores</h5>
                    <div class="chart-wrapper">
                        <canvas id="quizScoresChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h5>Level Top Scores</h5>
                    <div class="chart-wrapper">
                        <canvas id="levelScoresDoughnutChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h5>Student Attempts</h5>
                    <div class="chart-wrapper">
                        <canvas id="studentAttemptsPieChart"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- Loading and Error States -->
            <div v-if="loading" class="loading-state">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>Loading Summary Data...</p>
            </div>
            <div v-if="error" class="alert alert-danger mt-5">
                {{ error }}
            </div>
        </div>

        <!-- Footer -->
        <footer class="footer">
            <p>© 2025 Ischool Admin. All Rights Reserved.</p>
        </footer>
    </div>
</template>


<script>
import axios from 'axios';


export default {
    name: 'AdminSummary',
    data() {
        return {
            summary: null,
            loading: true,
            error: null,
            charts: {}
        };
    },

    methods: {
        async fetchAndRenderCharts() {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get('http://127.0.0.1:5000/admin_dashboard/summary');
                this.summary = response.data;

                this.$nextTick(() => {
                    this.createAllCharts();
                });

            } catch (err) {
                console.error('Failed to fetch summary data:', err);
                this.error = 'Could not load summary data. Please try again later.';
            } finally {
                this.loading = false;
            }
        },

        createAllCharts() {
            if (!this.summary) return;

            // 1. Pie Chart: Subjects per Level
            this.createPieChart('levelSubjectsChart', 'Subjects', this.summary.subjects_per_level);

            // 2. Doughnut Chart: Quizzes per Subject
            this.createDoughnutChart('subjectQuizzesChart', 'Quizzes', this.summary.quizzes_per_subject);

            // 3. Bar Chart: Quiz max attempts
            this.createBarChart('quizAttemptsChart', 'Max Attempts', this.summary.quiz_max_attempts);

            // 4. Bar Chart: Quiz scores
            const quizScores = {};
            for (const quiz in this.summary.quiz_wise_top_scorer) {
                quizScores[quiz] = this.summary.quiz_wise_top_scorer[quiz].score;
            }
            this.createBarChart('quizScoresChart', 'Top Score', quizScores);

            // 5. Doughnut Chart: Level scores distribution
            const levelScores = {};
            for (const level in this.summary.level_top_scorer) {
                levelScores[level] = this.summary.level_top_scorer[level].score;
            }
            this.createDoughnutChart('levelScoresDoughnutChart', 'Top Score', levelScores);

            // 6. Pie Chart: Student attempts distribution
            this.createPieChart('studentAttemptsPieChart', 'Attempts', this.studentAttemptData);
        },

        createChart(chartId, type, label, dataObject, backgroundColor, borderColor) {
            if (this.charts[chartId]) {
                this.charts[chartId].destroy();
            }

            const ctx = document.getElementById(chartId);
            if (!ctx) return;

            const labels = Object.keys(dataObject);
            const data = Object.values(dataObject);

            this.charts[chartId] = new Chart(ctx, {
                type: type,
                data: {
                    labels: labels,
                    datasets: [{
                        label: label,
                        data: data,
                        backgroundColor: backgroundColor,
                        borderColor: borderColor,
                        borderWidth: 1.5,
                        hoverOffset: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: type === 'pie' || type === 'doughnut' ? 'right' : 'top',
                        },
                        tooltip: {
                            backgroundColor: '#333',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            callbacks: {
                                label: function (context) {
                                    return `${context.label}: ${context.raw}`;
                                }
                            }
                        }
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    },
                    // For bar charts
                    scales: type === 'bar' ? {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    } : undefined
                }
            });
        },

        createPieChart(id, label, data) {
            const colors = this.generateColors(Object.keys(data).length, 'pastel');
            this.createChart(id, 'pie', label, data, colors, '#ffffff');
        },

        createDoughnutChart(id, label, data) {
            const colors = this.generateColors(Object.keys(data).length, 'vibrant');
            this.createChart(id, 'doughnut', label, data, colors, '#ffffff');
        },

        createBarChart(id, label, data) {
            const colors = this.generateColors(Object.keys(data).length, 'distinct');
            this.createChart(id, 'bar', label, data, colors, colors.map(c => this.adjustColor(c, -20)));
        },

        generateColors(count, palette = 'default') {
            const palettes = {
                default: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'],
                pastel: ['#a3bffa', '#81e6d9', '#fde68a', '#fecaca', '#d8b4fe', '#fbcfe8'],
                vibrant: ['#6366f1', '#06b6d4', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6'],
                distinct: ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            };

            const selected = palettes[palette] || palettes.default;
            return Array(count).fill().map((_, i) => selected[i % selected.length]);
        },

        adjustColor(hex, percent) {
            // Adjust color brightness
            let R = parseInt(hex.substring(1, 3), 16);
            let G = parseInt(hex.substring(3, 5), 16);
            let B = parseInt(hex.substring(5, 7), 16);

            R = Math.min(255, Math.max(0, R + R * percent / 100));
            G = Math.min(255, Math.max(0, G + G * percent / 100));
            B = Math.min(255, Math.max(0, B + B * percent / 100));

            return `#${this.toHex(R)}${this.toHex(G)}${this.toHex(B)}`;
        },

        toHex(value) {
            value = Math.round(value);
            const hex = value.toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        }
    },
    async mounted() {
        await this.fetchAndRenderCharts();
    },














    beforeUnmount() {
        for (const chartId in this.charts) {
            if (this.charts[chartId]) {
                this.charts[chartId].destroy();
            }
        }
    },
    computed: {
        topScorer() {
            if (!this.summary || !this.summary.level_top_scorer) return null;

            // Find the highest score across all levels
            let highestScore = 0;
            let topScorer = null;

            for (const level in this.summary.level_top_scorer) {
                const scorer = this.summary.level_top_scorer[level];
                if (scorer.score > highestScore) {
                    highestScore = scorer.score;
                    topScorer = scorer;
                }
            }

            return topScorer;
        },
        studentAttemptData() {
            if (!this.summary || !this.summary.student_with_most_attempts) return {};

            // Create data for pie chart showing top students
            const topStudents = {};

            // Add the top student
            topStudents[this.summary.student_with_most_attempts.student_name] =
                this.summary.student_with_most_attempts.total_attempts;

            // Add "Others" category if needed
            // You could expand this to show more students if needed
            if (Object.keys(this.summary.quiz_wise_top_scorer).length > 1) {
                topStudents['Other Students'] =
                    Object.values(this.summary.quiz_wise_top_scorer)
                        .filter(s => s.student_name !== this.summary.student_with_most_attempts.student_name)
                        .reduce((total, student) => total + (student.score > 0 ? 1 : 0), 0);
            }

            return topStudents;
        }
    },
};
</script>

<style scoped>
/* General Page Wrapper */
.admin-summary-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- NAVBAR STYLING (Consistent with other pages) --- */
.navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 25px;
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}
.navbar-brand {
    font-size: 26px;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}
.navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.navbar-toggler:focus {
    box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}
.navbar-nav .nav-link {
    color: #e0e0e0;
    font-size: 15px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    margin: 0 5px;
    border-radius: 6px;
    transition: color 0.3s ease, background-color 0.3s ease, transform 0.2s ease;
}
.navbar-nav .nav-link:hover,
.navbar-nav .nav-link.active {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}
@media (max-width: 991.98px) {
    .navbar-nav .nav-link:hover,
    .navbar-nav .nav-link.active {
        transform: none;
    }
    .navbar-collapse {
        padding-top: 15px;
    }
}

/* --- MAIN CONTENT STYLING --- */
.dashboard-container {
    max-width: 1400px;
    margin: 30px auto;
    padding: 0 20px;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}

/* Summary Cards Grid */
.summary-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 25px;
    margin-bottom: 40px;
}

.summary-card {
    background: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    display: flex;
    align-items: center;
    gap: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.summary-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.card-icon-wrapper {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
}

.card-content {
    line-height: 1.3;
}

.card-title {
    font-size: 14px;
    color: #7f8c8d;
    margin-bottom: 5px;
    font-weight: 500;
}

.card-value {
    font-size: 22px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.card-subtitle {
    font-size: 14px;
    color: #555;
    margin: 0;
}

/* --- CHART STYLING (THE FIX IS HERE) --- */
.charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
}

.chart-card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
}

.chart-card h5 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #34495e;
    font-weight: 600;
    flex-shrink: 0; /* Prevent title from shrinking */
}

/* This wrapper is the key to fixing the chart distortion */
.chart-wrapper {
    position: relative;
    flex-grow: 1; /* Allows the wrapper to fill the available space */
    min-height: 250px; /* Give it a minimum height to look good */
}

/* The canvas will now perfectly fit inside the wrapper */
.chart-wrapper canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100% !important;
    height: 100% !important;
}


/* Loading State */
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 50px;
    color: #7f8c8d;
}

/* Footer */
.footer {
    margin-top: 40px;
    text-align: center;
    padding: 25px;
    background: #121212;
    color: #888;
    font-size: 14px;
    border-top: 1px solid #2a2a2a;
}

/* Responsive Adjustments */
@media (max-width: 991.98px) {
    .charts-grid {
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    }
}

@media (max-width: 768px) {
    .charts-grid {
        grid-template-columns: 1fr; /* Stack charts on tablets and smaller */
    }
}

@media (max-width: 576px) {
    .dashboard-container {
        padding: 0 15px;
    }
    .summary-card {
        flex-direction: column;
        text-align: center;
    }
}
</style>