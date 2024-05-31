FROM python:3.10
ENV PYTHONUNBUFFERED=1

WORKDIR /wdir

RUN mkdir -p /wdir/database
RUN pip install --upgrade pip

COPY requirements.txt /wdir/
COPY static/ /wdir/static/

RUN pip install -r ./requirements.txt

CMD ["python", "/wdir/src/startup.py"]