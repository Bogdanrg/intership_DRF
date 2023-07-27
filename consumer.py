import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
import json

from dotenv import load_dotenv
from kafka import KafkaConsumer

from src.promotions.models import Promotion

load_dotenv()

consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC_NAME"), bootstrap_servers=[os.getenv("BOOTSTRAP_SERVER")]
)
print("Consumer's listening: ")

while True:
    for message in consumer:
        consumed_message = json.loads(message.value)
        if consumed_message["property"] == "pull":
            for promotion in consumed_message["result"]:
                Promotion.objects.create(avatar="AWS", description="Desc", **promotion)
