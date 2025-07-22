<template>
    <div class="admin-search-wrapper">
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
                            <a class="nav-link active" href="/a/search"><i class="fas fa-question-circle"></i> Search</a>
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
            <h2 class="section-title">Search Records</h2>
            
            <!-- Search Form Card -->
            <div class="search-card">
                <form @submit.prevent="handleSearch" class="search-form">
                    <div class="form-group select-group">
                        <i class="fas fa-filter form-icon"></i>
                        <select v-model="selectedParameter" class="form-control" required>
                            <option value="" disabled>Select Parameter</option>
                            <option value="quiz_title">Quiz Title</option>
                            <option value="date">Date</option>
                            <option value="chapter_name">Chapter Name</option>
                            <option value="subject_name">Subject Name</option>
                            <option value="user_id">User ID</option>
                        </select>
                    </div>
                    <div class="form-group input-group">
                        <i class="fas fa-keyboard form-icon"></i>
                        <input type="text" v-model="searchQuery" class="form-control" :placeholder="placeholderText" required>
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
                    <p>Fetching results...</p>
                </div>

                <div v-else-if="!isLoading && searchResults.length > 0" class="table-responsive-wrapper">
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th v-for="header in Object.keys(searchResults[0])" :key="header">
                                    {{ header.replace(/_/g, ' ').toUpperCase() }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in searchResults" :key="index">
                                <td v-for="(value, key) in item" :key="key" :data-label="key.replace(/_/g, ' ').toUpperCase()">
                                    {{ value }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-else-if="!isLoading && hasSearched" class="empty-state">
                    <i class="fas fa-search-minus empty-icon"></i>
                    <h3>No Results Found</h3>
                    <p>Your search for "{{ searchQuery }}" did not return any results. Try a different query.</p>
                </div>

                <div v-else class="empty-state">
                    <i class="fas fa-search empty-icon"></i>
                    <h3>Ready to Search</h3>
                    <p>Use the form above to search for records across the system.</p>
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
    name: 'AdminSearch',
    data() {
        return {
            selectedParameter: '',
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
        async handleSearch() {
            if (!this.selectedParameter || !this.searchQuery) {
                alert('Please select a parameter and enter a search query.');
                return;
            }

            this.isLoading = true;
            this.hasSearched = true;
            this.searchResults = [];

            try {
                const params = new FormData();
                params.append('parameter', this.selectedParameter);
                params.append('query', this.searchQuery)
                alert(`${this.selectedParameter}, ${this.searchQuery}`)
                const apiUrl = await axios.post(`http://127.0.0.1:5000/api/admin/search`, params);
                this.searchResults = apiUrl.data.results;

            } catch (error) {
                console.error('Error fetching search results:', error);
                alert('An error occurred while searching. Please check the console for details.');
            } finally {
                this.isLoading = false;
            }
        }
    },
    mounted() {
        this.checker();
    },
    computed: {

        placeholderText() {
            switch (this.selectedParameter) {
                case 'date':
                    return 'Enter date (e.g., 25-12-2024)';
                case 'user_id':
                    return 'Enter the User ID';
                case 'quiz_title':
                    return 'Enter the quiz title';
                case 'chapter_name':
                    return 'Enter the chapter name';
                case 'subject_name':
                    return 'Enter the subject name';
                default:
                    return 'Enter your search query...';
            }
        }
    },
};
</script>


<style scoped>
/* General Page Wrapper */
.admin-search-wrapper {
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
    grid-template-columns: 1fr 2fr auto;
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
    padding: 10px 15px 10px 40px; /* Padding for icon */
    border: 1px solid #ced4da;
    border-radius: 6px;
    font-size: 15px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.form-control:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    outline: none;
}

.search-button {
    padding: 10px 25px;
    font-size: 15px;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

/* Results Card */
.results-card {
    background: #ffffff;
    padding: 25px;
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
    padding: 12px 15px;
    border-bottom: 1px solid #e9ecef;
    text-align: left;
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
        grid-template-columns: 1fr; /* Stack form elements */
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
}
</style>

