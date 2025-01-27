import os, pyodbc, datetime
from requests import post
from dotenv import load_dotenv
from src.models import *
from src.constants import *

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
CHAT = os.getenv('CHAT_ID')
ADDR = os.getenv('DB_ADDR')
USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')

def PostTelegramMessage(message: str, topic_id: str = None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT}&message_thread_id={topic_id}&text={message}"
    post(url)

def getConnectionString(db:str):
    return f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={ADDR};DATABASE={db};UID={USER};PWD={PASS};TrustServerCertificate=yes'

def updateReportValues(report: Report, db: str, query: str, type: int):
    conn = pyodbc.connect(getConnectionString(db))
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    for r in records:
        report.update_magnitude(r.MagnitudeId, r.Value, type)

def jointReport(db: str, topicId: str, time: datetime.datetime):

    # Queries

    queryMin = f"""
SELECT Value, CurrentTime, MagnitudeId
FROM dbo.MinValue
WHERE CurrentTime > '{time}'
"""
    
    queryMean = f"""
SELECT Value, EndTime, MagnitudeId
FROM dbo.MeanValue
WHERE EndTime > '{time}'
"""

    queryMax = f"""
SELECT Value, CurrentTime, MagnitudeId
FROM dbo.MaxValue
WHERE CurrentTime > '{time}'
"""
    # report
    report = Report()

    # update values
    updateReportValues(report, db, queryMin, MIN)
    updateReportValues(report, db, queryMean, MEAN)
    updateReportValues(report, db, queryMax, MAX)

    if not report.isempty():
        PostTelegramMessage(str(report), topicId)