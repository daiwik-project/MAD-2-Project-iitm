<template>
    <div class="view-subject-wrapper">
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
                <h2 class="section-title">Subject Details</h2>
                <button class="btn btn-back" @click="$router.push(`/${level_id}/view/Level`)">
                    <i class="fas fa-arrow-left"></i> Back to Level
                </button>
            </div>

            <!-- Subject Info Card -->
            <div class="subject-info-card">
                <div class="subject-info-icon">
                    <i class="fas fa-book-open"></i>
                </div>
                <div class="subject-info-content">
                    <h1>{{ subject_name }}</h1>
                    <p>{{ subject_description }}</p>
                </div>
            </div>

            <h3 class="chapters-title">Chapters in this Subject</h3>

            <!-- Chapters Grid -->
            <div class="chapters-grid">
                <div class="chapter-card" v-for="(chapter, index) in chapters" :key="index">
                    <div class="chapter-card-header">
                        <div class="chapter-card-icon">
                            <i class="fas fa-file-alt"></i>
                        </div>
                        <h5 class="chapter-card-title">{{ chapter[1] }}</h5>
                    </div>
                    <p class="chapter-card-description">{{ chapter[2] }}</p>
                    <div class="chapter-card-actions">
                        <button class="btn btn-action btn-view" @click="View_chapter(chapter[0])"><i class="fas fa-eye"></i> View</button>
                        <button class="btn btn-action btn-edit" :data-bs-toggle="'modal'" :data-bs-target="'#edit-' + chapter[0]"><i class="fas fa-edit"></i> Edit</button>
                        <button class="btn btn-action btn-delete" @click="delete_chapter(chapter[0])"><i class="fas fa-trash"></i> Delete</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- MODALS ARE MOVED HERE, OUTSIDE THE MAIN CONTAINER AND THE V-FOR LOOP -->
        <div v-for="(chapter, index) in chapters" :key="'modal-' + index">
            <div class="modal fade" :id="'edit-' + chapter[0]" tabindex="-1" aria-labelledby="editChapterLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editChapterLabel">Edit Chapter: {{ chapter[1] }}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="updateChapter(chapter[0], chapter[1], chapter[2])">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label :for="'chapter_name_' + chapter[0]" class="form-label">Chapter Name</label>
                                    <input type="text" class="form-control" :id="'chapter_name_' + chapter[0]" v-model="chapter[1]" required>
                                </div>
                                <div class="mb-3">
                                    <label :for="'chapter_desc_' + chapter[0]" class="form-label">Chapter Description</label>
                                    <textarea class="form-control" :id="'chapter_desc_' + chapter[0]" v-model="chapter[2]" rows="3" required></textarea>
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
        <a class="btn-add-floating" :href="`/${level_id}/level/${subject_id}/subject/createchapter`" title="Add New Chapter">
            <i class="fas fa-plus"></i>
        </a>

        <!-- Footer -->
        <footer class="footer">
            <p>© 2025 Ischool Admin. All Rights Reserved.</p>
        </footer>
    </div>
</template>

<script>
import axios from 'axios'; // Keep if used elsewhere
import VueCookies from 'vue-cookies'; // Keep if used elsewhere
// import View_chapter from './view_chapter.vue';

export default {
  name: 'ViewSubject',
  data() {
    return {
      // Add more chapters as needed
      level_id: this.$route.params.level_id,
      subject_id: this.$route.params.subject_id,
      subject_name: "",
      subject_description: "",
      chapters: [],

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
    // method to handle adding a chapter
    async getchapters() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/admin_dashboard/subject/${this.subject_id}`);
        const backendData = response.data;
        this.subject_name = backendData.info[1];
        this.subject_description = backendData.info[2];
        this.chapters = backendData.info[3];

      } catch (error) {
        console.error("Error fetching chapters:", error);
      }
    },
    async updateChapter(chapterId, chapterName, chapterDescription) {
      const chapterData = new FormData();
      chapterData.append('chapter_name', chapterName);
      chapterData.append('chapter_description', chapterDescription);
      // alert(`Chapter Id: ${chapterId},Chapter Name: ${chapterName}, Chapter Description: ${chapterDescription}`);
      try {
        const response = await axios.post(`http://127.0.1:5000/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${chapterId}/update/chapter`, chapterData);
        // alert(`Message From Backend: ${response.data.message}`);
      } catch (error) {
        alert("Error updating chapter:", error);
        console.log(error);
      }
    },
    async View_chapter(chapterId) {
      this.$router.push(`/${this.level_id}/level/${this.subject_id}/subject/${chapterId}/view/chapter`);
    },
    async delete_chapter(chapterId) {
      try {
        const response = await axios.delete(`http://127.0.1:5000/admin_dashboard/${this.level_id}/level/${this.subject_id}/subject/${chapterId}/delete/chapter`);
        this.getchapters(); // Refresh the chapter list after deletion
      } catch (error) {
        alert("Error deleting chapter:", error);
      }
    },



  },
  mounted() {
    this.checker();
    // Fetch data or perform actions when the component is mounted
    this.getchapters();
  }
};
</script>

