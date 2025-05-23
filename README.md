# BloodConnect 🚑
A web platform connecting blood donors with those in need.

## Features
- Donor registration and profile management
- Blood request creation and management
- Search functionality for finding donors
- Admin dashboard for platform management
- Emergency request system
- User authentication and authorization

## Tech Stack
- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite
- Authentication: Django AllAuth

## Setup Instructions

```
git clone https://github.com/0xarun/Mini-Projects.git
cd Mini-Projects
cd BloodConnet
```

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure
```
bloodconnect/
├── manage.py
├── requirements.txt
├── bloodconnect/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
├── donors/
├── requests/
├── static/
└── templates/
```

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details. 
