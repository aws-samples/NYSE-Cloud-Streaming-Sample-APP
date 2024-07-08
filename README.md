# NYSE Cloud Streaming sample consumer

This project helps customers to start consuming NYSE Cloud Streaming maket data in AWS.

## NYSE Cloud Streaming

[NYSE Cloud Streaming](https://www.nyse.com/data-products), is a data distribution platform that enables customers to access and consume real-time streaming exchange data quickly, in a developer-friendly format. With NYSE Cloud Streaming, customers gain access to market data with sub-hundreds of milliseconds latency in the cloud. They can also spin up an environment in AWS within minutes without the upfront cost and logistical hurdles of building out a physical infrastructure footprint. Besides easing challenges related to infrastructure, data is published via NYSE Cloud Streaming in a Kafka-compatible stream, allowing developers to integrate data more easily in a widely used format.

For more details check this [blog post](https://aws.amazon.com/blogs/industries/how-the-new-york-stock-exchange-built-its-real-time-market-data-platform-on-aws/).

## NYSE Cloud Streaming Sample APP

This project will build the necessary infra structure using [AWS CDK](https://aws.amazon.com/cdk/) and deploy a sample python script on an EC2 instance to consume the market data.

![Image]()

## Deploying Sample APP

### Prerequisites

1. NYSE Cloud Stream credentials.
2. NYSE Cloud Stream environment.
3. Have AWS CLI installed, to connect to your EC2 instance that will consume the market data. Click [here]() for how to install AWS CLI.

To get credentials and the right environment to use, reach out to NYSE via their [website](https://www.nyse.com/market-data/real-time#contact).

---
**NOTE**
Only after you provide your AWS account ID and get the credentials you will be able to connect to NYSE Cloud Stream

---


### Deployment Steps

1. Clone this repository in your local machine and install the requirements.

```
git clone https://github.com/aws-samples/NYSE-Cloud-Streaming-Sample-APP.git
cd NYSE-Cloud-Streaming-Sample-APP
pip install –r requirements.txt
```

2. Create a [key-pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html) that will be used in your EC2 Instance.

3. Change your configuration file to add:
    - NYSE Cloud Stream credentials
    - Your EC2 Instance Key Pair
    - Adjust Bootstrap brokers, Endpoint Service IDs, AZ IDs and Topics according to the environment that you choose to connect to.

```
vi nyse_cloud_stream_client/config.py
```

4. Set the below environment variables. Specify your AWS account ID below.

```
set CDK_DEFAULT_ACCOUNT={your_aws_account_id}
set CDK_DEFAULT_REGION=us-east-1
```

5. Bootstrap the environment
```
cdk bootstrap
```

6. Deploy the sample app
```
cdk deploy
```

After the code deploys, you should see an output that looks like

`NyseCloudStreamClientStack.InstanceID = i-0123456789abcedfg`

Take note of the instance id to connect to it.

### Starting the Kafka Client

1. Connect to your EC2 Instance. (Use the instance-id provided on the CDK Deployment output)
```
aws ec2-instance-connect ssh --instance-id i-0123456789abcedfg
```

2. Go to the client directory and activate your virtual environment
```
cd kafka-clients/
source .venv/bin/activate
```

3. Start the client
```
python3 nyse-consumer-proto.py 
```

Enjoy!

## Supporting links
