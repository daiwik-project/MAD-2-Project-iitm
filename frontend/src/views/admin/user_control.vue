<template>
    <div class="admin-user-control-wrapper">
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
                            <a class="nav-link" href="/admindashboard"><i class="fas fa-book"></i> Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/a/summary"><i class="fas fa-chart-line"></i> Summary</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/a/search"><i class="fas fa-question-circle"></i> Search</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/user-control"><i class="fas fa-users-cog"></i> User control</a>
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
            <h2 class="section-title">User Control & Management</h2>

            <!-- Search Form Card -->
            <div class="search-card">
                <form @submit.prevent="performSearch" class="search-form">
                    <div class="form-group input-group">
                        <i class="fas fa-user-tag form-icon"></i>
                        <input type="text" class="form-control" v-model="searchQuery"
                            placeholder="Type a User ID or Username..." @keyup.enter="performSearch" required>
                    </div>
                    <button type="submit" class="btn btn-primary search-button" :disabled="isLoading">
                        <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <i v-else class="fas fa-search"></i>
                        <span>{{ isLoading ? 'Searching...' : 'Search' }}</span>
                    </button>
                </form>
            </div>

            <!-- Search Results Area -->
            <div class="results-card">
                <div v-if="isLoading" class="loading-state">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p>Searching for users...</p>
                </div>

                <div v-else-if="searchResults.length > 0" class="table-responsive-wrapper">
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>User ID</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th class="text-center">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in searchResults" :key="user.uuid">
                                <td data-label="User ID">{{ user.uuid }}</td>
                                <td data-label="Username">{{ user.username }}</td>
                                <td data-label="Email">{{ user.email }}</td>
                                <td data-label="Action" class="action-cell">
                                    <button v-if="user.block_status == true" class="btn btn-action btn-block" @click="blockuser(user.uuid)">
                                        <i class="fas fa-user-lock"></i> Block 
                                    </button>
                                    <button v-else class="btn btn-action btn-unblock" @click="unblockuser(user.uuid)">
                                        <i class="fas fa-user-check"></i> Unblock 
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-else-if="hasSearched" class="empty-state">
                    <i class="fas fa-user-slash empty-icon"></i>
                    <h3>No Users Found</h3>
                    <p>Your search for "{{ searchQuery }}" did not return any results. Please try another name or ID.</p>
                </div>
                
                <div v-else class="empty-state">
                    <i class="fas fa-search empty-icon"></i>
                    <h3>Find a User</h3>
                    <p>Use the search bar above to find and manage users in the system.</p>
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
    name: 'UserControl',

    data() {
        return {
            searchQuery: '',
            searchResults: [],
            isLoading: false,
            hasSearched: false,
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
        // This function is called when the Search button is clicked or Enter is pressed
        async performSearch() {
            // Re-enabled this check. 
            if (!this.searchQuery.trim()) {
                this.searchResults = [];
                this.hasSearched = false;
                return;
            }

            this.isLoading = true;
            this.hasSearched = true;

            try {
                const response = await axios.get('http://127.0.0.1:5000/api/admin/find_users', {
                    params: {
                        query: this.searchQuery
                    }
                });
                
                console.log("Data received from API:", response.data);
                this.searchResults = response.data.users;

            } catch (error) {
                console.error('Error searching for users:', error);
                alert('An error occurred while fetching user data.');
                this.searchResults = []; 
            } finally {
                this.isLoading = false;
            }
        },

        handleUserAction(user) {
            console.log('Admin clicked action for user:', user);
            console.log('Selected User ID is:', user.uuid);
            alert(`You clicked on user: ${user.username} (ID: ${user.uuid})`);
        },

        async blockuser(user_id) {
            try {
                const url = 'http://127.0.0.1:5000/api/admin/block_user';
                
                const data = { user_id: user_id };

                await axios.post(url, data);

                alert('User blocked successfully!');
                const user = this.searchResults.find(u => u.uuid === user_id);
                if (user) {
                    user.block_status = true; 
                }

            } catch (error) {
                console.error('Error blocking user:', error);
                alert('Failed to block user.');
            }
        },

        async unblockuser(user_id) {
            try {
                const url = 'http://127.0.0.1:5000/api/admin/unblock_user';
                const data = { user_id: user_id };

                await axios.post(url, data);

                alert('User unblocked successfully!');

                const user = this.searchResults.find(u => u.uuid === user_id);
                if (user) {
                    user.block_status = false; 
                }

            } catch (error) {
                console.error('Error unblocking user:', error);
                alert('Failed to unblock user.');
            }
        }

    },
    mounted() {
        this.checker();
    }
};
</script>

