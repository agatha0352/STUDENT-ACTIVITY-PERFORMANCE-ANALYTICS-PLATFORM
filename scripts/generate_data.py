import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

NUM_STUDENTS = 150
START_DATE = datetime(2025, 8, 1)
END_DATE = datetime(2026, 6, 1)
DAYS_RANGE = (END_DATE - START_DATE).days

DEPARTMENTS = ["Computer Science", "Data Science", "Business", "Design", "Marketing"]
COLLEGES = ["Riverdale Institute", "Northgate College", "Summit University"]
BATCHES = ["2025-A", "2025-B", "2026-A"]
DEVICES = ["Mobile", "Laptop", "Desktop"]
COURSES = ["Python", "SQL", "Power BI", "Excel", "Machine Learning", "Statistics"]
WEBINARS = ["AI Workshop", "Data Science Bootcamp", "Career Readiness",
            "Resume Building", "Interview Prep", "Capstone Showcase"]
EVENTS = ["Hackathon", "Networking Mixer", "Guest Lecture", "Sports Day", "Orientation Day"]
MENTORS = [f"MT{100+i}" for i in range(10)]

def random_date():
    return START_DATE + timedelta(days=random.randint(0, DAYS_RANGE))

# ---- 1. Students (master data) ----
students = []
engagement_levels = {}  # hidden "true engagement" driving every other table
for i in range(NUM_STUDENTS):
    sid = f"ST{101+i}"
    engagement_levels[sid] = np.random.beta(2, 2)  # spread between 0 and 1
    students.append({
        "student_id": sid,
        "name": fake.name(),
        "college": random.choice(COLLEGES),
        "department": random.choice(DEPARTMENTS),
        "batch": random.choice(BATCHES),
        "enrollment_status": "Active" if random.random() > 0.05 else "Inactive"
    })
students_df = pd.DataFrame(students)

# ---- 2. Login activity ----
logins = []
login_id = 1
for sid, eng in engagement_levels.items():
    num_logins = max(0, int(np.random.poisson(eng * 45)))
    for _ in range(num_logins):
        d = random_date()
        logins.append({
            "login_id": login_id,
            "student_id": sid,
            "login_date": d.strftime("%Y-%m-%d"),
            "login_time": fake.time(pattern="%I:%M %p"),
            "device": random.choice(DEVICES),
            "session_duration": int(np.clip(np.random.normal(20 + eng * 30, 10), 5, 90))
        })
        login_id += 1
logins_df = pd.DataFrame(logins)

# ---- 3. Course progress ----
courses = []
course_id = 1
for sid, eng in engagement_levels.items():
    enrolled = random.sample(COURSES, k=random.randint(2, 4))
    for c in enrolled:
        progress = int(np.clip(np.random.normal(eng * 100, 15), 0, 100))
        courses.append({
            "course_id": f"CRS{course_id:04d}",
            "student_id": sid,
            "course_name": c,
            "progress": progress,
            "completed": "Yes" if progress >= 90 else "No"
        })
        course_id += 1
courses_df = pd.DataFrame(courses)

# ---- 4. Webinar attendance ----
webinars = []
for sid, eng in engagement_levels.items():
    for idx, w in enumerate(WEBINARS, start=1):
        attended = "Yes" if random.random() < eng else "No"
        webinars.append({
            "webinar_id": f"WB{idx:02d}",
            "student_id": sid,
            "webinar_name": w,
            "attended": attended
        })
webinars_df = pd.DataFrame(webinars)

# ---- 5. Forum activity ----
forum = []
for sid, eng in engagement_levels.items():
    forum.append({
        "student_id": sid,
        "questions": int(np.random.poisson(eng * 6)),
        "answers": int(np.random.poisson(eng * 9)),
        "comments": int(np.random.poisson(eng * 15))
    })
forum_df = pd.DataFrame(forum)

# ---- 6. Offline events ----
events = []
for sid, eng in engagement_levels.items():
    for idx, e in enumerate(EVENTS, start=1):
        participated = "Attended" if random.random() < eng * 0.8 else "Not Attended"
        events.append({
            "event_id": f"EV{idx:02d}",
            "student_id": sid,
            "event_name": e,
            "participation_type": participated
        })
events_df = pd.DataFrame(events)

# ---- 7. Mentor meetings ----
meetings = []
meeting_id = 1
for sid, eng in engagement_levels.items():
    num_meetings = int(np.random.poisson(eng * 5))
    for _ in range(num_meetings):
        meetings.append({
            "meeting_id": meeting_id,
            "student_id": sid,
            "mentor_id": random.choice(MENTORS),
            "meeting_date": random_date().strftime("%Y-%m-%d"),
            "duration": random.randint(15, 60)
        })
        meeting_id += 1
meetings_df = pd.DataFrame(meetings)

# ---- Save everything ----
students_df.to_csv("data/raw/students.csv", index=False)
logins_df.to_csv("data/raw/login_activity.csv", index=False)
courses_df.to_csv("data/raw/course_progress.csv", index=False)
webinars_df.to_csv("data/raw/webinar_attendance.csv", index=False)
forum_df.to_csv("data/raw/forum_activity.csv", index=False)
events_df.to_csv("data/raw/offline_events.csv", index=False)
meetings_df.to_csv("data/raw/mentor_meetings.csv", index=False)

print("Data generation complete!")
print(f"  students:            {len(students_df)} rows")
print(f"  login_activity:      {len(logins_df)} rows")
print(f"  course_progress:     {len(courses_df)} rows")
print(f"  webinar_attendance:  {len(webinars_df)} rows")
print(f"  forum_activity:      {len(forum_df)} rows")
print(f"  offline_events:      {len(events_df)} rows")
print(f"  mentor_meetings:     {len(meetings_df)} rows")