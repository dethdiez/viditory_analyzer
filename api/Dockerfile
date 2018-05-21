FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt | sudo apt-get install python-wand
CMD ["python", "test_Flask.py"]