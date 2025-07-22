<template>
    <div class="quiz-summary-page-wrapper">

        <header class="quiz-page-header">
            <div class="quiz-info">
                <h1 class="quiz-main-title">Quiz Results</h1>
                <h6 class="quiz-chapter-info">{{ quizDetails.title }}</h6>
                <p class="quiz-chapter-info">Chapter : {{ quizDetails.chapter_name }}</p>
            </div>

            <div class="score-summary-group">
                <div class="score-card final-score">
                    <span class="score-value">{{ score.user_score }}</span>
                    <span class="score-label">Your Score</span>
                </div>
                <div class="score-card correct-answers">
                     <span class="score-value">{{ quizDetails.positive_marking }}</span>
                    <span class="score-label">On Correct</span>
                </div>
                <div class="score-card wrong-answers">
                    <span class="score-value">{{ quizDetails.negative_marking }}</span>
                    <span class="score-label">On Wrong</span>
                </div>
                <div class="score-card unattempted">
                     <span class="score-value">{{ quizDetails.max_score }}</span>
                    <span class="score-label">Max. Marks</span>
                </div>
            </div>
        </header>

        <main class="summary-layout-container">
            

           
                <div v-for="(question, index) in questions" :key="question.question_id" class="question-summary-card card-animated">
                    <div class="question-header">
                        <span class="question-number">Question {{ index +1 }}</span>
                    </div>
                    <div class="question-statement">
                        <h3>{{ question.question }}</h3>
                    </div>

                    <div class="options-container">

                        <div class="option-item" :class="{
                            'correct': correctAnswers[question.question_id] === 'A',
                            'incorrect': userAnswers[question.question_id] === 'A' && correctAnswers[question.question_id] !== 'A'
                        }">
                            <span class="option-letter">A.</span> {{ question.option1 }}
                            <span v-if="userAnswers[question.question_id] === 'A'" class="user-choice-indicator">Your Answer</span>
                        </div>

                        <div class="option-item" :class="{
                            'correct': correctAnswers[question.question_id] === 'B',
                            'incorrect': userAnswers[question.question_id] === 'B' && correctAnswers[question.question_id] !== 'B'
                        }">
                            <span class="option-letter">B.</span> {{ question.option2}}
                            <span v-if="userAnswers[question.question_id] === 'B'" class="user-choice-indicator">Your Answer</span>
                        </div>

                        <div class="option-item" :class="{
                            'correct': correctAnswers[question.question_id] === 'C',
                            'incorrect': userAnswers[question.question_id] === 'C' && correctAnswers[question.question_id] !== 'C'
                        }">
                            <span class="option-letter">C.</span> {{ question.option3 }}
                            <span v-if="userAnswers[question.question_id] === 'C'" class="user-choice-indicator">Your Answer</span>
                        </div>

                        <div class="option-item" :class="{
                            'correct': correctAnswers[question.question_id] === 'D',
                            'incorrect': userAnswers[question.question_id] === 'D' && correctAnswers[question.question_id] !== 'D'
                        }">
                            <span class="option-letter">D.</span> {{ question.option4 }}
                            <span v-if="userAnswers[question.question_id] === 'D'" class="user-choice-indicator">Your Answer</span>
                        </div>

                    </div>
                    
                </div>




            <div class="summary-actions">
                <a href="/dashboard" class="btn btn-primary btn-dashboard">Go to Dashboard</a>
                <button @click="downloadReport" class="btn btn-secondary btn-download">
                    <i class="fas fa-download"></i> Download This Report
                </button>
            </div>

        </main>
    </div>
</template>

<script>
import axios from 'axios';
import vuecookies from 'vue-cookies';

