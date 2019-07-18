from django.db import migrations
import requests
import json



def get_top_cities():
	"""

	Uses Opendata API to get top 100 cities by population in a sorted order

	Note:
		Does not require an API Key

	Returns:
		Response from API decoded in Dictionary Format

	Raises:
		HTTPError: When there is an http error when making the request
		Exception: Any other errors that occur when making the request
	
	"""
	api_url_base = 'https://public.opendatasoft.com/api/records/1.0/'
	query = 'search/?dataset=worldcitiespop&rows=100&sort=population&refine.country=us'

	url = api_url_base + query
	
	try:
		response = requests.get(url)
		response.raise_for_status()
	except requests.HTTPError as http_err:
		print('HTTP Error Occured : {}'.format(http_err))
	except Exception as err:
		print('Non-HTTP Error Occured: {}'.format(err))
	else:
		if response.status_code == 200:
			print("Successfully Acquired Top 100 Cities With Highest Populations")
			return json.loads(response.content.decode())
	
	print("Unable To Acquire Top 100 Cities With Highest Populations")
	return None


def parse_data(data):
	"""

	Parses the data received in JSON format and returns them in a list and dictionary

	Args:
		data (dict): The decoded response from the API

	Returns:
		cities (list): All the top 100 cities found from the API in list format where each element is a tuple in the format city,state
		locations (dict):  The locations of the top 100 cities represented via latitude and longitude mapped -> city:location

	
	"""
	cities = []
	locations = dict()

	if data:

		RECORDS = 'records'
		FIELDS = 'fields'
		CITY = 'accentcity'
		STATE = 'region'
		LONGITUDE = 'longitude'
		LATITUDE = 'latitude'

		records = data[RECORDS]
		for record in records:
			fields = record[FIELDS]
			city_name = fields[CITY]
			state = fields[STATE]
			longitude = fields[LONGITUDE]
			latitude = fields[LATITUDE]

			cities.append((city_name,state))
			locations[(city_name,state)] = [latitude,longitude]

	return cities,locations

def save_data(cities,locations,apps):
	"""

	Saves the top 100 cities found from the API into the Database

	Args:
		cities (list): All the top 100 cities found from the API in list format where each element is a tuple in the format city,state
		locations (dict):  The locations of the top 100 cities represented via latitude and longitude mapped -> city:location
		apps (Object): The Apps Registry
	
	
	"""
	if len(cities) == 0:
		return

	City = apps.get_model('suscriber','City')
	for i in range(len(cities)):
		current = cities[i]
		name = current[0]
		state = current[1]
		longitude = locations[current][1]
		lattitude = locations[current][0]

		entry = City(name=name,state=state,longitude=longitude,lattitude=lattitude)
		entry.save()

		

def get_cities(apps,schema_editor):
	"""

	Top level function used to find top 100 cities by population

	Args:
		apps (Object): Apps Registry 
		schema_editor (Object):  Schema Editor
	
	"""
	data = get_top_cities()
	cities, locations = parse_data(data)
	save_data(cities,locations,apps)


class Migration(migrations.Migration):

    dependencies = [
        ('suscriber', '0001_initial'),
    ]

    operations = [migrations.RunPython(get_cities)]
