# راهنمای جامع GitHub CLI برای Projects

این مستند راهنمای کامل استفاده از GitHub CLI برای کار با Projects است.

## فهرست مطالب

- [نصب و راه‌اندازی](#نصب-و-راهاندازی)
- [احراز هویت](#احراز-هویت)
- [دستورات پایه Projects](#دستورات-پایه-projects)
- [مشاهده اطلاعات پروژه](#مشاهده-اطلاعات-پروژه)
- [لیست آیتم‌ها](#لیست-آیتمها)
- [فیلتر و جستجو](#فیلتر-و-جستجو)
- [صادرات داده](#صادرات-داده)
- [دستورات پیشرفته](#دستورات-پیشرفته)
- [نکات و ترفندها](#نکات-و-ترفندها)

---

## نصب و راه‌اندازی

### نصب GitHub CLI

**Windows:**
```bash
# با winget
winget install --id GitHub.cli

# با Chocolatey
choco install gh

# با Scoop
scoop install gh
```

**macOS:**
```bash
# با Homebrew
brew install gh

# با MacPorts
sudo port install gh
```

**Linux:**

**Debian/Ubuntu:**
```bash
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y
```

**Fedora/RHEL:**
```bash
sudo dnf install gh
```

**Arch Linux:**
```bash
sudo pacman -S github-cli
```

### بررسی نصب

```bash
gh --version
# خروجی: gh version 2.x.x (...)
```

---

## احراز هویت

### ورود به GitHub

```bash
gh auth login
```

**مراحل:**
1. انتخاب GitHub.com یا GitHub Enterprise
2. انتخاب پروتکل (HTTPS یا SSH)
3. احراز هویت از طریق مرورگر یا توکن
4. تایید دسترسی‌ها

### بررسی وضعیت احراز هویت

```bash
gh auth status
```

**خروجی نمونه:**
```
github.com
  ✓ Logged in to github.com as YourUsername
  ✓ Git operations for github.com configured to use https protocol.
  ✓ Token: gho_************************************
  ✓ Token scopes: gist, read:org, repo, workflow
```

### تازه‌سازی توکن با دسترسی Project

```bash
gh auth refresh -s project
```

**نکته:** برای کار با Projects، حتماً scope `project` را اضافه کنید.

### خروج از حساب

```bash
gh auth logout
```

---

## دستورات پایه Projects

### لیست پروژه‌ها

```bash
# لیست پروژه‌های سازمان
gh project list --owner ORGANIZATION_NAME

# لیست پروژه‌های کاربر
gh project list --owner USERNAME

# مثال
gh project list --owner TechBurst-Pro
```

**خروجی نمونه:**
```
NUMBER  TITLE                      STATE  ID
2       Andropay Task Management   OPEN   PVT_kwDOCBxBz84BGVfV
1       Old Project                CLOSED PVT_kwDOCBxBz84ABCDEF
```

### مشاهده جزئیات پروژه

```bash
# مشاهده پروژه خاص
gh project view NUMBER --owner OWNER

# مثال
gh project view 2 --owner TechBurst-Pro
```

**خروجی نمونه:**
```
Andropay Task Management
Project ID: PVT_kwDOCBxBz84BGVfV
State: OPEN
Created: 2024-01-15
Updated: 2025-11-08
```

### مشاهده با فرمت JSON

```bash
gh project view 2 --owner TechBurst-Pro --format json
```

**خروجی JSON:**
```json
{
  "id": "PVT_kwDOCBxBz84BGVfV",
  "number": 2,
  "title": "Andropay Task Management",
  "state": "OPEN",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2025-11-08T15:45:00Z"
}
```

---

## لیست آیتم‌ها

### دریافت تمام آیتم‌ها

```bash
# لیست آیتم‌ها (پیش‌فرض: 30 آیتم)
gh project item-list NUMBER --owner OWNER

# با محدودیت تعداد
gh project item-list 2 --owner TechBurst-Pro --limit 100

# تمام آیتم‌ها (حداکثر 500)
gh project item-list 2 --owner TechBurst-Pro --limit 500
```

### خروجی JSON

```bash
gh project item-list 2 --owner TechBurst-Pro --format json --limit 100
```

**ساختار JSON:**
```json
{
  "items": [
    {
      "id": "PVTI_lADOCBxBz84BGVfVzgXYZ",
      "title": "Implement user authentication",
      "status": "In Progress",
      "priority": "P1",
      "assignees": ["AmirCpu2"],
      "estimate (Hrs)": 8.0,
      "labels": ["backend", "security"],
      "content": {
        "type": "Issue",
        "number": 123,
        "repository": "TechBurst-Pro/andropay",
        "url": "https://github.com/TechBurst-Pro/andropay/issues/123"
      }
    }
  ],
  "totalCount": 76
}
```

### خروجی CSV

```bash
gh project item-list 2 --owner TechBurst-Pro --format csv --limit 100 > items.csv
```

---

## فیلدهای پروژه

### لیست فیلدها

```bash
gh project field-list NUMBER --owner OWNER

# مثال
gh project field-list 2 --owner TechBurst-Pro
```

**خروجی نمونه:**
```
NAME            TYPE          OPTIONS
Title           TEXT          
Status          SINGLE_SELECT Backlog, Todo, Pending, In Progress, In Review, Done
Priority        SINGLE_SELECT P🔥, P0, P1, P2
Assignees       ASSIGNEES     
Estimate (Hrs)  NUMBER        
Labels          LABELS        
Repository      REPOSITORY    
```

### خروجی JSON فیلدها

```bash
gh project field-list 2 --owner TechBurst-Pro --format json
```

**ساختار JSON:**
```json
{
  "fields": [
    {
      "id": "PVTF_lADOCBxBz84BGVfVzgABC",
      "name": "Status",
      "dataType": "SINGLE_SELECT",
      "options": [
        {"id": "opt1", "name": "Backlog"},
        {"id": "opt2", "name": "Todo"},
        {"id": "opt3", "name": "In Progress"},
        {"id": "opt4", "name": "Done"}
      ]
    }
  ]
}
```

---

## فیلتر و جستجو

### فیلتر با PowerShell

```powershell
# دریافت داده
$data = gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 | ConvertFrom-Json

# فیلتر بر اساس وضعیت
$data.items | Where-Object { $_.status -eq "In Progress" }

# فیلتر بر اساس اولویت
$data.items | Where-Object { $_.priority -eq "P🔥" }

# فیلتر بر اساس مسئول
$data.items | Where-Object { $_.assignees -contains "AmirCpu2" }

# فیلتر ترکیبی
$data.items | Where-Object { 
    $_.status -eq "Todo" -and $_.priority -in @("P🔥", "P0") 
}
```

### فیلتر با jq (Linux/Mac)

```bash
# دریافت داده
gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 > items.json

# فیلتر بر اساس وضعیت
cat items.json | jq '.items[] | select(.status == "In Progress")'

# فیلتر بر اساس اولویت
cat items.json | jq '.items[] | select(.priority == "P🔥")'

# فیلتر بر اساس مسئول
cat items.json | jq '.items[] | select(.assignees[] == "AmirCpu2")'

# شمارش آیتم‌ها بر اساس وضعیت
cat items.json | jq '[.items[] | .status] | group_by(.) | map({status: .[0], count: length})'
```

---

## صادرات داده

### صادرات به JSON

```bash
# صادرات کامل
gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 > project-data.json

# صادرات با timestamp
gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 > "project-$(date +%Y%m%d-%H%M%S).json"
```

### صادرات به CSV

```bash
# صادرات کامل
gh project item-list 2 --owner TechBurst-Pro --format csv --limit 100 > project-data.csv

# صادرات با timestamp
gh project item-list 2 --owner TechBurst-Pro --format csv --limit 100 > "project-$(date +%Y%m%d-%H%M%S).csv"
```

### صادرات فیلتر شده

```powershell
# فقط آیتم‌های In Progress
$data = gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 | ConvertFrom-Json
$data.items | Where-Object { $_.status -eq "In Progress" } | ConvertTo-Json | Out-File "in-progress.json"

# فقط آیتم‌های با اولویت بالا
$data.items | Where-Object { $_.priority -in @("P🔥", "P0") } | ConvertTo-Json | Out-File "high-priority.json"
```

---

## دستورات پیشرفته

### محاسبه آمار

```powershell
# دریافت داده
$data = gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 | ConvertFrom-Json
$items = $data.items

# تعداد کل
$total = $items.Count

# تعداد بر اساس وضعیت
$items | Group-Object status | Select-Object Name, Count

# تعداد بر اساس اولویت
$items | Group-Object priority | Select-Object Name, Count

# تعداد بر اساس مسئول
$items | ForEach-Object { $_.assignees } | Group-Object | Select-Object Name, Count

# محاسبه تخمین کل
$totalEstimate = ($items | Where-Object { $_.'estimate (Hrs)' } | Measure-Object -Property 'estimate (Hrs)' -Sum).Sum

# درصد تکمیل
$done = ($items | Where-Object { $_.status -eq "Done" }).Count
$completionPercentage = [math]::Round(($done / $total) * 100, 1)

Write-Host "Total Items: $total"
Write-Host "Done: $done ($completionPercentage%)"
Write-Host "Total Estimate: $totalEstimate hours"
```

### مقایسه دو اسنپ‌شات

```powershell
# اسنپ‌شات قدیم
$old = Get-Content "snapshot-old.json" | ConvertFrom-Json

# اسنپ‌شات جدید
$new = Get-Content "snapshot-new.json" | ConvertFrom-Json

# آیتم‌های جدید
$newItems = $new.items | Where-Object { $_.id -notin $old.items.id }
Write-Host "New Items: $($newItems.Count)"

# آیتم‌های تکمیل شده
$completed = $new.items | Where-Object { 
    $_.status -eq "Done" -and 
    ($old.items | Where-Object { $_.id -eq $_.id }).status -ne "Done"
}
Write-Host "Completed Items: $($completed.Count)"
```

### تولید گزارش سریع

```powershell
# اسکریپت ساده برای گزارش
$data = gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 | ConvertFrom-Json
$items = $data.items

$report = @"
# Project Status Report
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Summary
- Total Items: $($items.Count)
- Done: $(($items | Where-Object { $_.status -eq "Done" }).Count)
- In Progress: $(($items | Where-Object { $_.status -eq "In Progress" }).Count)
- Todo: $(($items | Where-Object { $_.status -eq "Todo" }).Count)

## High Priority Items
$(($items | Where-Object { $_.priority -in @("P🔥", "P0") } | ForEach-Object { "- [$($_.priority)] $($_.title)" }) -join "`n")
"@

$report | Out-File "quick-report.md"
```

---

## نکات و ترفندها

### 1. استفاده از Aliases

```bash
# ایجاد alias برای دستورات پرکاربرد
alias ghpl='gh project item-list 2 --owner TechBurst-Pro --format json --limit 100'
alias ghpv='gh project view 2 --owner TechBurst-Pro'

# استفاده
ghpl | jq '.items[] | select(.status == "In Progress")'
```

### 2. اسکریپت خودکار برای بک‌آپ

```bash
#!/bin/bash
# backup-project.sh

DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="backups"

mkdir -p $BACKUP_DIR

# بک‌آپ آیتم‌ها
gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 > "$BACKUP_DIR/items-$DATE.json"

# بک‌آپ فیلدها
gh project field-list 2 --owner TechBurst-Pro --format json > "$BACKUP_DIR/fields-$DATE.json"

# بک‌آپ جزئیات پروژه
gh project view 2 --owner TechBurst-Pro --format json > "$BACKUP_DIR/project-$DATE.json"

echo "Backup completed: $BACKUP_DIR/*-$DATE.json"
```

### 3. مانیتورینگ تغییرات

```powershell
# check-changes.ps1
$previous = Get-Content "previous-snapshot.json" | ConvertFrom-Json
$current = gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 | ConvertFrom-Json

$changes = @()

foreach ($item in $current.items) {
    $oldItem = $previous.items | Where-Object { $_.id -eq $item.id }
    
    if (-not $oldItem) {
        $changes += "NEW: $($item.title)"
    }
    elseif ($oldItem.status -ne $item.status) {
        $changes += "STATUS CHANGE: $($item.title) ($($oldItem.status) -> $($item.status))"
    }
}

if ($changes.Count -gt 0) {
    Write-Host "Changes detected:"
    $changes | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "No changes detected"
}

# ذخیره اسنپ‌شات جدید
$current | ConvertTo-Json -Depth 10 | Out-File "previous-snapshot.json"
```

### 4. یکپارچه‌سازی با Slack/Teams

```powershell
# send-to-slack.ps1
$data = gh project item-list 2 --owner TechBurst-Pro --format json --limit 100 | ConvertFrom-Json
$highPriority = $data.items | Where-Object { $_.priority -in @("P🔥", "P0") -and $_.status -ne "Done" }

if ($highPriority.Count -gt 0) {
    $message = "⚠️ High Priority Items Not Done: $($highPriority.Count)`n"
    $message += ($highPriority | ForEach-Object { "- $($_.title)" }) -join "`n"
    
    # ارسال به Slack webhook
    $webhook = "YOUR_SLACK_WEBHOOK_URL"
    $body = @{ text = $message } | ConvertTo-Json
    Invoke-RestMethod -Uri $webhook -Method Post -Body $body -ContentType 'application/json'
}
```

---

## محدودیت‌ها و نکات مهم

### محدودیت‌های API

- **Rate Limiting:** GitHub API محدودیت تعداد درخواست دارد
- **Limit پیش‌فرض:** 30 آیتم (حداکثر 500)
- **Pagination:** برای پروژه‌های بزرگ نیاز به pagination

### نکات امنیتی

- **توکن‌ها را ذخیره نکنید:** از `gh auth` استفاده کنید
- **Scope مناسب:** فقط دسترسی‌های لازم را بدهید
- **تازه‌سازی منظم:** توکن‌ها را به‌روز نگه دارید

### بهترین روش‌ها

1. **استفاده از JSON:** برای پردازش خودکار
2. **محدود کردن limit:** فقط داده مورد نیاز را دریافت کنید
3. **Cache کردن:** برای کاهش درخواست‌های API
4. **Error Handling:** همیشه خطاها را مدیریت کنید

---

## منابع بیشتر

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub Projects API](https://docs.github.com/en/graphql/reference/objects#projectv2)
- [GitHub CLI Extensions](https://github.com/topics/gh-extension)

---

**آخرین بروزرسانی:** 2025-11-08
