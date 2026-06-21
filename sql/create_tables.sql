CREATE TABLE students (
    student_id          VARCHAR2(10)  PRIMARY KEY,
    name                VARCHAR2(100),
    college             VARCHAR2(100),
    department          VARCHAR2(50),
    batch               VARCHAR2(20),
    enrollment_status   VARCHAR2(20)
);

CREATE TABLE login_activity (
    login_id            NUMBER        PRIMARY KEY,
    student_id          VARCHAR2(10)  REFERENCES students(student_id),
    login_date          DATE,
    login_time          VARCHAR2(20),
    device              VARCHAR2(20),
    session_duration    NUMBER
);

CREATE TABLE course_progress (
    course_id           VARCHAR2(10)  PRIMARY KEY,
    student_id          VARCHAR2(10)  REFERENCES students(student_id),
    course_name         VARCHAR2(50),
    progress            NUMBER,
    completed           VARCHAR2(5)
);

CREATE TABLE webinar_attendance (
    attendance_id       NUMBER        PRIMARY KEY,
    webinar_id          VARCHAR2(10),
    student_id          VARCHAR2(10)  REFERENCES students(student_id),
    webinar_name        VARCHAR2(100),
    attended             VARCHAR2(5)
);

CREATE TABLE forum_activity (
    student_id          VARCHAR2(10)  PRIMARY KEY REFERENCES students(student_id),
    questions           NUMBER,
    answers              NUMBER,
    comments             NUMBER
);

CREATE TABLE offline_events (
    event_record_id     NUMBER        PRIMARY KEY,
    event_id             VARCHAR2(10),
    student_id          VARCHAR2(10)  REFERENCES students(student_id),
    event_name          VARCHAR2(100),
    participation_type  VARCHAR2(20)
);

CREATE TABLE mentor_meetings (
    meeting_id           NUMBER        PRIMARY KEY,
    student_id          VARCHAR2(10)  REFERENCES students(student_id),
    mentor_id            VARCHAR2(10),
    meeting_date         DATE,
    duration              NUMBER
);