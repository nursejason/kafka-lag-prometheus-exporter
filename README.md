## Kafka-Ops
This script is based on the Kafka-Ops portion of Pykafka.

We use this to establish reporting for various metrics VIA the outlet of your choice.

Presently we are using this in Changelog with a prometheus adapter to send metrics to our prometheus server.

This can be run in Docker, using the Dockerfile, or just spun up from nohup.

#### Docker Run
```docker
docker run -d --label SERVICE_TAGS=monitor -p 7110:7110 7bab30428315 --prometheus --kafka 96.119.241.163:6667,96.119.242.125:6667,96.119.244.3:6667 events_1:grp_event_1 logs_1:grp_log_1 ingest_failed_events:ingest_error_processor_01
```
