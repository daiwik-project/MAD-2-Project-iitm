<template>
    <div class="create-question-wrapper">
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
                <div>
                    <h2 class="section-title">Create Questions</h2>
                    <p class="section-subtitle">For Quiz: <strong>{{ quiz_title }}</strong></p>
                </div>
                <button class="btn btn-back" @click="$router.push(`/${level_id}/level/${subject_id}/subject/${chapter_id}/view/chapter`)">
                    <i class="fas fa-arrow-left"></i> Back to Chapter
                </button>
            </div>

            <!-- Create Form -->
            <form @submit.prevent="submitAll">
                <div class="question-card" v-for="i in question_length" :key="i">
                    <div class="question-card-header">
                        <div class="question-card-icon">
                            <i class="fas fa-question-circle"></i>
                        </div>
                        <h3 class="question-card-title">Question {{ i }}</h3>
                    </div>

                    <div class="form-group">
                        <label :for="'statement_' + i">Question Statement</label>
                        <textarea class="form-control" rows="3" required v-model="questions[`Quest_${i}`].statement" :id="'statement_' + i" placeholder="Enter the full question here..."></textarea>
                    </div>

                    <div class="options-grid">
                        <div class="form-group">
                            <label :for="'option1_' + i">Option 1</label>
                            <input type="text" class="form-control" v-model="questions[`Quest_${i}`].options[0]" :id="'option1_' + i" placeholder="Enter first answer choice" required>
                        </div>
                        <div class="form-group">
                            <label :for="'option2_' + i">Option 2</label>
                            <input type="text" class="form-control" v-model="questions[`Quest_${i}`].options[1]" :id="'option2_' + i" placeholder="Enter second answer choice" required>
                        </div>
                        <div class="form-group">
                            <label :for="'option3_' + i">Option 3</label>
                            <input type="text" class="form-control" v-model="questions[`Quest_${i}`].options[2]" :id="'option3_' + i" placeholder="Enter third answer choice" required>
                        </div>
                        <div class="form-group">
                            <label :for="'option4_' + i">Option 4</label>
                            <input type="text" class="form-control" v-model="questions[`Quest_${i}`].options[3]" :id="'option4_' + i" placeholder="Enter fourth answer choice" required>
                        </div>
                    </div>

                    <div class="form-group correct-answer-group">
                        <label :for="'correct_' + i">Correct Answer</label>
                        <select class="form-select" required v-model="questions[`Quest_${i}`].correct" :id="'correct_' + i">
                            <option value="" disabled>Select the correct option</option>
                            <option value="A">Option 1 is correct</option>
                            <option value="B">Option 2 is correct</option>
                            <option value="C">Option 3 is correct</option>
                            <option value="D">Option 4 is correct</option>
                        </select>
                    </div>
                </div>

                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Save All Questions
                    </button>
                </div>
            </form>
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
    name: 'CreateQuestion',
    data() {
        return {

            quiz_title: '',
            subject_name: '',
            chapter_name: '',
            level_id: this.$route.params.level_id,   // <-- add this
            subject_id: this.$route.params.subject_id,
            chapter_id: this.$route.params.chapter_id,
            quiz_id: this.$route.params.quiz_id,

            question_length: 0,
            questions: {}
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

        async getlength_question() {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${this.quiz_id}/quiz/que_length`);
                this.question_length = response.data.info[0];
                this.quiz_title = response.data.info[1];
                this.chapter_name = response.data.info[2];
                this.subject_name = response.data.info[3];


                for (let i = 1; i <= this.question_length; i++) {
                    this.questions[`Quest_${i}`] = {
                        statement: '',
                        options: ['', '', '', ''],
                        correct: ''
                    };

                }
                console.log(this.questions);
                // alert(`The quiz has ${this.questions} questions`);
            } catch (error) {
                console.error('Error fetching question length:', error);
                alert('Failed to fetch question length.');
            }
        },

        async submitAll() {
            try {
                const request = await axios.post(`http://127.0.0.1:5000/api/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/chapter/${this.quiz_id}/quiz/create/question`, this.questions);
                // message if needed
                alert('Questions created successfully!');
                this.$router.push(`/${this.level_id}/level/${this.subject_id}/subject/${this.chapter_id}/view/chapter`);
            } catch (error) {
                console.error('Error creating question:', error);
                alert('Failed to create question.');
            }
        }
    },
    mounted() {
        this.checker();
        this.getlength_question();
    }
};
</script>


<style scoped>
/* General Page Wrapper */
.create-question-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- NAVBAR STYLING (Consistent with other pages) --- */
.create-question-wrapper .navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 25px;
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}
.create-question-wrapper .navbar-brand {
    font-size: 26px;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}
.create-question-wrapper .navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.create-question-wrapper .navbar-toggler:focus {
    box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}
.create-question-wrapper .navbar-nav .nav-link {
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
.create-question-wrapper .navbar-nav .nav-link:hover,
.create-question-wrapper .navbar-nav .nav-link.active {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}
@media (max-width: 991.98px) {
    .create-question-wrapper .navbar-nav .nav-link:hover,
    .create-question-wrapper .navbar-nav .nav-link.active {
        transform: none;
    }
    .create-question-wrapper .navbar-collapse {
        padding-top: 15px;
    }
}

/* --- MAIN CONTENT STYLING --- */
.create-question-wrapper .dashboard-container {
    max-width: 900px;
    margin: 30px auto;
    padding: 0 20px;
}

.create-question-wrapper .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    flex-wrap: wrap;
    gap: 15px;
}

.create-question-wrapper .section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}
.create-question-wrapper .section-subtitle {
    font-size: 16px;
    color: #7f8c8d;
    margin-top: 5px;
}

.create-question-wrapper .btn-back {
    background-color: #fff;
    color: #34495e;
    border: 1px solid #e0e6ed;
    padding: 8px 16px;
    font-weight: 500;
    border-radius: 6px;
    transition: all 0.2s ease;
}
.create-question-wrapper .btn-back:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Question Card */
.create-question-wrapper .question-card {
    background: #ffffff;
    padding: 25px 30px;
    border-radius: 12px;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.07);
    margin-bottom: 30px;
}

.create-question-wrapper .question-card-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
}
.create-question-wrapper .question-card-icon {
    font-size: 24px;
    color: #3498db;
}
.create-question-wrapper .question-card-title {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.create-question-wrapper .form-group {
    margin-bottom: 20px;
}
.create-question-wrapper .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 8px;
    color: #495057;
    font-size: 15px;
}
.create-question-wrapper .form-control, .create-question-wrapper .form-select {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #ced4da;
    border-radius: 6px;
    font-size: 15px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.create-question-wrapper .form-control:focus, .create-question-wrapper .form-select:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    outline: none;
}

.create-question-wrapper .options-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.create-question-wrapper .correct-answer-group {
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid #e9ecef;
}

.create-question-wrapper .form-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 10px;
}
.create-question-wrapper .btn-primary {
    padding: 12px 30px;
    font-size: 16px;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    border-radius: 6px;
}

/* Footer */
.create-question-wrapper .footer {
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
    .create-question-wrapper .dashboard-container {
        padding: 0 15px;
    }
}
@media (max-width: 576px) {
    .create-question-wrapper .options-grid {
        grid-template-columns: 1fr;
    }
    .create-question-wrapper .question-card {
        padding: 20px;
    }
}

</style>