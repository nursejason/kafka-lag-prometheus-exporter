################################################################################
# Dockerfile to build Image for a Kafka Tools Ops API                          #
# Based on CentOS                                                              #
################################################################################
FROM docker.comcast.net/aaa/aaa_base:2.3
MAINTAINER AAA

####################
#    Image Setup   #
####################
# Install Python Kafka lib and dependencies
RUN pip install pykafka==2.4.0

# Install Prometheus lib
RUN pip install prometheus_client==0.0.13

#####################
#   Logging Setup   #
#####################
VOLUME /var/log/AAA

##################
#   Misc Setup   #
##################

# Expose Web port
EXPOSE 7110

##########################
#    Application Setup   #
##########################
# Copy lib folder inside the container
ADD /. /usr/local/kafka-ops/

# Set the default directory where CMD will execute
WORKDIR /usr/local/kafka-ops/

# Set the default command to execute
ENTRYPOINT ["python2.7", "api.py"]
