# Library FastAPI

یک سیستم ساده‌ی کتابداری با **FastAPI**. برای سادگی، از دیتابیس استفاده نشده و داده‌ها داخل یک متغیر (دیکشنری) در حافظه نگهداری می‌شوند؛ بنابراین با هر بار ری‌استارت سرور، داده‌ها به حالت اولیه برمی‌گردند.

## نصب و اجرا

```bash
git clone <repo-url>
cd library-fastapi

python -m venv .venv
source .venv/bin/activate        # در ویندوز: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn main:app --reload
```

بعد از اجرا:

- API: http://127.0.0.1:8000
- مستندات Swagger: http://127.0.0.1:8000/docs
- مستندات ReDoc: http://127.0.0.1:8000/redoc

## Endpointها

| متد | مسیر | توضیح | کد پاسخ |
|---|---|---|---|
| GET | `/books` | لیست همه‌ی کتاب‌ها | 200 |
| POST | `/books` | افزودن کتاب جدید | 201 |
| GET | `/books/{id}` | دریافت یک کتاب | 200 / 404 |
| PATCH | `/books/{id}` | ویرایش جزئی کتاب | 200 / 404 |
| DELETE | `/books/{id}` | حذف کتاب | 204 / 404 |

## مدل کتاب

```json
{
  "id": 1,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "year": 2008,
  "isbn": "9780132350884",
  "available": true
}
```

فیلدهای اجباری هنگام ساخت: `title` و `author`.

## نمونه درخواست‌ها

```bash
# افزودن کتاب
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Refactoring", "author": "Martin Fowler", "year": 1999}'

# ویرایش جزئی (مثلاً امانت داده شد)
curl -X PATCH http://127.0.0.1:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"available": false}'

# حذف
curl -X DELETE http://127.0.0.1:8000/books/2
```

## ساختار پروژه

```
library-fastapi/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
