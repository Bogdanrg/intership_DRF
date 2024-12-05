from kafka import KafkaConsumer

consumer = KafkaConsumer("trading", bootstrap_servers=["kafka:29090"])

while True:
    for message in consumer:
        print(message)
