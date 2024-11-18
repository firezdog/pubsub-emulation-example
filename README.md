# What It Does
Example emulation of a GCP pubsub.  Consists of three components:

1. pubsub-emulator: actual fake pubsub
2. pubsub-users: pubsub clients
3. pubsub-db: an instance of alloydb

To make things interesting, a publisher publishes to the default topic every second; a beam job then listens for messages and writes them to the database.

# How To Run It
When you run docker-compose up, all containers are provisioned.  The clients container waits for the other containers, then runs the scripts to subscribe and publish.

Note that the database ports have been exposed (see the config and yaml files) -- you can hook up an external tool such as DBVisualizer to see updates to the database (test.messages).

# Is It Any Good?
No.
