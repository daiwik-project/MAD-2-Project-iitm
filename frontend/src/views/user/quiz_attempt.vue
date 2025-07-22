<template>
    <div class="quiz-attempt-page-wrapper">

        <!-- Quiz Header -->
        <header class="quiz-page-header">
            <div class="quiz-info">
                <h1 class="quiz-main-title">{{quizDetails.title}}</h1>
                <p class="quiz-chapter-info">{{quizDetails.chapterName}}</p>
            </div>

            <div class="header-meta-group">
                <div class="timer-section">
                    <i class="fas fa-stopwatch timer-icon"></i>
                    <span id="time-display" class="time-value">00:00 MIN</span>
                </div>
                <div class="quiz-progress-info">
                    <i class="fas fa-check-circle"></i>
                    <span>{{ Object.keys(userAnswers).length }} / {{ total_questions }}</span>
                </div>
                <div class="header-actions">
                    <button type="button" class="btn intruction btn-outline-light btn-sm" data-bs-toggle="modal"
                        data-bs-target="#instructionModal">
                        <i class="fas fa-info-circle"></i> Instructions
                    </button>
                </div>
            </div>
        </header>

        <!-- Main Quiz Layout -->
        <main class="quiz-layout-container">
            <aside class="question-navigation-sidebar card-animated">
                <h3 class="sidebar-title">Question Palette</h3>
                <ul class="question-nav-list">
                    <li v-for="(question, index) in questions" :key="index" @click="goToQuestion(index)">
                        
                        <!-- Case 1: Active AND Answered (This is the main fix) -->
                        <div v-if="currentQuestionIndex == index && userAnswers[question[0]]" class="nav-item active answered">
                            {{ index+1 }}
                        </div>
                        <!-- Case 2: Just Active -->
                        <div v-else-if="currentQuestionIndex === index" 
                            class="nav-item active">
                            {{ index + 1 }}
                        </div>
                        <!-- Case 3: Just Answered -->
                        <div v-else-if="userAnswers[question[0]]"  class="nav-item active">
                            {{ index + 1 }}
                        </div>
                        <!-- Case 4: Default (Not active, not answered) -->
                        <div v-else class="nav-item ">
                            {{ index + 1 }}
                        </div>
                    </li>

                </ul>
                <div class="sidebar-actions">
                    <button class="btn btn-submit-quiz-sidebar btn-primary" @click="submit_quiz">Submit Quiz</button>
                </div>
            </aside>

            <section class="question-display-area card-animated" v-if="questions[currentQuestionIndex]">
                <div class="question-header" >
                    <span class="question-number">Question {{ currentQuestionIndex + 1 }} of {{ total_questions }}</span>
                </div>
                <div class="question-statement">
                    Question Statement:
                    <h3>{{ questions[currentQuestionIndex][1] }}</h3>
                </div>
                <div class="options-container" >
                    <div v-for="(optionText, index) in questions[currentQuestionIndex]" :key="index">
                        <div v-if="index > 1">
                            <div v-if="userAnswers[questions[currentQuestionIndex][0]] ===  optionLetters[index - 2]" class="option-item selected" @click="addUserAnswer(questions[currentQuestionIndex][0], optionLetters[index - 2])">
                                <label class="option-label">
                                    <span class="option-letter" >{{ optionLetters[index -2] }}</span> {{ optionText }}
                                </label>
                            </div>
                            <div v-else class="option-item" @click="addUserAnswer(questions[currentQuestionIndex][0], optionLetters[index -2])">
                                <label class="option-label">
                                    <span class="option-letter">{{ optionLetters[index - 2 ] }}.</span>
                                    {{ optionText }}
                                </label>
                            </div>

                        </div>
                    </div>
                </div>

                <div class="question-navigation-buttons">
                    <button  @click="prevQuestion" :disabled="currentQuestionIndex == 0" class="btn btn-secondary btn-nav" >
                        Previous
                    </button>
                    <button @click="nextQuestion" :disabled="currentQuestionIndex == total_questions - 1"  class="btn btn-info btn-nav">
                        Next
                    </button>
                </div>
            </section>
        </main>


        <!-- Instructions Modal -->
        <div class="modal fade" id="instructionModal" tabindex="-1" aria-labelledby="instructionModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header instruction-header">
                        <h5 class="modal-title" id="instructionModalLabel">
                            <i class="fas fa-book-open"></i> Quiz Instructions
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">
                                Max. Marks: <span class="fw-bold float-end">{{ max_score }}</span>
                            </li>
                            <li class="list-group-item">
                                For each correct answer: <span class="fw-bold text-success float-end">+{{ correct_score }}</span>
                            </li>
                            <li class="list-group-item">
                                For each wrong answer: <span class="fw-bold text-danger float-end">-{{ wrong_score }}</span>
                            </li>
                            <li class="list-group-item">
                                <strong>If you don't know the answer, please skip the question to avoid penalty. </strong>
                            </li>
                        </ul>

                        <div class="alert alert-info mt-4 text-center">
                            <h4 class="alert-heading fw-bold">Important!</h4>
                            <p class="mb-0 fs-5">
                                You have to attempt only <strong class="fs-4">{{ max_score / correct_score }}</strong> questions to get full marks.
                            </p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Got it!</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>




