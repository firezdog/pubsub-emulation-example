import logging
import uuid
import time

from config import PROJECT_ID, TOPIC

from google.cloud import pubsub_v1


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC)

    while True:
        try:
            message = str(uuid.uuid1()).encode('utf-8')
            publisher.publish(topic_path, message).result()
            LOGGER.info('message published')
            time.sleep(1)
        except KeyboardInterrupt:
            LOGGER.info('shutting down -- goodbye')
            break


if __name__ == '__main__':
    main()
