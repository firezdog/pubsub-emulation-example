import os


PROJECT_ID = os.getenv('PUBSUB_PROJECT_ID')
DB_HOST = os.getenv("DB_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


TOPIC = 'test-topic'
SUBSCRIPTION = 'test-subscription'
