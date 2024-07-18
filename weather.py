#3f731e7bd75d09070d0f046fb7dd56a9
import datetime as dt
import requests

baseurl="http://api.openweathermap.org/data/2.5/weather?q=Mandi,in&APPID=3f731e7bd75d09070d0f046fb7dd56a9"
apikey="3f731e7bd75d09070d0f046fb7dd56a9"
city="mandi,in"
url=baseurl+apikey+"&q="+city
print(baseurl)
response = requests.get(baseurl).json()
temp_k=response['main']['temp']
temp=temp_k-273.15
temp=round(temp,2)
desc=response['weather'][0]['description']
print(f"it is {temp} degree celsius here in mandi and weather is {desc}")