<script>
import axios from 'axios';
import vuecookies from 'vue-cookies';

export default {
    name: 'QuizAttempt',
    data() {
        return {
            quizDetails: {
                title: 'a',
                chapterName: 'b',
            },
            quiz_id: this.$route.params.quiz_id,
            attempt_no: this.$route.params.attempt_number,
            time: 1,
            max_score: 0,
            total_questions: 0,
            correct_score: 0,
            wrong_score: 0,
            questions: [], 
            userAnswers: {},
            optionLetters: ['A', 'B', 'C', 'D'],
            currentQuestionIndex: 0

        };
    },
    methods: {
        async intial_info() {
            try {
                let token = this.$route.query.token;
                if (token) {
                    console.log("Token found in URL. Saving to cookies.");
                    // Set the cookie to expire in 1 day.
                    vuecookies.set('access_token', token, '1d');
                } else {
                    // 3. If it's not in the URL, fall back to checking the cookies.
                    console.log("No token in URL, checking cookies.");
                    token = vuecookies.get('access_token');
                }
                // const token = vuecookies.get('access_token');
                const req = await axios.get(`http://127.0.0.1:5000/quiz_info_start?token=${token}&quiz_id=${this.quiz_id}`);
                
                const quizData = req.data.quiz_data;
                this.quizDetails.title = quizData[0];
                this.time = quizData[1];
                this.max_score = quizData[2];
                this.correct_score = quizData[3];
                this.wrong_score = quizData[4];
                this.quizDetails.chapterName = quizData[5];
                this.total_questions = quizData[6];
                this.questions = Object.values(quizData[7]);
                this.start_timer();

            }
            catch (error) {
                console.error("Error fetching quiz info:", error);
            }    
        },
        
        start_timer() {
            let timerDisplay = document.getElementById('time-display');
            let totalSeconds = this.time * 60;
            const self = this;

            function updateTimer() {
                let minutes = Math.floor(totalSeconds / 60);
                let seconds = totalSeconds % 60;
                let formattedSeconds = seconds;
                if (seconds < 10) {
                    formattedSeconds = '0' + seconds;
                }
                timerDisplay.textContent = `${minutes}:${formattedSeconds} MIN`;

                if (totalSeconds > 0) {
                    totalSeconds--;
                    self.timerId = setTimeout(updateTimer, 1000);
                } else {
                    alert("Time's up! Your quiz will be submitted automatically.");
                    self.submit_quiz();
                }
            }
            updateTimer();
        },
        goToQuestion(index) {
            this.currentQuestionIndex = index;
        },
        addUserAnswer(question_id, option_id){
            this.userAnswers[question_id] = option_id
            // alert(`this is ${question} nad ${option_id}`)
            console.log(this.userAnswers)
        },
        nextQuestion() {
            if (this.currentQuestionIndex < this.total_questions - 1) {
                this.currentQuestionIndex++;
            }
        },

        prevQuestion() {
            if (this.currentQuestionIndex > 0) {
                this.currentQuestionIndex--;
            }
        },

        async submit_quiz(){
            try {
                const token = vuecookies.get('access_token');
                const req = await axios.post(`http://127.0.0.1:5000/quiz_submit/${this.quiz_id}/${this.attempt_no}?token=${token}`, 
                {
                    userAnswers: this.userAnswers
                })
                this.$router.push(`/dashboard/summary/${this.quiz_id}/attempt_=${this.attempt_no}`)
                alert("Quiz submitted successfully!");
                
            } catch (error) {
                console.error("Error fetching quiz info:", error);
            }
        }
    },
    mounted() {
        this.intial_info();
    }
};
</script>





<style scoped>
/* --- GLOBAL & PAGE WRAPPER --- */
.quiz-attempt-page-wrapper {
    background-color: #f0f4f8;
    min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* --- HEADER SECTION --- */
.quiz-page-header {
    /* This dark header is consistent with your other pages' navbars */
    background: #0f0c29;
    color: #fff;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    position: sticky;
    top: 0;
    z-index: 1010;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.quiz-info .quiz-main-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
}

.quiz-info .quiz-chapter-info {
    font-size: 0.9rem;
    color: #bdc3c7;
    margin: 0;
}

.header-meta-group {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.timer-section,
.quiz-progress-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
    color: #bdc3c7;
}

.timer-icon,
.quiz-progress-info i {
    font-size: 1.25rem;
}

.timer-icon {
    color: #f1c40f;
    /* Kept yellow for standard timer warning color */
}

.quiz-progress-info i {
    color: #2ecc71;
    /* Kept green for standard success color */
}

.time-value {
    font-weight: 700;
    color: #fff;
}

/* --- MAIN CONTENT LAYOUT --- */
.quiz-layout-container {
    display: flex;
    flex-grow: 1;
    padding: 1.5rem;
    gap: 1.5rem;
    max-width: 1500px;
    width: 100%;
    margin: 0 auto;
}

.card-animated {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-animated:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* --- QUESTION PALETTE (LEFT SIDEBAR) --- */
.question-navigation-sidebar {
    width: 280px;
    flex-shrink: 0;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    max-height: calc(100vh - 120px);
}

.intruction:hover{
    color: #0f0c29;
}
.sidebar-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e9ecef;
}

.question-nav-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(45px, 1fr));
    gap: 0.75rem;
    overflow-y: auto;
    flex-grow: 1;
    margin-bottom: 1.5rem;
}

