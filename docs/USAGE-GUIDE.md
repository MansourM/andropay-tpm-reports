# راهنمای استفاده از GitHub Projects Reporter

این راهنما نحوه استفاده از ابزار گزارش‌ساز پروژه‌های GitHub را به صورت کامل توضیح می‌دهد.

## فهرست مطالب

- [شروع سریع](#شروع-سریع)
- [دستورات پایه](#دستورات-پایه)
- [سناریوهای کاربردی](#سناریوهای-کاربردی)
- [تنظیمات پیشرفته](#تنظیمات-پیشرفته)
- [خروجی‌های مختلف](#خروجیهای-مختلف)
- [ردیابی هفتگی](#ردیابی-هفتگی)
- [نکات و ترفندها](#نکات-و-ترفندها)

---

## شروع سریع

### نصب و راه‌اندازی اولیه

```bash
# 1. نصب وابستگی‌ها
pip install -r requirements.txt

# 2. احراز هویت GitHub CLI
gh auth login

# 3. ایجاد فایل تنظیمات
cp config.example.json config.json

# 4. ویرایش تنظیمات
# فایل config.json را باز کرده و مقادیر را تنظیم کنید
```

### اولین گزارش

```bash
# تولید گزارش HTML
python -m src.main

# گزارش در reports/report.html ذخیره می‌شود
```

---

## دستورات پایه

### تولید گزارش با فرمت‌های مختلف

```bash
# HTML (پیش‌فرض - با نمودارهای تعاملی)
python -m src.main --format html

# Markdown (برای مستندسازی)
python -m src.main --format md

# CSV (برای Excel)
python -m src.main --format csv

# JSON (برای پردازش خودکار)
python -m src.main --format json
```

### مشخص کردن مسیر خروجی

```bash
# ذخیره در مسیر سفارشی
python -m src.main --output my-reports/weekly-report.html

# ذخیره با نام سفارشی
python -m src.main --format md --output reports/sprint-review.md
```

### کار با پروژه‌های مختلف

```bash
# پروژه خاص
python -m src.main --owner MyOrg --project 5

# استفاده از فایل تنظیمات متفاوت
python -m src.main --config team-config.json
```

---

## سناریوهای کاربردی

### 1. گزارش روزانه برای استندآپ

```bash
# تولید گزارش سریع Markdown
python -m src.main --format md --output daily/standup-$(date +%Y%m%d).md
```

**استفاده:**
- مرور سریع آیتم‌های In Progress
- بررسی آیتم‌های با اولویت بالا
- شناسایی موارد بلوکه شده

### 2. گزارش هفتگی برای مدیریت

```bash
# تولید گزارش HTML کامل
python -m src.main --format html --output weekly/week-$(date +%U).html
```

**محتوا:**
- نمودارهای تعاملی پیشرفت
- مقایسه با هفته قبل
- تحلیل بار کاری تیم
- آیتم‌های برنامه‌ریزی نشده

### 3. صادرات داده برای تحلیل

```bash
# صادرات CSV برای Excel
python -m src.main --format csv --output analysis/project-data.csv

# صادرات JSON برای اسکریپت‌ها
python -m src.main --format json --output data/project-snapshot.json
```

### 4. گزارش چند پروژه

```bash
# پروژه اول
python -m src.main --project 1 --output reports/project-1.html

# پروژه دوم
python -m src.main --project 2 --output reports/project-2.html

# پروژه سوم
python -m src.main --project 3 --output reports/project-3.html
```

### 5. گزارش بدون ذخیره اسنپ‌شات

```bash
# برای تست یا گزارش‌های موقت
python -m src.main --no-snapshot
```

---

## تنظیمات پیشرفته

### فایل config.json

```json
{
  "owner": "TechBurst-Pro",
  "project_number": 2,
  "default_format": "html",
  "output_directory": "reports"
}
```

### چند فایل تنظیمات برای تیم‌های مختلف

**team-a-config.json:**
```json
{
  "owner": "MyOrg",
  "project_number": 1,
  "default_format": "html",
  "output_directory": "reports/team-a"
}
```

**team-b-config.json:**
```json
{
  "owner": "MyOrg",
  "project_number": 2,
  "default_format": "md",
  "output_directory": "reports/team-b"
}
```

**استفاده:**
```bash
python -m src.main --config team-a-config.json
python -m src.main --config team-b-config.json
```

---

## خروجی‌های مختلف

### HTML - گزارش تعاملی

**مزایا:**
- نمودارهای تعاملی Plotly
- جدول قابل مرتب‌سازی
- طراحی زیبا و حرفه‌ای
- تک‌فایله (بدون نیاز به اینترنت)
- واکنش‌گرا (موبایل، تبلت، دسکتاپ)

**مناسب برای:**
- ارائه به مدیریت
- اشتراک‌گذاری با ذینفعان
- آرشیو گزارش‌های هفتگی

**مثال:**
```bash
python -m src.main --format html --output reports/sprint-review.html
```

### Markdown - مستندسازی

**مزایا:**
- قابل خواندن در GitHub
- قابل ویرایش
- سبک و سریع
- مناسب برای version control

**مناسب برای:**
- مستندسازی پروژه
- گزارش‌های روزانه
- یادداشت‌های تیم

**مثال:**
```bash
python -m src.main --format md --output docs/project-status.md
```

### CSV - تحلیل داده

**مزایا:**
- قابل باز شدن در Excel
- مناسب برای تحلیل آماری
- قابل import در ابزارهای دیگر

**مناسب برای:**
- تحلیل داده‌ها
- گزارش‌های مالی
- محاسبات پیشرفته

**مثال:**
```bash
python -m src.main --format csv --output exports/items.csv
```

### JSON - پردازش خودکار

**مزایا:**
- ساختار کامل داده
- قابل پردازش توسط اسکریپت‌ها
- شامل متادیتا

**مناسب برای:**
- اتوماسیون
- یکپارچه‌سازی با سیستم‌های دیگر
- پردازش batch

**مثال:**
```bash
python -m src.main --format json --output data/project.json
```

---

## ردیابی هفتگی

### نحوه کار اسنپ‌شات‌ها

هر بار که گزارش تولید می‌کنید، یک اسنپ‌شات از وضعیت فعلی پروژه ذخیره می‌شود:

```
snapshots/
├── snapshot-20251108-140530.json
├── snapshot-20251108-153045.json
└── snapshot-20251109-091520.json
```

### مقایسه با هفته قبل

ابزار به صورت خودکار آخرین اسنپ‌شات را با اسنپ‌شات قبلی مقایسه می‌کند:

```
📊 Changes since last snapshot:
   Items completed: 5
   Items added: 3
   Status changes: 8
```

### غیرفعال کردن اسنپ‌شات

برای گزارش‌های موقت:

```bash
python -m src.main --no-snapshot
```

### پاک‌سازی اسنپ‌شات‌های قدیمی

```bash
# حذف اسنپ‌شات‌های قدیمی‌تر از 30 روز (Windows)
forfiles /p snapshots /s /m *.json /d -30 /c "cmd /c del @path"

# حذف اسنپ‌شات‌های قدیمی‌تر از 30 روز (Linux/Mac)
find snapshots -name "*.json" -mtime +30 -delete
```

---

## نکات و ترفندها

### 1. اتوماسیون گزارش‌های هفتگی

**Windows Task Scheduler:**
```batch
@echo off
cd C:\path\to\project
python -m src.main --format html --output reports\weekly\week-%date:~0,4%%date:~5,2%%date:~8,2%.html
```

**Linux/Mac Cron:**
```bash
# هر دوشنبه ساعت 9 صبح
0 9 * * 1 cd /path/to/project && python -m src.main --format html --output reports/weekly/week-$(date +\%Y\%W).html
```

### 2. اسکریپت Batch برای چند فرمت

**generate-all-reports.bat:**
```batch
@echo off
echo Generating HTML report...
python -m src.main --format html --output reports/report.html

echo Generating Markdown report...
python -m src.main --format md --output reports/report.md --no-snapshot

echo Generating CSV export...
python -m src.main --format csv --output exports/data.csv --no-snapshot

echo Done!
```

### 3. بررسی سریع معیارها

```bash
# تولید JSON و استخراج معیارها
python -m src.main --format json --output temp.json --no-snapshot
cat temp.json | jq '.metrics'
```

### 4. مقایسه دو پروژه

```bash
# پروژه A
python -m src.main --project 1 --format json --output project-a.json --no-snapshot

# پروژه B
python -m src.main --project 2 --format json --output project-b.json --no-snapshot

# مقایسه
# استفاده از ابزار diff یا jq
```

### 5. گزارش فقط برای آیتم‌های خاص

در حال حاضر ابزار تمام آیتم‌ها را نمایش می‌دهد. برای فیلتر کردن:

```bash
# تولید JSON و فیلتر با jq
python -m src.main --format json --output temp.json --no-snapshot
cat temp.json | jq '.items[] | select(.priority == "P🔥")'
```

### 6. بررسی سلامت پروژه

معیارهای مهم برای بررسی:

- **درصد تکمیل < 30%**: 🔴 نیاز به توجه
- **برنامه‌ریزی نشده > 20%**: 🔴 مشکل در برنامه‌ریزی
- **اولویت بالا شروع نشده > 5**: 🔴 تاخیر در کارهای مهم
- **بار کاری تیم > 10 آیتم**: 🔴 اضافه‌بار

---

## عیب‌یابی رایج

### مشکل: گزارش خالی است

**علت:** ممکن است پروژه آیتمی نداشته باشد یا دسترسی نداشته باشید.

**راه‌حل:**
```bash
# بررسی دسترسی
gh project view 2 --owner TechBurst-Pro

# بررسی آیتم‌ها
gh project item-list 2 --owner TechBurst-Pro --limit 10
```

### مشکل: نمودارها نمایش داده نمی‌شوند

**علت:** مرورگر از JavaScript پشتیبانی نمی‌کند یا Plotly لود نشده.

**راه‌حل:**
- از مرورگر مدرن استفاده کنید
- JavaScript را فعال کنید
- اتصال اینترنت را بررسی کنید (برای CDN)

### مشکل: خطای encoding در CSV

**علت:** Excel ممکن است UTF-8 را به درستی تشخیص ندهد.

**راه‌حل:**
- فایل با UTF-8 BOM ذخیره می‌شود (خودکار)
- در Excel: Data > From Text/CSV > انتخاب UTF-8

### مشکل: اسنپ‌شات‌ها زیاد شده‌اند

**راه‌حل:**
```bash
# نگه‌داری فقط 10 اسنپ‌شات آخر (Windows PowerShell)
Get-ChildItem snapshots\*.json | Sort-Object LastWriteTime -Descending | Select-Object -Skip 10 | Remove-Item

# نگه‌داری فقط 10 اسنپ‌شات آخر (Linux/Mac)
ls -t snapshots/*.json | tail -n +11 | xargs rm
```

---

## منابع بیشتر

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [راهنمای دستورات GitHub CLI](./GITHUB-CLI-REFERENCE.md)
- [Plotly Documentation](https://plotly.com/python/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

---

## پشتیبانی

برای سوالات یا مشکلات:
1. مستندات را مطالعه کنید
2. بخش عیب‌یابی را بررسی کنید
3. یک Issue در GitHub ایجاد کنید

---

**آخرین بروزرسانی:** 2025-11-08
