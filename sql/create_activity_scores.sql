CREATE TABLE activity_scores (
    student_id      VARCHAR2(20),
    name            VARCHAR2(100),
    department      VARCHAR2(100),
    batch           VARCHAR2(20),
    login_score     NUMBER(5,2),
    course_score    NUMBER(5,2),
    webinar_score   NUMBER(5,2),
    offline_score   NUMBER(5,2),
    forum_score     NUMBER(5,2),
    mentor_score    NUMBER(5,2),
    activity_score  NUMBER(5,2),
    segment         VARCHAR2(30)
);