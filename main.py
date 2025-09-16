from flask import Flask
app = Flask(__name__)

import requests
from datetime import datetime
import json

class Lesson:
    def __init__(self, subject, teachers, date, begin, end, classroom):
        self.subject = subject
        self.teachers = teachers
        self.date = date
        self.begin = self.convert_date(date, begin)
        self.end = self.convert_date(date, end)
        self.classroom = classroom
    
    def __str__(self):
        return f'{self.subject} by {self.teachers} on {self.date} from {self.begin} to {self.end} in {self.classroom}'

    def convert_date(self, date, time):
        combined_str = f"{date} {time}"
        input_format = "%d-%m-%Y %H:%M"
        dt = datetime.strptime(combined_str, input_format)
        return dt.isoformat()
        
    def __dict__(self):
        return {
            "name": self.subject,
            "teachers": self.teachers,
            "date": self.date,
            "begin": (datetime.fromisoformat(self.begin)).strftime("%H:%M"),
            "end": (datetime.fromisoformat(self.end)).strftime("%H:%M"),
            "classroom": self.classroom
        }

    
def get_lessons():
    url = "https://logistica.unisalento.it/PortaleStudenti/grid_call.php"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.5",
        "accept-encoding": "gzip, deflate, br, zstd",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "PHPSESSID=9l33ejd1iuo2gbtm8h3q3sekf1",
        "origin": "https://logistica.unisalento.it",
        "referer": "https://logistica.unisalento.it/PortaleStudenti/?view=easycourse&form-type=corso&include=corso&txtcurr=&anno=2025&corso=LB55&anno2%5B%5D=999%7C2&visualizzazione_orario=cal&date=27-08-2025&periodo_didattico=&_lang=it&list=1&week_grid_type=1&ar_codes_=&ar_select_=&col_cells=0&empty_box=0&only_grid=0&highlighted_date=0&all_events=0&faculty_group=0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {
        "view": "easycourse",
        "form-type": "corso",
        "include": "corso",
        "txtcurr": "",
        "anno": "2025",
        "corso": "LB55",
        "anno2[]": "999|2",
        "visualizzazione_orario": "cal",
        "date": "27-08-2025",
        "periodo_didattico": "",
        "_lang": "it",
        "list": "1",
        "week_grid_type": "1",
        "ar_codes_": "",
        "ar_select_": "",
        "col_cells": "0",
        "empty_box": "0",
        "only_grid": "0",
        "highlighted_date": "0",
        "all_events": "0",
        "faculty_group": "0",
        "all_events": "1",
    }

    response = requests.post(url, headers=headers, data=data)

    # with open("bullshit.json", "w") as f:
    #     f.write(response.text)

    lessons_rndm_bullshit = (response.json()).get("celle")
    lessons = []
    subjects = []
    for l in lessons_rndm_bullshit:
        if l.get("tipo") == "Lezione":
            subject = l.get("nome_insegnamento")
            teachers = ["Undefined"] if not (docente := l.get("docente")) else docente.split(", ")
            date = l.get("data")
            begin = l.get("ora_inizio")
            end = l.get("ora_fine")
            classroom = l.get("aula").replace(', ', ' -')
            l1 = Lesson(subject, teachers, date, begin, end, classroom)
            lessons.append(l1)
            if subject not in subjects:
                subjects.append(subject)
    lessons_data = [lesson.__dict__() for lesson in lessons]

    with open('lessons.json', 'w', encoding='utf-8') as f:
        json.dump(lessons_data, f, ensure_ascii=False, indent=4)
 
@app.route('/newClasses')
def hello_world():
    get_lessons()
    with open('lessons.json', 'r', encoding='utf-8') as f:
        lessons_data = json.load(f)

    return lessons_data
 
 
if __name__ == "__main__":
    app.run()
