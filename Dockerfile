FROM python:3

WORKDIR /usr/src/app

ENV SECRET_KEY=5791628bb0b13ce0c676dfde280ba245

ENV HOST=localhost:5000

#Please paste the email and password of gmail with less secure apps access turned on
ENV EMAIL_USER=""

ENV EMAIL_PASS=""

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "db", "init"]

CMD ["python", "app.py"]