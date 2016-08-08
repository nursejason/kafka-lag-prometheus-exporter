
#import os
import sys # TODO
import time

import argparse
from prometheus_client import start_http_server, Gauge
from tools import generate_lag_all_topics, TopicGroupPair

MONITOR_PORT = 7110

def bootstrap():
    """ Turn on prometheus monitor """
    parser = argparse.ArgumentParser()
    parser.add_argument('--kafka', action='store', required=True,
                        dest='kafka_str', help='CSV kafka:port string')
    parser.add_argument('--prometheus', action='store_true',
                        dest='prometheus_enable', help='Enable Prometheus')
    parser.add_argument('topic_group_pairs', metavar='topic:group', type=str,
                        nargs='+', help='topic:group list separated by spaces')

    args = parser.parse_args()
    topic_group_list = generate_topic_group_pairs(args.topic_group_pairs)

    if args.prometheus_enable:
        start_http_server(MONITOR_PORT)

    config = {
        'kafka_str': args.kafka_str,
        'prometheus_enable': args.prometheus_enable,
        'topic_group_pairs': topic_group_list
    }
    print 'Config opts for Kafka-Ops monitor %s' % config
    return config

def generate_topic_group_pairs(topic_group_pairs):
    """ Splits topic:group into a list and generates a TopicGroupPair object """
    formatted_pairs = []
    for pair in topic_group_pairs:
        topic_group = pair.split(':')
        formatted_pairs.append(TopicGroupPair(topic_group[0], topic_group[1]))

    return formatted_pairs

def get_lag(kafka_str, topic_group_list):
    """ Get lag from imported function """
    generate_lag_all_topics(kafka_str, topic_group_list)

def set_lag_prometheus(topic_group_list, gauge):
    """ Loops through all topics and sets lags for prometheus metrics """
    for topic_group in topic_group_list:
        gauge.labels(topic_group.name, topic_group.group).set(topic_group.lag)

def main():
    """ Initialize the monitor and set lag for each topic """
    config_dict = bootstrap()
    gauge = None
    if config_dict['prometheus_enable']:
        gauge = Gauge(
            'kafka_topic_group_lag', 'topic group pair lag', ['topic', 'group'])
    topic_group_list = config_dict['topic_group_pairs']
    sleep_duration = 10

    while 1:
        get_lag(config_dict['kafka_str'], topic_group_list)

        print 'Kafka lag for this run.'
        for topic in topic_group_list:
            print topic.__dict__

        if config_dict['prometheus_enable']:
            set_lag_prometheus(topic_group_list, gauge)

        print 'Run complete, sleeping for %s seconds.' % sleep_duration
        time.sleep(sleep_duration)

if __name__ == '__main__':
    main()
