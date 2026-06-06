import sqlite3

conn = sqlite3.connect('internship.db')
cursor = conn.cursor()

# Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'student'
)
""")

# Admin table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Applications table
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    internship_title TEXT,
    company TEXT,
    status TEXT DEFAULT 'Applied',
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

cursor.execute("""
INSERT OR IGNORE INTO admins (email,password)
VALUES ('testadmin@email.com','admin123')
""")


conn.commit()
conn.close()

print("Database initialized successfully!")