## Kafka-Ops
This script is based on the Kafka-Ops portion of Pykafka.

We use this to establish reporting for various metrics VIA the outlet of your choice.

Presently we are using this in Changelog with a prometheus adapter to send metrics to our prometheus server.

This can be run in Docker, using the Dockerfile, or just spun up from nohup.

#### Docker Run
```
docker run -d --label SERVICE_TAGS=monitor -p 7110:7110 7bab30428315 --prometheus --kafka IP1:Port,IP2:Port,...,IPn:Port Topic1:Group1 Topic2:Group1 Topic2:Group2
```
