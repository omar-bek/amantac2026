# دليل البدء السريع - Quick Start Guide

## 🚀 البدء السريع

### 1. إعداد Backend

```bash
# الانتقال لمجلد Backend
cd backend

# تثبيت المتطلبات
pip install -r ../requirements.txt

# إنشاء ملف البيئة
copy .env.example .env
# على Linux/macOS: cp .env.example .env

# تعديل ملف .env وإضافة بيانات قاعدة البيانات
# DATABASE_URL=postgresql://user:password@localhost:5432/amantac_db
# SECRET_KEY=your-secret-key-here

# تهيئة قاعدة البيانات
python setup.py

# تشغيل الخادم
python main.py
```

Backend سيعمل على: **http://localhost:8000**
- API Docs: http://localhost:8000/docs

### 2. إعداد Frontend

```bash
# في terminal جديد، الانتقال لمجلد Frontend
cd frontend

# تثبيت المتطلبات
npm install

# إنشاء ملف البيئة
copy .env.example .env
# على Linux/macOS: cp .env.example .env

# تشغيل التطبيق
npm run dev
```

Frontend سيعمل على: **http://localhost:3000**

### 3. تسجيل الدخول

افتح المتصفح على: http://localhost:3000

**حساب Admin افتراضي:**
- البريد: `admin@amantac.com`
- كلمة المرور: `admin123`

⚠️ **مهم**: غيّر كلمة المرور بعد أول تسجيل دخول!

## 📱 الصفحات المتاحة

- `/login` - تسجيل الدخول
- `/register` - إنشاء حساب جديد
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

## 🔧 استكشاف الأخطاء

### Backend لا يعمل
- تأكد من تشغيل PostgreSQL
- تحقق من ملف `.env` وصحة بيانات الاتصال
- تأكد من تثبيت جميع المتطلبات

### Frontend لا يعمل
- تأكد من تثبيت Node.js 16+
- تحقق من تثبيت المتطلبات: `npm install`
- تأكد من تشغيل Backend على المنفذ 8000

### مشاكل الاتصال
- تأكد من تشغيل Backend قبل Frontend
- تحقق من `VITE_API_URL` في ملف `.env` للـ Frontend
- تحقق من CORS settings في Backend

## 📚 الوثائق

- `README.md` - نظرة عامة
- `SETUP.md` - دليل الإعداد الكامل
- `FRONTEND_SETUP.md` - دليل Frontend
- `docs/API_DOCUMENTATION.md` - وثائق API
- `docs/ARCHITECTURE.md` - بنية النظام

## 🎨 الميزات

✅ **تصميم عصري** - واجهة مستخدم جميلة وسهلة الاستخدام
✅ **متجاوب** - يعمل على جميع الأجهزة (موبايل، تابلت، ديسكتوب)
✅ **RTL Support** - دعم كامل للغة العربية
✅ **Real-time** - تحديثات فورية
✅ **آمن** - نظام مصادقة قوي

## 🚀 الخطوات التالية

1. ✅ Backend جاهز
2. ✅ Frontend جاهز
3. ⏳ Mobile App (قيد التطوير)
4. ⏳ Hardware Integration (RFID, GPS)
5. ⏳ SMS/Email Notifications

---

**استمتع باستخدام النظام! 🎉**





