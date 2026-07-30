# 🔗 URL Shortener Service

A modern, high-performance REST API service for shortening URLs, built with Django REST Framework, Celery, Redis, and Docker.

---

## 🚀 Key Features

* **URL Shortening:** Generates unique short codes for long links.
* **Redirection & Analytics:** Redirects users and tracks total click counts per URL.
* **Time-To-Live (TTL):** Supports setting expiration dates (`expires_at`) for links.
* **Automated Cleanup (Celery + Redis):** Runs background periodic tasks to prune expired links without blocking the primary HTTP API.
* **Full Containerization:** Spuns up the entire infrastructure with a single command via Docker Compose.
* **Interactive Documentation (Swagger/OpenAPI):** Provides an interactive UI to explore and test endpoints.

---

## 🛠️ Tech Stack

* **Python 3.12 / Django 6.0 / Django REST Framework**
* **Celery 5.6** (Background Tasks)
* **Celery Beat** (Task Scheduler)
* **Redis 7.4** (Message Broker & Result Backend)
* **Docker / Docker Compose**
* **python-dotenv** (Environment Configuration)

---

## 📦 Quickstart with Docker

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/django-url-shortener.git](https://github.com/your-username/django-url-shortener.git)
cd django-url-shortener

2. Configure Environment Variables
Create a .env file in the root directory (you can reference .env.example):
DEBUG=True
SECRET_KEY='django-insecure-your-secret-key-here'

# Redis & Celery Configs
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

3. Build & Run Containers
Launch all 4 services (web, redis, celery, celery_beat) with a single command:
docker-compose up --build

4. Testing by Swagger 
