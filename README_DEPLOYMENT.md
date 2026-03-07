# ملفات النشر على Plesk - Plesk Deployment Files

هذا المجلد يحتوي على جميع الملفات اللازمة لنشر المشروع على Plesk.

## 📄 الملفات المهمة

### للمطورين
- `PLESK_DEPLOYMENT.md` - دليل شامل خطوة بخطوة للنشر
- `DEPLOYMENT_CHECKLIST.md` - قائمة تحقق للتأكد من اكتمال النشر
- `ENV_TEMPLATE.md` - قالب متغيرات البيئة

### ملفات الإعداد
- `backend/passenger_wsgi.py` - نقطة دخول Passenger لتشغيل FastAPI
- `backend/.htaccess` - إعدادات Apache للـ Backend
- `.htaccess` - إعدادات Apache الرئيسية للـ Frontend

### سكريبتات البناء
- `build_frontend.sh` - سكريبت بناء Frontend على Linux/macOS
- `build_frontend.bat` - سكريبت بناء Frontend على Windows

## 🚀 البدء السريع

1. **اقرأ الدليل الكامل:**
   ```bash
   # افتح PLESK_DEPLOYMENT.md
   ```

2. **ابنِ Frontend:**
   ```bash
   # Windows
   build_frontend.bat
   
   # Linux/macOS
   ./build_frontend.sh
   ```

3. **اتبع خطوات النشر في PLESK_DEPLOYMENT.md**

4. **استخدم DEPLOYMENT_CHECKLIST.md للتأكد من اكتمال كل شيء**

## 📋 الترتيب الموصى به

1. اقرأ `PLESK_DEPLOYMENT.md` بالكامل
2. راجع `ENV_TEMPLATE.md` وأعد ملفات `.env`
3. ابنِ Frontend باستخدام السكريبتات
4. ارفع الملفات إلى Plesk
5. اتبع `DEPLOYMENT_CHECKLIST.md` خطوة بخطوة

## ❓ أسئلة شائعة

**س: هل أحتاج إلى تعديل ملفات .htaccess؟**
ج: نعم، يجب تحديث المسارات في `backend/.htaccess` حسب موقعك على الخادم.

**س: ماذا لو لم يعمل Passenger؟**
ج: تحقق من سجلات الأخطاء في Plesk وتأكد من تثبيت جميع المتطلبات.

**س: كيف أحدّث التطبيق بعد النشر؟**
ج: راجع قسم "عملية التحديث" في `PLESK_DEPLOYMENT.md`.

## 🔗 روابط مفيدة

- [وثائق Plesk](https://docs.plesk.com/)
- [وثائق Passenger](https://www.phusionpassenger.com/docs/)
- [وثائق FastAPI](https://fastapi.tiangolo.com/)

---

**تم إعداد المشروع للنشر! 🎉**
