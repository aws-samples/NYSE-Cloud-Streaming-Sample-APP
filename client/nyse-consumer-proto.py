from kafka import KafkaConsumer
import os
import BQT_Cloud_Streaming_pb2 as BQT

#Import Bootstrap server from environment variable
brokers = os.environ.get('BROKERS')
group_id = os.environ.get("KAFKA_GROUP_ID")

#Create Consumer
consumer = KafkaConsumer(
    'bqt_qte_str_1','bqt_qte_str_2','bqt_qte_str_3','bqt_qte_str_4','bqt_trd_str_1', #topics to consume
    group_id=group_id, #local consumer name
    bootstrap_servers=brokers, #Brokers List
    api_version=(3,5,1),
    # For mTLS auth:
    security_protocol='SASL_PAINTEXT',
    ssl_check_hostname=True,
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username=os.environ.get("KAFKA_SASL_USERNAME"),
    sasl_plain_password=os.environ.get("KAFKA_SASL_PASSWORD"),
)

print("Starting Kafka Consumer with brokers at ", brokers)

bqt_message = BQT.BQTMessage()

# Loop to consume messages and Print details.
for message in consumer:
    bqt_message.ParseFromString(message.value)
    print(bqt_message)
