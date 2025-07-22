<template>
    <div class="view-chapter-wrapper">
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
                            <a class="nav-link active" href="/admindashboard"><i class="fas fa-book"></i> Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/a/summary"><i class="fas fa-chart-line"></i> Summary</a>
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
            <div class="page-header">
                <h2 class="section-title">Chapter Details</h2>
                <button class="btn btn-back" @click="$router.push(`/${level_id}/level/${subject_id}/view/subject`)">
                    <i class="fas fa-arrow-left"></i> Back to Subject
                </button>
            </div>

            <!-- Chapter Info Card -->
            <div class="chapter-info-card">
                <div class="chapter-info-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <div class="chapter-info-content">
                    <h1>{{ chapter_name }}</h1>
                    <p>{{ chapter_description }}</p>
                </div>
            </div>

            <!-- Quizzes Table Card -->
            <div class="quizzes-card">
                <h3 class="quizzes-title">Quizzes in this Chapter</h3>
                <div class="table-responsive-wrapper">
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>Quiz Title</th>
                                <th>Description</th>
                                <th>Marks</th>
                                <th>Scores (+/-)</th>
                                <th>Date</th>
                                <th>Duration</th>
                                <th>Questions</th>
                                <th class="text-center">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="quizezz.length === 0">
                                <td colspan="8" class="text-center py-5">
                                    <div class="empty-state">
                                        <i class="fas fa-inbox empty-icon"></i>
                                        <h3>No Quizzes Yet</h3>
                                        <p>Click the '+' button to create the first quiz for this chapter.</p>
                                    </div>
                                </td>
                            </tr>
                            <tr v-else v-for="(quiz, index) in quizezz" :key="index">
                                <td data-label="Quiz Title">{{ quiz[1] }}</td>
                                <td data-label="Description">{{ quiz[2] }}</td>
                                <td data-label="Marks">{{ quiz[3] }}</td>
                                <td data-label="Scores (+/-)">
                                    <span class="score-correct">+{{ quiz[4] }}</span> / <span class="score-wrong">-{{ quiz[5] }}</span>
                                </td>
                                <td data-label="Date">{{ quiz[6] }}</td>
                                <td data-label="Duration">{{ quiz[7] }} mins</td>
                                <td data-label="Questions">
                                    <span class="fw-bold">{{ quiz[9] }}</span> / {{ quiz[8] }}
                                    <div class="progress mt-1" style="height: 5px;">
                                        <div class="progress-bar" role="progressbar" :style="{ width: (quiz[9] / quiz[8] * 100) + '%' }" aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                </td>
                                <td data-label="Actions" class="action-cell">
                                    <button v-if="quiz[10] > 0" @click="createquestions(quiz[0])" class="btn btn-action btn-add-q" title="Add Questions">
                                        <i class="fas fa-plus"></i>
                                    </button>
                                    <button class="btn btn-action btn-view" @click="viewquestions(quiz[0])" title="View Questions">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button class="btn btn-action btn-edit" :data-bs-toggle="'modal'" :data-bs-target="'#edit' + quiz[0]" title="Edit Quiz">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="btn btn-action btn-delete" @click="delete_quiz(quiz[0])" title="Delete Quiz">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Floating Action Button for Creating Quiz -->
        <button type="button" class="btn-add-floating" data-bs-toggle="modal" data-bs-target="#createQuizModal" title="Create New Quiz">
            <i class="fas fa-plus"></i>
        </button>

        <!-- Create Quiz Modal -->
        <div class="modal fade" id="createQuizModal" tabindex="-1" aria-labelledby="createQuizModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="createQuizModalLabel">Create New Quiz</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form @submit.prevent="createquiz">
                        <div class="modal-body">
                            <div class="mb-3">
                                <label for="quizTitle" class="form-label">Quiz Title</label>
                                <input type="text" class="form-control" id="quizTitle" v-model="quizTitle" placeholder="e.g., Introduction to HTML Basics" required>
                            </div>
                            <div class="mb-3">
                                <label for="quizDescription" class="form-label">Description</label>
                                <textarea class="form-control" id="quizDescription" v-model="quizDescription" required></textarea>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="quizMaxMarks" class="form-label">Max Marks</label>
                                    <input type="number" class="form-control" id="quizMaxMarks" v-model="quizMaxMarks" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="quiztotalquestion" class="form-label">Total Questions</label>
                                    <input type="number" class="form-control" id="quiztotalquestion" v-model="quizTotalQuestions" required min="1" step="1">
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="quizcorrectscore" class="form-label">Correct Score</label>
                                    <input type="number" class="form-control" id="quizcorrectscore" v-model="quizCorrectScore" required step="any">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="quizwrongscore" class="form-label">Wrong Score</label>
                                    <input type="number" class="form-control" id="quizwrongscore" v-model="quizWrongScore" required step="any">
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="quizScheduledDate" class="form-label">Scheduled Date</label>
                                    <input type="date" class="form-control" id="quizScheduledDate" v-model="quizScheduledDate" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="quizMaxTime" class="form-label">Duration (mins)</label>
                                    <input type="number" class="form-control" id="quizMaxTime" v-model="quizMaxTime" min="1" step="1">
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Create Quiz</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Edit Quiz Modals  -->
        <div v-for="(quiz, index) in quizezz" :key="'modal-' + index">
            <div class="modal fade" :id="'edit' + quiz[0]" tabindex="-1" aria-labelledby="editQuizLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editQuizLabel">Edit Quiz: {{ quiz[1] }}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="update_quiz_det(quiz[0], quiz[1], quiz[2], quiz[3], quiz[4], quiz[5], quiz[6], quiz[7], quiz[8])">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label :for="'editQuizTitle' + quiz[0]" class="form-label">Quiz Title</label>
                                    <input type="text" class="form-control" :id="'editQuizTitle' + quiz[0]" v-model="quiz[1]" required>
                                </div>
                                <div class="mb-3">
                                    <label :for="'editQuizDescription' + quiz[0]" class="form-label">Description</label>
                                    <textarea class="form-control" :id="'editQuizDescription' + quiz[0]" v-model="quiz[2]" required></textarea>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label :for="'editQuizsMaxMarks' + quiz[0]" class="form-label">Max Marks</label>
                                        <input type="number" class="form-control" :id="'editQuizsMaxMarks' + quiz[0]" v-model="quiz[3]" required step="any">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label :for="'editQuiztotalquestion' + quiz[0]" class="form-label">Total Questions</label>
                                        <input type="number" class="form-control" :id="'editQuiztotalquestion' + quiz[0]" v-model="quiz[8]" required min="1" step="1">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label :for="'editQuizcorrectscore' + quiz[0]" class="form-label">Correct Score</label>
                                        <input type="number" class="form-control" :id="'editQuizcorrectscore' + quiz[0]" v-model="quiz[4]" required step="any">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label :for="'editQuizwrongscore' + quiz[0]" class="form-label">Wrong Score</label>
                                        <input type="number" class="form-control" :id="'editQuizwrongscore' + quiz[0]" v-model="quiz[5]" required step="any">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label :for="'editQuizScheduledDate' + quiz[0]" class="form-label">Scheduled Date</label>
                                        <input type="date" class="form-control" :id="'editQuizScheduledDate' + quiz[0]" v-model="quiz[6]" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label :for="'editQuizMaxTime' + quiz[0]" class="form-label">Duration (mins)</label>
                                        <input type="number" class="form-control" :id="'editQuizMaxTime' + quiz[0]" v-model="quiz[7]" required min="1" step="1">
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save Changes</button>
                            </div>
                        </form>
                    </div>
                </div>
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
import VueCookies from 'vue-cookies'

