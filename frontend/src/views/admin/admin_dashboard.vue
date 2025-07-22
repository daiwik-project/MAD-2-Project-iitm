<template>
    <div class="admin-dashboard-wrapper">
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

        <!-- Main Dashboard Content -->
        <div class="dashboard-container">
            <h2 class="section-title">Manage Levels</h2>
            <div class="levels-grid">
                <!-- Level Cards -->
                <div class="level-card" v-for="(level, levelIndex) in levels" :key="levelIndex">
                    <div class="level-card-header">
                        <div class="level-card-icon">
                            <i class="fas fa-layer-group"></i>
                        </div>
                        <h3 class="level-card-title">{{ level[0] }}</h3>
                    </div>
                    
                    <p class="level-card-description">{{ level[1] }}</p>
                    
                    <div class="subjects-list">
                        <strong>Subjects:</strong>
                        <span v-if="level[3] && level[3].length > 0">
                            <span v-for="(subject, subIndex) in level[3]" :key="subIndex">
                                {{ subject }}<span v-if="subIndex < level[3].length - 1">, </span>
                            </span>
                        </span>
                        <span v-else class="text-muted">
                            No subjects assigned.
                        </span>
                    </div>

                    <div class="level-card-actions">
                        <button class="btn btn-action btn-view" @click="view_level_info(level[2])"><i class="fas fa-eye"></i> View</button>
                        <button class="btn btn-action btn-edit" :data-bs-toggle="'modal'" :data-bs-target="'#edit-'+ level[2]"><i class="fas fa-edit"></i> Edit</button>
                        <button class="btn btn-action btn-delete" @click="delete_level(level[2])"><i class="fas fa-trash"></i> Delete</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- MODALS ARE MOVED HERE, OUTSIDE THE MAIN CONTAINER AND THE V-FOR LOOP -->
        <div v-for="(level, levelIndex) in levels" :key="'modal-' + levelIndex">
            <div class="modal fade" :id="'edit-' + level[2]" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editModalLabel">Edit Level: {{ level[0] }}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="update_level(level[2], level[0], level[1])">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label :for="'level_name_' + level[2]" class="form-label">Level Name</label>
                                    <input type="text" class="form-control" :id="'level_name_' + level[2]" v-model="level[0]" required>
                                </div>
                                <div class="mb-3">
                                    <label :for="'level_des_' + level[2]" class="form-label">Level Description</label>
                                    <textarea class="form-control" :id="'level_des_' + level[2]" v-model="level[1]" rows="3" required></textarea>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save Changes</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- Floating Action Button -->
        <a class="btn-add-floating" href="/createlevel" title="Add New Level">
            <i class="fas fa-plus"></i>
        </a>

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
    name: 'AdminDashboard',
    data() {
        return {
            levels: [],
            update_info: {
                level_name: '',
                level_des: '',
                level_id: '',
            },

        };
    },
    methods: {



        async fetchLevels() {
            if (!VueCookies.get('admin_token')) {
                alert('You are not logged in.')
                this.$router.push('/admin/login')
                return;
            }
            try {
                const res = await axios.get('http://127.0.0.1:5000/api/admin_dashboard');
                const backendData = res.data;
                this.levels = backendData.info; 
                

            } catch (error) {
                alert('Error fetching Levels:', error);
            }
        },


        async view_level_info(level_id) {
            alert('View level info for ID: ' + level_id);
            this.$router.push(`/${level_id}/view/Level`);
        },

        async update_level(level_id, level_name, level_des){
            const formData = new FormData();
            formData.append('level_name', level_name);
            formData.append('level_description', level_des);
            try{
                const response = axios.post(`http://127.0.0.1:5000/admin_dashboard/${level_id}/update/level`, formData);
                alert('Level updated successfully!');
            }catch(error){
                console.error('Error updating subject:', error);
            }
        },

        async delete_level(level_id) {
            alert('Delete level info for ID: ' + level_id);
        },

        
    },
    mounted() {
        // await this.dologin();
        // await this.verify_admin();

        this.fetchLevels();
    }
}
</script>


<style scope>
/* General Page Wrapper */
.admin-dashboard-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- NAVBAR STYLING --- */
/* Base Navbar Style */
.navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 25px; /* Adjusted padding for responsiveness */
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}

/* Brand/Title Styling */
.navbar-brand {
    font-size: 26px;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

/* Hamburger Button Styling */
.navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.navbar-toggler:focus {
    box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}

/* Styling for the Links */
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

/* On mobile, when collapsed, remove the hover transform */
@media (max-width: 991.98px) {
    .navbar-nav .nav-link:hover,
    .navbar-nav .nav-link.active {
        transform: none;
    }
    .navbar-collapse {
        padding-top: 15px; /* Add some space above the links when menu is open */
    }
}


/* --- MAIN CONTENT STYLING (Unchanged) --- */
.dashboard-container {
    max-width: 1400px;
    margin: 30px auto;
    padding: 30px 40px;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}

.levels-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
}

.level-card {
    background: #ffffff;
    border: 1px solid #e0e6ed;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
}

.level-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 25px rgba(52, 152, 219, 0.15);
}

.level-card-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.level-card-icon {
    font-size: 24px;
    color: #3498db;
    background-color: rgba(52, 152, 219, 0.1);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
    flex-shrink: 0;
}

.level-card-title {
    font-size: 18px;
    font-weight: 600;
    color: #34495e;
    margin: 0;
}

.level-card-description, .subjects-list {
    font-size: 14px;
    color: #555;
    line-height: 1.6;
    margin-bottom: 15px;
    white-space: normal;
    text-overflow: initial;
    word-break: break-word;
    flex-grow: 1;
}

.subjects-list {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 6px;
    border-left: 3px solid #bdc3c7;
}

.level-card-actions {
    margin-top: auto;
    padding-top: 15px;
    border-top: 1px solid #f0f2f5;
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}

.btn-action {
    padding: 6px 12px;
    font-size: 13px;
    border-radius: 5px;
    border: none;
    color: white;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: all 0.2s ease;
}
.btn-action:hover {
    transform: scale(1.05);
    filter: brightness(1.1);
}
.btn-view { background-color: #3498db; }
.btn-edit { background-color: #f1c40f; }
.btn-delete { background-color: #e74c3c; }

.btn-add-floating {
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
    box-shadow: 0 6px 20px rgba(54, 101, 255, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.btn-add-floating:hover {
    transform: translateY(-5px) scale(1.1);
    box-shadow: 0 10px 25px rgba(54, 101, 255, 0.5);
}

.modal-content {
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: none;
}
.modal-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
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

@media (max-width: 768px) {
    .dashboard-container {
        padding: 20px 15px;
    }
    .levels-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 576px) {
    .navbar {
        padding: 15px 20px;
    }
    .navbar-brand {
        font-size: 22px;
    }
    .btn-add-floating {
        width: 50px;
        height: 50px;
        font-size: 24px;
        bottom: 20px;
        right: 20px;
    }
}
</style>