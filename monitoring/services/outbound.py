from monitoring.models import Endpoint, CallResult
from backend.customs.outbounds import send


def call_endpoint(endpoint_id: int):
    endpoint = Endpoint.objects.get(id=endpoint_id)
    result = send(
        url=endpoint.base_url,
        method=dict(Endpoint.METHODS)[endpoint.method],
        good_status_code=endpoint.healthy_status_code,
        parameters=endpoint.query_params,
        headers=endpoint.headers,
        body=endpoint.body,
        convert_body_to_json=endpoint.convert_body_to_json,
    )
    CallResult.objects.create(
        endpoint = endpoint,
        status_code = result["code"],
        
    )
