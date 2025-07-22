<template>
    <div class="profile-page-wrapper">
        <!-- Navbar  -->
        <nav class="navbar">
            <h1>User Profile</h1>
            <div class="nav-links">
                <router-link to="/dashboard">Dashboard <i class="fas fa-tachometer-alt"></i></router-link>
                <router-link to="/search">Search <i class="fas fa-search"></i></router-link>
                <router-link to="/summary">Summary <i class="fas fa-chart-line"></i></router-link>
                <router-link to="/login">Logout <i class="fas fa-sign-out-alt"></i></router-link>
            </div>
        </nav>

        <!-- Main Profile Content-->
        <div class="profile-content-container">
            <div class="profile-grid">
                <div class="profile-main-column">
                    <div class="profile-card card-animated">
                        <div class="profile-header">
                            <div class="profile-avatar-wrapper">
                                <i class="fas fa-user-circle avatar-icon"></i>
                            </div>
                            <div class="profile-user-details">
                                <h2>{{ user.username }}</h2>
                                <p class="user-id">User ID: {{ user.uuid }}</p>
                                <p class="join-date">Joined: {{ user.created_at }}</p>
                            </div>
                        </div>
                        <form class="profile-form">
                            <!-- ... form content ... -->
                            <h3 class="form-section-title"><i class="fas fa-edit"></i> Edit Information</h3>
                            <div class="form-group">
                                <label for="username-display">Username</label>
                                <input type="text" id="username-display" :value="user.username" disabled>
                                <small class="form-text text-muted">Username cannot be changed.</small>
                            </div>

                            <div class="form-group">
                                <label for="email">Email Address</label>
                                <input type="email" id="email" v-model="editableUser.email" required>
                            </div>

                            <h3 class="form-section-title"><i class="fas fa-key"></i> Change Password</h3>
                            <div class="form-group">
                                <label for="password">New Password</label>
                                <input type="password" id="password" v-model="editableUser.password"
                                    placeholder="Still type your current password to do changes or change your password!" required> 
                            </div>
                            <div class="form-group">
                                <label for="confirmPassword">Confirm New Password</label>
                                <input type="password" id="confirmPassword" v-model="editableUser.confirmPassword"
                                    placeholder="Confirm new password" required>
                            </div>

                            <button type="submit" @click="saveProfileChanges(user.username, editableUser.email, editableUser.password, editableUser.confirmPassword)" class="btn btn-primary btn-save-changes">
                                <i class="fas fa-save"></i> Save Changes
                            </button>
                        </form>
                    </div>
                    <div class="account-actions-card card-animated">
                        <h3 class="form-section-title"><i class="fas fa-cog"></i> Account Actions</h3>
                        <button @click="confirmDeleteAccount" class="btn btn-danger btn-delete-account">
                            <i class="fas fa-trash-alt"></i> Delete Account
                        </button>
                        <!-- <small class="form-text text-muted">This action is irreversible.</small> -->
                    </div>
                    
                </div>

                <!-- Right Column: Preferences & Activity -->
                <div class="profile-side-column">
                    <div class="preferences-card card-animated">
                        <h3 class="section-title-alt"><i class="fas fa-sliders-h"></i> Your Preferences</h3>
                        
                        <div class="preference-item">
                            <h4><i class="fas fa-layer-group"></i> Selected Levels:</h4>
                            <p>
                                <span v-for="(level, index) in user.user_level" :key="level[0]">
                                    {{ level[1] }}{{ index < user.user_level.length - 1 ? ', ' : '' }}
                                </span>
                                <span v-if="!user.user_level || user.user_level.length === 0">None selected</span>
                            </p>
                        </div>
                        <div class="preference-item">
                            <h4><i class="fas fa-book"></i> Selected Subjects:</h4>
                            <p>
                                <span v-for="(subject, index) in user.user_selected_subject" :key="subject[0]">
                                    {{ subject[1] }}{{ index < user.user_selected_subject.length - 1 ? ', ' : '' }}
                                </span>
                                <span v-if="!user.user_selected_subject || user.user_selected_subject.length === 0">None selected</span>
                            </p>
                        </div>
                        <button @click="redirectstartdashbord" 
                            class="btn btn-secondary btn-manage-prefs">
                            <i class="fas fa-edit"></i> Manage Preferences
                        </button>

                    </div>
                </div>
            </div>
        </div>



        <!-- Footer (No changes here) -->
        <footer class="footer">
            <p>© 2025 Ischool. All Rights Reserved.</p>
        </footer>
    </div>
