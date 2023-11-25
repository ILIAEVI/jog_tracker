import requests


def get_weather_condition(api_key, date, location):

    api_url = 'https://api.weatherapi.com/v1/forecast.json'

    formatted_date = date.strftime('%Y-%m-%d')

    params = {
        'key': api_key,
        'q': location,
        'dt': formatted_date,
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        data = response.json()

        day_forecast = next((day for day in data['forecast']['forecastday'] if day['date'] == formatted_date), None)

        if day_forecast:
            condition = day_forecast['day']['condition']['text']
            avg_temperature = day_forecast['day']['avgtemp_c']
            max_temperature = day_forecast['day']['maxtemp_c']
            min_temperature = day_forecast['day']['mintemp_c']
            return {
                'condition': condition,
                'max_temperature': max_temperature,
                'min_temperature': min_temperature,
                'avg_temperature': avg_temperature
            }
        else:
            print(f"No forecast data found for {formatted_date}")
            return None

    except requests.exceptions.RequestException as e:

        print(f"Error in weather API request: {e}")
        return None

    except KeyError as e:

        print(f"Error parsing API response: {e}")
        return None
