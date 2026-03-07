# دليل النشر على Plesk - Plesk Deployment Guide

## 📋 المتطلبات الأساسية

قبل البدء، تأكد من توفر:
- حساب Plesk مع صلاحيات إدارة
- Python 3.9+ مثبت على الخادم
- Node.js و npm (لبناء Frontend)
- قاعدة بيانات (SQLite أو PostgreSQL)

## 🚀 خطوات النشر

### 1. إعداد المشروع محلياً

#### أ. بناء Frontend
```bash
# على Windows
build_frontend.bat

# على Linux/macOS
chmod +x build_frontend.sh
./build_frontend.sh
```

سيتم إنشاء مجلد `frontend/dist` يحتوي على الملفات الجاهزة للنشر.

#### ب. إعداد ملفات البيئة

**في مجلد `backend`، أنشئ ملف `.env`:**
```env
DATABASE_URL=sqlite:///./amantac.db
# أو لقاعدة بيانات PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/amantac_db

SECRET_KEY=your-very-secure-secret-key-here-change-this
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ENVIRONMENT=production
LOG_LEVEL=INFO
```

**في مجلد `frontend`، أنشئ ملف `.env`:**
```env
VITE_API_URL=https://yourdomain.com/api
VITE_ENVIRONMENT=production
```

### 2. رفع الملفات إلى Plesk

#### هيكل المجلدات المطلوب:
```
httpdocs/
├── .htaccess                    (من جذر المشروع)
├── backend/
│   ├── .htaccess               (من backend/)
│   ├── passenger_wsgi.py      (من backend/)
│   ├── .env                    (أنشئه محلياً)
│   ├── main.py
│   ├── app/
│   ├── uploads/
│   └── ... (جميع ملفات backend)
└── frontend/
    └── dist/                   (محتوى مجلد dist بعد البناء)
        ├── index.html
        ├── assets/
        └── ...
```

#### خطوات الرفع:
1. سجل الدخول إلى Plesk
2. افتح **File Manager** أو استخدم **FTP/SFTP**
3. ارفع الملفات إلى مجلد `httpdocs` الخاص بالدومين

### 3. إعداد Python Application في Plesk

#### أ. تفعيل Passenger
1. في Plesk، اذهب إلى **Domains** > **yourdomain.com**
2. افتح **Python**
3. قم بتفعيل **Passenger** إذا لم يكن مفعلاً
4. حدد:
   - **Application root**: `/var/www/vhosts/yourdomain.com/httpdocs/backend`
   - **Application startup file**: `passenger_wsgi.py`
   - **Application type**: `WSGI`
   - **Python version**: `3.9` أو أحدث

#### ب. تثبيت المتطلبات
1. افتح **Terminal** في Plesk
2. انتقل إلى مجلد backend:
```bash
cd /var/www/vhosts/yourdomain.com/httpdocs/backend
```

3. أنشئ بيئة افتراضية (اختياري ولكن موصى به):
```bash
python3 -m venv venv
source venv/bin/activate
```

4. ثبت المتطلبات:
```bash
pip install -r ../../requirements.txt
```

**ملاحظة:** إذا كان `requirements.txt` في المجلد الرئيسي، اضبط المسار حسب موقعك.

### 4. إعداد قاعدة البيانات

#### خيار 1: SQLite (بسيط)
- تأكد من أن مجلد `backend` لديه صلاحيات الكتابة
- قاعدة البيانات ستُنشأ تلقائياً عند أول تشغيل

#### خيار 2: PostgreSQL (موصى به للإنتاج)
1. في Plesk، اذهب إلى **Databases** > **PostgreSQL Databases**
2. أنشئ قاعدة بيانات جديدة
3. أنشئ مستخدم جديد واربطه بقاعدة البيانات
4. حدّث ملف `.env` في `backend`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

5. قم بتشغيل تهيئة قاعدة البيانات:
```bash
cd /var/www/vhosts/yourdomain.com/httpdocs/backend
python3 setup.py
```

### 5. تهيئة قاعدة البيانات وإنشاء المستخدمين

