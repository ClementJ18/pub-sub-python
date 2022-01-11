FROM python:3.8.12-bullseye
WORKDIR /geo
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN python -m unittest tests/tests.py
CMD ["python", "geo/worker.py"]