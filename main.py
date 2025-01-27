
import threading, json, datetime, random, queue
from src.utils import jointReport, notificationsWorker

threads = []
itemsqueue = queue.Queue()

def make_report(db_name, topicId, minutes_offset):
    try:
        offset = datetime.timedelta(hours=5,minutes=minutes_offset)
        difference = datetime.datetime.utcnow() - offset
        sqltime = difference.strftime('%Y-%m-%d %H:%M:%S')
        return threading.Thread(target=jointReport, args=(itemsqueue, db_name, topicId, sqltime,))
    
    except Exception as e:
        print(e)

def create_bot(botid):
    t = threading.Thread(target=notificationsWorker, args=(botid, itemsqueue,))
    t.start()

with open('stations.json', encoding='UTF-8') as f:
    stations = json.load(f)

for x in stations:
    threads.append(make_report(x["db"], x["topic"], x["offset"]))

random.shuffle(threads)

for t in threads:
    t.start()

for t in threads:
    t.join()

with open('bots.json', encoding='UTF-8') as f:
    bots = json.load(f)

for x in bots:
    create_bot(x)

itemsqueue.join()