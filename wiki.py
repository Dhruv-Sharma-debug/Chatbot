import wikipedia
from wikipedia.exceptions import PageError
querry=querry.lower()
if "wikipedia" in querry:
    querry=querry.replace("wikipedia")
if "according to wikipedia" in querry:
    querry = querry.replace("according to wikipedia")
try:
    result=wikipedia.summary(querry,sentences=2)
    result="according to wikipedia "+result
    print(result)
except PageError as e:
    print(f"no page found on wikipedia related to {querry}")