# دليل النشر السريع - Quick Deployment Guide

دليل مختصر لنشر المشروع على Plesk في 5 خطوات.

## ⚡ الخطوات السريعة

### 1️⃣ بناء Frontend
```bash
# Windows
build_frontend.bat

# Linux/macOS  
chmod +x build_frontend.sh && ./build_frontend.sh
```

### 2️⃣ إعداد ملفات البيئة

**أنشئ `backend/.env`:**
```env
DATABASE_URL=sqlite:///./amantac.db
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://yourdomain.com
ENVIRONMENT=production
```

**أنشئ `frontend/.env`:**
```env
VITE_API_URL=https://yourdomain.com/api
```

### 3️⃣ رفع الملفات

ارفع الملفات إلى Plesk بهذا الهيكل:
```
httpdocs/
├── .htaccess
├── backend/
│   ├── .htaccess
│   ├── passenger_wsgi.py
│   ├── .env
│   └── ... (جميع ملفات backend)
└── frontend/
    └── dist/ (محتوى dist بعد البناء)
```

### 4️⃣ إعداد Python في Plesk

1. **Domains** > **yourdomain.com** > **Python**
2. فعّل **Passenger**
3. حدد:
   - **Application root**: `/var/www/vhosts/yourdomain.com/httpdocs/backend`
   - **Startup file**: `passenger_wsgi.py`
   - **Type**: `WSGI`

### 5️⃣ تثبيت المتطلبات

في Terminal Plesk:
```bash
cd /var/www/vhosts/yourdomain.com/httpdocs/backend
pip3 install -r ../../requirements.txt
python3 setup.py
python3 seed_all_users.py
```

## ✅ اختبار

- Frontend: `https://yourdomain.com`
- API Health: `https://yourdomain.com/api/health`
- API Docs: `https://yourdomain.com/api/docs`

## 🔧 تعديلات مهمة

**في `backend/.htaccess`**، غيّر:
```apache
PassengerAppRoot /var/www/vhosts/yourdomain.com/httpdocs/backend
```
إلى المسار الصحيح لدومينك.

---

**للمزيد من التفاصيل، راجع `PLESK_DEPLOYMENT.md`**
