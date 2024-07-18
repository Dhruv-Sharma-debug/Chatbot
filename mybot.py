import json
from difflib import get_close_matches
import requests
import wikipedia
from wikipedia.exceptions import PageError
from gtts import gTTS
import pygame
def loadkb(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def savekb(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def findmatch(ques: str, questions: list[str]) -> str | None:
    best_match:list = get_close_matches(ques, questions,n=1,cutoff=0.7)
    return best_match[0] if best_match else None

def getans(question: str, kb: dict) -> str | None:
    for q in kb["questions"]:
        if q["ques"] == question:
            return q["answer"]

def cbot(querry)->str:
    if "weather" in querry.lower():
        baseurl = "http://api.openweathermap.org/data/2.5/weather?q=Mandi,in&APPID=3f731e7bd75d09070d0f046fb7dd56a9"
        response = requests.get(baseurl).json()
        temp_k = response['main']['temp']
        temp = temp_k - 273.15
        temp = round(temp, 2)
        desc = response['weather'][0]['description']
        return f"it is {temp} degree celsius here in mandi and weather is {desc}"
    elif "wikipedia" in querry.lower():
        querry = querry.lower()
        if "according to wikipedia" in querry:
            querry = querry.replace("according to wikipedia","")
        if "wikipedia" in querry:
            querry = querry.replace("wikipedia","")
        try:
            result = wikipedia.summary(querry, sentences=2)
            result = "according to wikipedia " + result
            return result
        except PageError as e:
            return f"no page found on wikipedia related to {querry}"

    else:
        kbase: dict = loadkb('knowledge_base.json')
        user_input: str = querry.lower()
        best_match: str | None = findmatch(user_input, [q["ques"] for q in kbase["questions"]])

        if best_match:
            answer: str = getans(best_match, kbase)
            return answer
        else:
            print("bot: don't know the answer")
            nanswer: str = input("can you teach me or skip: ").lower()
            if nanswer.lower() != "skip":
                kbase["questions"].append({"ques": user_input, "answer": nanswer})
                savekb('knowledge_base.json', kbase)
                print("bot: thank you")

if __name__ == "__main__":
    query=input("you : ")
    result=cbot(query)
    tospeak=result;
    tts=gTTS(text=tospeak,lang='en')

    tts.save("output.mp3")

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
          pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    pygame.quit()
    print(result)

