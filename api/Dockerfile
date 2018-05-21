FROM python:3.6
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt | sudo apt-get install python-wand
CMD ["python", "test_Flask.py"]