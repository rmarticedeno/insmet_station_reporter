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

def checkValidity(cursor, db, type):
    sqlcheck = f"""SELECT modify_date
    FROM "{db}"."sys"."objects"
    WHERE "type" IN ('P', 'U', 'V', 'TR', 'FN', 'TF', 'IF')
    AND name = '{type}';"""

    cursor.execute(sqlcheck)
    value = cursor.fetchall()[0]
    
    offset = datetime.timedelta(hours=5)
    difference = datetime.datetime.utcnow() - offset - value

    return difference.seconds < 60
    offset = datetime.timedelta(hours=5)
    difference = datetime.datetime.utcnow() - offset - row.EndTime
    
    return difference.seconds < 60

def getReportValues(db: str, topicId: str, query: str, report_name: str, check = None):
    report = Report(report_name)

    conn = pyodbc.connect(getConnectionString(db))
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    for r in records:
        report.update_magnitude(r.MagnitudeId, r.Value)
    
    if check is not None and not check(cursor):
        return

    PostTelegramMessage(str(report), topicId)

def getMaxValueReport(db: str, topicId: str):

    query = """
SELECT Value, CurrentTime, MagnitudeId
FROM dbo.MaxValue
WHERE CurrentTime = (
    SELECT MAX(CurrentTime)
    FROM dbo.MaxValue
)
"""
    getReportValues(db, topicId, query, 'Valores Máximos', lambda x: checkValidity(x, db, 'MaxValue'))

def getMinValueReport(db: str, topicId: str):
    query = """
SELECT Value, CurrentTime, MagnitudeId
FROM dbo.MinValue
WHERE CurrentTime = (
    SELECT MAX(CurrentTime)
    FROM dbo.MinValue
)
"""
    getReportValues(db, topicId, query, 'Valores Mínimos', lambda x: checkValidity(x, db, 'MinValue'))

def getMeanValueReport(db: str, topicId: str):

    query = """
SELECT Value, EndTime, MagnitudeId
FROM dbo.MeanValue
WHERE EndTime = (
    SELECT MAX(EndTime)
    FROM dbo.MeanValue
)
"""
    getReportValues(db, topicId, query, 'Valores Promedio', lambda x: checkValidity(x, db, 'MeanValue'))
