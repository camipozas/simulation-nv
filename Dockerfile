FROM python:3.7

# copy requirements
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

ADD . .



ENTRYPOINT ["python"]
CMD ["main.py"]

