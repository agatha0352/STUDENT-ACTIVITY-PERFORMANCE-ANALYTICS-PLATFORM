import pandas as pd
import oracledb
from sqlalchemy import create_engine

oracledb.init_oracle_client(
    lib_dir=r"C:\Users\AGATHA\Downloads\instantclient-basic-windows.x64-23.26.2.0.0\instantclient_23_0"
)

engine = create_engine(
    "oracle+oracledb://student_analytics:Welcome123@localhost:1521/?service_name=XE"
)

# ---- DAU / WAU / MAU (averaged across the whole data period) ----
dau = pd.read_sql("""
    SELECT ROUND(AVG(daily_count)) AS avg_dau FROM (
        SELECT login_date, COUNT(DISTINCT student_id) AS daily_count
        FROM login_activity GROUP BY login_date
    )
""", engine).iloc[0, 0]

wau = pd.read_sql("""
    SELECT ROUND(AVG(weekly_count)) AS avg_wau FROM (
        SELECT TRUNC(login_date, 'IW') AS wk, COUNT(DISTINCT student_id) AS weekly_count
        FROM login_activity GROUP BY TRUNC(login_date, 'IW')
    )
""", engine).iloc[0, 0]

mau = pd.read_sql("""
    SELECT ROUND(AVG(monthly_count)) AS avg_mau FROM (
        SELECT TRUNC(login_date, 'MM') AS mo, COUNT(DISTINCT student_id) AS monthly_count
        FROM login_activity GROUP BY TRUNC(login_date, 'MM')
    )
""", engine).iloc[0, 0]

# ---- Completion / attendance / participation rates ----
completion_rate = pd.read_sql("""
    SELECT ROUND(SUM(CASE WHEN completed='Yes' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS rate
    FROM course_progress
""", engine).iloc[0, 0]

webinar_rate = pd.read_sql("""
    SELECT ROUND(SUM(CASE WHEN attended='Yes' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS rate
    FROM webinar_attendance
""", engine).iloc[0, 0]

event_rate = pd.read_sql("""
    SELECT ROUND(SUM(CASE WHEN participation_type='Attended' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS rate
    FROM offline_events
""", engine).iloc[0, 0]

# ---- Average activity score + at-risk count (from the table you just built) ----
avg_score = pd.read_sql("SELECT ROUND(AVG(activity_score), 1) AS v FROM activity_scores", engine).iloc[0, 0]
at_risk_count = pd.read_sql("SELECT COUNT(*) AS v FROM activity_scores WHERE segment = 'At Risk'", engine).iloc[0, 0]

kpis = pd.DataFrame([
    {"kpi": "Daily Active Users (avg)", "value": dau},
    {"kpi": "Weekly Active Users (avg)", "value": wau},
    {"kpi": "Monthly Active Users (avg)", "value": mau},
    {"kpi": "Course Completion Rate (%)", "value": completion_rate},
    {"kpi": "Webinar Attendance Rate (%)", "value": webinar_rate},
    {"kpi": "Event Participation Rate (%)", "value": event_rate},
    {"kpi": "Average Activity Score", "value": avg_score},
    {"kpi": "At-Risk Student Count", "value": at_risk_count},
])

kpis.to_csv("data/processed/kpi_summary.csv", index=False)

# Write to Oracle with a plain cursor (avoids a pandas/Oracle FLOAT type mismatch)
raw_conn = engine.raw_connection()
cursor = raw_conn.cursor()
cursor.execute("DELETE FROM kpi_summary")
cursor.executemany(
    "INSERT INTO kpi_summary (kpi, value) VALUES (:1, :2)",
    list(kpis.itertuples(index=False, name=None))
)
raw_conn.commit()
cursor.close()
raw_conn.close()

print(kpis.to_string(index=False))
print("\nSaved to data/processed/kpi_summary.csv and Oracle table KPI_SUMMARY")