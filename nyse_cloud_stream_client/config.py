###
### Feed Information (Provided by NYSE)
###
feed_domain_name = "bqt.pulse.nyse"
bootstrap_brokers = ["broker1.bqt.pulse.nyse:9092","broker2.bqt.pulse.nyse:9092","broker3.bqt.pulse.nyse:9092"]
vpc_azs_ids=["use1-az1", "use1-az2", "use1-az4"]
endpoint_service_ids = ["com.amazonaws.vpce.us-east-1.vpce-svc-0aa21b8c29d33d773", "com.amazonaws.vpce.us-east-1.vpce-svc-0d93d7b236569b53f", "com.amazonaws.vpce.us-east-1.vpce-svc-0dacde25dc79ff380"]
CLOUDSTREAM_USERNAME="pulse_test_user"
CLOUDSTREAM_PASSWORD="RMg%C%ny6O"
CLOUDSTREAN_SASL_MECHANISM="SCRAM-SHA-256"

###
### Infrastructure configuration(DO NOT CHANGE)
###
EC2_KEY_PAIR="pulse-key"
vpc_cidr = "10.10.0.0/16"
vpc_azs = []

###
### Kafka Configuration
###
kafkaTopic="bqt_qte_str_2"
kafkaConsumerGroupId="bqt_qte_str_2_GRP"