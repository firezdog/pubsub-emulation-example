python -m pubsub-create;
# will publish a message every second and push to db
python -m pubsub-read-beam & python -m pubsub-publish;
