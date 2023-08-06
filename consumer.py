import json
import logging
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.conf import settings
from kafka import KafkaConsumer

from src.promotions.services import PromotionService


class PromotionConsumer:
    action_handlers = {
        "rate_pull": PromotionService.promotion_pull,
        "rate_update": PromotionService.promotion_update,
        "no_action": lambda: "Provide valid action",
    }

    def __init__(self) -> None:
        self.consumer = KafkaConsumer(
            settings.KAFKA_TOPIC_NAME, bootstrap_servers=[settings.BOOTSTRAP_SERVER]
        )

    def start_consuming(self) -> None:
        logging.info("Connected to bootstrap server")
        while True:
            for message in self.consumer:
                consumed_message = json.loads(message.value)
                logging.info(consumed_message)
                event_type = consumed_message.get("action", "no_action")
                event_handler = self.action_handlers.get(event_type)
                if callable(event_handler):
                    event_handler(consumed_message["result"])


if __name__ == "__main__":
    consumer = PromotionConsumer()
    consumer.start_consuming()
