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
        api = apigateway.RestApi(
            self,
            "MyApi",
            rest_api_name="MyApi",
            description="My api gateway",
        )
        # Integración de Lambda para un endpoint específico
        get_integration = apigateway.LambdaIntegration(my_lambda)

        # Definir un recurso y método GET
        api_resource = api.root.add_resource("myresource")
        api_method = api_resource.add_method("GET", get_integration)

        # Crear una API Key
        api_key = api.add_api_key("ApiKey", api_key_name="MyApiKey")

        # Crear un plan de uso y asociar la API Key y el método
        usage_plan = api.add_usage_plan(
            "UsagePlan",
            name="MyUsagePlan",
            throttle=apigateway.ThrottleSettings(rate_limit=10, burst_limit=2),
        )

        # Asociar el plan de uso con la etapa de la API
        usage_plan.add_api_stage(
            stage=api.deployment_stage,
            throttle=[
                {"method": api_method, "throttle": {"rate_limit": 10, "burst_limit": 2}}
            ],
        )

        # Asociar la API Key con el plan de uso
        usage_plan.add_api_key(api_key)

        # Aquí es donde construimos la URL manualmente
        region = Aws.REGION
        api_id = api.rest_api_id
        stage = (
            "prod"  # Asume que usas el stage predeterminado que crea `LambdaRestApi`
        )

        api_url = f"https://{api_id}.execute-api.{region}.amazonaws.com/{stage}"
        my_lambda.add_environment("API_URL", api_url)
