import aws_cdk as core
import aws_cdk.assertions as assertions

from apigateway_stages.apigateway_stages_stack import ApigatewayStagesStack

# example tests. To run these tests, uncomment this file along with the example
# resource in apigateway_stages/apigateway_stages_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ApigatewayStagesStack(app, "apigateway-stages")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