<style scoped>
/* General Page Wrapper */
.admin-user-control-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- NAVBAR STYLING (Consistent with other pages) --- */
.navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 25px;
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}
.navbar-brand {
    font-size: 26px;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}
.navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.navbar-toggler:focus {
    box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}
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
@media (max-width: 991.98px) {
    .navbar-nav .nav-link:hover,
    .navbar-nav .nav-link.active {
        transform: none;
    }
    .navbar-collapse {
        padding-top: 15px;
    }
}

/* --- MAIN CONTENT STYLING --- */
.dashboard-container {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}

/* Search Form Card */
.search-card {
    background: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    margin-bottom: 30px;
}

.search-form {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 15px;
    align-items: center;
}

.form-group {
    position: relative;
}

.form-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #aaa;
    pointer-events: none;
}

.form-control {
    width: 100%;
    padding: 12px 15px 12px 40px; /* Adjusted padding for larger size */
    border: 1px solid #ced4da;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.form-control:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    outline: none;
}

.search-button {
    padding: 12px 25px;
    font-size: 16px;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

/* Results Card */
.results-card {
    background: #ffffff;
    padding: 10px 25px 25px 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    min-height: 300px;
    display: flex;
    flex-direction: column;
}

.table-responsive-wrapper {
    overflow-x: auto;
}

.results-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.results-table th, .results-table td {
    padding: 15px;
    border-bottom: 1px solid #e9ecef;
    text-align: left;
    vertical-align: middle;
}
.results-table th {
    background-color: #f8f9fa;
    font-weight: 600;
    color: #495057;
    white-space: nowrap;
}
.results-table tbody tr:hover {
    background-color: #f1f5f8;
}
.action-cell {
    text-align: center;
    white-space: nowrap;
}
.btn-action {
    padding: 6px 15px;
    font-size: 13px;
    border-radius: 5px;
    border: none;
    color: white;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
    min-width: 100px;
    justify-content: center;
}
.btn-action:hover {
    filter: brightness(1.1);
}
.btn-block { background-color: #e74c3c; }
.btn-unblock { background-color: #2ecc71; }

/* Loading and Empty States */
.loading-state, .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #7f8c8d;
    flex-grow: 1;
    padding: 40px;
}
.empty-icon {
    font-size: 48px;
    color: #bdc3c7;
    margin-bottom: 20px;
}
.empty-state h3 {
    font-size: 20px;
    color: #34495e;
    margin-bottom: 5px;
}

/* Footer */
.footer {
    margin-top: 40px;
    text-align: center;
    padding: 25px;
    background: #121212;
    color: #888;
    font-size: 14px;
    border-top: 1px solid #2a2a2a;
}

/* --- RESPONSIVE ADJUSTMENTS --- */
@media (max-width: 768px) {
    .search-form {
        grid-template-columns: 1fr;
    }
    .dashboard-container {
        padding: 0 15px;
    }
    .results-table {
        display: block;
        width: 100%;
    }
    .results-table thead { display: none; }
    .results-table tbody, .results-table tr, .results-table td { display: block; width: 100%; }
    .results-table tr {
        margin-bottom: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
    }
    .results-table td {
        text-align: right;
        padding-left: 50%;
        position: relative;
        border-bottom: 1px solid #eee;
    }
    .results-table td:before {
        content: attr(data-label);
        position: absolute;
        left: 15px;
        width: 45%;
        padding-right: 10px;
        white-space: nowrap;
        text-align: left;
        font-weight: bold;
    }
    .results-table td:last-child {
        border-bottom: 0;
    }
    .action-cell {
        text-align: right; /* Align button to the right on mobile */
    }
}
</style>