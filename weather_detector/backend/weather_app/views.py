from django.http import JsonResponse
import json
import urllib.request

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))  # Parse JSON
        city = data.get("city", "").strip()  # Get city from JSON

        if city:
            try:

                res = urllib.request.urlopen(
                    f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=da63ed3d7fe23de14d3bcc4e2cbbb80c'
                ).read()
                json_data = json.loads(res)
                data = {
                    "country_code": json_data['sys']['country'],
                    "coordinate": f"{json_data['coord']['lon']} {json_data['coord']['lat']}",
                    "temp": f"{json_data['main']['temp']}K",
                    "pressure": str(json_data['main']['pressure']),
                    "humidity": str(json_data['main']['humidity']),
                    "weather_description": json_data['weather'][0]['description'],
                }
                return JsonResponse({"city": city, "data": data})

            except urllib.error.HTTPError as e:
                message = "City not found" if e.code == 404 else "Error processing request"
                return JsonResponse({"city": city, "message": message}, status=400)
        print("City name not provided.")
        return JsonResponse({"message": "Please enter a city name."}, status=400)
    return JsonResponse({"message": "Invalid request method."}, status=405)
