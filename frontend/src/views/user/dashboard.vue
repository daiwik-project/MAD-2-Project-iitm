<template>
    <div class="dashboard-page-wrapper">
        <!-- Navbar -->
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

        <!-- Main Dashboard Content -->
        <div class="dashboard-container">
            <!-- Section 1: Chapter Boxes -->
            <section class="chapters-section">
                <h2 class="section-title">Your Chapters</h2>
                <div class="chapters-grid" >

                    <div class="chapter-box" v-for="chapter in chapters" :key="chapter[0]">
                        <div class="chapter-box-icon">
                            <i class="fas fa-book"></i>
                        </div>
                        <h3 class="chapter-box-title">{{ chapter[1] }}</h3>
                        <p class="chapter-box-description"> {{ chapter[2] }}</p>
                        <i class="chapter-box-description">From Subject: {{ chapter[3] }} </i>
                        <button class="btn btn-view-chapter" @click="view_the_chap(chapter[0])">View Chapter</button>

                    </div>
                </div>
            </section>

            <!-- Section 2: Upcoming Quizzes Table -->
            <section class="quizzes-section">
                <h2 class="section-title">Upcoming Quizzes</h2>
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
                            <tr v-for="(quiz, index) in quizzes" :key="quiz[0]">
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

            <!-- Button to trigger the single chapter preference modal -->
            <div style="margin-top: 30px; text-align: center;">
                <button class="btn btn-primary" @click="list_all_chapters_from_user_sub" data-bs-toggle="modal" data-bs-target="#chapterPreferenceModal">
                    <i class="fas fa-cogs"></i> Manage Chapter Preferences
                </button>
            </div>

        </div> 

        <div class="modal fade" id="chapterPreferenceModal" tabindex="-1" aria-labelledby="chapterPreferenceModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="chapterPreferenceModalLabel"><i class="fas fa-cogs"></i> Manage Chapter Preferences</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p class="text-muted">Select chapters you want to focus on or bookmark for quick access.</p>
                        <ul class="list-group" v-for="(chapter, index) in all_chapters_for_prefrence" :key="chapter[0]">
                            <li class="list-group-item">
                                <input class="form-check-input me-2" 
                                type="checkbox" 
                                :checked="isChapterInUserList(chapter[0])" 
                                :id="'chapterSelect' + index"
                                @click="adding_bookmark(chapter[0], chapter[1])"
                                >
                                <label class="form-check-label" for="chapterSelect1">Chapter {{ index+1 }}: {{ chapter[1] }}</label>
                            </li>
                        </ul>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="senduser_fav_chapter">Save Preferences</button>
                    </div>
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
    name: 'DashboardPage',
    data() {
        return {
            // empty
            chapters: [],
            quizzes: [],
            all_chapters_for_prefrence: [],
            bookemarked_chapters_currently_from_user: [],

            // below list captures the list of all uuid of users fav chapters.
            user_fav_chapter: {}
        };
    },
    methods: {
        // empty
        async list_all_chapters_n_quiz() {
            // Logic to fetch all chapters
            const token = vuecookies.get('access_token');
            try {
                const req = await axios.get(`http://127.0.0.1:5000/dashboard/chapter_n_quiz?token=${token}`);
                this.chapters = req.data.chapters;
                this.quizzes = req.data.quiz;
                console.log(this.chapters)

            }catch (error) {
                console.error('Error fetching chapters:', error);
            }

        },
        async view_the_chap(chapter_id){
            this.$router.push(`/dashboard/chapter/${chapter_id}`);
        }, 

        async list_all_chapters_from_user_sub() {
            const token = vuecookies.get('access_token');
            try {
                const req = await axios.get(`http://127.0.0.1:5000/dashboard/chapter_preference?token=${token}`);
                this.all_chapters_for_prefrence = req.data.all_chapters;

                this.user_fav_chapter = {};
                // Auto-add already bookmarked chapters into the dictionary
                // Now, we loop through the chapters already on the dashboard (`this.chapters`)
                // and add each one to our `user_fav_chapter` object.
                // This gives us the correct starting point.
                for (let i = 0; i < this.chapters.length; i++) {
                    let currentChapter = this.chapters[i];
                    let chapterId = currentChapter[0];
                    let chapterName = currentChapter[1];
                    this.user_fav_chapter[chapterName] = chapterId;
                }
                console.log("Modal opened. Starting favorites:", this.user_fav_chapter);


            } catch (error) {
                console.error('Error fetching chapters from user subscription:', error);
            }
        },

        
        isChapterInUserList(chapterId) {
            for (let i = 0; i < this.chapters.length; i++) {
                if (this.chapters[i][0] === chapterId) {
                    return true;
                }
            }
            return false;
        },
        //  Make this function ADD or REMOVE from the list
        async adding_bookmark(chapter_id, chapter_name) {
            // We DO NOT erase the list here anymore.

            // We check if the chapter is already in our list of favorites.
            if (this.user_fav_chapter[chapter_name]) {
                // If it exists, the user is UNCHECKING the box.
                // So, we must REMOVE it from our list.
                // The 'delete' keyword is the simplest way to remove a property from an object.
                delete this.user_fav_chapter[chapter_name];
                console.log("REMOVED:", chapter_name);
            } else {
                // If it does not exist, the user is CHECKING the box.
                // So, we ADD it to our list.
                this.user_fav_chapter[chapter_name] = chapter_id;
                console.log("ADDED:", chapter_name);
            }
        },
        async senduser_fav_chapter(){
            const token = vuecookies.get('access_token');
            try {
                const req = await axios.post(`http://127.0.0.1:5000/dashboard/user_chapter_preference?token=${token}`, this.user_fav_chapter);

            }catch (error) {
                console.error('Error fetching chapters from user subscription:', error);
            }
        },
        startQuiz(quiz_id, attempt_number){
            this.$router.push(`/dashboard/attempt/${quiz_id}/attempt_=${attempt_number+1}`)
        },
        reattemptQuiz(quiz_id, attempt_number){
            attempt_number = attempt_number + 1;
            this.$router.push(`/dashboard/attempt/${quiz_id}/attempt_=${attempt_number}`)
        }


    },
    mounted() {
        this.list_all_chapters_n_quiz();
    }
};
</script>