</template>

<script>
import axios from 'axios';
import vuecookies from 'vue-cookies';

export default {
    name: 'Profile',
    data() {
        return {
            user: { 
                uuid: '',
                username: '',
                email: '',
                created_at: '',
                user_level: [],
                user_selected_subject: [],
            },
            editableUser: {
                email: '',
                password: '',
                confirmPassword: ''
            },
            modalStep: 1, 
            allLevels: [], 
            allSubjects: [], 
            tempSelectedLevels: {}, 
            tempSelectedSubjects: {}, 
        };
    },
    methods: {
        async fetchUserProfile() {
            try {
                const token = vuecookies.get('access_token');
                const req = await axios.get(`http://127.0.0.1:5000/u/profile?token=${token}`);
                const userData = req.data.user_data;
                this.user.uuid = userData.user_id;
                this.user.username = userData.username;
                this.user.email = userData.email;
                this.editableUser.email = userData.email;
                this.user.created_at = userData.joined_on;
                this.user.user_level = userData.user_level || []; 
                this.user.user_selected_subject = userData.user_selected_subject || [];
            } catch (error) {
                console.log("Couldn't get user profile:", error);
            }
        },
        

        
        async saveProfileChanges(username, email, pass, confirmpass) {
            if (pass !== confirmpass) {
                alert("Passwords do not match!");
                return;
            }
            if (pass.length === 0 || confirmpass.length === 0) {
                alert("Please enter a password!");
                return;
            }
            const token = vuecookies.get('access_token');
            const senddata = new FormData();
            senddata.append('username', username);
            senddata.append('email', email);
            senddata.append('password', pass);
            senddata.append('id', this.user.uuid)
            alert(`Username: ${username}\nEmail: ${email}\nPassword: ${pass}`)
            const req = await axios.post(`http://127.0.0.1:5000/u/profile/edit?token=${token}`, senddata)
            this.fetchUserProfile();

        },

        confirmDeleteAccount() {
            const token = vuecookies.get('access_token');
            
            if (confirm("Are you sure you want to delete your account?")) {
                axios.post(`http://127.0.0.1:5000/u/profile/delete?token=${token}`) 
            }
            this.$router.push('/');

        }, 

        async redirectstartdashbord() {
            this.$router.push('/dashboard/start');
        }
    },
    mounted() {
        this.fetchUserProfile();
    }
}
</script>

<style scoped>
/* All your original CSS goes here. It is perfect and does not need to be changed. */
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
    color: #fff;
}
.navbar h1 {
    font-size: 28px;
    font-weight: 700;
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
.footer {
    margin-top: 40px;
    text-align: center;
    padding: 25px;
    background: #121212;
    color: #888;
    font-size: 14px;
    border-top: 1px solid #2a2a2a;
}
.profile-page-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    padding-bottom: 1px;
}
.profile-content-container {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
}
.profile-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 30px;
}
.profile-card,
.preferences-card,
.activity-summary-card,
.account-actions-card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    padding: 30px;
    margin-bottom: 30px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card-animated:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}
.profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #e9ecef;
}
.profile-avatar-wrapper {
    margin-right: 25px;
}
.avatar-icon {
    font-size: 80px;
    color: #3498db;
    background-color: #e9f5ff;
    border-radius: 50%;
    padding: 15px;
    display: block;
}
.profile-user-details h2 {
    font-size: 26px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 5px;
}
.user-id,
.join-date {
    font-size: 14px;
    color: #7f8c8d;
    margin-bottom: 3px;
}
.form-section-title {
    font-size: 18px;
    font-weight: 600;
    color: #34495e;
    margin-top: 25px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
}
.form-section-title i {
    margin-right: 10px;
    color: #3498db;
}
.form-section-title:first-of-type {
    margin-top: 0;
}
.form-group {
    margin-bottom: 20px;
}
.form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 8px;
    color: #495057;
    font-size: 14px;
}
.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="password"] {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #ced4da;
    border-radius: 6px;
    font-size: 15px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.form-group input:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    outline: none;
}
.form-group input:disabled {
    background-color: #e9ecef;
    cursor: not-allowed;
}
.form-text.text-muted {
    font-size: 13px;
    color: #6c757d;
    margin-top: 5px;
}
.btn-save-changes {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    margin-top: 10px;
}
.account-actions-card {
    text-align: center;
}
.btn-delete-account {
    width: auto;
    padding: 10px 25px;
    background: linear-gradient(135deg, #e74c3c, #c0392b);
}
.btn-delete-account:hover {
    background: linear-gradient(135deg, #c0392b, #a93226);
    box-shadow: 0 6px 15px rgba(231, 76, 60, 0.4);
}
.section-title-alt {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    align-items: center;
}
.section-title-alt i {
    margin-right: 10px;
    color: #3498db;
}
.preference-item {
    margin-bottom: 20px;
}
.preference-item h4 {
    font-size: 15px;
    font-weight: 500;
    color: #34495e;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
}
.preference-item h4 i {
    margin-right: 8px;
    color: #5dade2;
}
.preference-item p {
    font-size: 14px;
    color: #555;
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    border-left: 3px solid #3498db;
    word-break: break-word;
    min-height: 40px;
}
.btn-manage-prefs {
    width: 100%;
    background: #6c757d;
    padding: 10px;
}
.btn-manage-prefs:hover {
    background: #5a6268;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
.btn {
    background: linear-gradient(to right, #ff6ec4, #0800ff);
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.btn:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 6px 15px rgba(128, 0, 128, 0.3);
}
.btn:disabled {
    background: #cccccc;
    color: #666666;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}
.btn-primary {
    background: linear-gradient(to right, #3665ff, #2548cc);
}
.btn-primary:hover {
    box-shadow: 0 6px 15px rgba(54, 101, 255, 0.4);
}
.btn-secondary {
    background: #6c757d;
    color: white;
}
.btn-secondary:hover {
    background: #5a6268;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
.btn-danger {
    background: linear-gradient(135deg, #e74c3c, #c0392b);
}
.btn-danger:hover {
    background: linear-gradient(135deg, #c0392b, #a93226);
    box-shadow: 0 6px 15px rgba(231, 76, 60, 0.4);
}
.modal-body .list-group-item {
    cursor: pointer;
    transition: background-color 0.2s ease;
}
.modal-body .list-group-item:hover {
    background-color: #f0f2f5;
}
@media (max-width: 992px) {
    .profile-grid {
        grid-template-columns: 1fr;
    }
}
@media (max-width: 768px) {
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
    .profile-content-container {
        margin: 20px auto;
        padding: 0 15px;
    }
    .profile-card,
    .preferences-card,
    .activity-summary-card,
    .account-actions-card {
        padding: 20px;
    }
    .profile-header {
        flex-direction: column;
        text-align: center;
    }
    .profile-avatar-wrapper {
        margin-right: 0;
        margin-bottom: 15px;
    }
    .avatar-icon {
        font-size: 70px;
    }
    .profile-user-details h2 {
        font-size: 22px;
    }
}
@media (max-width: 576px) {
    .navbar h1 {
        font-size: 22px;
    }
    .form-group input[type="text"],
    .form-group input[type="email"],
    .form-group input[type="password"] {
        padding: 10px 12px;
        font-size: 14px;
    }
    .btn {
        font-size: 14px;
        padding: 9px 18px;
    }
    .btn-save-changes {
        padding: 10px;
    }
}
</style>