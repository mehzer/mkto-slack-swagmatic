FROM python:3
MAINTAINER Marc Holmes <marc.holmes@gmail.com>

#Copy the app
ADD app.py /

#Install dependencies
ADD requirements.txt /build/
RUN pip install -r /build/requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]