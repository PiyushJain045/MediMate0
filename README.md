# MediMate: Your Personal Health Companion

MediMate is an intelligent, user-centric web application designed to serve as a personal health companion. It empowers users to better understand their health concerns through AI-driven diagnostic pathways, helps them find nearby medical specialists, and allows them to manage their appointments with automated reminders.

---

## Key Features

* **AI Symptom Analysis:** Utilizes a two-stage diagnostic process: first, a **Random Forest** machine learning model provides a preliminary disease prediction based on user symptoms. Then, the Google Gemini AI model generates a detailed assessment and advice based on this prediction.
* **AI Skin Analysis:** Features a powerful **Deep Learning** model for skin analysis. By leveraging a **Convolutional Neural Network (CNN)**, the tool analyzes user-uploaded photos to provide a potential classification of dermatological issues.
* **Find Nearby Specialists:** Based on the AI assessment, the application identifies the appropriate medical specialist and uses the Google Maps API to instantly provide a detailed list of nearby doctors, complete with contact information, ratings, address, and distance.
* **Appointment Calendar:** A personal calendar where users can schedule and view their medical appointments.
* **Automated Reminders:** An asynchronous reminder system, powered by Celery and Redis, that automatically sends email notifications to users one day before their scheduled appointments.
* **Secure User Authentication:** A complete user registration, login, and profile management system built with `django-allauth` to ensure a personalized and secure experience.
---

## Tech Stack

* **Backend:** Django, Python
* **Frontend:** HTML, CSS, JavaScript
* **Asynchronous Tasks:** Celery
* **Message Broker:** Redis
* **Database:** SQLite3 (for development)
* **AI & Machine Learning:**
    * Google Gemini API (for symptom assessment)
    * CNN for Skin Disease Classification
    * RandomForest for Disease/Symptom Classification
* **APIs:** Google Maps Platform (Places API, Distance Matrix API)
* **Authentication:** django-allauth

---

## Setup and Installation

Follow these steps to set up the project locally.

### 1. Prerequisites

* Python 3.10+
* Redis installed and running. (Download from [here](https://github.com/tporadowski/redis/releases) for Windows)

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 3. Set Up a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

- Create a .env. Add your secret keys and API credentials to this file:
```bash
GEMINI_API_KEY = "your-google-gemini-api-key"
GOOGLE_MAPS_API_KEY = "your-google-maps-api-key" 
```

### 6. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Running the Application

```bash
python manage.py runserver
celery -A your_project_name worker -l info -P solo
celery -A your_project_name beat -l info
```