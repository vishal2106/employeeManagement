FROM python:3
WORKDIR /usr/src/app
ENV SECRET_KEY=5791628bb0b13ce0c676dfde280ba245
ENV HOST=localhost:5000
ENV EMAIL_USER=ssdcapitalfund@gmail.com
ENV EMAIL_PASS=SSDCapital2412
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "db", "init"]
CMD ["python", "app.py"]