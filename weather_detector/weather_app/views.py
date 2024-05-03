from django.shortcuts import render, redirect
import json
import urllib.request
# Create your views here.



# def index(request):
#     if request.method == 'POST':
#         city = request.POST['city']
#         api_key = 'da63ed3d7fe23de14d3bcc4e2cbbb80c'
#         # res = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}').read()
#         json_data = json.loads(res)
#         data = {
#         'country_code': str(json_data['sys']['country']),
#         'coordinate': str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
#         'temperature': str(json_data['main']['temp']) + 'k',
#         'pressure': str(json_data['main']['pressure']),
#         'humidity': str(json_data['main']['pressure'])
#         }
#     else:
#         city = ''
#         data = {}
#
#     return render(request, 'index.html', {'city': city, 'data': data})


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        if city:
            try:
                res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=da63ed3d7fe23de14d3bcc4e2cbbb80c').read()

                json_data = json.loads(res)
                data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": str(json_data['coord']['lon']) + ' ' +
                str(json_data['coord']['lat']),
                "temp": str(json_data['main']['temp']) + 'k',
                "pressure": str(json_data['main']['pressure']),
                "humidity": str(json_data['main']['humidity']),
                "weather_description": str(json_data['weather'][0]['description']),
                }

            except urllib.error.HTTPError as e:
                if e.code == 404:
                    message = 'City was not found, please enter a valid city name'
                    return render(request, 'index.html', {'city': city, 'message': message})
                else:
                    message = "An error occurred while processing your request."
                    return render(request, 'index.html', {'city': city, 'message': message})

        else:
           message = "Please enter a city name."
           return render(request, 'index.html', {'city': city, 'message': message})
    else:
        city = ''
        data = {}

    return render(request, 'index.html', {'city': city, 'data': data})
