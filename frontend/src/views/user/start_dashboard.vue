<!-- 
 * we have to add a model in which user will see the list of 
 subjects which are related to the level he selected
  * and then he will select the subject and then 
  then again a new model is opened in which he will select the chapters to bookmark

  -->

<template>
    <div>
        <!-- Navbar -->
        <nav class="navbar">
            <h1>Start Your Journey</h1>
            <div class="nav-links">
                <router-link to="/dashboard">Dashboard <i class="fas fa-tachometer-alt"></i></router-link>
                <router-link to="/search">Search <i class="fas fa-search"></i></router-link>
                <router-link to="/summary">Summary <i class="fas fa-chart-line"></i></router-link>
                <router-link to="/profile">Profile <i class="fas fa-user"></i></router-link>
                <router-link to="/login">Logout <i class="fas fa-sign-out-alt"></i></router-link>
            </div>
        </nav>

        <div class="start-page-container">
            <div class="controls-header">
                <h2>Select Your Learning Levels</h2>
                <div class="select-all-container">
                    <label for="selectAllCheckbox">
                        <!-- <input type="checkbox" @change="select_all"  id="selectAllCheckbox" /> -->
                        <input type="checkbox" id="selectAllCheckbox" v-model="selectAll" @change="handleSelectAll" />

                        Select All Levels
                    </label>
                </div>
            </div>

            <div class="levels-grid container">
                <div class="row" v-for="(l, index) in level" :key="index">
                    <!-- Level cards will be rendered here -->
                    <div class="">
                        <div class="level-card " @click="selected_level(l[0], l[2])">
                            <h3 class="level-name" :title="l[0]"
                                style="overflow: hidden !important; white-space: nowrap; text-overflow: ellipsis;">{{
                                    l[0] }} </h3>

                            <p :title="l[1]" class="level-description"
                                style="white-space: nowrap; text-overflow: ellipsis;">{{ l[1] }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="selected-levels-display">
                <h3 style="color: aliceblue;">Selected Levels:</h3>
                <ul>
                    <li v-for="(id, name) in selectedLevels" :key="name">
                        {{ name }}

                        <button @click="removeLevel(name)" class="remove-btn" title="Remove Level">
                            <i class="fas fa-times-circle"></i>
                        </button>

                    </li>

                    <!-- Selected levels will be displayed here -->
                </ul>
                <button class="btn" @click="sendinfo" data-bs-toggle="modal"
                    data-bs-target="#edit-model">Proceed</button>

            </div>


            <!-- Modal -->
            <div class="modal fade" id="edit-model" tabindex="-1" aria-labelledby="exampleModalLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header d-flex flex-column align-items-start position-relative">
                            <h1 class="modal-title fs-5 mb-2" id="exampleModalLabel">Select Your Subjects</h1>
                            <p class=" mb-2">These You Will got notification w.r.t these Subjects</p>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="subjects-grid container">


                                <!-- Only render this row if the subject list has items -->
                                <div v-for="(sublis, level_title) in subjects_l">
                                    <div v-if="sublis.length > 0" class="row subjects-card" :key="level_title">
                                        <div v-for="sub in sublis" @click="select_sub(sub[0], sub[1])">
                                            <h3 class="subject-name"
                                                style="overflow: hidden !important; white-space: nowrap; text-overflow: ellipsis;">
                                                {{ sub[1] }}
                                            </h3>

                                            <p :title="sub[2]" class="level-description"
                                                style="white-space: nowrap; text-overflow: ellipsis;">
                                                {{ sub[2] }}
                                            </p>
                                            <i class="mt-4">By Level {{ level_title }}</i>
                                        </div>
                                    </div>
                                </div>



                            </div>
                            <div class="selected-sub-display">
                                <h3 style="color: aliceblue;">Selected Subjects:</h3>
                                <ul>
                                    <li v-for="(id, name) in selectedSub" :key="name">
                                        {{ name }}
                                        <button @click="removesub(name)" class="remove-btn" title="Remove Subject">
                                            <i class="fas fa-times-circle"></i>
                                        </button>

                                    </li>

                                    <!-- Selected levels will be displayed here -->
                                </ul>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" @click="send_sub">Save changes</button>
                        </div>
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
    name: 'StartDashboardPage',
    data() {
        return {
            level: [],
            selectedLevels: {},
            selectAll: false,
            subjects_l: {},
            selectedSub: {}
        }
    },
    methods: {

        async send_sub() {
            try {
                const token = vuecookies.get('access_token');

                const req = await axios.post(`http://127.0.1:5000/api/start/select_sub?token=${token}`, this.selectedSub);
                alert(req.data.message);
                this.$router.push('/dashboard');

            } catch (error) {
                throw new Error("Heyerror is here")
            }
        },
        async fetchLevels() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/level_info',  
                );
                const backendData = response.data;
                this.level = backendData.info; 

            } catch (error) {
                console.error('Error fetching levels:', error);
            }
        },
        async sendinfo() {
            const token = vuecookies.get('access_token');
            console.log(this.selectedLevels)
            const req = await axios.post(`http://127.0.1:5000/api/start/select_level?token=${token}`, this.selectedLevels);
            console.log(req.data.subjects);
            this.subjects_l = req.data.subjects

        },
        async select_sub(id, name) {
            this.selectedSub[name] = id;
        },
        async selected_level(name, id) {
            // Handle level selection
            const lev = [name, id];
            this.selectedLevels[name] = id;
        },
        async removeLevel(name) {
            delete this.selectedLevels[name];
        },
        async removesub(name) {
            delete this.selectedSub[name];
        },
        async handleSelectAll() {
            if (this.selectAll) {
                for (let i = 0; i < this.level.length; i++) {
                    this.selectedLevels[this.level[i][0]] = this.level[i][2];
                }
            } else {
                this.selectedLevels = {};
            }
        },

    },
    mounted() {

        this.fetchLevels();
    },
}
</script>