<style scoped>
/* Inherit Navbar and Footer styles from your global/existing styles if they match the example.
   If not, you can copy the relevant styles from your `startDashboard` example here.
   For brevity, I'm assuming these are globally available or you'll add them.
   Here are the styles specific to this DashboardPage and its new elements. */

/* Navbar (Styles from your example, slightly adapted) */
.navbar {
    background: rgba(15, 12, 41, 0.95);
    /* Dark, sophisticated */
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
    /* Light gray background for the whole page, if header/footer are not full width */
    min-height: 100vh;
}

.dashboard-container {
    background-color: #ffffff;
    /* White main content area */
    color: #333333;
    /* Dark text for readability */
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
    /* Dark blue-gray */
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
    /* Accent color */
    margin-right: 10px;
    border-radius: 3px;
}


/* Chapters Section */
.chapters-section {
    margin-bottom: 40px;
}

.chapters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
}

.chapter-box {
    background: #ffffff;
    border: 1px solid #e0e6ed;
    border-radius: 10px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.chapter-box:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 10px 25px rgba(52, 152, 219, 0.2);
    /* Brighter shadow on hover */
}

.chapter-box-icon {
    font-size: 32px;
    color: #3498db;
    /* Primary theme color */
    margin-bottom: 15px;
    background-color: rgba(52, 152, 219, 0.1);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chapter-box-title {
    font-size: 18px;
    font-weight: 600;
    color: #34495e;
    margin-bottom: 10px;
    min-height: 44px;
    /* Ensure consistent height for titles */
}

.chapter-box-description {
    font-size: 14px;
    color: #7f8c8d;
    margin-bottom: 20px;
    flex-grow: 1;
    /* Make description take available space */
    line-height: 1.5;
}

.btn-view-chapter {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    font-weight: 500;
    padding: 10px 20px;
    border-radius: 20px;
    /* Pill shape */
    font-size: 14px;
}

.btn-view-chapter:hover {
    background: linear-gradient(135deg, #2980b9, #1f638f);
    transform: scale(1.05);
}


/* Quizzes Section */
.quizzes-section {
    margin-top: 50px;
}

.table-responsive-wrapper {
    overflow-x: auto;
    /* Ensures table is scrollable on small screens */
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    padding: 10px;
    /* Add some padding around the table itself */
}

.quiz-table {
    width: 100%;
    border-collapse: separate;
    /* Use separate for border-radius on cells */
    border-spacing: 0;
    font-size: 14px;
    color: #333;
}

.quiz-table th,
.quiz-table td {
    padding: 15px 12px;
    text-align: left;
    border-bottom: 1px solid #e8ebee;
    /* Lighter border */
    vertical-align: middle;
}

.quiz-table th {
    background-color: #f8f9fa;
    /* Very light gray for header */
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


.quiz-table tbody tr {
    transition: background-color 0.2s ease;
}

.quiz-table tbody tr:hover {
    background-color: #f1f5f8;
    /* Subtle hover effect */
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
    /* Quiz Title */
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

.action-buttons .btn i {
    font-size: 1em;
    /* Relative to button font size */
}


/* General Button Styles (can be merged with your existing .btn) */
.btn {
    /* Using your existing gradient button style as a base for primary actions */
    background: linear-gradient(to right, #ff6ec4, #0800ff);
    color: #fff;
    padding: 10px 20px;
    /* Adjusted padding */
    border: none;
    border-radius: 6px;
    /* Slightly less rounded than pill */
    font-weight: 500;
    /* Adjusted weight */
    font-size: 15px;
    /* Adjusted size */
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    text-decoration: none;
    /* For router-link styled as button */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 6px 15px rgba(128, 0, 128, 0.3);
    /* Adjusted shadow for purple gradient */
}

.btn:disabled {
    background: #cccccc;
    color: #666666;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.btn-start-quiz {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
    /* Green gradient */
}

.btn-start-quiz:hover {
    background: linear-gradient(135deg, #27ae60, #229954);
    box-shadow: 0 6px 15px rgba(39, 174, 96, 0.3);
}

.btn-reattempt-quiz {
    background: linear-gradient(135deg, #e67e22, #d35400);
    /* Orange gradient */
}

.btn-reattempt-quiz:hover {
    background: linear-gradient(135deg, #d35400, #c0392b);
    box-shadow: 0 6px 15px rgba(230, 126, 34, 0.3);
}

.btn-secondary {
    /* For modal close, etc. */
    background: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background: #5a6268;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.btn-primary {
    /* For modal save, main actions */
    background: linear-gradient(to right, #3665ff, #2548cc);
    /* A more standard blue */
}

.btn-primary:hover {
    box-shadow: 0 6px 15px rgba(54, 101, 255, 0.4);
}


/* Modal Styling */
.modal-content {
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: none;
}

.modal-header {
    background-color: #f8f9fa;
    /* Light header */
    border-bottom: 1px solid #dee2e6;
    padding: 1rem 1.5rem;
}

.modal-header .modal-title {
    font-weight: 600;
    color: #343a40;
    font-size: 1.1rem;
}

.modal-header .btn-close {
    transition: transform 0.2s ease;
}

.modal-header .btn-close:hover {
    transform: scale(1.1);
}

.modal-body {
    padding: 1.5rem;
    font-size: 0.95rem;
    color: #495057;
}

.modal-body .list-group-item {
    transition: background-color 0.2s ease;
    border-radius: 6px;
    margin-bottom: 8px;
    border-color: #e9ecef;
}

.modal-body .list-group-item:hover {
    background-color: #e9f5ff;
    /* Light blue hover for list items */
    border-left: 3px solid #007bff;
}

.modal-body .list-group-item h6 {
    color: #0056b3;
}

.modal-body .form-check-input {
    border-color: #adb5bd;
}

.modal-body .form-check-input:checked {
    background-color: #007bff;
    border-color: #007bff;
}


.modal-footer {
    background-color: #f8f9fa;
    border-top: 1px solid #dee2e6;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: flex-end;
    /* Align buttons to the right */
}

.modal-footer .btn {
    min-width: 100px;
}


/* Footer (Styles from your example) */
.footer {
    margin-top: 40px;
    /* Reduced margin if dashboard container has its own */
    text-align: center;
    padding: 25px;
    background: #121212;
    /* Dark footer */
    color: #888;
    font-size: 14px;
    border-top: 1px solid #2a2a2a;
}

/* Responsive adjustments */
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

    .nav-links a {
        font-size: 14px;
        padding: 6px 10px;
    }

    .section-title {
        font-size: 20px;
    }

    .chapters-grid {
        grid-template-columns: 1fr;
        /* Stack chapter boxes on smaller screens */
    }

    .quiz-table th,
    .quiz-table td {
        padding: 10px 8px;
        font-size: 13px;
    }

    .action-buttons {
        flex-direction: column;
        /* Stack buttons in table on small screens */
        align-items: flex-start;
    }

    .action-buttons .btn {
        width: 100%;
        /* Make buttons full width in column */
        margin-bottom: 5px;
    }

    .action-buttons .btn:last-child {
        margin-bottom: 0;
    }
}

@media (max-width: 576px) {
    .navbar h1 {
        font-size: 22px;
    }

    .modal-dialog {
        margin: 0.5rem;
        /* Smaller margin for modals on very small screens */
    }

    .modal-body,
    .modal-header,
    .modal-footer {
        padding: 1rem;
    }
}
</style>
