import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { Toaster } from 'react-hot-toast'

// Auth pages
import { Login, Register } from './pages/auth'

// Parent pages
import {
  ParentDashboard,
  ParentProfile,
  ParentNotifications,
  ParentActivity,
  ChildDetail,
  LiveMap,
  Messages,
  TodayStatus,
  RouteTimeline,
  DailyDigest,
  RequestsApprovals,
  RequestDetail,
  NewRequest,
  ConcernsEscalations,
  ConcernDetail,
  NewConcern,
} from './pages/parent'

// Teacher pages
import {
  TeacherDashboard,
  TeacherAssignments,
  TeacherEvaluations,
  TeacherEvaluationNew,
  TeacherEvaluationDetail,
  TeacherStudentProfile,
  TeacherStudents,
  TeacherMessages,
  TeacherAnnouncements,
  TeacherAttendance,
  TeacherExams,
  ClassInsights,
  StudentNotes,
  NotificationsSummary,
  TeacherProfile,
} from './pages/teacher'

// Admin pages
import {
  AdminDashboard,
  AdminTeachers,
  AdminTeacherDetail,
  AdminClasses,
  AdminReports,
  AdminAuditLogs,
  AdminApprovals,
  AdminComplaints,
  SchoolAdminCommandCenter,
} from './pages/admin'

// Staff pages
import {
  StaffDashboard,
  StaffTeachers,
  StaffApprovals,
  StaffBuses,
  StaffNotifications,
  StaffStudents,
  StaffStudentProfile,
  StaffAttendance,
  StaffBehavior,
  StaffActivities,
} from './pages/staff'

// Driver pages
import {
  DriverDashboard,
  DriverRouteManagement,
  DriverIncidents,
  DriverLogin,
  VehicleChecklist,
  RouteExecution,
  StudentCheckIn,
  RouteSummary,
} from './pages/driver'

// Student pages
import {
  StudentDashboard,
  StudentProgress,
  StudentAssignments,
  SilentWellbeingCheckin,
} from './pages/student'

// Super Admin pages
import {
  SuperAdminDashboard,
  SuperAdminSchools,
  SuperAdminAnalytics,
  SuperAdminCompliance,
  SuperAdminBroadcast,
} from './pages/super-admin'

// Government pages
import { GovernmentDashboard } from './pages/government'

// Shared pages
import {
  Dashboard,
  Students,
  Attendance,
  Buses,
  Pickup,
  Dismissal,
  Academic,
  Behavior,
  Activities,
  Notifications,
  AIGuidance,
  TeacherWorkloadReduction,
  Test,
} from './pages/shared'

// Components
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import { ErrorBoundary } from './components/ErrorBoundary'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

