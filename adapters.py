""" Adapters for various dependency injection functions """

from prometheus_client import start_http_server, Gauge

class BaseMetricsAdapter(object):
    """ Acts as a naked object, does nothing, doesn't report metrics """
    def __init__(self):
        pass

    @staticmethod
    def update_metrics(topic_group_list):
        """ Nothing to update, passes through """
        print 'Kafka Lag for this run.'
        for topic_group in topic_group_list:
            BaseMetricsAdapter.update_topic_group_lag(
                topic_group.name, topic_group.group, topic_group.lag)

    @staticmethod
    def update_topic_group_lag(topic, group, lag):
        print 'Topic:Group pair (%s:%s) Lag = %s' % (topic, group, lag)

class PrometheusAdapter(object):
    """ Instantiates necessary prometheus objects to update metrics """
    def __init__(self, monitor_port):
        start_http_server(monitor_port)
        self.gauge = Gauge('kafka_topic_group_lag', 'topic group pair lag',
                           ['topic', 'group'])

    def update_metrics(self, topic_group_list):
        """ Updates Gauge and prints to console """
        for topic_group in topic_group_list:
            self.gauge.labels(
                topic_group.name, topic_group.group).set(topic_group.lag)
            BaseMetricsAdapter.update_topic_group_lag(
                topic_group.name, topic_group.group, topic_group.lag)
