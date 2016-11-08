
import time

import argparse
from adapters import BaseMetricsAdapter, PrometheusAdapter
from tools import generate_lag_all_topics, generate_kafka_client, TopicGroupPair

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

    metrics_adapter = BaseMetricsAdapter()
    if args.prometheus_enable:
        metrics_adapter = PrometheusAdapter(MONITOR_PORT)

    config = {
        'kafka_str': args.kafka_str,
        'topic_group_pairs': topic_group_list,
        'metrics_adapter': metrics_adapter
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

def main():
    """ Initialize the monitor and set lag for each topic """
    config_dict = bootstrap()
    metrics_adapter = config_dict['metrics_adapter']
    topic_group_list = config_dict['topic_group_pairs']
    sleep_duration = 10

    kafka_client = generate_kafka_client(config_dict['kafka_str'])
    while 1:
        get_lag(kafka_client, topic_group_list)
        metrics_adapter.update_metrics(topic_group_list)

        print 'Run complete, sleeping for %s seconds.' % sleep_duration
        time.sleep(sleep_duration)

if __name__ == '__main__':
    main()
