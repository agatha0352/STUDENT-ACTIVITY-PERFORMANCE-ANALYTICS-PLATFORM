import pandas as pd
import oracledb
from datetime import datetime

oracledb.init_oracle_client(
    lib_dir=r"C:\Users\AGATHA\Downloads\instantclient-basic-windows.x64-23.26.2.0.0\instantclient_23_0"
)

conn = oracledb.connect(
    user="student_analytics",
    password="Welcome123",
    dsn="localhost:1521/XE"
)
cursor = conn.cursor()

def to_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

# ---- 1. Students ----
df = pd.read_csv("data/raw/students.csv")
rows = list(df.itertuples(index=False, name=None))
cursor.executemany(
    "INSERT INTO students (student_id, name, college, department, batch, enrollment_status) "
    "VALUES (:1, :2, :3, :4, :5, :6)", rows
)
print(f"students: {len(rows)} rows loaded")

# ---- 2. Login activity ----
df = pd.read_csv("data/raw/login_activity.csv")
df["login_date"] = df["login_date"].apply(to_date)
rows = list(df.itertuples(index=False, name=None))
cursor.executemany(
    "INSERT INTO login_activity (login_id, student_id, login_date, login_time, device, session_duration) "
    "VALUES (:1, :2, :3, :4, :5, :6)", rows
)
print(f"login_activity: {len(rows)} rows loaded")

# ---- 3. Course progress ----
df = pd.read_csv("data/raw/course_progress.csv")
rows = list(df.itertuples(index=False, name=None))
cursor.executemany(
    "INSERT INTO course_progress (course_id, student_id, course_name, progress, completed) "
    "VALUES (:1, :2, :3, :4, :5)", rows
)
print(f"course_progress: {len(rows)} rows loaded")

# ---- 4. Webinar attendance (needs a generated attendance_id) ----
df = pd.read_csv("data/raw/webinar_attendance.csv")
df.insert(0, "attendance_id", range(1, len(df) + 1))
rows = list(df.itertuples(index=False, name=None))
cursor.executemany(
    "INSERT INTO webinar_attendance (attendance_id, webinar_id, student_id, webinar_name, attended) "
    "VALUES (:1, :2, :3, :4, :5)", rows
)
print(f"webinar_attendance: {len(rows)} rows loaded")

# ---- 5. Forum activity ----
df = pd.read_csv("data/raw/forum_activity.csv")
rows = list(df.itertuples(index=False, name=None))
cursor.executemany(
    "INSERT INTO forum_activity (student_id, questions, answers, comments) "
    "VALUES (:1, :2, :3, :4)", rows
)
print(f"forum_activity: {len(rows)} rows loaded")

# ---- 6. Offline events (needs a generated event_record_id) ----
df = pd.read_csv("data/raw/offline_events.csv")
df.insert(0, "event_record_id", range(1, len(df) + 1))
rows = list(df.itertuples(index=False, name=None))
cursor.executemany(
    "INSERT INTO offline_events (event_record_id, event_id, student_id, event_name, participation_type) "
    "VALUES (:1, :2, :3, :4, :5)", rows
)
print(f"offline_events: {len(rows)} rows loaded")

# ---- 7. Mentor meetings ----
df = pd.read_csv("data/raw/mentor_meetings.csv")
df["meeting_date"] = df["meeting_date"].apply(to_date)
rows = list(df.itertuples(index=False, name=None))
cursor.executemany(
    "INSERT INTO mentor_meetings (meeting_id, student_id, mentor_id, meeting_date, duration) "
    "VALUES (:1, :2, :3, :4, :5)", rows
)
print(f"mentor_meetings: {len(rows)} rows loaded")

conn.commit()
cursor.close()
conn.close()
print("\nAll data loaded and committed successfully!")