export default {
    name: 'QuizSummary',
    data() {
        return {
            quiz_id: this.$route.params.quiz_id,
            attempt_no: this.$route.params.attempt_number,
            quizDetails: {
                title: '',
                chapter_name: '',
                max_score: 0,
                positive_marking: 0,
                negative_marking: 0,
            },
            score: {
                user_score: 0,
            },
            questions: [],
            userAnswers: {},
            correctAnswers: {}
        };
    },
    methods: {
        async firstinfo() {
            try {
                const token = vuecookies.get('access_token');
                const req = await axios.get(`http://127.0.0.1:5000/quiz_summary_info/${this.quiz_id}/${this.attempt_no}?token=${token}`);
                this.quizDetails = req.data.quiz_details;
                this.score.user_score = req.data.score.user_score;
                this.questions = req.data.questions;
                this.userAnswers = req.data.user_answer;
                this.correctAnswers = req.data.correct_answer;
            } catch(error) {
                console.error("Error fetching quiz info:", error);
            }
        },
        downloadReport() {
            const headers = [
                'quiz_id', 'quiz_name', 'chapter_name', 'question_statement',
                'option1', 'option2', 'option3', 'option4',
                'positive_marking', 'negative_marking', 'your_option',
                'corrected_option', 'your_score'
            ];

            // A helper function to safely format data for CSV (handles commas and quotes)
            const escapeCsvField = (field) => {
                if (field === null || field === undefined) {
                    return '';
                }
                const stringField = String(field);
                // If the field contains a comma, a double-quote, or a newline, enclose it in double-quotes.
                if (stringField.includes(',') || stringField.includes('"') || stringField.includes('\n')) {
                    // Also, any double-quote within the field must be escaped by another double-quote.
                    return `"${stringField.replace(/"/g, '""')}"`;
                }
                return stringField;
            };

            const optionMap = { A: 'option1', B: 'option2', C: 'option3', D: 'option4' };

            // Map each question to a CSV row
            const rows = this.questions.map(question => {
                const userChoiceKey = this.userAnswers[question.question_id];
                const correctChoiceKey = this.correctAnswers[question.question_id];
                
                let questionScore = 0;
                if (userChoiceKey) { // If the user attempted the question
                    if (userChoiceKey === correctChoiceKey) {
                        questionScore = this.quizDetails.positive_marking;
                    } else {
                        questionScore = this.quizDetails.negative_marking;
                    }
                }
                
                const yourOptionText = userChoiceKey ? question[optionMap[userChoiceKey]] : 'Not Attempted';
                const correctedOptionText = correctChoiceKey ? question[optionMap[correctChoiceKey]] : 'N/A';

                return [
                    this.quiz_id,
                    this.quizDetails.title,
                    this.quizDetails.chapter_name,
                    question.question,
                    question.option1,
                    question.option2,
                    question.option3,
                    question.option4,
                    this.quizDetails.positive_marking,
                    this.quizDetails.negative_marking,
                    yourOptionText,
                    correctedOptionText,
                    questionScore
                ].map(escapeCsvField).join(','); // Escape each field and join with a comma
            });

            // Combine headers and rows into a single CSV string
            const csvContent = [headers.join(','), ...rows].join('\n');

            // Create a Blob and trigger the download
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            if (link.download !== undefined) { // Check for browser support
                const url = URL.createObjectURL(blob);
                const safeTitle = this.quizDetails.title.replace(/[^a-z0-9]/gi, '_'); // Sanitize filename
                link.setAttribute('href', url);
                link.setAttribute('download', `Quiz-Report-${safeTitle}.csv`);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url); // Clean up the URL object
            }
        }
    },
    async mounted() {
        await this.firstinfo();
    }
};
</script>



<style scoped>
/* --- GLOBAL & PAGE WRAPPER --- */
.quiz-summary-page-wrapper {
    background-color: #f0f4f8;
    min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
/* Add this inside your <style scoped> tag */
.btn-secondary {
    background: linear-gradient(135deg, #6c757d, #495057);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

/* Optional: Adjust layout for multiple buttons */
.summary-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap; /* Allows buttons to stack on small screens */
}

/* --- HEADER SECTION (Adapted for Summary) --- */
.quiz-page-header {
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

.score-summary-group {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.score-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    text-align: center;
    min-width: 100px;
}

.score-card .score-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
}

.score-card .score-label {
    font-size: 0.8rem;
    color: #bdc3c7;
    text-transform: uppercase;
}

.score-card.final-score .score-value { color: #f1c40f; }
.score-card.correct-answers .score-value { color: #2ecc71; }
.score-card.wrong-answers .score-value { color: #e74c3c; }
.score-card.unattempted .score-value { color: #95a5a6; }


/* --- MAIN CONTENT LAYOUT --- */
.summary-layout-container {
    padding: 2rem;
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.card-animated {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
}

/* --- QUESTION SUMMARY CARD --- */
.question-summary-card {
    padding: 2rem;
}

.question-header {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e9ecef;
}

.question-number {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c3e50;
}

.question-statement {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #34495e;
    margin-bottom: 2rem;
    min-height: 40px;
}

.options-container {
    display: grid;
    gap: 1rem;
}

.option-item {
    background-color: #f8f9fa;
    border: 2px solid #e0e6ed;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    position: relative;
}

.option-letter {
    font-weight: 700;
    color: #34495e;
    margin-right: 0.75rem;
}

/* --- CORE STYLES FOR CORRECT/INCORRECT/SELECTED --- */
.option-item.correct {
    background-color: #e8f5e9;
    border-color: #2ecc71;
    color: #1e8e3e;
    font-weight: 500;
}
.option-item.correct .option-letter { color: #2ecc71; }

.option-item.incorrect {
    background-color: #fbe9e7;
    border-color: #e74c3c;
    color: #c0392b;
    font-weight: 500;
}
.option-item.incorrect .option-letter { color: #e74c3c; }

.user-choice-indicator {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.75rem;
    font-weight: 600;
    background-color: #34495e;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 10px;
}
.option-item.correct .user-choice-indicator { background-color: #27ae60; }
.option-item.incorrect .user-choice-indicator { background-color: #c0392b; }

/* --- NEW: ACTION BUTTONS --- */
.summary-actions {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid #e9ecef;
    text-align: center;
}

.btn {
    border-radius: 8px;
    font-weight: 600;
    padding: 0.7rem 1.5rem;
    transition: all 0.3s ease;
    border: none;
    color: white;
    cursor: pointer;
    border-radius: 2rem;
}
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.btn-primary {
    background: linear-gradient(135deg, #3665ff, #2548cc) ;
    /* background: linear-gradient(to right, #ff6ec4, #0800ff); */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-dashboard {
    min-width: 220px;
    font-size: 1.1rem;
    padding: 0.8rem 2rem;
}

/* --- RESPONSIVE DESIGN --- */
@media (max-width: 768px) {
    .quiz-page-header {
        flex-direction: column;
        align-items: flex-start;
    }
    .score-summary-group {
        width: 100%;
        justify-content: space-between;
    }
    .score-card { flex-grow: 1; }
    .summary-layout-container { padding: 1rem; }
    .question-summary-card { padding: 1.5rem; }
}
</style>