# -*- coding:utf-8 -*-
from pykafka import KafkaClient
import json
import threading
from config import cf
from api.serializers import DataSearchSerializer, DataBrowseSerializer

# 另起一个守护线程跑consumer
class ConsumerBak(threading.Thread):
    def run(self):
        balanced_consumer = topic.get_balanced_consumer(
            consumer_group='kafka-prd-group',
            auto_commit_enable=True,
            zookeeper_connect=cf.get("kafka", "zookeeperurl")
        )
        # consumer = topic.get_simple_consumer()
        for message in balanced_consumer:
            if message is not None:
                # print message.offset, message.value
                data = json.loads(message.value)
                if data['method'] == 'search':
                    serializer = DataSearchSerializer(data=data)
                elif data['method'] == 'browse':
                    serializer = DataBrowseSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()


client = KafkaClient(cf.get("kafka", "kafkaurl"))
# print client.topics
topic = client.topics['kafka-prd-user']
producer = topic.get_producer()

consumer = ConsumerBak()
consumer.start()

def produce(message):
    producer.produce(message)


