from flask_mail import Message
from employeeManagement import mail
from flask import render_template, url_for


def send_mail(to, subject, template, **kwargs):
    content = {
        "subject": subject,
        "sender": "Employee Management<noreply@vishal-employee.herokuapp.com>",
        "recipients": [to],
        "template": template,
        "kwargs": kwargs
    }

    msg = create_message(content)
    mail.send(msg)


def create_message(content):
    msg = Message(
        content["subject"],
        sender=content["sender"],
        recipients=content["recipients"]
    )
    msg.body = render_template(content["template"] + ".txt", **content["kwargs"])
    msg.html = render_template(content["template"] + ".html", **content["kwargs"])

    return msg


def send_password_reset_mail(user):
    send_mail(
        user.email,
        "Reset Password",
        "emails/auth/password_reset",
        username=user.username,
        password_reset_link=url_for(
            "auth.update_password",
            token=user.reset_token,
            email=user.email,
            _external=True
        )
    )
