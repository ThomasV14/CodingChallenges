# Weather Powered Email

- Send emails to subscribers with the weather for their respective location
- Provides a web interface to sign up for emails

## Installation

0. Activate Virtual Environment
1. Use a package manager like [pip](https://pip.pypa.io/en/stable/) to install everything found in requirements.txt after navigating to project
2. Navigate to application

```bash
cd WeatherEmail/
source env/bin/activate 
cd weatherapp/
```

## Usage

### Web Interface

```bash
python manage.py runserver
```
Open development server in your browser and use interface

### Sending Emails to Subscribers

```bash
python manage.py sendemails
```

## Notes

- Sending emails requires an API Key, get your own from Darksky and place in WeatherEmail/weatherapp/suscriber/management/commands/sendemails.py
- Read about API at [Dark Sky](https://darksky.net/dev/docs/faq)
- Sign in information for Django Admin -> Username: Admin, Password: password

### Coding Challenge Notes
- This is my first time using the Django framework

- The app is currently using SQLite database, not suitable for a production environment, so should switch to something more scalable like Postgres

- Accuracy of weather is completely dependent on API

- Throughout the app, subscriber has been misspelled as suscriber, please ignore that! Nothing client facing besides the URL contains that misspelling

- One bottleneck of the current implementation is that API only allows 1000 Calls per day and sending emails to subscribers requires at least 600 requests

- Top 100 cities are only found once, so are "static" by design. I assumed this shouldn't be a problem as these cities shouldn't change often.

- Notable Files (Commented):
	- WeatherEmail/weatherapp/suscriber/management/commands/sendemails.py -> Django management command to send emails
	- WeatherEmail/weatherapp/suscriber/migrations/0002_auto_20190623_2338.py -> Migration that takes place to find top 100 cities by population

- CSS was done inline, but should have been placed in STATIC folders.
