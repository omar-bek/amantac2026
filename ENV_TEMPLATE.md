# قالب متغيرات البيئة - Environment Variables Template

استخدم هذا الملف كمرجع عند إعداد ملفات `.env` للنشر.

## 📁 backend/.env

```env
# Database Configuration
# For SQLite (default - سهل للبدء):
DATABASE_URL=sqlite:///./amantac.db

# For PostgreSQL (موصى به للإنتاج):
# DATABASE_URL=postgresql://username:password@localhost:5432/amantac_db

# Security - غيّر هذا إلى قيمة عشوائية قوية!
SECRET_KEY=your-very-secure-secret-key-change-this-in-production

# CORS Settings - قائمة الدومينات المسموح بها (مفصولة بفواصل)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Redis (اختياري - للتخزين المؤقت)
# REDIS_URL=redis://localhost:6379/0

# Environment
ENVIRONMENT=production

# Logging Level
LOG_LEVEL=INFO
```

## 📁 frontend/.env

```env
# API Base URL - رابط API الخاص بك
VITE_API_URL=https://yourdomain.com/api

# Environment
VITE_ENVIRONMENT=production
```

## 🔐 كيفية إنشاء SECRET_KEY آمن

يمكنك استخدام Python لإنشاء مفتاح آمن:

```python
import secrets
print(secrets.token_urlsafe(32))
```

أو عبر Terminal:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## ⚠️ تحذيرات مهمة

1. **لا ترفع ملفات `.env` إلى Git!** - تأكد من وجودها في `.gitignore`
2. **غيّر `SECRET_KEY`** - لا تستخدم القيمة الافتراضية
3. **راجع `ALLOWED_ORIGINS`** - حدد الدومينات المسموح بها فقط
4. **احتفظ بنسخة احتياطية** - من ملفات `.env` في مكان آمن
