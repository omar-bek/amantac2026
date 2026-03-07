# دليل إعداد Frontend

## المتطلبات

- Node.js 16+ 
- npm أو yarn

## التثبيت

```bash
cd frontend
npm install
```

## التطوير

```bash
npm run dev
```

التطبيق سيعمل على: http://localhost:3000

## إعداد المتغيرات البيئية

أنشئ ملف `.env` في مجلد `frontend`:

```env
VITE_API_URL=http://localhost:8000/api
```

## البناء للإنتاج

```bash
npm run build
```

الملفات المبنية ستكون في مجلد `dist`

## الميزات

✅ **تصميم عصري وبسيط** مع Tailwind CSS
✅ **دعم RTL** (من اليمين لليسار)
✅ **تصميم متجاوب** (Responsive) لجميع الأجهزة
✅ **أيقونات عصرية** من Lucide React
✅ **إشعارات فورية** مع React Hot Toast
✅ **إدارة حالة** مع Zustand
✅ **API Integration** مع React Query

## الصفحات

- `/login` - تسجيل الدخول
- `/register` - التسجيل
- `/` - لوحة التحكم
- `/students` - إدارة الطلاب
- `/attendance` - الحضور والغياب
- `/buses` - تتبع الحافلات
- `/pickup` - الاستلام الآمن
- `/dismissal` - إذونات المغادرة
- `/academic` - الأداء الأكاديمي
- `/behavior` - السلوك
- `/activities` - الأنشطة
- `/notifications` - الإشعارات

## الربط مع Backend

التطبيق مربوط تلقائياً مع Backend عبر:
- Proxy في `vite.config.ts` للـ API calls
- Axios client في `src/api/client.ts`
- Token authentication تلقائي

## الألوان

- Primary: Blue (#0ea5e9)
- Success: Green
- Warning: Yellow
- Danger: Red
- Gray: للخلفيات والنصوص

## الخطوات التالية

1. تأكد من تشغيل Backend على http://localhost:8000
2. شغّل Frontend: `npm run dev`
3. افتح http://localhost:3000
4. سجّل دخول أو أنشئ حساب جديد





