"""
Main cli or app entry point
"""

import asyncio
from aiohttp import web

import aiohttp

class Weather:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.weatherapi.com/v1/'

    async def get_weather(self, location):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}forecast.json?key={self.api_key}&q={location}&days=7&aqi=no&alerts=no"
            async with session.get(url) as response:
                data = await response.json()
                return data

async def hello(request):
    return web.Response(text="Weather Forecast")

async def get_weather_forecast(request):
    postal_code_name = request.match_info['postal_code_name']
    api_key = "8c6f3dd4789e4646a5d44946231402"
    api = Weather(api_key)
    forecast = await api.get_weather(postal_code_name)

    last_updated = forecast['current']['last_updated']
    timezone = forecast['location']['tz_id']
    localtime = forecast['location']['localtime']

    forecast_strings = []
    for forecast_day in forecast['forecast']['forecastday']:
        date = forecast_day['date']
        max_temp = forecast_day['day']['maxtemp_f']
        min_temp = forecast_day['day']['mintemp_f']
        avg_temp = forecast_day['day']['avgtemp_f']
        weather_condition = forecast_day['day']['condition']['text']
        chance_of_rain = forecast_day['day']['daily_chance_of_rain']
        chance_of_snow = forecast_day['day']['daily_chance_of_snow']
        avg_humidity = forecast_day['day']['avghumidity']
        sunrise = forecast_day['astro']['sunrise']
        sunset = forecast_day['astro']['sunset']

        forecast_string = (
            f"\nDate: {date},\n"
            f"Maximum temperature: {max_temp}°F,\n"
            f"Minimum temperature: {min_temp}°F,\n"
            f"Average temperature: {avg_temp}°F,\n"
            f"Weather condition: {weather_condition}\n"
            f"The probability of rain is {chance_of_rain}%,\n"
            f"The probability of snow is {chance_of_snow}%,\n"
            f"The average humidity is {avg_humidity}%,\n"
            f"Sunrise: {sunrise}; Sunset: {sunset}.\n"
        )

        forecast_strings.append(forecast_string)

    forecast_string = ''.join(forecast_strings)

    output_string = (
        f"Weather forecast for {forecast['location']['name']} "
        f"({forecast['location']['region']}, {forecast['location']['country']})\n"
        f"Last updated time: {last_updated}\n"
        f"Time zone: {timezone}\n"
        f"The query time is {localtime}\n"
        f"Today is {forecast['forecast']['forecastday'][0]['date']}\n"
        f"{forecast_string}"
    )

    print(output_string)

    return web.Response(text=output_string)

async def start_app():
    app = web.Application()
    app.add_routes([
        web.get('/', hello),
        web.get('/{postal_code_name}', get_weather_forecast)
    ])
    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(start_app())
    web.run_app(app)
    