export default {
    name: 'ViewChapter',
    data() {
        return {
            // Define any data properties you need here
            // subject_name: '',
            // subject_description: '',
            level_id: this.$route.params.level_id,
            subject_id: this.$route.params.subject_id,
            chapter_id: this.$route.params.chapter_id,

            chapter_name: '',
            chapter_description: '',
            quizezz: [],

            // use in create quiz modal
            quizTitle: '',
            quizDescription: '',
            quizMaxMarks: null,
            quizCorrectScore: null,
            quizWrongScore: null,
            quizScheduledDate: null,
            quizMaxTime: null,
            quizTotalQuestions: null,
        };
    },
    methods: {
        async checker(){
            if (!VueCookies.get('admin_token')) {
                alert('You are not logged in.')
                this.$router.push('/admin/login')
                return;
            }
        },

        async fetchChapterData() {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}`);
                const backendData = response.data;
                this.chapter_name = backendData.info[1];
                this.chapter_description = backendData.info[2];
                this.quizezz = backendData.info[3];

                // alert(`backendData.info[1]: ${this.chapter_name}`);
            } catch (error) {
                alert('Error fetching chapter data:', error);
            }
        },
        // Define any methods you need here
        async createquiz() {
            const quizData = new FormData();
            quizData.append('quizTitle', this.quizTitle);
            quizData.append('quizDescription', this.quizDescription);
            quizData.append('quizMaxMarks', this.quizMaxMarks);
            quizData.append('quizcorrectscore', this.quizCorrectScore);
            quizData.append('quizwrongscore', this.quizWrongScore);
            quizData.append('quizScheduledDate', this.quizScheduledDate);
            quizData.append('quizMaxTime', this.quizMaxTime);
            quizData.append('quiztotalquestion', this.quizTotalQuestions);


            try {
                // alert(`level_id: ${this.level_id}, subject_id: ${this.subject_id}, chapter_id: ${this.chapter_id}`);
                const response = await axios.post(`http://127.0.0.1:5000/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/create/quiz`, quizData);
                // alert(`Quiz created successfully! ${response.data.message}`);
                // this.$router.push(`/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/view/chapter`);
                this.fetchChapterData(); // Refresh the chapter data to show the new quiz
            } catch (error) {
                this.fetchChapterData(); // Refresh the chapter data to show the new quiz
                // alert('Error creating quiz:', error);
            }
        },
        async update_quiz_det(id, title, description, max_marks, correct_score, wrong_score, scheduled_date, max_time, total_questions) {
            const quizData = new FormData();
            quizData.append('quizTitle', title);
            quizData.append('quizDescription', description);
            quizData.append('quizMaxMarks', max_marks);
            quizData.append('quizcorrectscore', correct_score);
            quizData.append('quizwrongscore', wrong_score);
            quizData.append('quizScheduledDate', scheduled_date);
            quizData.append('quizMaxTime', max_time);
            quizData.append('quiztotalquestion', total_questions);

            // alert(`quizid, ${id} quizData.name: ${title}, quizData.description: ${description}, quizData.max_marks: ${max_marks}, quizData.correct_score: ${correct_score}, quizData.wrong_score: ${wrong_score}, quizData.scheduled_date: ${scheduled_date}, quizData.max_time: ${max_time}, quizData.total_questions: ${total_questions}`);
            try {
                const response = await axios.post(`http://127.0.1:5000/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${id}/update/quiz`, quizData);
                alert(`Quiz updated successfully! ${response.data.message}`);
                this.$router.push(`/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/view/chapter`);

            } catch (error) {
                // alert('Error updating quiz:', error);
            }

        },

        async delete_quiz(quiz_id) {
            // Logic to delete the quiz
            // alert(`Deleting quiz with ID: ${quiz_id}`);
            try {
                const response = await axios.delete(`http:////127.0.0.1:5000/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${quiz_id}/delete/quiz`);
                // alert(`Quiz deleted successfully! ${response.data.message}`);
                this.fetchChapterData(); // Refresh the chapter data to show the updated list of quizzes
            } catch (error) {
                alert('Error deleting quiz:', error);
            }
        },

        async createquestions(quiz_id) {
            // Logic to create questions for the quiz
            // alert(`Creating questions for quiz ID: ${quiz_id}`);

            this.$router.push(`/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${quiz_id}/quiz/createquestions`);

        },
        async viewquestions(quiz_id) {
            this.$router.push(`/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${quiz_id}/quiz/viewquestions`);
        }

    },
    mounted() {
        this.checker();
        // Fetch data when the component is mounted
        this.fetchChapterData();
    }
};


