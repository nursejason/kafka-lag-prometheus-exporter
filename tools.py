""" Helper functions to communicate with Kafka """
import calendar
import datetime as dt

import pykafka

def _create_client(kafka_str):
    return pykafka.KafkaClient(hosts=kafka_str)

def generate_lag_all_topics(kafka_str, topics_group_list):
    """ Call helper function by establishing a client and kafka objects """
    client = _create_client(kafka_str)
    for topic_group in topics_group_list:
        kafka_topic = client.topics[topic_group.name]
        lag_dict = _fetch_consumer_lag(client, kafka_topic, topic_group.group)
        lag = 0
        for _, offset_tuple in lag_dict.iteritems():
            published_offset, consumed_offset = offset_tuple
            lag += published_offset - consumed_offset

        topic_group.lag = lag

def _fetch_offsets(client, topic, offset):
    """Fetch raw offset data from a topic.
    :param client: KafkaClient connected to the cluster.
    :type client:  :class:`pykafka.KafkaClient`
    :param topic:  Name of the topic.
    :type topic:  :class:`pykafka.topic.Topic`
    :param offset: Offset to reset to. Can be earliest, latest or a datetime.
        Using a datetime will reset the offset to the latest message published
        *before* the datetime.
    :type offset: :class:`pykafka.common.OffsetType` or
        :class:`datetime.datetime`
    :returns: {partition_id: :class:`pykafka.protocol.OffsetPartitionResponse`}
    """
    if offset.lower() == 'earliest':
        return topic.earliest_available_offsets()
    elif offset.lower() == 'latest':
        return topic.latest_available_offsets()
    else:
        offset = dt.datetime.strptime(offset, "%Y-%m-%dT%H:%M:%S")
        offset = int(calendar.timegm(offset.utctimetuple())*1000)
        return topic.fetch_offset_limits(offset)


def _fetch_consumer_lag(client, topic, consumer_group):
    """Get raw lag data for a topic/consumer group.
    :param client: KafkaClient connected to the cluster.
    :type client:  :class:`pykafka.KafkaClient`
    :param topic:  Name of the topic.
    :type topic:  :class:`pykafka.topic.Topic`
    :param consumer_group: Name of the consumer group to fetch lag for.
    :type consumer_groups: :class:`str`
    :returns: dict of {partition_id: (latest_offset, consumer_offset)}
    """
    latest_offsets = _fetch_offsets(client, topic, 'latest')
    consumer = topic.get_simple_consumer(consumer_group=consumer_group,
                                         auto_start=False)
    current_offsets = consumer.fetch_offsets()
    return {p_id: (latest_offsets[p_id].offset[0], res.offset)
            for p_id, res in current_offsets}

class TopicGroupPair(object):
    def __init__(self, name_str, group_str, gauge=None):
        self.name = name_str
        self.group = group_str
        self.gauge = gauge
        self.lag = None
