FROM python:3.8.9
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -e git+https://github.com/scaleoutsystems/fedn.git@develop#egg=fedn\&subdirectory=fedn
RUN pip install -r requirements.txt
