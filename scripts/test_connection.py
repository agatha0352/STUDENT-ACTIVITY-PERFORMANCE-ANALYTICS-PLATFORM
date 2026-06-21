import oracledb

oracledb.init_oracle_client(lib_dir=r"C:\Users\AGATHA\Downloads\instantclient-basic-windows.x64-23.26.2.0.0\instantclient_23_0")

conn = oracledb.connect(
    user="student_analytics",
    password="Welcome123",
    dsn="localhost:1521/XE"
)

print("Connected successfully!")

cursor = conn.cursor()
cursor.execute("SELECT 'Hello from Oracle' FROM dual")
print(cursor.fetchone())

conn.close()
