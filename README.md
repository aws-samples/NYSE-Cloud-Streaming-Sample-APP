# NYSE Cloud Streaming sample consumer

This project helps customers to start consuming NYSE Cloud Streaming maket data in AWS.

## NYSE Cloud Streaming

[NYSE Cloud Streaming](https://www.nyse.com/data-products), is a data distribution platform that enables customers to access and consume real-time streaming exchange data quickly, in a developer-friendly format. With NYSE Cloud Streaming, customers gain access to market data with sub-hundreds of milliseconds latency in the cloud. They can also spin up an environment in AWS within minutes without the upfront cost and logistical hurdles of building out a physical infrastructure footprint. Besides easing challenges related to infrastructure, data is published via NYSE Cloud Streaming in a Kafka-compatible stream, allowing developers to integrate data more easily in a widely used format.

For more details check this [blog post](https://aws.amazon.com/blogs/industries/how-the-new-york-stock-exchange-built-its-real-time-market-data-platform-on-aws/).

## NYSE Cloud Streaming Sample APP

## Deploying Sample APP

### Prerequisites

### Deployment Steps


```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
