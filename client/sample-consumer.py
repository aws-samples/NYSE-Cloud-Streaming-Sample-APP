from kafka import KafkaConsumer
import json,os

#Import Bootstrap server from environment variable
brokers = os.environ.get('BOOTSTRAP_SERVERS')
    
#Create Consumer
consumer = KafkaConsumer(
    'topic1', #topic to consume
    group_id='consumer_python', #local consumer name
    bootstrap_servers=brokers, #Brokers List
    api_version=(3,5,1),
    # For mTLS auth:
    security_protocol='SASL_SSL',
    ssl_check_hostname=True,
    sasl_mechanism=os.environ.get("KAFKA_SASL_MECHANISM"),
    sasl_plain_username=os.environ.get("KAFKA_SASL_USERNAME"),
    sasl_plain_password=os.environ.get("KAFKA_SASL_PASSWORD"),
)

# Loop to consume messages and Print details.
for message in consumer:
    print ("%s:%d:%d: value=%s" % (message.topic, message.partition,message.offset,message.value))
    try: 
        print(json.loads(message.value))
    except:
        print(message.value.decode('utf-8'))
