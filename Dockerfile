################################################################################
# Based on CentOS                                                              #
################################################################################
FROM centos:latest

####################
#    Image Setup   #
####################
# Install retrying python lib
RUN pip install retrying==1.3.3

# Install Python Kafka lib and dependencies
RUN pip install pykafka==2.4.0

# Install Prometheus lib
RUN pip install prometheus_client==0.0.13

#####################
#   Logging Setup   #
#####################
VOLUME /var/log/kafka-lag-exporter

##################
#   Misc Setup   #
##################
EXPOSE 7110

##########################
#    Application Setup   #
##########################
# Copy lib folder inside the container
ADD /. /usr/local/kafka-lag-exporter

# Set the default directory where CMD will execute
WORKDIR /usr/local/kafka-lag-exporter/

# Set the default command to execute
ENTRYPOINT ["python2.7", "main.py"]
