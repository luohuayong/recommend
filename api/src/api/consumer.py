__author__ = 'Administrator'
from pykafka import KafkaClient


client = KafkaClient('192.168.1.168:9092')
topic = client.topics['kafkatopic']

consumer = topic.get_simple_consumer()
for message in consumer:
    if message is not None:
        print message.offset, message.value