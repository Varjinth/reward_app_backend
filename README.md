# Travel Management System 

This is a full-stack web application built using **Django (backend)** and **React (frontend)**. The system allows users to apply for trips, view past trips, and for admins to approve trip requests.

---

## Tech Stack

- **Backend:** Django & Django REST Framework
- **Frontend:** React (in the `frontend` folder)
- **Database:** SQLite (default), but supports PostgreSQL & MySQL
- **Styling:** MDBootstrap (Material Design for Bootstrap)

---

## 🚀 How to Run the Project

### Backend (Django)
1. Install dependencies:
   pip install -r requirements.txt

2. Apply migrations:
    python manage.py migrate

3. Start the server: 
    python manage.py runserver

### Frontend (React)

  1. Navigate to the frontend folder:
     cd frontend

  2. Install dependencies:
     npm install

  3. Set up CORS to avoid errors:

     Open frontend/package.json and add the backend base URL:

    "proxy": "http://127.0.0.1:8000"

  4. Start the frontend:

    npm start

⚙️ Database Configuration

By default, SQLite is used. However, you can switch to PostgreSQL or MySQL by updating settings.py.

### PostgreSQL Configuration

  1. Install PostgreSQL and the Django adapter:

    pip install psycopg2

  2. Update DATABASES in settings.py:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

 
 ### MySQL Configuration

    1. Install MySQL and the Django adapter:

       pip install mysqlclient

    2. Update DATABASES in settings.py:

       DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '3306',
          }
      }

🎨 CSS Styling with MDB in React

For UI styling, we use MDBootstrap (Material Design for Bootstrap).
### How to Install MDB in React

   If not already installed, run:

    npm install mdb-react-ui-kit

    Then import it in index.js or App.js:

    import 'mdb-react-ui-kit/dist/css/mdb.min.css';
    import 'bootstrap/dist/css/bootstrap.min.css';

