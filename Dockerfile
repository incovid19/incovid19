FROM python:3.8-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /home/incovid19
COPY requirements_camelot.txt requirements.txt /home/incovid19/
RUN pip install -r requirements_camelot.txt
RUN pip install -r requirements.txt
COPY . /home/incovid19/
CMD ["sh", "./run.sh"]
