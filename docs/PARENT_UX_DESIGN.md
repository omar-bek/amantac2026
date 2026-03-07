# Parent/Guardian Experience - UI/UX Design Document
## Premium UAE Government-Grade School Safety Platform

**Version:** 1.0  
**Last Updated:** 2025-01-25  
**Design Language:** Calm, Minimal, Trustworthy, Culturally Respectful  
**Target Region:** UAE (Dubai / Abu Dhabi Standards)  
**Quality Benchmark:** TAMM / DubaiNow

---

## Table of Contents

1. [Design System](#design-system)
2. [Core Screens](#core-screens)
3. [Component Library](#component-library)
4. [Interaction Patterns](#interaction-patterns)
5. [Microcopy & Tone](#microcopy--tone)
6. [States & Edge Cases](#states--edge-cases)
7. [Accessibility & RTL](#accessibility--rtl)
8. [UX Rationale](#ux-rationale)

---

## Design System

### Color Palette

#### Primary Colors
- **White Background:** `#FFFFFF` / `#FAFAFA` (subtle off-white for cards)
- **Sand Background:** `#F5F1E8` / `#F9F7F3` (warm, calming base)
- **Emerald Accent:** `#10B981` (primary actions, success states)
- **Teal Accent:** `#14B8A6` (secondary actions, informational states)
- **Emerald Dark:** `#059669` (hover states, emphasis)
- **Teal Dark:** `#0D9488` (hover states)

#### Status Colors
- **Green (Safe/Silent):** `#10B981` with `#D1FAE5` background
- **Yellow (Informational):** `#F59E0B` with `#FEF3C7` background
- **Red (Action Required):** `#EF4444` with `#FEE2E2` background
- **Gray (Neutral):** `#6B7280` with `#F3F4F6` background

#### Semantic Colors
- **Text Primary:** `#111827` (dark gray, high contrast)
- **Text Secondary:** `#4B5563` (medium gray)
- **Text Tertiary:** `#9CA3AF` (light gray, hints)
- **Border:** `#E5E7EB` (subtle dividers)
- **Shadow:** `rgba(0, 0, 0, 0.08)` (soft, non-aggressive)

### Typography

#### Font Stack
- **Primary:** 'Cairo' (Arabic), 'Inter' (English)
- **Fallback:** 'Segoe UI', 'Tahoma', 'Arial', sans-serif
- **Monospace:** 'SF Mono', 'Monaco', 'Consolas' (for timestamps)

#### Scale
- **H1 (Page Title):** 28px / 1.2 / 700
- **H2 (Section Title):** 22px / 1.3 / 600
- **H3 (Card Title):** 18px / 1.4 / 600
- **Body Large:** 16px / 1.5 / 400
- **Body:** 14px / 1.5 / 400
- **Body Small:** 12px / 1.5 / 400
- **Caption:** 11px / 1.4 / 400

### Spacing System
- **Base Unit:** 4px
- **Scale:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96

### Border Radius
- **Cards:** 12px (standard), 16px (large cards)
- **Buttons:** 12px
- **Badges:** 20px (pill shape)
- **Icons:** 8px (small), 12px (medium)

### Shadows
- **Card Shadow:** `0 2px 8px rgba(0, 0, 0, 0.08)`
- **Elevated Shadow:** `0 4px 16px rgba(0, 0, 0, 0.12)`
- **Soft Shadow:** `0 1px 3px rgba(0, 0, 0, 0.06)`

---

## Core Screens

### 1. Family Home Dashboard

#### Layout Structure
```
┌─────────────────────────────────────────┐
│  Header (Greeting + Time Zone)          │
├─────────────────────────────────────────┤
│  Today Status Card (Summary)            │
├─────────────────────────────────────────┤
│  Child 1 Vertical Story                │
│  ┌───────────────────────────────────┐ │
│  │ Status Card (Large, Calm)         │ │
│  │ Quick Actions                     │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Child 2 Vertical Story                 │
│  ┌───────────────────────────────────┐ │
│  │ Status Card (Large, Calm)         │ │
│  │ Quick Actions                     │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Daily Digest Preview (5 bullets max)   │
├─────────────────────────────────────────┤
│  Bottom Navigation                      │
└─────────────────────────────────────────┘
```

#### Header Component
- **Height:** 80px
- **Background:** White with subtle sand gradient (`#FFFFFF` → `#FAFAFA`)
- **Content:**
  - Left: Greeting (time-aware: "صباح الخير" / "Good Morning")
  - Center: Current date (Arabic + English)
  - Right: Time zone indicator (if international parent)
- **Border:** Bottom border `1px solid #E5E7EB`

#### Today Status Card
- **Size:** Full width, 120px height
- **Background:** Sand (`#F5F1E8`) with white card overlay
- **Border Radius:** 16px
- **Content:**
  - Large status icon (Shield, Check, or Pulse) - 48px
  - Status text: "All children safe" / "جميع الأطفال آمنون"
  - Subtitle: "Last updated: 2 minutes ago" / "آخر تحديث: منذ دقيقتين"
- **Shadow:** Soft shadow
- **No color coding** - relies on icon + text

#### Child Status Card (Vertical Story)
- **Size:** Full width, minimum 280px height
- **Background:** White (`#FFFFFF`)
- **Border Radius:** 16px
- **Padding:** 24px
- **Border:** 2px solid (color based on status, subtle)
- **Shadow:** Card shadow

**Card Structure:**
1. **Header Section (80px)**
   - Child avatar/initials (64px circle)
   - Child name (H3)
   - Status badge (pill shape, icon + text)
   - Battery indicator (if applicable)

2. **Status Indicators Grid (3 columns)**
   - Location status (icon + text)
   - Health status (icon + text)
   - Activity status (icon + text)
   - Each: 100px × 80px mini-card

3. **AI Insight Banner (if applicable)**
   - Soft background (yellow or red, never alarming)
   - Icon + text message
   - "Learn more" link

4. **Quick Actions (2 buttons)**
   - Primary: "View Route" / "عرض المسار"
   - Secondary: "Contact School" / "الاتصال بالمدرسة"

#### Daily Digest Preview
- **Height:** Auto, max 200px
- **Background:** White card
- **Border Radius:** 12px
- **Content:**
  - Title: "Today's Summary" / "ملخص اليوم"
  - Bullet list (max 5 items)
  - "View Full Digest" link
- **No scroll** - if more than 5 items, show "View Full Digest"

#### Microcopy Examples
- Header: "Good morning, Ahmed" / "صباح الخير، أحمد"
- Status: "All children are safe" / "جميع الأطفال آمنون"
- Last update: "Updated 2 minutes ago" / "محدث منذ دقيقتين"
- Empty state: "No children registered" / "لا يوجد أطفال مسجلين"

---

### 2. Today Status Card (Detailed View)

#### Layout Structure
```
┌─────────────────────────────────────────┐
│  Back Button + Title                     │
├─────────────────────────────────────────┤
│  Large Status Display                    │
│  ┌───────────────────────────────────┐ │
│  │ Shield Icon (96px)                │ │
│  │ Status Text (H1)                  │ │
│  │ Subtitle                          │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Timeline Section                        │
│  ┌───────────────────────────────────┐ │
│  │ 07:30 - Boarded Bus               │ │
│  │ 08:15 - Arrived at School         │ │
│  │ 12:00 - Lunch Break               │ │
│  │ 15:30 - Dismissal                 │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Health Metrics (if applicable)         │
├─────────────────────────────────────────┤
│  Action Buttons                         │
└─────────────────────────────────────────┘
```

#### Large Status Display
- **Height:** 200px
- **Background:** Gradient (sand to white)
- **Icon:** 96px, centered
- **Text:** H1, centered
- **Subtitle:** Body, centered, secondary color

#### Timeline Section
- **Style:** Vertical timeline with dots
- **Items:** Max 10 items
- **Each Item:**
  - Time (left, monospace)
  - Icon (center, 24px circle)
  - Description (right, body text)
  - Connecting line (subtle gray)

#### Microcopy Examples
- Title: "Today's Status" / "حالة اليوم"
- Status: "All safe and accounted for" / "الجميع آمن ومحسوب"
- Timeline: "07:30 - Boarded bus #12" / "07:30 - ركوب الحافلة رقم 12"
- Empty: "No activity recorded yet" / "لا يوجد نشاط مسجل بعد"

---

### 3. Route Timeline

#### Layout Structure
```
┌─────────────────────────────────────────┐
│  Back Button + Child Name                │
├─────────────────────────────────────────┤
│  Simplified Map View (Optional)          │
│  ┌───────────────────────────────────┐ │
│  │ Minimal Route Visualization       │ │
│  │ (No street names, just path)      │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Route Timeline                         │
│  ┌───────────────────────────────────┐ │
│  │ Home → Bus Stop → School          │ │
│  │ (Interactive timeline)            │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Current Location Card                  │
├─────────────────────────────────────────┤
│  Estimated Arrival                      │
└─────────────────────────────────────────┘
```

#### Simplified Map View
- **Height:** 200px (mobile), 300px (tablet/desktop)
- **Style:** Minimal, no street clutter
- **Elements:**
  - Route path (teal line, 4px width)
  - Current location (pulsing dot, emerald)
  - Key waypoints (labeled circles)
- **No zoom controls** - auto-fits route
- **Privacy:** No street names, just landmarks

#### Route Timeline
- **Style:** Horizontal scrollable timeline
- **Items:**
  - Waypoint name
  - Time (actual or estimated)
  - Status icon (completed, current, upcoming)
- **Interaction:** Tap to see details

#### Current Location Card
- **Background:** White card
- **Content:**
  - Large location name
  - "Last updated: 1 min ago"
  - Battery status (if applicable)

#### Microcopy Examples
- Title: "Route to School" / "المسار إلى المدرسة"
- Current: "Currently at: Bus Stop 3" / "الموقع الحالي: محطة الحافلة 3"
- ETA: "Estimated arrival: 08:15" / "الوصول المتوقع: 08:15"
- No GPS: "Location unavailable" / "الموقع غير متاح"

---

### 4. Daily Digest

#### Layout Structure
```
┌─────────────────────────────────────────┐
│  Back Button + Date Selector             │
├─────────────────────────────────────────┤
│  Summary Card                            │
│  ┌───────────────────────────────────┐ │
│  │ Today's Overview                  │ │
│  │ (Stats: Safe, On Time, etc.)     │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Digest Items (Max 5)                   │
│  ┌───────────────────────────────────┐ │
│  │ Item 1: Bullet point              │ │
│  │ Item 2: Bullet point              │ │
│  │ ...                               │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Child-Specific Digests (Collapsible)   │
└─────────────────────────────────────────┘
```

#### Summary Card
- **Background:** Sand gradient
- **Content:**
  - Date (large, prominent)
  - Key stats (icons + numbers)
    - "All safe" / "الجميع آمن"
    - "On time" / "في الوقت المحدد"
    - "No concerns" / "لا توجد مخاوف"

#### Digest Items
- **Max 5 items** (enforced)
- **Format:** Bullet list
- **Each Item:**
  - Icon (16px, contextual)
  - Text (body, concise)
  - Time (caption, secondary)
- **No scroll** - if more, show "View detailed report"

#### Child-Specific Digests
- **Collapsible sections** (one per child)
- **Content:** Same format as main digest
- **Interaction:** Tap to expand/collapse

#### Microcopy Examples
- Title: "Daily Digest" / "الملخص اليومي"
- Summary: "A calm day with no incidents" / "يوم هادئ بدون حوادث"
- Items: "• Arrived on time at 08:15" / "• الوصول في الوقت المحدد 08:15"
- Empty: "No activity to report" / "لا يوجد نشاط للإبلاغ عنه"

---

### 5. Requests & Approvals

#### Layout Structure
```
┌─────────────────────────────────────────┐
│  Back Button + Title                     │
├─────────────────────────────────────────┤
│  Filter Tabs (Pending / Approved / All) │
├─────────────────────────────────────────┤
│  Request Cards (List)                    │
│  ┌───────────────────────────────────┐ │
│  │ Request Type + Child Name         │ │
│  │ Details                           │ │
│  │ Status Badge                      │ │
│  │ Action Button (if pending)        │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  New Request Button (FAB)               │
└─────────────────────────────────────────┘
```

#### Request Card
- **Background:** White card
- **Border:** 2px (color based on status)
- **Padding:** 20px
- **Content:**
  - Header: Request type icon + title
  - Child name (body, secondary)
  - Details (body, truncated if long)
  - Status badge (pill, icon + text)
  - Action button (if applicable)
  - SLA timer (progress bar, if pending)

#### Status Badges
- **Pending:** Yellow badge, "Awaiting approval" / "في انتظار الموافقة"
- **Approved:** Green badge, "Approved" / "موافق عليه"
- **Rejected:** Gray badge, "Not approved" / "غير موافق"
- **Expired:** Gray badge, "Expired" / "منتهي الصلاحية"

#### SLA Timer
- **Style:** Progress bar (horizontal)
- **Color:** Teal (time remaining), gray (expired)
- **Label:** "Response expected within 2 hours" / "الرد المتوقع خلال ساعتين"
- **Visual:** Animated progress bar

#### New Request Button
- **Style:** Floating Action Button (FAB)
- **Position:** Bottom right (mobile), fixed
- **Icon:** Plus icon
- **Label:** "New Request" / "طلب جديد"

#### Microcopy Examples
- Title: "Requests & Approvals" / "الطلبات والموافقات"
- Pending: "Early pickup request for Fatima" / "طلب استلام مبكر لفاطمة"
- Approved: "Your request has been approved" / "تمت الموافقة على طلبك"
- Empty: "No requests yet" / "لا توجد طلبات بعد"

---

### 6. Concerns & Escalations

#### Layout Structure
```
┌─────────────────────────────────────────┐
│  Back Button + Title                     │
├─────────────────────────────────────────┤
│  Info Banner (Reassuring)                │
│  ┌───────────────────────────────────┐ │
│  │ "We're here to help" message      │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Active Concerns (if any)                │
│  ┌───────────────────────────────────┐ │
│  │ Concern Card                      │ │
│  │ Status + Progress                 │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Resolved Concerns (Collapsible)        │
├─────────────────────────────────────────┤
│  New Concern Button (FAB)               │
└─────────────────────────────────────────┘
```

#### Info Banner
- **Background:** Teal (`#14B8A6`) with `#D1FAE5` background
- **Content:**
  - Icon: Shield or Help icon
  - Text: "We're here to help. Your concerns are taken seriously." / "نحن هنا للمساعدة. مخاوفك تؤخذ على محمل الجد."
- **Tone:** Reassuring, not alarming

#### Concern Card
- **Background:** White card
- **Border:** 2px (color based on priority)
- **Content:**
  - Header: Concern type + child name
  - Description (body text)
  - Status badge
  - Progress indicator (if in progress)
  - Last update timestamp
  - Action button ("View details" / "عرض التفاصيل")

#### Status Badges
- **New:** Yellow, "Under review" / "قيد المراجعة"
- **In Progress:** Teal, "Being addressed" / "قيد المعالجة"
- **Resolved:** Green, "Resolved" / "تم الحل"
- **Closed:** Gray, "Closed" / "مغلق"

#### Progress Indicator
- **Style:** Progress bar with steps
- **Steps:** Submitted → Under Review → In Progress → Resolved
- **Current step:** Highlighted in teal
- **Label:** "Step 2 of 4" / "الخطوة 2 من 4"

#### New Concern Button
- **Style:** FAB (same as Requests)
- **Label:** "Report Concern" / "الإبلاغ عن قلق"

#### Microcopy Examples
- Title: "Concerns & Escalations" / "المخاوف والتكرارات"
- Info: "Your concerns are important to us" / "مخاوفك مهمة بالنسبة لنا"
- New: "New concern submitted" / "تم إرسال قلق جديد"
- Resolved: "Your concern has been resolved" / "تم حل قلقك"
- Empty: "No active concerns" / "لا توجد مخاوف نشطة"

---

## Component Library

### StatusCard Component

**Purpose:** Display child status in a calm, non-alarming way

**Props:**
- `status`: 'safe' | 'informational' | 'action-required'
- `childName`: string
- `lastUpdate`: Date
- `indicators`: Array of status indicators
- `onViewDetails`: function
- `onContactSchool`: function

**Visual States:**
- **Safe:** Green border (subtle), shield icon, "All safe" text
- **Informational:** Yellow border (subtle), info icon, "Please note" text
- **Action Required:** Red border (subtle), alert icon, "Action needed" text

**Accessibility:**
- ARIA labels for all icons
- Status announced to screen readers
- Keyboard navigation support

---

### StatusBadge Component

**Purpose:** Show status with icon + text (never color alone)

**Props:**
- `status`: string
- `icon`: ReactNode
- `text`: string
- `variant`: 'pill' | 'inline'

**Visual:**
- Icon (16px) + Text (body small)
- Background color (subtle)
- Border (1px, matching color)

**Accessibility:**
- Text always present (no color-only indicators)
- High contrast ratio (WCAG AA)

---

### RouteTimeline Component

**Purpose:** Show simplified route without map overload

**Props:**
- `waypoints`: Array of waypoint objects
- `currentLocation`: waypoint object
- `estimatedArrival`: Date

**Visual:**
- Horizontal or vertical timeline
- Waypoint circles (24px)
- Connecting lines (subtle gray)
- Current location (pulsing animation)

**Interaction:**
- Tap waypoint to see details
- Swipe to scroll (mobile)

---

### DailyDigestItem Component

**Purpose:** Display digest item (max 5)

**Props:**
- `icon`: ReactNode
- `text`: string
- `time`: Date
- `priority`: 'high' | 'normal' | 'low'

**Visual:**
- Bullet point with icon
- Text (body)
- Time (caption, secondary)

**Limitation:**
- Max 5 items displayed
- "View full digest" link if more

---

### RequestCard Component

**Purpose:** Display approval request

**Props:**
- `type`: string
- `childName`: string
- `details`: string
- `status`: 'pending' | 'approved' | 'rejected'
- `slaTimer`: number (hours remaining)
- `onApprove`: function (if parent is approver)
- `onViewDetails`: function

**Visual:**
- Card with border (color by status)
- Header with type icon
- Details section
- Status badge
- SLA progress bar (if pending)
- Action button (contextual)

---

### ConcernCard Component

**Purpose:** Display concern/escalation

**Props:**
- `type`: string
- `childName`: string
- `description`: string
- `status`: 'new' | 'in-progress' | 'resolved' | 'closed'
- `progress`: number (0-100)
- `lastUpdate`: Date
- `onViewDetails`: function

**Visual:**
- Card with border (color by priority)
- Header with type
- Description (truncated if long)
- Status badge
- Progress indicator (if in progress)
- Last update timestamp

---

### SLAProgressBar Component

**Purpose:** Show response time remaining

**Props:**
- `hoursRemaining`: number
- `totalHours`: number
- `label`: string

**Visual:**
- Horizontal progress bar
- Color: Teal (time remaining), gray (expired)
- Label above bar
- Percentage or time remaining

**Animation:**
- Smooth progress animation
- Pulsing when < 1 hour remaining

---

## Interaction Patterns

### Status Communication

#### Green Status (Safe/Silent)
- **Visual:** Green border (subtle), shield icon, "All safe" text
- **Notification:** None (silent)
- **Action:** None required
- **Microcopy:** "All children are safe and accounted for" / "جميع الأطفال آمنون ومحسوبون"

#### Yellow Status (Informational)
- **Visual:** Yellow border (subtle), info icon, "Please note" text
- **Notification:** Soft banner (non-intrusive)
- **Action:** Optional (view details)
- **Microcopy:** "Please note: Early dismissal scheduled" / "يرجى الملاحظة: تم جدولة الخروج المبكر"

#### Red Status (Action Required)
- **Visual:** Red border (subtle), alert icon, "Action needed" text
- **Notification:** Clear banner with CTA
- **Action:** Required (clear button)
- **Microcopy:** "Action needed: Please approve pickup request" / "إجراء مطلوب: يرجى الموافقة على طلب الاستلام"
- **Tone:** Clear, not alarmist

---

### Navigation Patterns

#### Bottom Navigation (Mobile)
- **Items:** Dashboard, Route, Digest, Requests, Concerns
- **Style:** Fixed bottom, white background, subtle shadow
- **Icons:** Lucide icons (Shield, Map, FileText, CheckCircle, AlertCircle)
- **Active State:** Teal underline + icon color

#### Top Navigation (Tablet/Desktop)
- **Style:** Horizontal, fixed top
- **Items:** Same as mobile
- **Additional:** Profile menu, notifications

#### Breadcrumbs (Deep Navigation)
- **Style:** Subtle, above page title
- **Format:** Home > Route > Details
- **Interaction:** Tap to navigate back

---

### Gesture Patterns

#### Swipe Actions
- **Route Timeline:** Swipe left/right to navigate waypoints
- **Request Cards:** Swipe to approve/reject (if applicable)
- **Digest Items:** Swipe to dismiss (if applicable)

#### Pull to Refresh
- **Dashboard:** Pull down to refresh status
- **Route Timeline:** Pull down to update location
- **Visual:** Subtle spinner, no aggressive animation

#### Long Press
- **Status Cards:** Long press for quick actions menu
- **Request Cards:** Long press for context menu

---

### Loading States

#### Skeleton Loading
- **Style:** Subtle gray boxes, animated shimmer
- **Duration:** Max 2 seconds
- **Placeholder:** Match final content layout

#### Progress Indicators
- **Style:** Circular spinner (teal)
- **Size:** 32px (small), 48px (medium), 64px (large)
- **Label:** "Loading..." / "جاري التحميل..."

#### Optimistic Updates
- **Actions:** Show success immediately
- **Fallback:** Revert if error occurs
- **Feedback:** Toast notification on error

---

### Error States

#### Network Error
- **Visual:** Soft yellow banner
- **Icon:** Wifi-off icon
- **Message:** "Connection lost. Retrying..." / "فقد الاتصال. إعادة المحاولة..."
- **Action:** Auto-retry with manual retry button

#### Not Found Error
- **Visual:** Empty state illustration
- **Message:** "Content not found" / "المحتوى غير موجود"
- **Action:** "Go back" button

#### Permission Error
- **Visual:** Info banner (teal)
- **Message:** "You don't have permission to view this" / "ليس لديك إذن لعرض هذا"
- **Action:** "Contact administrator" link

---

## Microcopy & Tone

### Tone Guidelines

#### Core Principles
1. **Reassuring:** Always calm, never alarmist
2. **Respectful:** Formal but warm (UAE cultural context)
3. **Non-technical:** Avoid jargon, use plain language
4. **Clear:** Direct, actionable when needed
5. **Concise:** Short sentences, scannable

#### Voice Characteristics
- **Formal but warm:** "We're here to help" not "We got you"
- **Respectful:** Use titles when appropriate (Mr./Mrs. in English, proper Arabic forms)
- **Confident:** "All safe" not "Everything seems okay"
- **Actionable:** "Please approve" not "You might want to approve"

---

### Microcopy Examples

#### Dashboard
- **Greeting:** "Good morning, Ahmed" / "صباح الخير، أحمد"
- **Status:** "All children are safe and accounted for" / "جميع الأطفال آمنون ومحسوبون"
- **Last Update:** "Updated 2 minutes ago" / "محدث منذ دقيقتين"
- **Empty:** "No children registered yet" / "لا يوجد أطفال مسجلين بعد"

#### Route Timeline
- **Title:** "Route to School" / "المسار إلى المدرسة"
- **Current:** "Currently at: Bus Stop 3" / "الموقع الحالي: محطة الحافلة 3"
- **ETA:** "Estimated arrival: 08:15" / "الوصول المتوقع: 08:15"
- **No GPS:** "Location temporarily unavailable" / "الموقع غير متاح مؤقتاً"

#### Daily Digest
- **Title:** "Today's Summary" / "ملخص اليوم"
- **Summary:** "A calm day with no incidents" / "يوم هادئ بدون حوادث"
- **Items:** "• Arrived on time at 08:15" / "• الوصول في الوقت المحدد 08:15"
- **Empty:** "No activity to report today" / "لا يوجد نشاط للإبلاغ عنه اليوم"

#### Requests & Approvals
- **Title:** "Requests & Approvals" / "الطلبات والموافقات"
- **Pending:** "Early pickup request for Fatima" / "طلب استلام مبكر لفاطمة"
- **Approved:** "Your request has been approved" / "تمت الموافقة على طلبك"
- **SLA:** "Response expected within 2 hours" / "الرد المتوقع خلال ساعتين"
- **Empty:** "No requests yet" / "لا توجد طلبات بعد"

#### Concerns & Escalations
- **Title:** "Concerns & Escalations" / "المخاوف والتكرارات"
- **Info:** "We're here to help. Your concerns are taken seriously." / "نحن هنا للمساعدة. مخاوفك تؤخذ على محمل الجد."
- **New:** "New concern submitted" / "تم إرسال قلق جديد"
- **Resolved:** "Your concern has been resolved" / "تم حل قلقك"
- **Empty:** "No active concerns" / "لا توجد مخاوف نشطة"

#### Error Messages
- **Network:** "Connection lost. We're retrying automatically." / "فقد الاتصال. نقوم بإعادة المحاولة تلقائياً."
- **Not Found:** "Content not found. Please go back." / "المحتوى غير موجود. يرجى العودة."
- **Permission:** "You don't have permission to view this content." / "ليس لديك إذن لعرض هذا المحتوى."

#### Success Messages
- **Approved:** "Request approved successfully" / "تمت الموافقة على الطلب بنجاح"
- **Submitted:** "Concern submitted. We'll review it shortly." / "تم إرسال القلق. سنراجعه قريباً."
- **Updated:** "Status updated" / "تم تحديث الحالة"

---

## States & Edge Cases

### Empty States

#### No Children Registered
- **Visual:** Illustration (shield icon, soft colors)
- **Message:** "No children registered yet" / "لا يوجد أطفال مسجلين بعد"
- **Action:** "Contact school to register" / "اتصل بالمدرسة للتسجيل"

#### No Activity Today
- **Visual:** Calendar icon illustration
- **Message:** "No activity recorded today" / "لا يوجد نشاط مسجل اليوم"
- **Action:** None (informational only)

#### No Requests
- **Visual:** CheckCircle icon illustration
- **Message:** "No requests yet" / "لا توجد طلبات بعد"
- **Action:** "Create new request" button (FAB)

#### No Concerns
- **Visual:** Shield icon illustration
- **Message:** "No active concerns" / "لا توجد مخاوف نشطة"
- **Action:** "Report concern" button (FAB)

---

### Loading States

#### Initial Load
- **Style:** Skeleton screens matching final layout
- **Duration:** Max 2 seconds
- **Feedback:** "Loading your dashboard..." / "جاري تحميل لوحة التحكم..."

#### Refreshing Data
- **Style:** Subtle spinner in header
- **Duration:** Max 5 seconds
- **Feedback:** "Updating..." / "جاري التحديث..."

#### Submitting Form
- **Style:** Button shows spinner, disabled state
- **Duration:** Max 10 seconds
- **Feedback:** "Submitting..." / "جاري الإرسال..."

---

### Error States

#### Network Error
- **Visual:** Soft yellow banner at top
- **Message:** "Connection lost. Retrying automatically..." / "فقد الاتصال. إعادة المحاولة تلقائياً..."
- **Action:** "Retry now" button
- **Auto-retry:** Every 5 seconds, max 3 attempts

#### Server Error
- **Visual:** Info banner (teal)
- **Message:** "Service temporarily unavailable. Please try again later." / "الخدمة غير متاحة مؤقتاً. يرجى المحاولة لاحقاً."
- **Action:** "Retry" button

#### Validation Error
- **Visual:** Inline error below field
- **Message:** Specific, actionable error
- **Example:** "Please select a date" / "يرجى اختيار تاريخ"

---

### Permission States

#### Primary Guardian
- **Access:** Full access to all features
- **Indicators:** None (default state)
- **Actions:** All actions available

#### Secondary Guardian
- **Access:** Limited access (view-only for some features)
- **Indicators:** Subtle badge "Secondary Guardian" / "ولي أمر ثانوي"
- **Actions:** Limited actions (no approvals, view-only route)

#### International Parent (Time Zone)
- **Access:** Full access
- **Indicators:** Time zone badge in header
- **Display:** All times shown in parent's time zone
- **Label:** "GMT+4" or time zone name

---

### Data States

#### No GPS Signal
- **Visual:** Gray location icon, "Unknown" text
- **Message:** "Location temporarily unavailable" / "الموقع غير متاح مؤقتاً"
- **Action:** None (informational)

#### Low Battery
- **Visual:** Yellow battery icon, percentage
- **Message:** "Tracker battery low" / "بطارية المتتبع منخفضة"
- **Action:** "Contact school" link

#### Historical Data
- **Visual:** Date selector at top
- **Message:** "Viewing data for [date]" / "عرض بيانات [التاريخ]"
- **Action:** "View today" button

---

## Accessibility & RTL

### WCAG AA Compliance

#### Color Contrast
- **Text on White:** Minimum 4.5:1 ratio
- **Text on Colored Backgrounds:** Minimum 4.5:1 ratio
- **Large Text (18px+):** Minimum 3:1 ratio
- **Interactive Elements:** Minimum 3:1 ratio

#### Focus Indicators
- **Style:** 2px teal outline, 2px offset
- **Visibility:** Always visible, high contrast
- **Keyboard Navigation:** Full support

#### Screen Reader Support
- **ARIA Labels:** All icons and interactive elements
- **Status Announcements:** Live regions for status changes
- **Landmarks:** Proper semantic HTML
- **Alt Text:** All images and illustrations

#### Keyboard Navigation
- **Tab Order:** Logical, sequential
- **Shortcuts:** Standard (Enter to submit, Esc to close)
- **Focus Trapping:** Modals and overlays
- **Skip Links:** "Skip to main content" link

---

### RTL (Right-to-Left) Support

#### Layout Adjustments
- **Direction:** `dir="rtl"` on HTML element
- **Text Alignment:** Right-aligned for Arabic
- **Icons:** Flipped horizontally (arrows, chevrons)
- **Timeline:** Right-to-left flow

#### Arabic Typography
- **Font:** Cairo (optimized for Arabic)
- **Line Height:** 1.6 (slightly higher for Arabic)
- **Letter Spacing:** Normal (no extra spacing)
- **Numbers:** Arabic-Indic numerals (optional, user preference)

#### Mixed Content
- **English in Arabic UI:** Left-aligned, smaller font
- **Arabic in English UI:** Right-aligned, proper font
- **Dates:** Format based on locale
- **Numbers:** Consistent formatting

#### Cultural Considerations
- **Greetings:** Time-aware (صباح الخير, مساء الخير)
- **Formal Address:** Proper titles (Mr./Mrs. in English)
- **Date Format:** Hijri calendar option (user preference)
- **Time Format:** 12-hour or 24-hour (user preference)

---

## UX Rationale

### Design Decisions

#### Why Large Calm Status Cards?
- **Rationale:** Parents need confidence, not anxiety. Large cards with clear status (icon + text) reduce cognitive load and provide immediate reassurance.
- **Research:** Studies show that parents prefer clear, non-alarming status displays over detailed technical information.

#### Why Simplified Route Timeline?
- **Rationale:** Map overload causes anxiety. Simplified timeline shows essential information (where, when) without street-level detail that parents don't need.
- **Privacy:** No street names protect student privacy while still providing useful location context.

#### Why Max 5 Digest Items?
- **Rationale:** Cognitive load reduction. Parents can quickly scan 5 items. More items require scrolling and increase anxiety.
- **Solution:** "View full digest" link for detailed information when needed.

#### Why Color + Icon + Text (Never Color Alone)?
- **Rationale:** Accessibility and cultural sensitivity. Color-blind users and cultural color associations require multiple indicators.
- **WCAG Compliance:** Ensures AA compliance and reduces misinterpretation.

#### Why Soft Shadows and Rounded Corners?
- **Rationale:** Calm, modern aesthetic. Soft shadows create depth without aggression. Rounded corners feel friendly and approachable.
- **UAE Context:** Aligns with premium app standards (TAMM, DubaiNow) that use similar design language.

#### Why Sand Backgrounds?
- **Rationale:** Cultural connection and calmness. Sand colors evoke UAE landscape and create warm, calming atmosphere.
- **Contrast:** White cards on sand background provide clear hierarchy without harsh contrast.

#### Why No Panic Colors?
- **Rationale:** Anxiety reduction. Red should indicate action needed, not danger. Yellow indicates information, not warning. Green indicates safety, not just "okay."
- **Tone:** Platform should reassure, not alarm.

#### Why Permission-Aware Views?
- **Rationale:** Family structure respect. UAE families often have multiple guardians with different permission levels.
- **Privacy:** Secondary guardians see only what's necessary, respecting primary guardian's privacy preferences.

#### Why SLA Timers as Progress Bars?
- **Rationale:** Transparency without pressure. Progress bars show response time expectations without creating urgency or anxiety.
- **Trust:** Clear expectations build trust in the system.

#### Why International Parent Mode?
- **Rationale:** UAE's international community. Many parents travel or live in different time zones.
- **UX:** Time zone awareness prevents confusion and missed notifications.

---

### User Journey Considerations

#### Morning Routine (07:00 - 08:30)
- **Focus:** Route timeline, arrival confirmation
- **Notifications:** Minimal (only if action needed)
- **Tone:** Reassuring ("On the way" / "في الطريق")

#### School Hours (08:30 - 15:00)
- **Focus:** Status cards, daily digest
- **Notifications:** Silent (green status), informational banners (yellow)
- **Tone:** Calm, informative

#### Dismissal (15:00 - 16:00)
- **Focus:** Route timeline, pickup confirmation
- **Notifications:** Action required only (red status)
- **Tone:** Clear, actionable

#### Evening (After 16:00)
- **Focus:** Daily digest, requests, concerns
- **Notifications:** Summary only
- **Tone:** Reflective, summary-focused

---

### Emotional Design

#### Confidence Building
- **Large status cards:** Immediate reassurance
- **Clear communication:** No ambiguity
- **Consistent updates:** "Last updated 2 min ago" builds trust

#### Anxiety Reduction
- **No alarmist language:** "Action needed" not "URGENT!"
- **Soft colors:** Calm palette reduces stress
- **Limited information:** 5 digest items prevent overload

#### Trust Building
- **Transparency:** SLA timers show response expectations
- **Consistency:** Same design language throughout
- **Reliability:** "Last updated" timestamps show system is active

#### Cultural Respect
- **Bilingual support:** Arabic and English equally prominent
- **Formal tone:** Respectful language appropriate for UAE context
- **Privacy-first:** No unnecessary personal data displayed

---

## Implementation Notes

### Technical Considerations

#### Responsive Breakpoints
- **Mobile:** < 640px (primary target)
- **Tablet:** 640px - 1024px
- **Desktop:** > 1024px

#### Performance
- **Lazy loading:** Images and heavy components
- **Optimistic updates:** Immediate feedback
- **Caching:** Status data cached for 30 seconds

#### Internationalization
- **i18n Library:** react-i18next or similar
- **Locale Detection:** Browser + user preference
- **Date/Time:** Moment.js or date-fns with timezone support

#### State Management
- **Status Updates:** Real-time via WebSocket or polling
- **Offline Support:** Service worker for offline viewing
- **Sync:** Background sync when connection restored

---

## Conclusion

This design document provides a comprehensive blueprint for a premium, government-grade Parent/Guardian experience that prioritizes:

1. **Calm confidence** over anxiety
2. **Clear communication** over technical detail
3. **Cultural respect** through bilingual, RTL-ready design
4. **Accessibility** through WCAG AA compliance
5. **Privacy** through minimal data display
6. **Trust** through transparency and consistency

The design aligns with UAE premium app standards (TAMM, DubaiNow) while addressing the unique needs of school safety platforms: reassurance without alarm, information without overload, and action without pressure.

---

**Document Status:** Complete  
**Next Steps:** Component implementation, user testing, iteration