</script>


<style scoped>
/* General Page Wrapper */
.view-chapter-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- NAVBAR STYLING (Consistent with other pages) --- */
.view-chapter-wrapper .navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 25px;
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}
.view-chapter-wrapper .navbar-brand {
    font-size: 26px;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}
.view-chapter-wrapper .navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.view-chapter-wrapper .navbar-toggler:focus {
    box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}
.view-chapter-wrapper .navbar-nav .nav-link {
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
.view-chapter-wrapper .navbar-nav .nav-link:hover,
.view-chapter-wrapper .navbar-nav .nav-link.active {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}
@media (max-width: 991.98px) {
    .view-chapter-wrapper .navbar-nav .nav-link:hover,
    .view-chapter-wrapper .navbar-nav .nav-link.active {
        transform: none;
    }
    .view-chapter-wrapper .navbar-collapse {
        padding-top: 15px;
    }
}

/* --- MAIN CONTENT STYLING --- */
.view-chapter-wrapper .dashboard-container {
    max-width: 1400px;
    margin: 30px auto;
    padding: 0 20px;
}

.view-chapter-wrapper .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.view-chapter-wrapper .section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.view-chapter-wrapper .btn-back {
    background-color: #fff;
    color: #34495e;
    border: 1px solid #e0e6ed;
    padding: 8px 16px;
    font-weight: 500;
    border-radius: 6px;
    transition: all 0.2s ease;
}
.view-chapter-wrapper .btn-back:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Chapter Info Card */
.view-chapter-wrapper .chapter-info-card {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
    color: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(46, 204, 113, 0.3);
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    gap: 25px;
}
.view-chapter-wrapper .chapter-info-icon {
    font-size: 48px;
    opacity: 0.8;
}
.view-chapter-wrapper .chapter-info-content h1 {
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 5px 0;
}
.view-chapter-wrapper .chapter-info-content p {
    font-size: 16px;
    margin: 0;
    opacity: 0.9;
}

/* Quizzes Table Card */
.view-chapter-wrapper .quizzes-card {
    background: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.view-chapter-wrapper .quizzes-title {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 20px;
}

.view-chapter-wrapper .table-responsive-wrapper {
    overflow-x: auto;
}

.view-chapter-wrapper .results-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.view-chapter-wrapper .results-table th, .view-chapter-wrapper .results-table td {
    padding: 12px 15px;
    border-bottom: 1px solid #e9ecef;
    text-align: left;
    vertical-align: middle;
    white-space: nowrap;
}
.view-chapter-wrapper .results-table th {
    background-color: #f8f9fa;
    font-weight: 600;
    color: #495057;
}
.view-chapter-wrapper .results-table tbody tr:hover {
    background-color: #f1f5f8;
}
.view-chapter-wrapper .score-correct { color: #2ecc71; font-weight: 500; }
.view-chapter-wrapper .score-wrong { color: #e74c3c; font-weight: 500; }

.view-chapter-wrapper .action-cell {
    text-align: center;
    display: flex;
    gap: 8px;
}
.view-chapter-wrapper .btn-action {
    padding: 6px 10px;
    font-size: 13px;
    border-radius: 5px;
    border: none;
    color: white;
    transition: all 0.2s ease;
}
.view-chapter-wrapper .btn-action:hover {
    transform: scale(1.05);
    filter: brightness(1.1);
}
.view-chapter-wrapper .btn-add-q { background-color: #2ecc71; }
.view-chapter-wrapper .btn-view { background-color: #3498db; }
.view-chapter-wrapper .btn-edit { background-color: #f1c40f; }
.view-chapter-wrapper .btn-delete { background-color: #e74c3c; }

/* Empty State */
.view-chapter-wrapper .empty-state {
    color: #7f8c8d;
}
.view-chapter-wrapper .empty-icon {
    font-size: 48px;
    color: #bdc3c7;
    margin-bottom: 20px;
}
.view-chapter-wrapper .empty-state h3 {
    font-size: 20px;
    color: #34495e;
    margin-bottom: 5px;
}

/* Floating Add Button */
.view-chapter-wrapper .btn-add-floating {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3665ff, #2548cc);
    color: white;
    font-size: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    border: none;
    box-shadow: 0 6px 20px rgba(54, 101, 255, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.view-chapter-wrapper .btn-add-floating:hover {
    transform: translateY(-5px) scale(1.1);
    box-shadow: 0 10px 25px rgba(54, 101, 255, 0.5);
}

/* Modal Styling */
.view-chapter-wrapper .modal-content {
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: none;
}
.view-chapter-wrapper .modal-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

/* Footer */
.view-chapter-wrapper .footer {
    margin-top: 40px;
    text-align: center;
    padding: 25px;
    background: #121212;
    color: #888;
    font-size: 14px;
    border-top: 1px solid #2a2a2a;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .view-chapter-wrapper .dashboard-container {
        padding: 0 15px;
    }
    .view-chapter-wrapper .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    .view-chapter-wrapper .results-table {
        display: block;
        width: 100%;
    }
    .view-chapter-wrapper .results-table thead { display: none; }
    .view-chapter-wrapper .results-table tbody, .view-chapter-wrapper .results-table tr, .view-chapter-wrapper .results-table td { display: block; width: 100%; }
    .view-chapter-wrapper .results-table tr {
        margin-bottom: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
    }
    .view-chapter-wrapper .results-table td {
        text-align: right;
        padding-left: 50%;
        position: relative;
        border-bottom: 1px solid #eee;
    }
    .view-chapter-wrapper .results-table td:before {
        content: attr(data-label);
        position: absolute;
        left: 15px;
        width: 45%;
        padding-right: 10px;
        white-space: nowrap;
        text-align: left;
        font-weight: bold;
    }
    .view-chapter-wrapper .results-table td:last-child {
        border-bottom: 0;
    }
    .view-chapter-wrapper .action-cell {
        display: flex;
        justify-content: flex-end;
    }
}
@media (max-width: 576px) {
    .view-chapter-wrapper .chapter-info-card {
        flex-direction: column;
        text-align: center;
    }
    .view-chapter-wrapper .chapter-info-content h1 {
        font-size: 24px;
    }
}
</style>