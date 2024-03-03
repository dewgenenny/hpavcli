FROM python:3.9
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD hpavcli.py /
ADD interface.py /
ADD model.py /
ADD mqtt_client.py /
CMD [ "python", "./hpavcli.py" ]