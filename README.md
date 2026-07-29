# 🔗 Django URL Shortener API

A modern REST API service for shortening URLs, featuring detailed click analytics and automated cleanup of expired links.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12+
* **Framework:** Django, Django REST Framework (DRF)
* **Documentation:** OpenAPI 3.0 / Swagger (drf-spectacular)
* **Utilities:** `user-agents` (User-Agent parsing)

---

## ✨ Features

* ✂️ **URL Shortening:** Generate unique short codes or set custom aliases.
* ⏰ **Expiration (TTL):** Set custom lifetimes for links with automatic expiration checks upon redirect.
* 📊 **Advanced Analytics:** Track IP addresses, browsers, OS, and device types (Mobile/PC/Tablet).
* 🧹 **Management Commands:** Custom command to purge expired URLs from the database (`purge_expired`).
* 📖 **Interactive Docs:** Full Swagger UI for exploring and testing API endpoints.

---

## 🚀 Quickstart

### 1. Clone the repository and install dependencies

```bash
git clone [https://github.com/your-username/django-url-shortener.git](https://github.com/your-username/django-url-shortener.git)
cd django-url-shortener

# Create and activate a virtual environment
python -m venv venv
# Linux/macOS: source venv/bin/activate
# Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

2. Run migrations and start the server
Bash
python manage.py migrate
python manage.py runserver

Method	URL	Description
POST	/api/shorten/	Create a short URL
GET	/r/{short_code}/	Redirect to the original URL
GET	/api/analytics/{short_code}/	Get click analytics for a link
DELETE	/api/delete/{short_code}/	Delete a short URL
GET	/docs/	Swagger UI Documentation
⚙️ Additional Commands
I have a purge expired command, this command can clean all links what are expired
