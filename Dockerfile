FROM python:3.9
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD hpavcli.py /
ADD interface.py /
ADD model.py /
ADD mqtt_client.py /
ADD venvtools.py /
CMD exec python ./hpavcli.py --mqtt_server $MQTT_SERVER --mqtt_topic $MQTT_TOPIC --mqtt_user $MQTT_USER --mqtt_password $MQTT_PASSWORD --mqtt_topic $MQTT_TOPIC networks
