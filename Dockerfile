FROM python:3.9-slim-bullseye
WORKDIR /app
#ENV APP_PATH=services/worker
COPY . .
#RUN pip install -r $APP_PATH/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
#CMD ["python3", "-m", "$APP_PATH/app.py"]
CMD ["python3", "-m", "app.py"]