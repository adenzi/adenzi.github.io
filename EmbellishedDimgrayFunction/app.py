from flask import Flask, render_template, request, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
import uuid  # Import the uuid module

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        age = request.form['age']
        school_branch = request.form['school_branch']
        known_chapters = request.form['known_chapters']

        # Generate a unique ID for the submission
        unique_id = str(uuid.uuid4())

        # Send email
        send_email(name, grade, age, school_branch, known_chapters, unique_id)

        # Write to file
        write_to_file(name, grade, age, school_branch, known_chapters, unique_id)

        return redirect(url_for('thank_you'))

    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return "شكرا لتقديمكم معنا"

def send_email(name, grade, age, school_branch, known_chapters, unique_id):
    user = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_PASSWORD')

    # Create the email content
    subject = 'تقديم جديد في مسابقة القرآن'
    body = ("مرحبا, هناك مشترك جديد في المسابقة\n"
            f"الرقم الفريد: {unique_id}\n"
            f"الاسم: {name}\n"
            f"الصف: {grade}\n"
            f"العمر: {age}\n"
            f"فرع المدرسة: {school_branch}\n"
            f"الاجزاء المحفوظه: {known_chapters}\n"
            "يرجي التسجيل")

    msg = MIMEText(body)
    msg['Subject'] = f"تقديم جديد في المسابقة {name}"
    msg['From'] = user
    msg['To'] = ", ".join([
        "adiscord91900130@gmail.com",
        "opuzum@gmail.com"
    ])

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(user, password)
            server.send_message(msg)
    except Exception as e:
        print(f"Error: {e}")

def write_to_file(name, grade, age, school_branch, known_chapters, unique_id):
    with open('in.txt', 'a', encoding='utf-8') as f:
        f.write(f"الرقم الفريد:\n {unique_id}\n")
        f.write(f"الاسم: {name}\n")
        f.write(f"الصف: {grade}\n")
        f.write(f"العمر: {age}\n")
        f.write(f"فرع المدرسة: {school_branch}\n")
        f.write(f"الاجزاء المحفوظه: {known_chapters}\n")
        f.write("-" * 30 + "\n")  # Separator for each entry

if __name__ == '__main__':
    app.run(debug=True)
