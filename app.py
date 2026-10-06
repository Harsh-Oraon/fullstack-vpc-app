from flask import Flask, request, render_template_string
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Guestbook</title></head>
<body style="font-family: sans-serif; max-width: 500px; margin: 40px auto;">
  <h1>Guestbook</h1>
  <form method="POST">
    <input type="text" name="name" placeholder="Your name" required>
    <button type="submit">Sign</button>
  </form>
  <ul>
    {% for entry in entries %}
      <li>{{ entry.name }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def guestbook():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                name = request.form.get('name')
                cursor.execute("INSERT INTO entries (name) VALUES (%s)", (name,))
                conn.commit()

            cursor.execute("SELECT name FROM entries ORDER BY id DESC")
            entries = cursor.fetchall()
    finally:
        conn.close()

    return render_template_string(PAGE_TEMPLATE, entries=entries)

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)