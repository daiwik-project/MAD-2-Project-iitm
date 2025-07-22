<template>
    <div class="view-questions-wrapper">
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
                <h2 class="section-title">Manage Questions</h2>
                <button class="btn btn-back" @click="$router.push(`/${level_id}/level/${subject_id}/subject/${chapter_id}/view/chapter`)">
                    <i class="fas fa-arrow-left"></i> Back to Chapter
                </button>
            </div>

            <!-- Questions Grid -->
            <div class="questions-grid">
                <div class="question-card" v-for="(question, index) in questions" :key="index">
                    <div class="question-card-header">
                        <h5 class="question-card-title">Question {{ index + 1 }}</h5>
                        <div class="question-card-actions">
                            <button class="btn btn-action btn-edit" data-bs-toggle="modal" :data-bs-target="'#edit' + question.uuid"><i class="fas fa-edit"></i></button>
                            <button class="btn btn-action btn-delete" @click="delete_question(question.uuid)"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                    <div class="question-card-body">
                        <p class="question-statement">{{ question["question"] }}</p>
                        <ul class="options-list">
                            <li :class="{ 'correct-answer': question.correct_option === 'A' }"><span>A</span> {{ question["option1"] }}</li>
                            <li :class="{ 'correct-answer': question.correct_option === 'B' }"><span>B</span> {{ question["option2"] }}</li>
                            <li :class="{ 'correct-answer': question.correct_option === 'C' }"><span>C</span> {{ question["option3"] }}</li>
                            <li :class="{ 'correct-answer': question.correct_option === 'D' }"><span>D</span> {{ question["option4"] }}</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Empty State Card -->
                <div v-if="questions.length === 0" class="empty-state-card">
                    <div class="empty-state">
                        <i class="fas fa-question-circle empty-icon"></i>
                        <h3>No Questions Yet</h3>
                        <p>This quiz is empty. Add questions by going back to the chapter page.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- MODALS ARE MOVED HERE, OUTSIDE THE V-FOR LOOP -->
        <div v-for="(question, index) in questions" :key="'modal-' + index">
            <div class="modal fade" :id="'edit' + question.uuid" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editModalLabel">Edit Question {{ index + 1 }}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="updateQuestion(question.uuid, question.question, question.option1, question.option2, question.option3, question.option4, question.correct_option)">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label class="form-label">Question Statement</label>
                                    <textarea class="form-control" v-model="question.question" rows="3" required></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Option A</label>
                                    <input type="text" class="form-control" v-model="question.option1" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Option B</label>
                                    <input type="text" class="form-control" v-model="question.option2" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Option C</label>
                                    <input type="text" class="form-control" v-model="question.option3" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Option D</label>
                                    <input type="text" class="form-control" v-model="question.option4" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Correct Answer</label>
                                    <select class="form-select" v-model="question.correct_option" required>
                                        <option value="A">A</option>
                                        <option value="B">B</option>
                                        <option value="C">C</option>
                                        <option value="D">D</option>
                                    </select>
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
import VueCookies from 'vue-cookies';


export default {
  name: 'ViewQuestions',
  data() {
    return {
      level_id: this.$route.params.level_id,   
      subject_id: this.$route.params.subject_id,
      chapter_id: this.$route.params.chapter_id,
      quiz_id: this.$route.params.quiz_id,

      que_legth: 0,
      questions: [],
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
    async fetchQuestions() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${this.quiz_id}/quiz/get_questions`);
        this.questions = response.data.info[1]; 
        //   alert(`Total questions: dxe${this.questions}`); 
      } catch (error) {
        console.error('Error fetching questions:', error);
      }
    },
    async updateQuestion(uuid, question, option1, option2, option3, option4, correct_option) {
      const ques_data = new FormData();
      ques_data.append('question', question);
      ques_data.append('option1', option1);
      ques_data.append('option2', option2);
      ques_data.append('option3', option3);
      ques_data.append('option4', option4);
      ques_data.append('correct_option', correct_option);

      try {
        const response = await axios.post(`http://127.0.0.1:5000/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${this.quiz_id}/quiz/${uuid}/update/question`, ques_data);
        alert(`Question updated successfully: ${response.data.message}`);
      } catch (error) {
        console.error('Error updating question:', error);
      }
    },
    async delete_question(uuid) {
      try {
        const req = await axios.delete(`http://127.0.0.1:5000/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${this.quiz_id}/quiz/${uuid}/delete/question`);
        alert(`Question deleted successfully: ${req.data.message}`);
        this.fetchQuestions(); // Refresh the questions list after deletion
        // this.$router.push(`/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${this.quiz_id}/quiz/viewquestions`);
      } catch (error) {
        console.error('Error deleting question:', error);
      }
    }
  },
  mounted() {
    this.checker();
    // called when component is mounted
    this.fetchQuestions();
  }
};
</script>

