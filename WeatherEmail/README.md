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