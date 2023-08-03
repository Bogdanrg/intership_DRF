import json
import logging
import time

from django.conf import settings
from kafka import KafkaConsumer

from promotions.services import PromotionService


class PromotionConsumer:
    action_handlers = {
        "rate_pull": PromotionService.promotion_pull,
        "rate_update": PromotionService.promotion_update,
        None: lambda: "Provide valid action",
    }

    def __init__(self) -> None:
        self.consumer = KafkaConsumer(
            settings.KAFKA_TOPIC_NAME, bootstrap_servers=[settings.BOOTSTRAP_SERVER]
        )

    def start_consuming(self) -> None:
        for retrie in range(10):
            if self.consumer.bootstrap_connected():
                logging.info("Connected to bootstrap server")
                while True:
                    for message in self.consumer:
                        consumed_message = json.loads(message)
                        event_type = consumed_message.get("action")
                        event_handler = self.action_handlers.get(event_type)
                        event_handler(consumed_message["result"])
            logging.info("Can't connect")
            time.sleep(5)
        logging.warning("Max retries are spent")
