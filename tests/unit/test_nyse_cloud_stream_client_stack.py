import aws_cdk as core
import aws_cdk.assertions as assertions

from nyse_cloud_stream_client.nyse_cloud_stream_client_stack import NyseCloudStreamClientStack

# example tests. To run these tests, uncomment this file along with the example
# resource in nyse_cloud_stream_client/nyse_cloud_stream_client_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = NyseCloudStreamClientStack(app, "nyse-cloud-stream-client")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
