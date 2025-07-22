<template>
    <div class="create-level-wrapper">
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
                <h2 class="section-title">Create New Level</h2>
                <button class="btn btn-back" @click="$router.push(`/admindashboard`)">
                    <i class="fas fa-arrow-left"></i> Back to Dashboard
                </button>
            </div>

            <!-- Create Form Card -->
            <div class="form-card">
                <div class="form-card-header">
                    <div class="form-card-icon">
                        <i class="fas fa-layer-group"></i>
                    </div>
                    <div class="form-card-title">
                        <h3>Level Information</h3>
                        <p>Fill out the details below to add a new level.</p>
                    </div>
                </div>
                <form @submit.prevent="create_level">
                    <div class="form-group">
                        <label for="level_name">Level Name</label>
                        <input type="text" class="form-control" v-model="level_name" id="level_name" placeholder="e.g., Beginner Python" required>
                    </div>
                    <div class="form-group">
                        <label for="level_description">Description</label>
                        <textarea class="form-control" v-model="level_description" id="level_description" placeholder="Enter a brief description of this level..." rows="4" required></textarea>
                    </div>
                    <div class="form-actions">
                        <button type="reset" class="btn btn-secondary">
                            <i class="fas fa-undo"></i> Reset
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i> Create Level
                        </button>
                    </div>
                </form>
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
    name: 'CreateLevel',
    data() {
        return {
            level_name: '',
            level_description: '',
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
        async create_level(){

            const level_data = new FormData();
            level_data.append('level_name', this.level_name);
            level_data.append('level_description', this.level_description);

            try {
                const response = await axios.post('http://127.0.0.1:5000/admin_dashboard/create/level', level_data);
                const levelId = response.data.level_id;

                alert('Level created successfully! ' + response.data.message);
                this.$router.push(`/${levelId}/createsubject`);

            } catch (error) {
                // console.error(error);
                alert(`Error creating level! ${error.message}`);
            }
        }
    },
    mounted() {
        this.checker();
    },
};
</script>

<style scoped>
/* General Page Wrapper */
.create-level-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- NAVBAR STYLING (Consistent with other pages) --- */
.create-level-wrapper .navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 25px;
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}
.create-level-wrapper .navbar-brand {
    font-size: 26px;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}
.create-level-wrapper .navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.create-level-wrapper .navbar-toggler:focus {
    box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}
.create-level-wrapper .navbar-nav .nav-link {
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
.create-level-wrapper .navbar-nav .nav-link:hover,
.create-level-wrapper .navbar-nav .nav-link.active {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}
@media (max-width: 991.98px) {
    .create-level-wrapper .navbar-nav .nav-link:hover,
    .create-level-wrapper .navbar-nav .nav-link.active {
        transform: none;
    }
    .create-level-wrapper .navbar-collapse {
        padding-top: 15px;
    }
}

/* --- MAIN CONTENT STYLING --- */
.create-level-wrapper .dashboard-container {
    max-width: 800px; /* Optimal width for a form */
    margin: 30px auto;
    padding: 0 20px;
}

.create-level-wrapper .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.create-level-wrapper .section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.create-level-wrapper .btn-back {
    background-color: #fff;
    color: #34495e;
    border: 1px solid #e0e6ed;
    padding: 8px 16px;
    font-weight: 500;
    border-radius: 6px;
    transition: all 0.2s ease;
}
.create-level-wrapper .btn-back:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Form Card */
.create-level-wrapper .form-card {
    background: #ffffff;
    padding: 30px 35px;
    border-radius: 12px;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.07);
}

.create-level-wrapper .form-card-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #e9ecef;
}
.create-level-wrapper .form-card-icon {
    font-size: 28px;
    color: #3498db;
    background-color: rgba(52, 152, 219, 0.1);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.create-level-wrapper .form-card-title h3 {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0 0 5px 0;
}
.create-level-wrapper .form-card-title p {
    font-size: 14px;
    color: #7f8c8d;
    margin: 0;
}

.create-level-wrapper .form-group {
    margin-bottom: 25px;
}
.create-level-wrapper .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 8px;
    color: #495057;
    font-size: 15px;
}
.create-level-wrapper .form-control {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #ced4da;
    border-radius: 6px;
    font-size: 15px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.create-level-wrapper .form-control:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    outline: none;
}

.create-level-wrapper .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #e9ecef;
}
.create-level-wrapper .btn {
    padding: 10px 25px;
    font-size: 15px;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    border-radius: 6px;
}

/* Footer */
.create-level-wrapper .footer {
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
    .create-level-wrapper .dashboard-container {
        padding: 0 15px;
    }
    .create-level-wrapper .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
}
@media (max-width: 576px) {
    .create-level-wrapper .form-card {
        padding: 25px 20px;
    }
    .create-level-wrapper .form-actions {
        flex-direction: column;
    }
    .create-level-wrapper .form-actions .btn {
        width: 100%;
    }
}
</style>