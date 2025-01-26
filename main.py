
import threading, json, datetime
from src.utils import getMaxValueReport, getMinValueReport, getMeanValueReport

threads = []

def make_report(db_name, topicId):
    try:
        offset = datetime.timedelta(hours=5,minutes=10)
        difference = datetime.datetime.utcnow() - offset

        max = threading.Thread(target=getMaxValueReport, args=(db_name, topicId, difference,))
        mean = threading.Thread(target=getMeanValueReport, args=(db_name, topicId, difference,))
        min = threading.Thread(target=getMinValueReport, args=(db_name, topicId, difference,))

        threads.append(max)
        threads.append(min)
        threads.append(mean)
    except Exception as e:
        print(e)

with open('stations.json', encoding='UTF-8') as f:
    stations = json.load(f)

for x in stations:
    make_report(x["db"], x["topic"])

for t in threads:
    t.start()

for t in threads:
    t.join()