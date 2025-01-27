
import threading, json, datetime
from src.utils import jointReport

threads = []

def make_report(db_name, topicId, minutes_offset):
    try:
        offset = datetime.timedelta(hours=5,minutes=minutes_offset)
        difference = datetime.datetime.utcnow() - offset
        sqltime = difference.strftime('%Y-%m-%d %H:%M:%S')

        t = threading.Thread(target=jointReport, args=(db_name, topicId, sqltime,))
        threads.append(t)
        
    except Exception as e:
        print(e)

with open('stations.json', encoding='UTF-8') as f:
    stations = json.load(f)

for x in stations:
    make_report(x["db"], x["topic"], x["offset"])

for t in threads:
    t.start()

for t in threads:
    t.join()