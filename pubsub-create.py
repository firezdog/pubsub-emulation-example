import logging

from config import PROJECT_ID, TOPIC, SUBSCRIPTION

from google.cloud import pubsub_v1


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC)
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION)

    try:
        publisher.create_topic(request={'name': topic_path})
        LOGGER.info(f'topic created: {topic_path}')
    except Exception as e:
        LOGGER.info(f'topic creation failed (might already exist): {e}')

    # Create Subscription
    try:
        subscriber.create_subscription(
            request={
                'name': subscription_path,
                'topic': topic_path,
            }
        )
        LOGGER.info(f'subscription created: {subscription_path}')
    except Exception as e:
        LOGGER.info(f'subscription creation failed (might already exist): {e}')


if __name__ == '__main__':
    main()
