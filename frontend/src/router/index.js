import { createRouter, createWebHistory } from 'vue-router'

//  Admin ROutes
import Home from '../views/index.vue'

import AdminLogin from '../views/admin/admin_login.vue'
import AdminDashboard from '../views/admin/admin_dashboard.vue'
import AdminSearch from '../views/admin/admin_search.vue'
import AdminSummary from '../views/admin/admin_summary.vue'
import UserControl from '../views/admin/user_control.vue'
import ViewLevel from '../views/admin/view_level.vue'
import ViewSubject from '../views/admin/view_subject.vue'
import ViewChapter from '../views/admin/view_chapter.vue'
import ViewQuestions from '../views/admin/view_questions.vue'
import CreateLevel from '../views/admin/create_level.vue'
import CreateSubject from '../views/admin/create_subject.vue'
import CreateChapter from '../views/admin/create_chapter.vue'
import CreateQuestion from '../views/admin/create_question.vue'

import NotFound from '../views/Error/404.vue'


import Login from '../views/user/login.vue'
import Register from '../views/user/register.vue'
import StartDashboardPage from '../views/user/start_dashboard.vue'
import DashboardPage from '../views/user/dashboard.vue'
import User_Chap_Page from '../views/user/user_chapter_quiz_list.vue'
import QuizAttempt from '../views/user/quiz_attempt.vue'
import QuizSummary from '../views/user/quizsolution.vue'
import SummaryPage from '../views/user/summary.vue'
import Search from '../views/user/search.vue'
import Profile from '../views/user/profile.vue'

const routes = [
  {
    path:'/',
    name: 'home',
    component: Home
  },
  {
    path: '/admin/login',
    name: 'adminlogin',
    component: AdminLogin
  },
  {
    path: '/admindashboard',
    name: 'admindashborad',
    component: AdminDashboard
  },
  {
    path: '/a/search',
    name: 'admin_search',
    component: AdminSearch
  },
  {
    path: '/a/summary',
    name: 'admin_summary',
    component: AdminSummary,
  },
  {
    path: '/user-control',
    name: 'usercntrol',
    component: UserControl
  },
  {
    path: '/:level_id/view/Level',
    name: 'viewlevel',
    component: ViewLevel
  },
  {
    path: '/:level_id/Level/:subject_id/view/subject',
    name: 'viewsubject',
    component: ViewSubject
  },
  {
    path: '/:level_id/level/:subject_id/subject/:chapter_id/view/chapter',
    name: 'viewchapter',
    component: ViewChapter
  },
  {
    path: '/:level_id/level/:subject_id/subject/:chapter_id/chapter/:quiz_id/quiz/viewquestions',
    name: 'viewquestions',
    component: ViewQuestions
  },
  {
    path: '/createlevel',
    name: 'createlevel',
    component: CreateLevel
  },
  {
    path: '/:level_id/createsubject',
    name: 'createsubject',
    component: CreateSubject
  },
  {
    path: '/:level_id/level/:subject_id/subject/createchapter',
    name: 'createchapter',
    component: CreateChapter
  },
  {
    path: "/:level_id/level/:subject_id/subject/:chapter_id/chapter/:quiz_id/quiz/createquestions",
    name: "CreateQuestion",
    component: CreateQuestion
  },
  // user
  {
    path: '/login',
    name: 'login',
    component: Login

  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardPage
  },
  {
    path: '/dashboard/start',
    name: 'startdashboard',
    component: StartDashboardPage
  },
  {
    path: '/dashboard/chapter/:chapter_id',
    name: 'user_chap_page',
    component: User_Chap_Page
  },
  {
    path: '/dashboard/attempt/:quiz_id/attempt_=:attempt_number',
    name: 'quizattempt',
    component: QuizAttempt
  },
  {
    path: "/dashboard/summary/:quiz_id/attempt_=:attempt_number",
    name: 'QuizSummary',
    component: QuizSummary
  },
  {
    path: '/summary',
    name: 'summary',
    component: SummaryPage
  },
  {
    path: '/search',
    name: "search",
    component: Search
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile
  },
  {
    path: '/:catchAll(.*)',
    name: 'notfound',
    component: NotFound
  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
