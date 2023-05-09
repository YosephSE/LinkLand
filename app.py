from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = '50a4e988380c09d290acdab4bd53d24ee7b497df'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
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

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("select users.first_name, users.last_name, posts.post_time, posts.title, posts.content from users inner join posts on posts.user_id = users.id")
    posts = cur.fetchall()
    cur.close()
    return render_template('index.html', posts = posts)
@app.route('/post')
def post():
    
    return render_template('post.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