<style scoped>
/* General Page Wrapper */
.view-questions-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- NAVBAR STYLING (Consistent with other pages) --- */
.view-questions-wrapper .navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 25px;
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}
.view-questions-wrapper .navbar-brand {
    font-size: 26px;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}
.view-questions-wrapper .navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.view-questions-wrapper .navbar-toggler:focus {
    box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}
.view-questions-wrapper .navbar-nav .nav-link {
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
.view-questions-wrapper .navbar-nav .nav-link:hover,
.view-questions-wrapper .navbar-nav .nav-link.active {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}
@media (max-width: 991.98px) {
    .view-questions-wrapper .navbar-nav .nav-link:hover,
    .view-questions-wrapper .navbar-nav .nav-link.active {
        transform: none;
    }
    .view-questions-wrapper .navbar-collapse {
        padding-top: 15px;
    }
}

/* --- MAIN CONTENT STYLING --- */
.view-questions-wrapper .dashboard-container {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
}

.view-questions-wrapper .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.view-questions-wrapper .section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.view-questions-wrapper .btn-back {
    background-color: #fff;
    color: #34495e;
    border: 1px solid #e0e6ed;
    padding: 8px 16px;
    font-weight: 500;
    border-radius: 6px;
    transition: all 0.2s ease;
}
.view-questions-wrapper .btn-back:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Questions Grid */
.view-questions-wrapper .questions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
}

.view-questions-wrapper .question-card {
    background: #ffffff;
    border: 1px solid #e0e6ed;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
}
.view-questions-wrapper .question-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.view-questions-wrapper .question-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background-color: #f8f9fa;
    border-bottom: 1px solid #e0e6ed;
}
.view-questions-wrapper .question-card-title {
    font-size: 16px;
    font-weight: 600;
    color: #34495e;
    margin: 0;
}
.view-questions-wrapper .question-card-actions {
    display: flex;
    gap: 8px;
}
.view-questions-wrapper .btn-action {
    padding: 5px 8px;
    font-size: 12px;
    border-radius: 5px;
    border: none;
    color: white;
    transition: all 0.2s ease;
}
.view-questions-wrapper .btn-action:hover {
    filter: brightness(1.1);
}
.view-questions-wrapper .btn-edit { background-color: #f1c40f; }
.view-questions-wrapper .btn-delete { background-color: #e74c3c; }

.view-questions-wrapper .question-card-body {
    padding: 20px;
}
.view-questions-wrapper .question-statement {
    font-size: 15px;
    font-weight: 500;
    color: #2c3e50;
    margin-bottom: 20px;
    line-height: 1.6;
}
.view-questions-wrapper .options-list {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 14px;
}
.view-questions-wrapper .options-list li {
    background-color: #f8f9fa;
    padding: 10px 15px;
    border-radius: 6px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    border: 1px solid #e9ecef;
}
.view-questions-wrapper .options-list li span {
    font-weight: 600;
    margin-right: 10px;
    color: #3498db;
}
.view-questions-wrapper .options-list li.correct-answer {
    background-color: rgba(46, 204, 113, 0.1);
    border-color: rgba(46, 204, 113, 0.3);
    color: #1a6840;
    font-weight: 500;
}
.view-questions-wrapper .options-list li.correct-answer span {
    color: #2ecc71;
}

/* Empty State */
.view-questions-wrapper .empty-state-card {
    grid-column: 1 / -1; /* Make it span the full width */
}
.view-questions-wrapper .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #7f8c8d;
    padding: 40px;
    background-color: #fff;
    border-radius: 12px;
}
.view-questions-wrapper .empty-icon {
    font-size: 48px;
    color: #bdc3c7;
    margin-bottom: 20px;
}
.view-questions-wrapper .empty-state h3 {
    font-size: 20px;
    color: #34495e;
    margin-bottom: 5px;
}

/* Modal Styling */
.view-questions-wrapper .modal-content {
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: none;
}
.view-questions-wrapper .modal-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

/* Footer */
.view-questions-wrapper .footer {
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
    .view-questions-wrapper .dashboard-container {
        padding: 0 15px;
    }
    .view-questions-wrapper .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
}
</style>