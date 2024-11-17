import logging

import config

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message
import psycopg2 as pg
from psycopg2 import sql as pg_sql

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def callback(message: Message):
    LOGGER.info('received message')

    DB_CONFIG = {
        "host": config.DB_HOST,
        "dbname": config.POSTGRES_DB,
        "user": config.POSTGRES_USER,
        "password": config.POSTGRES_PASSWORD,
    }
    connection = pg.connect(**DB_CONFIG)
    cursor = connection.cursor()
    query = pg_sql.SQL(
        'INSERT INTO'
        '   messages (uuid, created_at)'
        '   VALUES (%s, CURRENT_TIMESTAMP);'
    )
    cursor.execute(query, [message.data.decode('utf-8')])
    connection.commit()
    cursor.close()
    connection.close()

    message.ack()


def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(config.PROJECT_ID, config.SUBSCRIPTION)

    # Subscribe and listen for messages
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    LOGGER.info(f'listening for messages on {subscription_path}')

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        print('shutting down -- goodbye')


if __name__ == '__main__':
    main()
