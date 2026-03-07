# Amantac System Architecture

## Overview

Amantac is a comprehensive school management system focused on student safety tracking and academic monitoring. The system integrates hardware devices (RFID cards, smartwatches) with a web and mobile application platform.

## System Components

### 1. Backend API (FastAPI)
- **Technology**: Python 3.9+, FastAPI, SQLAlchemy, PostgreSQL
- **Purpose**: Core business logic, data management, API endpoints
- **Location**: `backend/`

### 2. Database (PostgreSQL)
- **Purpose**: Persistent data storage
- **Models**: Users, Students, Buses, Attendance, Grades, etc.

### 3. Hardware Integration Layer
- **RFID Readers**: For bus boarding, school entry/exit
- **Smartwatches**: GPS tracking, attendance logging
- **GPS Devices**: Real-time bus location tracking
- **Cameras**: Optional bus surveillance

### 4. Frontend Web Application
- **Technology**: React.js or Vue.js (to be implemented)
- **Purpose**: Web interface for parents, teachers, and administrators
- **Location**: `frontend/` (to be created)

### 5. Mobile Application
- **Technology**: React Native or Flutter (to be implemented)
- **Purpose**: Mobile access for parents and staff
- **Location**: `mobile/` (to be created)

### 6. Real-time Communication
- **WebSocket**: For live updates (bus location, notifications)
- **Redis**: Caching and pub/sub for notifications

## Data Flow

### Student Safety Tracking Flow

1. **Boarding Bus**
   - RFID/Smartwatch scanned on bus
   - Device ID verified against database
   - Attendance log created
   - Notification sent to parent

2. **Entering School**
   - RFID/Smartwatch scanned at school gate
   - Attendance log created
   - Attendance record updated

3. **Exiting School**
   - RFID/Smartwatch scanned at exit
   - Attendance log created
   - If pickup request exists, verification required

4. **Arriving Home**
   - Smartwatch GPS detects home location
   - Attendance log created
   - Notification sent to parent

### Smart Pickup Flow

1. **Parent Request**
   - Parent creates pickup request via app
   - QR code generated
   - Request status: PENDING

2. **School Approval**
   - Teacher/Admin reviews and approves
   - Request status: APPROVED
   - Notification sent to parent

3. **Pickup Verification**
   - Recipient arrives at school
   - QR code scanned or NFC/Bluetooth verified
   - Request status: COMPLETED
   - Notification sent to parent

### Early Dismissal Flow

1. **Parent Request**
   - Parent creates dismissal request
   - Reason provided
   - Request status: PENDING

2. **Teacher Approval**
   - Teacher reviews and approves
   - Request status: TEACHER_APPROVED

3. **Admin Approval**
   - Admin reviews and approves
   - Request status: ADMIN_APPROVED
   - Notification sent to parent

## Security Features

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control (Parent, Teacher, Admin, Staff, Driver)

2. **Device Verification**
   - Device IDs registered and linked to students
   - Only authorized devices can log attendance

3. **Pickup Security**
   - QR code verification
   - NFC/Bluetooth verification
   - Authorization required from school

4. **Data Protection**
   - Encrypted passwords
   - Secure API endpoints
   - Audit logs for all operations

## Scalability Considerations

1. **Database**
   - Indexed queries for performance
   - Connection pooling
   - Read replicas for reporting

2. **Caching**
   - Redis for frequently accessed data
   - Cache bus locations
   - Cache student information

3. **Real-time Updates**
   - WebSocket connections for live tracking
   - Pub/Sub pattern for notifications

4. **API Rate Limiting**
   - Prevent abuse
   - Ensure fair resource usage

## Integration Points

### External Systems
- **Ministry of Education**: Data export, reporting
- **SMS Gateway**: SMS notifications
- **Email Service**: Email notifications
- **GPS Service**: Bus location tracking
- **Payment Gateway**: (Future) Fee payments

### Hardware Devices
- **RFID Readers**: Via serial/USB connection or network API
- **Smartwatches**: Via Bluetooth or network API
- **GPS Trackers**: Via network API
- **Cameras**: Via RTSP stream or network API

## Deployment Architecture

### Development
- Local PostgreSQL database
- Local Redis instance
- Development server with hot reload

### Production
- PostgreSQL on dedicated server or cloud
- Redis cluster for high availability
- Application servers behind load balancer
- CDN for static assets
- SSL/TLS encryption

## Monitoring & Logging

1. **Application Logs**
   - Request/response logging
   - Error tracking
   - Performance metrics

2. **Database Monitoring**
   - Query performance
   - Connection pool status
   - Slow query logs

3. **System Health**
   - API health checks
   - Database connectivity
   - Redis connectivity
   - Hardware device status

## Future Enhancements

1. **AI/ML Features**
   - Attendance pattern analysis
   - Behavior prediction
   - Academic performance insights

2. **Advanced Analytics**
   - Dashboard with charts and graphs
   - Custom reports
   - Data export

3. **Mobile Features**
   - Push notifications
   - Offline mode
   - Biometric authentication

4. **Integration**
   - Parent portal integration
   - School management system integration
   - Payment gateway integration





