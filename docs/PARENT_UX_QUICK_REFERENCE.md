# Parent UX - Quick Reference Guide
## For Developers & Designers

### Color Tokens (Tailwind/CSS Variables)

```css
/* Primary Colors */
--color-white: #FFFFFF;
--color-sand: #F5F1E8;
--color-emerald: #10B981;
--color-teal: #14B8A6;
--color-emerald-dark: #059669;
--color-teal-dark: #0D9488;

/* Status Colors */
--color-safe: #10B981;
--color-safe-bg: #D1FAE5;
--color-info: #F59E0B;
--color-info-bg: #FEF3C7;
--color-action: #EF4444;
--color-action-bg: #FEE2E2;

/* Text Colors */
--color-text-primary: #111827;
--color-text-secondary: #4B5563;
--color-text-tertiary: #9CA3AF;
--color-border: #E5E7EB;
```

### Component Specifications

#### StatusCard
- **Border Radius:** 16px
- **Padding:** 24px
- **Border:** 2px solid (status color, subtle)
- **Shadow:** `0 2px 8px rgba(0, 0, 0, 0.08)`
- **Min Height:** 280px

#### StatusBadge
- **Shape:** Pill (border-radius: 20px)
- **Padding:** 8px 16px
- **Icon Size:** 16px
- **Font Size:** 12px
- **Always includes:** Icon + Text (never color alone)

#### RouteTimeline
- **Waypoint Circle:** 24px
- **Line Width:** 2px, color: #E5E7EB
- **Current Location:** Pulsing animation (2s cycle)
- **Map Height:** 200px (mobile), 300px (desktop)

#### DailyDigest
- **Max Items:** 5 (hard limit)
- **Item Height:** Auto, min 48px
- **Bullet Icon:** 16px
- **Font Size:** 14px (body)

### Microcopy Templates

#### Status Messages
- Safe: "All children are safe and accounted for" / "جميع الأطفال آمنون ومحسوبون"
- Info: "Please note: [detail]" / "يرجى الملاحظة: [التفاصيل]"
- Action: "Action needed: [action]" / "إجراء مطلوب: [الإجراء]"

#### Time Formats
- Relative: "2 minutes ago" / "منذ دقيقتين"
- Absolute: "08:15 AM" / "08:15 صباحاً"
- Date: "January 25, 2025" / "25 يناير 2025"

#### Empty States
- Pattern: "[Context] not available yet" / "[السياق] غير متاح بعد"
- Action: "Contact school" / "اتصل بالمدرسة"

### Interaction Patterns

#### Status Communication Rules
1. **Green (Safe):** Silent, no notification
2. **Yellow (Info):** Soft banner, optional action
3. **Red (Action):** Clear banner, required action

#### Navigation
- **Mobile:** Bottom nav (fixed)
- **Tablet/Desktop:** Top nav (fixed)
- **Back Button:** Always visible, left-aligned (RTL: right-aligned)

#### Gestures
- **Swipe:** Route timeline (left/right)
- **Pull to Refresh:** Dashboard, route
- **Long Press:** Quick actions menu

### Accessibility Checklist

- [ ] All icons have ARIA labels
- [ ] Status announced to screen readers
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Keyboard navigation fully functional
- [ ] Focus indicators visible (2px teal outline)
- [ ] RTL support tested
- [ ] Text never relies on color alone

### RTL Implementation

```css
[dir="rtl"] {
  direction: rtl;
}

[dir="rtl"] .icon-arrow {
  transform: scaleX(-1); /* Flip arrows */
}
```

### State Management

#### Status States
```typescript
type Status = 'safe' | 'informational' | 'action-required';
type LocationStatus = 'ok' | 'warning' | 'unknown';
type RequestStatus = 'pending' | 'approved' | 'rejected' | 'expired';
type ConcernStatus = 'new' | 'in-progress' | 'resolved' | 'closed';
```

#### Permission Levels
```typescript
type GuardianRole = 'primary' | 'secondary';
type AccessLevel = 'full' | 'view-only';
```

### Performance Targets

- **Initial Load:** < 2 seconds
- **Status Update:** < 500ms
- **Route Render:** < 1 second
- **Image Load:** Lazy load, placeholder shown

### Testing Checklist

- [ ] All 6 core screens render correctly
- [ ] Status cards show correct colors/icons/text
- [ ] Route timeline scrolls smoothly
- [ ] Daily digest limits to 5 items
- [ ] Requests show SLA timers
- [ ] Concerns show progress indicators
- [ ] Empty states display correctly
- [ ] Loading states show skeletons
- [ ] Error states show appropriate messages
- [ ] RTL layout works correctly
- [ ] Arabic text renders properly
- [ ] Time zone conversion works
- [ ] Permission levels restrict access correctly
- [ ] All interactions work on mobile/tablet/desktop

---

**Quick Links:**
- Full Design Document: `PARENT_UX_DESIGN.md`
- Component Library: See main document
- API Integration: See `API_DOCUMENTATION.md`


