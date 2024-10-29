from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from bs4 import BeautifulSoup


SENDER_MAIL = "niksich.ivan@yahoo.com"
RECIPIENT_MAIL = "niksich.ivan@gmail.com"
SUBJECT_MAIL = "Consulta de formulario Solar Energy"


class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Dirección de mail', validators=[DataRequired()])
    body = CKEditorField('Hola, quiero que me contacten para conocer más sobre el servicio de asesoria.', validators=[DataRequired()])
    submit = SubmitField(label="Enviar")


def send_mail(subject, mail_body, sender, recipient):
    with smtplib.SMTP("smtp.mail.yahoo.com", 587) as connection:
        connection.starttls()
        connection.login(user=sender, password="kcabeheuoqnejpaa")
        connection.sendmail(from_addr=sender, to_addrs=recipient, msg=f"Subject: {subject}\n\n{mail_body}")
        connection.close()
        print("Mail sent.")
        return None


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)


@app.route("/")  # defines the route of the page that runs de function below.
def home():
    return render_template("index.html")


@app.route('/service')
def service():
    return render_template('/service.html')


@app.route('/prices')
def prices():
    return render_template('/prices.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        with app.app_context():
            client_name = form.name.data
            client_mail = form.email.data
            client_message = form.body.data
            soup = BeautifulSoup(client_message, 'html.parser')
            client_message = soup.get_text()

            body = f"Nombre: {client_name}.\nEmail: {client_mail}.\nConsulta: {client_message}."
            # print(body)

            send_mail(subject="This is a test:", mail_body="Hello. Testing.", sender=SENDER_MAIL, recipient=RECIPIENT_MAIL)

            return redirect(url_for("home"))

    return render_template('/contact.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)

