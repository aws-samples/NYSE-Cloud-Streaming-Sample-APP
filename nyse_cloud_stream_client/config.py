###
### Feed Information (Provided by NYSE)
### Below information was extracted from the Load Test Environment - https://www.nyse.com/publicdocs/nyse/data/NYSE_BQT_Cloud_Streaming_Client_Specification.pdf
###
feed_domain_name = "bqt.pulse.nyse"
bootstrap_brokers = ["broker1.bqt.pulse.nyse:9092","broker2.bqt.pulse.nyse:9092","broker3.bqt.pulse.nyse:9092"]
vpc_azs_ids=["use1-az1", "use1-az2", "use1-az4"]
endpoint_service_ids = ["com.amazonaws.vpce.us-east-1.vpce-svc-0aa21b8c29d33d773", "com.amazonaws.vpce.us-east-1.vpce-svc-0d93d7b236569b53f", "com.amazonaws.vpce.us-east-1.vpce-svc-0dacde25dc79ff380"]
cloudstream_group_id="bqt_qte_str_1_GRP"
cloudstream_topics=["bqt_trd_str_1","bqt_qte_str_1","bqt_qte_str_2","bqt_qte_str_3","bqt_qte_str_4"]
cloudstream_username=""
cloudstream_password=""

###
### Infrastructure configuration
###
ec2_key_pair=""
vpc_cidr = "10.10.0.0/16"