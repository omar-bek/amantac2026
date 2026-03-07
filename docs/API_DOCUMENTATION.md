# Amantac API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All endpoints (except `/api/auth/register` and `/api/auth/login`) require authentication using Bearer token.

### Register
```
POST /api/auth/register
```

### Login
```
POST /api/auth/login
```

Returns:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {...}
}
```

Use the token in subsequent requests:
```
Authorization: Bearer <token>
```

## Endpoints

### Students

#### Get All Students
```
GET /api/students/
```

#### Get Student by ID
```
GET /api/students/{student_id}
```

#### Get Students by Parent
```
GET /api/students/parent/{parent_id}
```

### Buses

#### Get All Buses
```
GET /api/buses/
```

#### Get Bus Details
```
GET /api/buses/{bus_id}
```

#### Get Bus Location (Real-time)
```
GET /api/buses/{bus_id}/location
```

#### Get Students on Bus
```
GET /api/buses/{bus_id}/students
```

### Attendance

#### Log Attendance Event
```
POST /api/attendance/log
```

Parameters:
- `student_id`: int
- `attendance_type`: "board_bus" | "enter_school" | "exit_school" | "arrive_home"
- `device_id`: string (RFID/Smartwatch ID)
- `location`: string (optional)

#### Get Student Attendance
```
GET /api/attendance/student/{student_id}
```

Query parameters:
- `start_date`: date (optional)
- `end_date`: date (optional)

#### Get Attendance Logs
```
GET /api/attendance/logs/{student_id}
```

### Pickup (Smart Private Pickup)

#### Create Pickup Request
```
POST /api/pickup/request
```

Parameters:
- `student_id`: int
- `recipient_name`: string
- `recipient_phone`: string
- `recipient_relation`: string
- `pickup_date`: datetime
- `pickup_time`: datetime
- `reason`: string (optional)

#### Approve Pickup Request
```
POST /api/pickup/{request_id}/approve
```

#### Verify Pickup
```
POST /api/pickup/{request_id}/verify
```

Parameters:
- `verification_code`: string (QR/NFC/Bluetooth code)

#### Get Pickup Requests
```
GET /api/pickup/student/{student_id}
```

### Dismissal (Early Dismissal)

#### Create Dismissal Request
```
POST /api/dismissal/request
```

Parameters:
- `student_id`: int
- `dismissal_date`: datetime
- `dismissal_time`: datetime
- `reason_type`: "medical" | "family" | "emergency" | "other"
- `reason_details`: string (optional)

#### Teacher Approve
```
POST /api/dismissal/{request_id}/teacher-approve
```

#### Admin Approve
```
POST /api/dismissal/{request_id}/admin-approve
```

#### Get Dismissal Requests
```
GET /api/dismissal/student/{student_id}
```

### Academic

#### Get Student Grades
```
GET /api/academic/grades/{student_id}
```

Query parameters:
- `subject`: string (optional)
- `semester`: string (optional)

#### Get Exams
```
GET /api/academic/exams
```

Query parameters:
- `class_name`: string (optional)

#### Get Assignments
```
GET /api/academic/assignments
```

Query parameters:
- `class_name`: string (optional)

#### Get Quizzes
```
GET /api/academic/quizzes
```

Query parameters:
- `class_name`: string (optional)

#### Add Grade
```
POST /api/academic/grade
```

Parameters:
- `student_id`: int
- `subject`: string
- `grade_value`: float
- `max_grade`: float (default: 100.0)
- `exam_id`: int (optional)
- `assignment_id`: int (optional)
- `quiz_id`: int (optional)
- `semester`: string (optional)
- `notes`: string (optional)

### Behavior

#### Log Behavior
```
POST /api/behavior/log
```

Parameters:
- `student_id`: int
- `behavior_type`: "positive" | "negative" | "neutral"
- `description`: string
- `location`: string (optional)

#### Create Behavior Note
```
POST /api/behavior/note
```

Parameters:
- `student_id`: int
- `behavior_type`: "positive" | "negative" | "neutral"
- `title`: string
- `description`: string

#### Get Student Behavior Logs
```
GET /api/behavior/student/{student_id}
```

Query parameters:
- `limit`: int (default: 50)

#### Get Behavior Notes
```
GET /api/behavior/notes/{student_id}
```

### Activities

#### Get All Activities
```
GET /api/activities/
```

Query parameters:
- `is_active`: bool (default: true)

#### Get Activity Details
```
GET /api/activities/{activity_id}
```

#### Get Student Activities
```
GET /api/activities/student/{student_id}
```

#### Add Activity Participation
```
POST /api/activities/participation
```

Parameters:
- `activity_id`: int
- `student_id`: int
- `participation_type`: string
- `achievement`: string (optional)
- `evaluation`: string (optional)

### Notifications

#### Get Notifications
```
GET /api/notifications/
```

Query parameters:
- `unread_only`: bool (default: false)
- `limit`: int (default: 50)

#### Mark Notification as Read
```
POST /api/notifications/{notification_id}/read
```

#### Get Unread Count
```
GET /api/notifications/unread/count
```

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message"
}
```

Common status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error





