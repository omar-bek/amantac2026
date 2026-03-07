# Amantac Smart School Management System - Architecture

## System Overview

Enterprise-grade Smart School Management System with role-based access, AI-driven insights, and comprehensive security.

## Roles & Permissions

### 1. Teacher Portal 👩‍🏫
- **Access**: Assigned students only
- **Restrictions**: No medical data, no GPS data, no student comparison
- **Features**:
  - Dashboard with KPIs
  - Student list (by class)
  - Daily evaluation with quick tags
  - Homework creation & tracking
  - Attendance marking
  - Class announcements
  - Parent messaging (controlled, work hours only)
  - File & image attachments
  - Exam & quiz schedule

### 2. School Admin Portal 🏫
- **Access**: Full school management
- **Features**:
  - School Dashboard
  - Student management
  - Teacher management
  - Class & schedule setup
  - Bus routes assignment
  - Pickup & dismissal approvals
  - Reports & exports
  - Complaints center
  - Notifications broadcast

### 3. Bus Driver Portal 🚌
- **Access**: Assigned routes only
- **Features**:
  - Driver dashboard
  - Route management
  - Live tracking (GPS only during trips)
  - Student boarding scan
  - Delay alerts
  - Emergency button
  - Incident reporting

### 4. Student Portal 🎒 (Optional)
- **Access**: Own data only
- **Restrictions**: No chat, no social features
- **Features**:
  - Daily schedule
  - Homework view
  - Activity reminders
  - Rewards & badges

### 5. Super Admin / Ministry Portal 🏛️
- **Access**: Nationwide overview
- **Restrictions**: Aggregated data only, no student names
- **Features**:
  - Schools overview
  - Aggregated analytics
  - Compliance monitoring
  - System health
  - Policy configuration
  - Emergency broadcast

### 6. Parent Portal 👨‍👩‍👧
- **Access**: Own children only
- **Features**:
  - Child dashboard
  - Attendance tracking
  - Homework view
  - Teacher communication
  - Pickup/dismissal requests
  - Notifications

## Security & Privacy

- Role-based access control (RBAC)
- Audit logs for all actions
- End-to-end messaging encryption
- Data encryption at rest
- Parental consent management
- Session limits & device binding
- GDPR-ready architecture
- Local data hosting
- Data retention rules
- Right to be forgotten

## AI & Smart Features

- Parent guidance suggestions
- Teacher workload reduction
- Anomaly detection (non-alarm)
- Smart summaries
- Predictive absenteeism
- **Ethical Guidelines**: No diagnosis, no student classification, no automated decisions

## Technology Stack

### Backend
- FastAPI (Python)
- PostgreSQL / SQLite
- SQLAlchemy ORM
- JWT Authentication
- WebSockets for real-time updates
- Multi-tenant architecture
- Feature flags
- Offline mode support

### Frontend
- React + TypeScript
- Vite
- Tailwind CSS
- Zustand (State Management)
- React Query (Data Fetching)
- React Router (Routing)
- Responsive design (Desktop, Tablet, Mobile)

## Database Schema

### Core Tables
- `users` - All system users (teachers, admins, parents, drivers, students)
- `students` - Student information
- `classes` - Class management
- `assignments` - Homework/assignments
- `evaluations` - Student evaluations
- `attendance` - Attendance records
- `messages` - Teacher-parent messaging
- `notifications` - System notifications
- `buses` - Bus management
- `routes` - Bus routes
- `pickup_requests` - Pickup requests
- `dismissal_requests` - Dismissal requests
- `audit_logs` - Security audit logs

## API Structure

```
/api/auth/* - Authentication
/api/students/* - Student management
/api/teachers/* - Teacher operations
/api/admin/* - Admin operations
/api/driver/* - Driver operations
/api/parent/* - Parent operations
/api/assignments/* - Assignment management
/api/evaluations/* - Evaluation system
/api/attendance/* - Attendance tracking
/api/messages/* - Messaging system
/api/buses/* - Bus management
/api/notifications/* - Notifications
/api/reports/* - Reports & analytics
/api/ai/* - AI features
```

## Frontend Routes

```
/login - Login page
/register - Registration

/teacher/* - Teacher portal
/admin/* - School admin portal
/driver/* - Driver portal
/student/* - Student portal (optional)
/parent/* - Parent portal
/super-admin/* - Ministry/Super admin portal
```

## Design Principles

1. **Trust**: Clear, transparent, secure
2. **Simplicity**: Easy to use, intuitive
3. **Clarity**: Clear information hierarchy
4. **Privacy**: Privacy-first design
5. **Accessibility**: WCAG compliant
6. **Performance**: Fast, responsive
7. **Scalability**: Modular, extensible

## Color Scheme

- Primary: Calm blue (#3B82F6)
- Success: Green (#10B981)
- Warning: Amber (#F59E0B)
- Error: Red (#EF4444)
- Neutral: Gray scale
- Background: Light gray/white

## Typography

- Headings: Bold, clear hierarchy
- Body: Readable, 16px minimum
- Arabic support: Proper RTL layout





