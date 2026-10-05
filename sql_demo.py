import sqlite3

conn = sqlite3.connect("demo.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    credit REAL
)
""")

cur.execute("INSERT INTO course (name, credit) VALUES (?, ?)", ("高等数学", 4.5))
cur.execute("INSERT INTO course (name, credit) VALUES (?, ?)", ("线性代数", 3.0))
cur.execute("INSERT INTO course (name, credit) VALUES (?, ?)", ("大学物理", 4.0))

cur.execute("UPDATE course SET credit = ? WHERE name = ?", (5.0, "高等数学"))

cur.execute("DELETE FROM course WHERE name = ?", ("大学物理",))

cur.execute("SELECT id, name, credit FROM course")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.commit()
conn.close()