<style scoped>
/* --- General Page Layout & Container --- */
/* This mimics the clean, card-on-background look from Page A */
.start-page-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.start-page-container {
    background-color: #ffffff;
    color: #333333;
    max-width: 1200px;
    margin: 30px auto;
    padding: 30px 40px;
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* --- Navbar --- */
/* Identical style to Page A for consistency */
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

/* --- Controls Header (Select Levels) --- */
/* Styled like a section header from Page A */
.controls-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 2px solid #e0e0e0;
}

.controls-header h2 {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.select-all-container label {
    font-size: 16px;
    color: #555;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
}

.select-all-container input[type="checkbox"] {
    accent-color: #3498db;
    transform: scale(1.2);
}

/* --- Level & Subject Cards --- */
/* This is the core style, making your cards look like the Chapter Boxes from Page A */
.levels-grid,
.subjects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
    margin-top: 30px;
}

.level-card,
.subjects-card>div {
    /* Target the inner div for subjects */
    background: #ffffff;
    border: 1px solid #e0e6ed;
    border-radius: 10px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    text-align: left;
}

.level-card:hover,
.subjects-card>div:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 25px rgba(52, 152, 219, 0.2);
}

.level-name,
.subject-name {
    font-size: 18px;
    font-weight: 600;
    color: #34495e;
    margin-bottom: 10px;
    min-height: 44px;
}

.level-description {
    font-size: 14px;
    color: #7f8c8d;
    line-height: 1.5;
    flex-grow: 1;
    /* Allows description to fill space */
    margin-bottom: 10px;
}

.subjects-card i {
    font-size: 13px;
    color: #95a5a6;
    margin-top: auto;
    /* Pushes it to the bottom */
}

/* --- Selected Items Display --- */
/* A clean, light box for showing selections */
.selected-levels-display,
.selected-sub-display {
    margin-top: 40px;
    background-color: #f8f9fa;
    padding: 20px 25px;
    border-radius: 8px;
    border: 1px solid #e9ecef;
}

.selected-levels-display h3,
.selected-sub-display h3 {
    color: #2c3e50;
    font-size: 18px;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 15px;
}

.selected-levels-display ul,
.selected-sub-display ul {
    padding-left: 0;
    list-style: none;
    margin-bottom: 0;
}

.selected-levels-display li,
.selected-sub-display li {
    background: #ffffff;
    padding: 12px 20px;
    margin: 8px 0;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #34495e;
    font-weight: 500;
    border: 1px solid #e9ecef;
}

/* --- Buttons --- */
/* Unified button styles from Page A */
.btn {
    background: linear-gradient(to right, #ff6ec4, #0800ff);
    color: #fff;
    padding: 12px 25px;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    margin-top: 20px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.btn:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 8px 20px rgba(52, 152, 219, 0.3);
}

.btn-secondary {
    background: #6c757d;
}

.btn-secondary:hover {
    background: #5a6268;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* Style for the remove button in the list */
.remove-btn {
    background: none;
    border: none;
    color: #e74c3c;
    cursor: pointer;
    font-size: 1.2rem;
    padding: 5px;
    line-height: 1;
    transition: color 0.2s ease, transform 0.2s ease;
}

.remove-btn:hover {
    color: #c0392b;
    transform: scale(1.1);
}

/* --- Modal Styling --- */
/* IMPORTANT: You need to change the modal class in your HTML for this to work */
/* Change `modal-fullscreen` to `modal-lg modal-dialog-centered` */
.modal-content {
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: none;
}

.modal-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
    padding: 1rem 1.5rem;
}

.modal-header .modal-title {
    font-weight: 600;
    color: #343a40;
    font-size: 1.2rem;
}

.modal-header p {
    color: #6c757d;
    font-size: 0.9rem;
    margin: 0;
}

.modal-header .btn-close {
    position: absolute;
    top: 1.2rem;
    right: 1.2rem;
    transition: transform 0.2s ease;
}

.modal-header .btn-close:hover {
    transform: scale(1.1);
}

.modal-body {
    padding: 1.5rem;
    background-color: #f0f2f5;
    /* Light gray background for modal body */
}

.modal-footer {
    background-color: #f8f9fa;
    border-top: 1px solid #dee2e6;
    padding: 1rem 1.5rem;
}

/* --- Footer --- */
/* Identical style to Page A */
.footer {
    margin-top: 40px;
    text-align: center;
    padding: 25px;
    background: #121212;
    color: #888;
    font-size: 14px;
    border-top: 1px solid #2a2a2a;
}

/* --- Responsive Tweaks --- */
@media (max-width: 768px) {
    .start-page-container {
        margin: 20px 15px;
        padding: 20px;
    }

    .navbar {
        flex-direction: column;
        gap: 15px;
        padding: 20px;
    }

    .controls-header {
        flex-direction: column;
        gap: 15px;
        text-align: center;
    }

    .btn {
        width: 100%;
    }

    .selected-levels-display li,
    .selected-sub-display li {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .remove-btn {
        align-self: flex-end;
    }
}
</style>
