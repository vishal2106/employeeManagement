FROM python:3
COPY . /app
WORKDIR /app
ENV SECRET_KEY=5791628bb0b13ce0c676dfde280ba245
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "db", "init"]
CMD ["python", "app.py"]