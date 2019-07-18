from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from suscriber.models import Subscription, City
from dateutil.relativedelta import relativedelta
from smtplib import SMTPException
import requests
import json
import datetime


DARK_SKY_API_KEY = '3e0450ad2b2ffe1dea1517d276e2b5e0'

class Command(BaseCommand):
    help = 'Sends email to suscribers'

    def handle(self, *args, **options):
        """
        Top level function used to handle command to send emails to subscribers
        Note:
            Progress is printed to standard out
        """
        FAILURE = "Unable To Send Emails To Subscribers"

        self.stdout.write("Preparing to Send Emails")

        cities = City.objects.all()
        
        subscribers = Subscription.objects.all()
        if len(subscribers) == 0:
            self.stdout.write("No Subscribers")
            return

        
        self.stdout.write("Acquiring Current Weather Conditions")

        current_temperatures = self.collect_current_temperatures(cities)
        if current_temperatures is None:
            self.stdout.write(FAILURE)
            return

        self.stdout.write("Acquiring Average Weather Conditions Over The Past 5 Years")

        average_temperatures = self.collect_average_temperatures(cities)

        if average_temperatures is None:
            self.stdout.write(FAILURE)
            return
        
        self.stdout.write("Sending Emails")


        self.send_emails(subscribers,current_temperatures,average_temperatures)

        self.stdout.write("Finished Sending Emails")

    def collect_current_temperatures(self,cities):
        """
        Uses Darksky API to get current temperature of all the top 100 cities
        Note:
            Requires an API Key
            Read more about response format at https://darksky.net/dev/docs/faq
            Checking the length is 101 is due to adding an extra city for testing purposes, change to 100 if not adding extra city
        Args:
            cities (Query_Set): All the top 100 cities currently in the database (+ 1 city for testing purposes)
        Returns:
            current_temperatures(dict): Dictionary containing mappings of cities to current weather conditions (temperature, summary, weather_icon)
        Raises:
            HTTPError: When there is an http error when making the request
            Exception: Any other errors that occur when making the request
        """
        current_temperatures = dict()
        api_url_base = 'https://api.darksky.net/forecast/'

        for city in cities:
            url = api_url_base + DARK_SKY_API_KEY + '/' + str(city.lattitude) + ',' + str(city.longitude)
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.HTTPError as http_err:
                self.stdout.write('HTTP Error Occured : {}'.format(http_err))
                break
            except Exception as err:
                self.stdout.write('Non-HTTP Error Occured: {}'.format(err))
                break
            else:
                if response.status_code == 200:

                    payload = json.loads(response.content.decode())
                    temperature = payload['currently']['temperature']
                    summary = payload['currently']['summary']
                    icon = payload['currently']['icon']
                    current_temperatures[city] = [temperature,summary,icon]
        
        if len(current_temperatures) == 101:
            self.stdout.write("Successfully Acquired Current Weather Conditions")
            return current_temperatures
        else:
            self.stdout.write("Unable To Acquire Current Weather Conditions")
            return None


    def collect_average_temperatures(self,cities):
        """
        Uses Darksky API to get average temperature of all the top 100 cities over the past five years
        Notes:
            Requires an API Key
            Read more about response format at https://darksky.net/dev/docs/faq
            Checking the length is 101 is due to adding an extra city for testing purposes, change to 100 if not adding extra city
            Average temperature is calculated using mean but median can be used instead if mean becomes skewed
            Makes 5 API Calls per city, so around 500 API Calls are made
        Args:
            cities (Query_Set): All the top 100 cities currently in the database (+ 1 city for testing purposes)
        Returns:
            average_temperatures(dict): Dictionary containing mappings of cities to average temperature over the past 5 years
        Raises:
            HTTPError: When there is an http error when making the request
            Exception: Any other errors that occur when making the request
        """
        years_back = 5
        current_date = datetime.datetime.now()
        years_ago = [current_date - relativedelta(years=year) for year in range(1,years_back+1)]
        unix_timestamps = [int(date.timestamp()) for date in years_ago]
        average_temperatures = dict()



        api_url_base = 'https://api.darksky.net/forecast/'
        for city in cities:
            average_temperatures[city] = []
            for timestamp in unix_timestamps:
                url = api_url_base + DARK_SKY_API_KEY + '/' + str(city.lattitude) + ',' + str(city.longitude) + ',' + str(timestamp)
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.HTTPError as http_err:
                    self.stdout.write('HTTP Error Occured : {}'.format(http_err))
                    break
                except Exception as err:
                    self.stdout.write('Non-HTTP Error Occured: {}'.format(err))
                    break
                else:
                    if response.status_code == 200:
                        payload = json.loads(response.content.decode())
                        temperature = payload['currently']['temperature']
                        average_temperatures[city].append(temperature)


        if len(average_temperatures) == 101:
            for city,temperatures in average_temperatures.items():
                average_temperatures[city] = sum(temperatures)//years_back
            self.stdout.write("Successfully Acquired Historical Weather Conditions")
            return average_temperatures
        else:
            self.stdout.write("Unable To Acquire Historical Weather Conditions")
            return None



    def send_emails(self,subscribers,current_temperatures,average_temperatures):
        """
        Sends emails to all subscribers depending on current and average temperatures of their respective location
        Notes:
            Only catching one type of exception, would be better to catch a more general error such as IOError
        Args:
            subscribers (Query_Set): All the subscribers
            current_temperatures(dict): Dictionary containing mappings of cities to current weather conditions (temperature, summary, weather_icon)
            average_temperatures(dict): Dictionary containing mappings of cities to average temperature over the past 5 years
        Raises:
            SMTPException: When there is an error sending emails
        """

        SUBJECT_GOOD = "It's nice out! Enjoy a discount on us."
        SUBJECT_BAD = "Not so nice out? That's okay, enjoy a discount on us." 
        SUBJECT_NEUTRAL = "Enjoy a discount on us."

        for suscriber in subscribers:
            email = suscriber.email
            city = suscriber.city
            current_temperature_city = current_temperatures[city][0]
            current_weather = current_temperatures[city][1]
            icon = current_temperatures[city][2]
            average_temperature_city = average_temperatures[city]

            EMAIL_SUBJECT = SUBJECT_NEUTRAL
            if current_temperature_city >= (average_temperature_city + 5) or icon == 'clear-day':
                EMAIL_SUBJECT = SUBJECT_GOOD
            elif current_temperature_city <= (average_temperature_city - 5) or icon == 'rain' or icon == 'snow':
                EMAIL_SUBJECT = SUBJECT_BAD

            EMAIL_BODY = 'Location: {} \n Weather: {} degrees, {}'.format(city,int(current_temperature_city),str(icon).lower().capitalize().replace('-',' '))
            try:
                send_mail(
                    EMAIL_SUBJECT,
                    EMAIL_BODY,
                    'weatherappdjangoklaviyo@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except SMTPException as e:
                self.stdout.write('There was an error sending mail')
        