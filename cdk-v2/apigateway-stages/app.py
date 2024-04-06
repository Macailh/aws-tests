#!/usr/bin/env python3
import os

import aws_cdk as cdk

from apigateway_stages.apigateway_stages_stack import ApigatewayStagesStack


app = cdk.App()
ApigatewayStagesStack(app, "ApigatewayStagesStack")
app.synth()
