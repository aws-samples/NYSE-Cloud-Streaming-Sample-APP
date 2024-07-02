#!/usr/bin/env python3
import os
import aws_cdk as cdk

from nyse_cloud_stream_client.nyse_cloud_stream_client_stack import NyseCloudStreamClientStack

app = cdk.App()
NyseCloudStreamClientStack(app, "NyseCloudStreamClientStack", 
                           
    # env=cdk.Environment(region="us-east-1"), availabilityZones=["use1-az1", "use1-az2", "use1-az4"],
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
