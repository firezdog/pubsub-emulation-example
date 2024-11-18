from typing import List
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.pubsub import ReadFromPubSub
import psycopg2 as pg
from psycopg2 import sql as pg_sql
from google.cloud import pubsub_v1
import config
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class WriteToPostgres(beam.DoFn):
    def __init__(self):
        # Database configuration
        self._db_config = {
            "host": config.DB_HOST,
            "dbname": config.POSTGRES_DB,
            "user": config.POSTGRES_USER,
            "password": config.POSTGRES_PASSWORD,
        }

    def setup(self):
        self.connection = pg.connect(
            host=config.DB_HOST,
            dbname=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
        )

    def teardown(self):
        self.connection.close()

    def process(self, element: List[str]):
        try:
            cursor = self.connection.cursor()
            query = pg_sql.SQL(
                'INSERT INTO messages (uuid, created_at) VALUES (%s, CURRENT_TIMESTAMP);'
            )
            cursor.execute(query, [element])
            self.connection.commit()
            cursor.close()
        except Exception as e:
            self.connection.rollback()
            LOGGER.error(f"Error writing to database: {e}")
            raise

        # avoid warning that no iterator was returned from DoFn
        return []


def run():
    # Define pipeline options
    pipeline_options = PipelineOptions(
        runner='DirectRunner',
        streaming=True,
    )

    subscription_path = pubsub_v1.PublisherClient.subscription_path(project=config.PROJECT_ID, subscription=config.SUBSCRIPTION)

    with beam.Pipeline(options=pipeline_options) as pipeline:
        LOGGER.info(f'starting pipeline -- reading from {subscription_path}')
        (
            pipeline
            | "Read from Pub/Sub" >> ReadFromPubSub(subscription=subscription_path)
            | "Decode" >> beam.Map(lambda message: message.decode('utf-8'))
            | "Write to Postgres" >> beam.ParDo(WriteToPostgres())
        )


if __name__ == "__main__":
    run()
