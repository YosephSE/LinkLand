from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import datetime

app = Flask(__name__)
app.secret_key = '50a4e988380c09d290acdab4bd53d24ee7b497df'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Yoseph'
app.config['MYSQL_PASSWORD'] = '1212'
app.config['MYSQL_DB'] = 'linkland'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'BGPHMS@gmail.com'
app.config['MAIL_PASSWORD'] = 'vjkcslwthvdgerod'

mysql = MySQL(app)
mail = Mail(app)

def send_email(subject, recipient_email, email_content):
    msg = Message(subject = subject,
                  recipients=[recipient_email],
                  sender=app.config.get("MAIL_USERNAME"))
    msg.body = email_content
    mail.send(msg)
@app.route("/ls")
def ls():
    return render_template("login.html")
@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        if password == user[2]:
            session['id'] = user[0]
            return redirect(url_for('home'))
        return "Account Not Found or Wrong Password"
    return "No"
        
@app.route('/signup', methods=["POST"])
def signup():
    if request.method == "POST":
        Fname = request.form["Fname"]
        Lname = request.form["Lname"]
        email = request.form["email"]
        password = request.form["password"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (Fname, Lname, email, password))
        mysql.connection.commit()
        cur0.close()
        session['id'] = 34
        return redirect(url_for('home'))

@app.route('/')
def home():
    if len(session.keys()) == 0:
        return redirect(url_for('ls'))
    cur = mysql.connection.cursor()
    cur.execute("select users.first_name, users.last_name, posts.publication_date, posts.title, posts.content, users.profile from users inner join posts on posts.user_id = users.id")
    posts = cur.fetchall()
    cur.close()
    return render_template('index.html', posts = posts)
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        now = datetime.datetime.now()
        year, month, date = now.strftime('%Y-%m-%d').split('-')
        month = int(month)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        time = now.strftime('%I:%M %p')
        time_str = f'{months[month - 1]} {date}, {year} {time}'
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO posts (title, content, publication_date) VALUES (%s, %s, %s)", (title, content, time_str))
        mysql.connection.commit()
        cur0.close()
        
        return redirect(url_for('post'))

    return render_template('post.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
