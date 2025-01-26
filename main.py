
import threading, json
from src.utils import getMaxValueReport, getMinValueReport, getMeanValueReport

threads = []

def make_report(db_name, topicId):
    try:
        max = threading.Thread(target=getMaxValueReport, args=(db_name, topicId,))
        mean = threading.Thread(target=getMeanValueReport, args=(db_name, topicId,))
        min = threading.Thread(target=getMinValueReport, args=(db_name, topicId,))

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