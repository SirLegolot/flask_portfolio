from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3

app = Flask(__name__, static_url_path='/static')

# Set up sqlite database connections.
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
        pass
    else:
        pass
    
@app.route('/delete-data', methods=['GET'])
def deleteComments():
    pass

# Run the application.
if __name__ == "__main__":
    createConnection()
    app.run()