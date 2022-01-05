FROM python:3.8-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /home/ops
COPY requirements_camelot.txt requirements.txt /home/ops/
RUN pip install -r requirements_camelot.txt
RUN pip install -r requirements.txt
COPY . /home/ops/
CMD tail -f /dev/null