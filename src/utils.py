import os, pyodbc, datetime
from requests import post
from dotenv import load_dotenv
from src.models import *

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

def getReportValues(db: str, topicId: str, query: str, report_name: str):
    report = Report(report_name)

    conn = pyodbc.connect(getConnectionString(db))
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    for r in records:
        report.update_magnitude(r.MagnitudeId, r.Value)

    if not report.isempty():
        PostTelegramMessage(str(report), topicId)

def getMaxValueReport(db: str, topicId: str, time: datetime.datetime):

    query = f"""
SELECT Value, CurrentTime, MagnitudeId
FROM dbo.MaxValue
WHERE CurrentTime > '{time}'
"""
    getReportValues(db, topicId, query, 'Valores Máximos')

def getMinValueReport(db: str, topicId: str, time: datetime.datetime):
    query = f"""
SELECT Value, CurrentTime, MagnitudeId
FROM dbo.MinValue
WHERE CurrentTime > '{time}'
"""
    getReportValues(db, topicId, query, 'Valores Mínimos')

def getMeanValueReport(db: str, topicId: str, time: datetime.datetime):

    query = f"""
SELECT Value, EndTime, MagnitudeId
FROM dbo.MeanValue
WHERE EndTime > '{time}'
"""
    getReportValues(db, topicId, query, 'Valores Promedio')