// Route guard to redirect users to their specific dashboards
function ParentRouteGuard({ children }: { children: React.ReactNode }) {
  // This component is not used anymore, kept for reference
  return <>{children}</>
}

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Routes>
            <Route path="/test" element={<Test />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/" element={<Navigate to="/login" replace />} />
            
            {/* Parent Dashboard Routes (without Layout) - Only for parents */}
            <Route
              path="/parent"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ParentDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/child/:id"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ChildDetail />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/child/:id"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ChildDetail />
                </ProtectedRoute>
              }
            />
            <Route
              path="/child/:id/map"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <LiveMap />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/child/:id/map"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <LiveMap />
                </ProtectedRoute>
              }
            />
            <Route
              path="/map"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <LiveMap />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/messages"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <Messages />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/profile"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ParentProfile />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/notifications"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ParentNotifications />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/activity"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ParentActivity />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/status"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <TodayStatus />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/route"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <RouteTimeline />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/route/:childId"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <RouteTimeline />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/digest"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <DailyDigest />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/requests"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <RequestsApprovals />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/requests/:id"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <RequestDetail />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/requests/new"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <NewRequest />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/concerns"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ConcernsEscalations />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/concerns/:id"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ConcernDetail />
                </ProtectedRoute>
              }
            />
            <Route
              path="/parent/concerns/new"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <NewConcern />
                </ProtectedRoute>
              }
            />
            <Route
              path="/ai-guidance/:student_id"
              element={
                <ProtectedRoute allowedRoles={['parent', 'teacher', 'admin']}>
                  <AIGuidance />
                </ProtectedRoute>
              }
            />

            {/* Teacher Routes (without Layout) */}
            <Route
              path="/teacher"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                  <TeacherDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/assignments"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherAssignments />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/assignments/new"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherAssignments />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/evaluations"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherEvaluations />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/evaluations/new"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherEvaluationNew />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/evaluations/:id"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherEvaluationDetail />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/students"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherStudents />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/students/:id"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherStudentProfile />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/messages"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherMessages />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/announcements"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherAnnouncements />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/attendance"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherAttendance />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/exams"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherExams />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/insights"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <ClassInsights />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/notes"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <StudentNotes />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/notifications"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <NotificationsSummary />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/profile"
              element={
                <ProtectedRoute allowedRoles={['teacher']}>
                    <TeacherProfile />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/workload-reduction"
              element={
                <ProtectedRoute allowedRoles={['teacher', 'admin']}>
                    <TeacherWorkloadReduction />
                  </ProtectedRoute>
              }
            />

            {/* Admin Routes (without Layout) */}
            <Route
              path="/admin"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                    <AdminDashboard />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/admin/teachers"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                    <AdminTeachers />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/admin/teachers/:id"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                    <AdminTeacherDetail />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/admin/classes"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                    <AdminClasses />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/admin/reports"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                    <AdminReports />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/admin/audit-logs"
              element={
                <ProtectedRoute allowedRoles={['admin', 'super_admin']}>
                    <AdminAuditLogs />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/admin/approvals"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                    <AdminApprovals />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/admin/complaints"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                    <AdminComplaints />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/admin/command-center"
              element={
                <ProtectedRoute allowedRoles={['admin', 'super_admin']}>
                    <SchoolAdminCommandCenter />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/students"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}>
                    <Students />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/students/:id"
              element={
                <ProtectedRoute allowedRoles={['admin', 'staff']}>
                    <StaffStudentProfile />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/attendance"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}>
                    <Attendance />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/buses"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher', 'staff', 'driver']}>
                    <Buses />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/pickup"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}>
                    <Pickup />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/dismissal"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}>
                    <Dismissal />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/academic"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher']}>
                    <Academic />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/behavior"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}>
                    <Behavior />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/activities"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}>
                    <Activities />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/notifications"
              element={
                <ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}>
                    <Notifications />
                  </ProtectedRoute>
              }
            />

            {/* Driver Routes (without Layout) */}
            <Route
              path="/driver/login"
              element={<DriverLogin />}
            />
            <Route
              path="/driver"
              element={
                <ProtectedRoute allowedRoles={['driver']}>
                    <DriverDashboard />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/driver/checklist"
              element={
                <ProtectedRoute allowedRoles={['driver']}>
                    <VehicleChecklist />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/driver/route"
              element={
                <ProtectedRoute allowedRoles={['driver']}>
                    <RouteExecution />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/driver/route/manage"
              element={
                <ProtectedRoute allowedRoles={['driver']}>
                    <DriverRouteManagement />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/driver/route/stop/:stopId/checkin"
              element={
                <ProtectedRoute allowedRoles={['driver']}>
                    <StudentCheckIn />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/driver/summary"
              element={
                <ProtectedRoute allowedRoles={['driver']}>
                    <RouteSummary />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/driver/summary/:routeId"
              element={
                <ProtectedRoute allowedRoles={['driver']}>
                    <RouteSummary />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/driver/incidents"
              element={
                <ProtectedRoute allowedRoles={['driver']}>
                    <DriverIncidents />
                  </ProtectedRoute>
              }
            />

            {/* Student Routes (without Layout) */}
            <Route
              path="/student"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                    <StudentDashboard />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/student/progress"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                    <StudentProgress />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/student/assignments"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                    <StudentAssignments />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/student/assignments/:id"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                    <StudentAssignments />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/student/wellbeing"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                    <SilentWellbeingCheckin />
                  </ProtectedRoute>
              }
            />

            {/* Super Admin Routes (without Layout) */}
            <Route
              path="/super-admin"
              element={
                <ProtectedRoute allowedRoles={['super_admin']}>
                    <SuperAdminDashboard />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/super-admin/schools"
              element={
                <ProtectedRoute allowedRoles={['super_admin']}>
                    <SuperAdminSchools />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/super-admin/analytics"
              element={
                <ProtectedRoute allowedRoles={['super_admin']}>
                    <SuperAdminAnalytics />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/super-admin/compliance"
              element={
                <ProtectedRoute allowedRoles={['super_admin']}>
                    <SuperAdminCompliance />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/super-admin/broadcast"
              element={
                <ProtectedRoute allowedRoles={['super_admin']}>
                    <SuperAdminBroadcast />
                  </ProtectedRoute>
              }
            />

            {/* Government/Authority Routes (without Layout) */}
            <Route
              path="/government"
              element={
                <ProtectedRoute allowedRoles={['government_admin', 'authority_admin', 'super_admin']}>
                  <GovernmentDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/government/dashboard"
              element={
                <ProtectedRoute allowedRoles={['government_admin', 'authority_admin', 'super_admin']}>
                  <GovernmentDashboard />
                  </ProtectedRoute>
              }
            />
            
            {/* Staff Routes (separate from Layout) */}
            <Route
              path="/staff"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffDashboard />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/teachers"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffTeachers />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/approvals"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffApprovals />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/buses"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffBuses />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/students"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffStudents />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/students/:id"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffStudentProfile />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/attendance"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffAttendance />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/behavior"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffBehavior />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/activities"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffActivities />
                  </ProtectedRoute>
              }
            />
            <Route
              path="/staff/notifications"
              element={
                <ProtectedRoute allowedRoles={['staff']}>
                    <StaffNotifications />
                  </ProtectedRoute>
              }
            />
            
            {/* Admin/Teacher Routes (with Layout) - Parents cannot access */}
            <Route
              path="/dashboard"
              element={
                <ParentRouteGuard>
                  <Layout />
                </ParentRouteGuard>
              }
            >
              <Route index element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}><Dashboard /></ProtectedRoute>} />
              <Route path="students" element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}><Students /></ProtectedRoute>} />
              <Route path="students/:id" element={<ProtectedRoute allowedRoles={['admin', 'staff']}><StaffStudentProfile /></ProtectedRoute>} />
              <Route path="attendance" element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}><Attendance /></ProtectedRoute>} />
              <Route path="buses" element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff', 'driver']}><Buses /></ProtectedRoute>} />
              <Route path="pickup" element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}><Pickup /></ProtectedRoute>} />
              <Route path="dismissal" element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}><Dismissal /></ProtectedRoute>} />
              <Route path="academic" element={<ProtectedRoute allowedRoles={['admin', 'teacher']}><Academic /></ProtectedRoute>} />
              <Route path="behavior" element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}><Behavior /></ProtectedRoute>} />
              <Route path="activities" element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}><Activities /></ProtectedRoute>} />
              <Route path="notifications" element={<ProtectedRoute allowedRoles={['admin', 'teacher', 'staff']}><Notifications /></ProtectedRoute>} />
            </Route>
          </Routes>
          <Toaster position="top-center" />
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  )
}

export default App

