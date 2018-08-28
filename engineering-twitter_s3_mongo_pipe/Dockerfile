FROM python
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY credentials.json .
COPY main.py .
COPY mongo.py .
COPY s3.py .
COPY twitter_funcs.py .
COPY utility.py .
ENTRYPOINT ["python", "-m", "main"]
