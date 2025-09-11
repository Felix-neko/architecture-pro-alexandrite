FROM python:3.12-slim
COPY app.py requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 8002
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8002"]