import paho.mqtt.client as mqtt

def publish_message(server, username, password, topic, message):
    client = mqtt.Client()
    client.username_pw_set(username=username, password=password)
    client.connect(server, 1883, 60 )
    client.publish(topic, message)
    client.disconnect()