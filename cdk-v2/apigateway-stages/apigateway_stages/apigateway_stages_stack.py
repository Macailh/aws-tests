from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct

class ApigatewayStagesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define la función Lambda que será el backend de tu API
        my_lambda = _lambda.Function(
            self, 'MyLambda',
            code=_lambda.Code.from_asset('apigateway_stages/lambda_code'),
            handler='main.handler',
            runtime=_lambda.Runtime.PYTHON_3_10,
        )

        # Crea el API Gateway sin despliegue automático
        api = apigateway.LambdaRestApi(
            self, 'MyAPI',
            handler=my_lambda,
            proxy=False,
            deploy=False,  # Evita el despliegue automático
        )

        # Crea el primer despliegue para el stage 'dev'
        dev_deployment = apigateway.Deployment(
            self, 'DevDeployment',
            api=api,
            # Es opcional agregar una descripción a tus despliegues
            description='Deployment for the development stage',
        )

        # Crea el stage 'dev' utilizando el despliegue anterior
        dev_stage = apigateway.Stage(
            self, 'DevStage',
            deployment=dev_deployment,
            stage_name='dev',
        )

        # Opcionalmente, añade el recurso '/docs' específicamente para 'dev'
        docs = api.root.add_resource('docs')
        docs.add_method('GET')  # Define cómo manejarás las solicitudes GET a '/docs'

        # Crea el segundo despliegue para el stage 'prod'
        prod_deployment = apigateway.Deployment(
            self, 'ProdDeployment',
            api=api,
            description='Deployment for the production stage',
        )

        # Crea el stage 'prod' utilizando el despliegue anterior
        prod_stage = apigateway.Stage(
            self, 'ProdStage',
            deployment=prod_deployment,
            stage_name='prod',
        )

        # Asigna uno de los stages como predeterminado, si es necesario
        api.deployment_stage = dev_stage
