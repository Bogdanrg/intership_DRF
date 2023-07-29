import os

import django

# flake8: noqa
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
import json

from dotenv import load_dotenv
from kafka import KafkaConsumer

from src.auto_orders.services import DistributiveAutoOrderService
from src.promotions.models import Promotion

load_dotenv()

consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC_NAME"), bootstrap_servers=[os.getenv("BOOTSTRAP_SERVER")]
)
print("Consumer's listening: ")

while True:
    for message in consumer:
        consumed_message = json.loads(message.value)
        print(consumed_message)
        if consumed_message.get("property", None) == "pull":
            for promotion in consumed_message["result"]:
                Promotion.objects.create(avatar="AWS", description="Desc", **promotion)
        else:
            promotions = Promotion.objects.all()
            for promotion_to_update in promotions:
                for promotion in consumed_message["result"]:
                    if promotion_to_update.name == promotion["name"]:
                        promotion_to_update.price = float(promotion["price"])
                        promotion_to_update.save()
                        DistributiveAutoOrderService.distribute(promotion_to_update)