<style scope>
/* General Page Wrapper */
.view-subject-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- NAVBAR STYLING (Consistent with other pages) --- */
.view-subject-wrapper .navbar {
    background: rgba(15, 12, 41, 0.95);
    padding: 15px 25px;
    backdrop-filter: blur(8px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    position: sticky;
    top: 0;
    z-index: 1000;
}
.view-subject-wrapper .navbar-brand {
    font-size: 26px;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}
.view-subject-wrapper .navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.view-subject-wrapper .navbar-toggler:focus {
    box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}
.view-subject-wrapper .navbar-nav .nav-link {
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
.view-subject-wrapper .navbar-nav .nav-link:hover,
.view-subject-wrapper .navbar-nav .nav-link.active {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}
@media (max-width: 991.98px) {
    .view-subject-wrapper .navbar-nav .nav-link:hover,
    .view-subject-wrapper .navbar-nav .nav-link.active {
        transform: none;
    }
    .view-subject-wrapper .navbar-collapse {
        padding-top: 15px;
    }
}

/* --- MAIN CONTENT STYLING --- */
.view-subject-wrapper .dashboard-container {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
}

.view-subject-wrapper .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.view-subject-wrapper .section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.view-subject-wrapper .btn-back {
    background-color: #fff;
    color: #34495e;
    border: 1px solid #e0e6ed;
    padding: 8px 16px;
    font-weight: 500;
    border-radius: 6px;
    transition: all 0.2s ease;
}
.view-subject-wrapper .btn-back:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Subject Info Card */
.view-subject-wrapper .subject-info-card {
    background: linear-gradient(135deg, #6f42c1, #563d7c);
    color: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(111, 66, 193, 0.3);
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    gap: 25px;
}
.view-subject-wrapper .subject-info-icon {
    font-size: 48px;
    opacity: 0.8;
}
.view-subject-wrapper .subject-info-content h1 {
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 5px 0;
}
.view-subject-wrapper .subject-info-content p {
    font-size: 16px;
    margin: 0;
    opacity: 0.9;
}

.view-subject-wrapper .chapters-title {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}

/* Chapters Grid */
.view-subject-wrapper .chapters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 25px;
}

.view-subject-wrapper .chapter-card {
    background: #ffffff;
    border: 1px solid #e0e6ed;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
}
.view-subject-wrapper .chapter-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.view-subject-wrapper .chapter-card-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}
.view-subject-wrapper .chapter-card-icon {
    font-size: 22px;
    color: #2ecc71;
    background-color: rgba(46, 204, 113, 0.1);
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
    flex-shrink: 0;
}
.view-subject-wrapper .chapter-card-title {
    font-size: 18px;
    font-weight: 600;
    color: #34495e;
    margin: 0;
}
.view-subject-wrapper .chapter-card-description {
    font-size: 14px;
    color: #555;
    line-height: 1.6;
    margin-bottom: 15px;
    flex-grow: 1;
}
.view-subject-wrapper .chapter-card-actions {
    margin-top: auto;
    padding-top: 15px;
    border-top: 1px solid #f0f2f5;
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}
.view-subject-wrapper .btn-action {
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
.view-subject-wrapper .btn-action:hover {
    transform: scale(1.05);
    filter: brightness(1.1);
}
.view-subject-wrapper .btn-view { background-color: #3498db; }
.view-subject-wrapper .btn-edit { background-color: #f1c40f; }
.view-subject-wrapper .btn-delete { background-color: #e74c3c; }

/* Floating Add Button */
.view-subject-wrapper .btn-add-floating {
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
.view-subject-wrapper .btn-add-floating:hover {
    transform: translateY(-5px) scale(1.1);
    box-shadow: 0 10px 25px rgba(54, 101, 255, 0.5);
}

/* Modal Styling */
.view-subject-wrapper .modal-content {
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: none;
}
.view-subject-wrapper .modal-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

/* Footer */
.view-subject-wrapper .footer {
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
    .view-subject-wrapper .dashboard-container {
        padding: 0 15px;
    }
    .view-subject-wrapper .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
}
@media (max-width: 576px) {
    .view-subject-wrapper .subject-info-card {
        flex-direction: column;
        text-align: center;
    }
    .view-subject-wrapper .subject-info-content h1 {
        font-size: 24px;
    }
}
</style>