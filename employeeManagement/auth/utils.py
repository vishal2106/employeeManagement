from flask import url_for, render_template
from flask_mail import Message
from employeeManagement import mail, celery


@celery.task
def send_mail_with_celery(content):
    msg = create_message(content)
    mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    content = {
        "subject": subject,
        "sender": "Employee Management <noreply@vishal-employee.herokuapp.com>",
        "recipients": [to],
        "template": template,
        "kwargs": kwargs
    }

    send_mail_with_celery.delay(content)


def create_message(content):
    msg = Message(
        content["subject"],
        sender=content["sender"],
        recipients=content["recipients"]
    )
    msg.body = render_template(content["template"] + ".txt", **content["kwargs"])
    msg.html = render_template(content["template"] + ".html", **content["kwargs"])

    return msg


def send_reset_email(user):
    send_mail(
        user.email,
        "Reset Password",
        "emails/auth/password_reset",
        username=user.username,
        password_reset_link=url_for(
            'auth.reset_token',
            token=user.get_reset_token(),
            _external=True
        )
    )
