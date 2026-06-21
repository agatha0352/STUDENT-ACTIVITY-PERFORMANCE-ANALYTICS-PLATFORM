-- Check for orphaned records (shouldn't be any, since FKs would block them)
SELECT COUNT(*) AS total_students FROM students;
SELECT COUNT(*) AS total_logins FROM login_activity;

-- Check for nulls in key fields
SELECT COUNT(*) AS null_progress FROM course_progress WHERE progress IS NULL;

-- Check for duplicate logins (same student, same date+time)
SELECT student_id, login_date, login_time, COUNT(*)
FROM login_activity
GROUP BY student_id, login_date, login_time
HAVING COUNT(*) > 1;