# Quiz

A Django application for testing interns. Trainers manage intern accounts and review results; interns take quizzes with up to 10 random questions and a 10-minute browser timer.

**Stack:** Python, Django, MySQL, Bootstrap, JavaScript.

## Setup

Requires Python 3.10+ and MySQL. Run from the directory containing `manage.py`:

```bash
python -m venv .venv
# Activate: .venv\Scripts\Activate.ps1 (Windows)
# Or: source .venv/bin/activate (Linux/macOS)
python -m pip install "Django==5.2.3" mysqlclient
```

Create the MySQL database `quiz_db` and configure credentials in `quiz/settings.py`, then run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Admin: `/admin/`.

## Usage

Register as a **trainer** at `/accounts/signup/`, create interns from the trainer dashboard, and add questions through admin. Interns can then log in and take quizzes.

## Google Sheets (Optional)

Install `gspread oauth2client`, enable Sheets and Drive APIs, place a service account key at `credentials.json`, and share the spreadsheet with its email.

Expected spreadsheet: **СВОД**, worksheet: **тест**. Columns: question, correct answer, three wrong answers. The first row is a header.

```bash
python -m app.command
```

Repeated imports create duplicates. Never commit credentials.

## Status

Development only: direct intern signup is broken; result ownership, server-side quiz validation, and attempt history need fixes. Before deployment, fix these issues, secure secrets, disable `DEBUG`, and restrict `ALLOWED_HOSTS`. Automated tests and a license are not included.
