import threading
import requests
from bs4 import BeautifulSoup
import csv

OBJECT_KEYS = [
    "name",
    "id",
    "bangla",
    "english",
    "ict",
    "physics",
    "chemistry",
    "main_subject",
    "4th_subject",
    "total",
]

# function for getting individual result
def get_result(id, level, exam_id):
    url = "http://180.211.183.206/EasyCollegeMate/public/result"
    post_object = {
        "_token": "wD2UgAwJ9mcvpUb1KPxqlKy6Ml1VdzOU136wWD2B",
        "student_id": id,
        "level": level,
        "exam_id": exam_id,
    }
    res = requests.post(url, params=post_object)
    return res


# function for scrapping result data from html
def getObject(html):
    obj = {}
    soup = BeautifulSoup(html.text, "html.parser")
    table1 = soup.find("div", attrs={"class": "col-sm-12"})

    name = table1.findAll("td")[3].text  # name is present in the 4th td
    studentID = table1.findAll("td")[9].text  # id is present in the 11th td

    obj[OBJECT_KEYS[0]] = name
    obj[OBJECT_KEYS[1]] = studentID

    table2 = soup.findAll("table", attrs={"class": "table table-bordered"})[1]
    marks = table2.findAll("td", attrs={"style": "text-align: center;"})

    try:
        row = [
            int(marks[4].text),
            int(marks[10].text),
            int(marks[20].text),
            int(marks[27].text),
            int(marks[34].text),
            int(marks[41].text),
            int(marks[48].text),
        ]
    except:
        row = [0, 0, 0, 0, 0, 0, 0]
        print(f"problem at id {studentID}")

    total = sum(row)
    row.append(total)

    for i in range(2, len(OBJECT_KEYS)):
        obj[OBJECT_KEYS[i]] = row[i - 2]

    return obj


def saveCSV():
    print("------------------------------------")
    print("----------STARTING SCRAPPING------------\n")
    filename = str(input("Enter filename to save: "))

    with open(f"{filename}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, OBJECT_KEYS)
        w.writeheader()
        for i in range(1, 273):
            studentID = int(f"2021000{i:03d}")
            res = get_result(studentID, 1, 2)
            obj = getObject(res)

            w.writerow(obj)
            print(f"written... studentID: {obj['id']}")

    print("----------DONE SCRAPPING------------\n")
    print("------------------------------------")


results = list()
threads = list()

def threadFunc(i):
    studentID = int(f"2021000{i:03d}")
    res = get_result(studentID, 1, 2)
    obj = getObject(res)

    results.append(obj)
    print(f"appended {obj['id']}")

# saveCSV()
for i in range(1, 273):
    x = threading.Thread(target=threadFunc, args=(i, ))
    threads.append(x)

for t in threads:
    t.start()

for result in results:
    with open("thread.csv", "w", newline="") as f:
        w = csv.DictWriter(f, OBJECT_KEYS)
        w.writeheader()
        for result in results:
            w.writerow(result)
            print(f"written... studentID: {result['id']}")