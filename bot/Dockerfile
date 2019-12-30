# Frosh build
FROM python:3.8.0-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# For dev only
ENTRYPOINT ["tail", "-f", "/dev/null"]
#CMD [ "python" ]
# CMD [ "python", "./your-daemon-or-script.py" ]

