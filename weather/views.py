import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request: object):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=6b18cc19387391228a2a3a31bc80404e'

    errorMess =  ''
    message = ''
    messageClass = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            newCity = form.cleaned_data['name']
            excitingcitycount = City.objects.filter(name=newCity).count()

            if excitingcitycount == 0:
                r = requests.get(url.format(newCity)).json()
                print(r)
                if r['cod'] ==200:
                    form.save()
                else:
                    errorMess = 'City does not exist'

            else:
                errorMess = 'City already exists'

        if errorMess:
            message = errorMess
            messageClass = 'is-danger'
        else:
            message = 'City added'
            messageClass= 'is-success'

    print(errorMess)

    form = CityForm()

    cities = City.objects.all()

    weatherData = []

    for city in cities:


        r = requests.get(url.format(city)).json()


        cityWeather = {
            'city': city.name,
            'temp': r['main']['temp'],
            'des': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weatherData.append(cityWeather)

        print(r)



    context = {
        'weatherData' : weatherData,
        'form' : form,
        'message': message,
        'messageClass': messageClass

    }
    return render(request, 'weather/weather.html', context)

def deleteCity(request, cityName):
    City.objects.get(name = cityName).delete()
    return redirect('home')