```bash
cd /var/www/vhosts/yourdomain.com/httpdocs/backend
python3 setup.py
python3 seed_all_users.py
```

### 6. إعداد الصلاحيات

تأكد من أن الملفات والمجلدات لديها الصلاحيات الصحيحة:

```bash
# في Terminal Plesk
cd /var/www/vhosts/yourdomain.com/httpdocs

# صلاحيات الملفات
find . -type f -exec chmod 644 {} \;

# صلاحيات المجلدات
find . -type d -exec chmod 755 {} \;

# صلاحيات الكتابة للمجلدات المطلوبة
chmod 755 backend/uploads
chmod 755 backend
```

### 7. تحديث إعدادات .htaccess

#### في `backend/.htaccess`:
عدّل المسارات حسب موقعك:
```apache
PassengerAppRoot /var/www/vhosts/yourdomain.com/httpdocs/backend
PassengerBaseURI /api
PassengerPython /usr/bin/python3
```

#### في `.htaccess` الرئيسي:
عدّل المسارات حسب هيكل مجلداتك.

### 8. إعداد SSL/HTTPS

1. في Plesk، اذهب إلى **SSL/TLS Settings**
2. فعّل **SSL/TLS support**
3. قم بتثبيت شهادة SSL (Let's Encrypt مجانية)

### 9. اختبار التطبيق

1. افتح المتصفح واذهب إلى: `https://yourdomain.com`
2. تحقق من أن Frontend يعمل
3. تحقق من API: `https://yourdomain.com/api/health`
4. تحقق من API Docs: `https://yourdomain.com/api/docs`

## 🔧 استكشاف الأخطاء

### المشكلة: Backend لا يعمل
- تحقق من سجلات الأخطاء في Plesk: **Logs** > **Error Log**
- تحقق من سجلات Passenger: `passenger_wsgi.py` في Terminal
- تأكد من تثبيت جميع المتطلبات في `requirements.txt`

### المشكلة: Frontend لا يعرض الصفحات
- تحقق من أن مجلد `frontend/dist` موجود ومليء بالملفات
- تحقق من ملف `.htaccess` الرئيسي
- تأكد من أن React Router يعمل بشكل صحيح

### المشكلة: خطأ CORS
- تحقق من إعدادات `ALLOWED_ORIGINS` في ملف `.env`
- تأكد من أن الدومين في القائمة المسموح بها

### المشكلة: قاعدة البيانات لا تعمل
- تحقق من `DATABASE_URL` في ملف `.env`
- تأكد من صلاحيات قاعدة البيانات
- تحقق من اتصال قاعدة البيانات

## 📝 ملاحظات مهمة

1. **الأمان:**
   - غيّر `SECRET_KEY` في ملف `.env`
   - استخدم HTTPS دائماً
   - راجع إعدادات CORS

2. **الأداء:**
   - استخدم PostgreSQL بدلاً من SQLite للإنتاج
   - فعّل Redis للتخزين المؤقت (اختياري)
   - راجع إعدادات Passenger

3. **النسخ الاحتياطي:**
   - قم بعمل نسخة احتياطية من قاعدة البيانات بانتظام
   - احتفظ بنسخة من ملف `.env`

4. **التحديثات:**
   - عند التحديث، أعد بناء Frontend
   - ثبت المتطلبات الجديدة
   - قم بتشغيل migrations إذا لزم الأمر

## 🔄 عملية التحديث

عند تحديث التطبيق:

1. ارفع الملفات الجديدة
2. ثبت المتطلبات الجديدة:
```bash
cd /var/www/vhosts/yourdomain.com/httpdocs/backend
pip install -r ../../requirements.txt --upgrade
```

3. أعد بناء Frontend محلياً وارفع مجلد `dist`
4. أعد تشغيل التطبيق من Plesk (Restart Application)

## 📞 الدعم

إذا واجهت مشاكل:
1. راجع سجلات الأخطاء في Plesk
2. تحقق من إعدادات Passenger
3. تأكد من أن جميع المسارات صحيحة

---

**تم إعداد المشروع للنشر على Plesk! 🎉**
