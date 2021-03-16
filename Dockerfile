FROM python:3
COPY . /app
WORKDIR /app
ENV SECRET_KEY=5791628bb0b13ce0c676dfde280ba245
ENV HOST=vishal-employee.herokuapp.com
RUN pip install -r requirements.txt
CMD ["flask", "db", "init"]
CMD ["python", "app.py"]