.nav-item {
    width: 45px;
    height: 45px;
    border: 2px solid #d1d8e0;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.nav-item:hover {
    /* GRADIENT: Using the primary blue for hover */
    border-color: #3498db;
    color: #3498db;
}

.nav-item.active {
    /* GRADIENT: Applying the blue gradient to the active question */
    background: linear-gradient(135deg, #000000, #0065fd);
    color: white;
    border-color: transparent;
    font-weight: 700;
    transform: scale(1.1);
}

.nav-item.answered {
    background-color: #e8f5e9;
    border-color: #2ecc71;
    color: #27ae60;
}

.nav-item.answered.active {
    /* GRADIENT: Overriding the green when an answered question is also active */
    background: linear-gradient(135deg, #2980b9, #1f638f);
    border-color: transparent;
    color: white;
}

.sidebar-actions {
    margin-top: auto;
}

/* --- QUESTION DISPLAY (RIGHT SIDE) --- */
.question-display-area {
    flex-grow: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
}

.question-header {
    margin-bottom: 1.5rem;
}

.question-number {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
}

.question-statement {
    font-size: 1.2rem;
    line-height: 1.6;
    color: #34495e;
    margin-bottom: 2rem;
    flex-grow: 1;
    min-height: 80px;
}

.options-container {
    display: grid;
    gap: 1rem;
    margin-bottom: 2rem;
}

.option-item {
    background-color: #f8f9fa;
    border: 2px solid #e0e6ed;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
}

.option-item:hover {
    border-color: #a3b1c0;
    background-color: #f1f3f5;
}

.option-item.selected {
    /* GRADIENT: Using the blue theme for selected answers */
    background-color: #e9f5ff;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.3);
}

.option-label {
    font-size: 1rem;
    color: #495057;
    cursor: pointer;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.option-letter {
    /* GRADIENT: Using the primary blue for the option letter */
    font-weight: 700;
    color: #3498db;
}

.option-item.selected .option-label {
    color: #2980b9;
    font-weight: 500;
}

.question-navigation-buttons {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
    padding-top: 1.5rem;
    border-top: 1px solid #e9ecef;
}

/* --- BUTTONS & MODAL --- */
.btn {
    border-radius: 8px;
    font-weight: 600;
    padding: 0.7rem 1.5rem;
    transition: all 0.3s ease;
    border: none;
    color: white;
}

.btn:hover {
    transform: translateY(-2px);
}

.btn:disabled {
    background: #cccccc;
    color: #666666;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.btn-nav {
    min-width: 120px;
}

/* GRADIENT: Applying the pink/purple gradient to primary buttons */
.btn-primary,
.btn-submit-quiz-sidebar {
    background: linear-gradient(to right, #ff6ec4, #0800ff);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    width: 100%;
}

.btn-primary:hover,
.btn-submit-quiz-sidebar:hover {
    box-shadow: 0 8px 20px rgba(255, 110, 196, 0.3);
}

/* GRADIENT: Applying the blue gradient to info/next buttons */
.btn-info {
    background: linear-gradient(135deg, #3665ff, #2548cc);
    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.2);
}

.btn-info:hover {
    box-shadow: 0 6px 15px rgba(52, 152, 219, 0.4);
}

/* GRADIENT: Using a neutral gray for secondary/previous buttons */
.btn-secondary {
    background-color: #6c757d;
}

.btn-secondary:hover {
    background-color: #5a6268;
}

.modal-header.instruction-header {
    background-color: #0f0c29;
    color: #fff;
    border-bottom: 1px solid #444;
}

.modal-header.instruction-header .btn-close {
    filter: invert(1) grayscale(100%) brightness(200%);
}

.list-group-item {
    border-left: 0;
    border-right: 0;
    padding: 1rem 0;
}

/* --- LOADING MESSAGE --- */
.no-questions-message {
    text-align: center;
    padding: 50px 20px;
    font-size: 1.1rem;
    color: #555;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.no-questions-message i {
    font-size: 3rem;
    color: #3498db;
    margin-bottom: 1rem;
}

/* --- RESPONSIVE DESIGN (MEDIA QUERIES) --- */
@media (max-width: 1200px) {
    .quiz-layout-container {
        flex-direction: column;
    }

    .question-navigation-sidebar {
        width: 100%;
        max-height: none;
        order: -1;
    }
}

@media (max-width: 992px) {
    .quiz-page-header {
        justify-content: center;
    }

    .header-meta-group {
        justify-content: center;
    }
}
</style>

