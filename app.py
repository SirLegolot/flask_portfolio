from flask import Flask, render_template, jsonify, send_from_directory, request, redirect
import sqlite3, time, json, http
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

# Sqlite helper functions.
def initDatabase():
    conn = createConnection()
    createTable(conn)
    conn.close()
    
def createConnection():
    conn = None
    try:
        conn = sqlite3.connect('comments.db')
    except FileNotFoundError:
        with open('comments.db', 'w') as fp:
            pass
        create_connection()
    except Error as e:
        print(e)
    return conn

def createTable(conn):
    sqlCreateCommentsTable = """ CREATE TABLE IF NOT EXISTS comments (
                                    timestamp integer PRIMARY KEY,
                                    username text NOT NULL,
                                    content text NOT NULL,
                                    date text NOT NULL
                                ); """
    c = conn.cursor()
    c.execute(sqlCreateCommentsTable)
    conn.commit()

def insertComment(conn, commentInputs):
    sqlInsertComment = """ INSERT INTO comments(timestamp, username, content, date)
                                VALUES(?,?,?,?)"""
    c = conn.cursor()
    c.execute(sqlInsertComment, commentInputs)
    conn.commit()

def retrieveComments(conn, numComments, sortOrder):
    sqlRetrieveComments = """ SELECT * FROM comments ORDER BY timestamp """
    if sortOrder == "descending":
        sqlRetrieveComments += "DESC"
    comments = []
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    count = 1
    for row in c.execute(sqlRetrieveComments):
        # numComments < 0 means that all comments will be displayed.
        # Otherwise, only display numComments many comments.
        if count > 0 and count > numComments:
            break
        comments.append({"username": row["username"],
                         "content": row["content"],
                         "date": row["date"]})
    return comments
    
def deleteComments(conn):
    sqlDeleteComments = """ DELETE FROM comments """
    c = conn.cursor()
    c.execute(sqlDeleteComments)
    conn.commit()

# All the html pages have routes that properly direct them.
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")
    
@app.route('/projects')
def projects():
    return render_template("projects.html")
    
@app.route('/photos')
def photos():
    return render_template("photos.html")
    
@app.route('/blog/snake')
def snake():
    return render_template("blogs/snake.html")
    
@app.route('/blog/hello')
def hello():
    return render_template("blogs/hello.html")
    
# Comment routes handle displaying and receiving comments.
@app.route('/data', methods=['GET', 'POST'])
def manageComments():
    if request.method == 'POST':
        # Get the user inputs from the form
        username = request.form.get('username')
        content = request.form.get('content')
        
        # Get current timestamp in milliseconds as well as
        # date.
        timestamp = int(round(time.time()*1000))
        now = datetime.now()
        date = now.strftime("%I:%M %p, %b %d, %Y")
        commentInputs = (timestamp, username, content, date)
        
        # Insert comment into database
        conn = createConnection()
        insertComment(conn, commentInputs)
        conn.close()
        return redirect("/blog")
    elif request.method == 'GET':
        # Return comments as a json object
        numComments = int(request.args.get("numComments"))
        sortOrder = request.args.get("sortOrder")
        conn = createConnection()
        comments = retrieveComments(conn, numComments, sortOrder)
        conn.close()
        return json.dumps(comments)
    
@app.route('/delete-data', methods=['POST'])
def delete():
    if request.method == 'POST':
        conn = createConnection()
        deleteComments(conn)
        conn.close()
        return http.HTTPStatus.NO_CONTENT

# Run the application.
if __name__ == "__main__":
    initDatabase()
    app.run()