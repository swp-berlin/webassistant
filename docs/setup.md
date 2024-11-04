# Manual Setup Guide

The recommended way to set up the SWP web assistant is by using Docker Compose. However, if you prefer to set up the
application manually, you can follow this guide.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.9
- PostgreSQL 13
- Node.js 14
- Redis 4
- Elasticsearch 8.4.3

## Step-by-Step Setup

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up Python Environment**

   Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python Dependencies**

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL**

   Create a PostgreSQL database and user:

   ```bash
   sudo -u postgres psql
   CREATE DATABASE swp;
   CREATE USER swp WITH PASSWORD 'swp';
   ALTER ROLE swp SET client_encoding TO 'utf8';
   ALTER ROLE swp SET default_transaction_isolation TO 'read committed';
   ALTER ROLE swp SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE swp TO swp;
   \q
   ```

5. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add the following environment variables:

   ```env
   DJANGO_SETTINGS_MODULE=swp.settings.dev
   ENVIRONMENT=develop
   DATABASE_HOST=localhost
   REDIS_HOST=localhost
   ELASTICSEARCH_HOSTNAME=localhost
   ELASTICSEARCH_SCHEME=http
   ELASTICSEARCH_PASSWORD=elastic
   ```

6. **Run Database Migrations**

   Apply the database migrations:

   ```bash
   python manage.py migrate
   ```

7. **Install Node.js Dependencies**

   Install the Node.js dependencies:

   ```bash
   npm install
   ```

8. **Run the Application**

   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

   In a separate terminal, start the frontend:

   ```bash
   npm run watch
   ```

9. **Access the Application**

   Open your web browser and go to `http://localhost:8000` to access the application.

## Additional Commands

- To run Celery workers:

  ```bash
  celery -A swp worker -B -Q celery,scraper -l DEBUG --purge
  ```

- To rebuild the search index:

  ```bash
  python manage.py search_index --rebuild -f
  ```

