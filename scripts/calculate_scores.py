import pandas as pd
import oracledb
from sqlalchemy import create_engine

# Oracle Client
oracledb.init_oracle_client(
    lib_dir=r"C:\Users\AGATHA\Downloads\instantclient-basic-windows.x64-23.26.2.0.0\instantclient_23_0"
)

# Database Connection
engine = create_engine(
    "oracle+oracledb://student_analytics:Welcome123@localhost:1521/?service_name=XE"
)

# -------------------------
# Load Data from Oracle
# -------------------------

students = pd.read_sql(
    "SELECT student_id, name, department, batch, college FROM students",
    engine
)

logins = pd.read_sql("""
    SELECT student_id,
           COUNT(*) AS login_count
    FROM login_activity
    GROUP BY student_id
""", engine)

courses = pd.read_sql("""
    SELECT student_id,
           AVG(progress) AS avg_progress
    FROM course_progress
    GROUP BY student_id
""", engine)

webinars = pd.read_sql("""
    SELECT student_id,
           SUM(CASE WHEN attended='Yes' THEN 1 ELSE 0 END) AS webinar_attended,
           COUNT(*) AS total_webinars
    FROM webinar_attendance
    GROUP BY student_id
""", engine)

forum = pd.read_sql("""
    SELECT student_id,
           questions,
           answers,
           comments
    FROM forum_activity
""", engine)

events = pd.read_sql("""
    SELECT student_id,
           SUM(CASE WHEN participation_type='Attended' THEN 1 ELSE 0 END) AS offline_attended,
           COUNT(*) AS total_events
    FROM offline_events
    GROUP BY student_id
""", engine)

mentors = pd.read_sql("""
    SELECT student_id,
           COUNT(*) AS meeting_count
    FROM mentor_meetings
    GROUP BY student_id
""", engine)

# -------------------------
# Merge Data
# -------------------------

df = students.merge(logins, on="student_id", how="left")
df = df.merge(courses, on="student_id", how="left")
df = df.merge(webinars, on="student_id", how="left")
df = df.merge(forum, on="student_id", how="left")
df = df.merge(events, on="student_id", how="left")
df = df.merge(mentors, on="student_id", how="left")

df = df.fillna(0)

print("Columns in DataFrame:")
print(df.columns.tolist())

# -------------------------
# Calculate Scores
# -------------------------

df["login_score"] = (
    df["login_count"] / 40 * 20
).clip(upper=20)

df["course_score"] = (
    df["avg_progress"] / 100 * 25
)

df["webinar_score"] = (
    df["webinar_attended"] /
    df["total_webinars"].replace(0, 1) * 15
).clip(upper=15)

df["offline_score"] = (
    df["offline_attended"] /
    df["total_events"].replace(0, 1) * 20
).clip(upper=20)

df["forum_score"] = (
    df["questions"] * 0.3 +
    df["answers"] * 0.4 +
    df["comments"] * 0.2
).clip(upper=10)

df["mentor_score"] = (
    df["meeting_count"] / 5 * 10
).clip(upper=10)

# -------------------------
# Total Score
# -------------------------

df["activity_score"] = (
    df["login_score"] +
    df["course_score"] +
    df["webinar_score"] +
    df["offline_score"] +
    df["forum_score"] +
    df["mentor_score"]
).round(1).clip(upper=100)

# -------------------------
# Segmentation
# -------------------------

def segment(score):
    if score >= 80:
        return "Highly Active"
    elif score >= 50:
        return "Moderately Active"
    else:
        return "At Risk"

df["segment"] = df["activity_score"].apply(segment)

# -------------------------
# Final Output
# -------------------------

result = df[
    [
        "student_id",
        "name",
        "department",
        "batch",
        "login_score",
        "course_score",
        "webinar_score",
        "offline_score",
        "forum_score",
        "mentor_score",
        "activity_score",
        "segment"
    ]
]

# -------------------------
# Save CSV
# -------------------------

result.to_csv(
    "data/processed/activity_scores.csv",
    index=False
)

print(f"\nScored {len(result)} students.")

print("\nStudent Segments:")
print(result["segment"].value_counts())

print("\nTop 5 Students:")
print(
    result.sort_values(
        by="activity_score",
        ascending=False
    ).head(5)[
        ["student_id", "name", "activity_score", "segment"]
    ]
)

print("\nActivity scores saved to:")
print("data/processed/activity_scores.csv")
# -------------------------
# Save to Oracle Database
# -------------------------

result.to_sql(
    "activity_scores",
    engine,
    if_exists="append",
    index=False
)

print("\nData successfully inserted into Oracle table: ACTIVITY_SCORES")