FROM python:3.12-slim
COPY app.py requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8000"]