from aws_cdk import Aws, Stack, aws_lambda as _lambda, aws_apigateway as apigateway
from constructs import Construct


class ApigatewayStagesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define la función Lambda que será el backend de tu API
        my_lambda = _lambda.Function(
            self,
            "MyLambda",
            code=_lambda.Code.from_asset("apigateway_stages/lambda_code"),
            handler="main.handler",
            runtime=_lambda.Runtime.PYTHON_3_10,
        )

        # Crea el API Gateway sin despliegue automático
        api = apigateway.LambdaRestApi(
            self,
            "MyAPI",
            handler=my_lambda,
            proxy=False,
            deploy=False,  # Evita el despliegue automático
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,  # Permite todos los orígenes
                allow_methods=apigateway.Cors.ALL_METHODS,  # Permite todos los métodos
                allow_headers=[
                    "Content-Type",
                    "X-Amz-Date",
                    "Authorization",
                    "X-Api-Key",
                ],  # Especifica las cabeceras permitidas
            ),
        )

        # Crea el primer despliegue para el stage 'dev'
        dev_deployment = apigateway.Deployment(
            self,
            "DevDeployment",
            api=api,
            # Es opcional agregar una descripción a tus despliegues
            description="Deployment for the development stage",
        )

        # Crea el stage 'dev' utilizando el despliegue anterior
        dev_stage = apigateway.Stage(
            self,
            "DevStage",
            deployment=dev_deployment,
            stage_name="dev",
        )

        # Opcionalmente, añade el recurso '/docs' específicamente para 'dev'
        api.root.add_method("GET")
        # docs = api.root.add_resource('docs')
        # docs.add_method('GET')  # Define cómo manejarás las solicitudes GET a '/docs'

        # Crea el segundo despliegue para el stage 'prod'
        prod_deployment = apigateway.Deployment(
            self,
            "ProdDeployment",
            api=api,
            description="Deployment for the production stage",
        )

        # Crea el stage 'prod' utilizando el despliegue anterior
        prod_stage = apigateway.Stage(
            self,
            "ProdStage",
            deployment=prod_deployment,
            stage_name="prod",
        )

        # Asigna uno de los stages como predeterminado, si es necesario
        # api.deployment_stage = dev_stage

        # Aquí es donde construimos la URL manualmente
        region = Aws.REGION
        api_id = api.rest_api_id
        stage = (
            "prod"  # Asume que usas el stage predeterminado que crea `LambdaRestApi`
        )

        api_url = f"https://{api_id}.execute-api.{region}.amazonaws.com/{stage}"
        my_lambda.add_environment("API_URL", api_url)
