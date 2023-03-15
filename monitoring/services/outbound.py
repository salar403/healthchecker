import time
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
    call_result = {
        "endpoint_id": endpoint.id,
        "response_time_ms": result["elapsed"],
        "status_code": result["code"],
    }
    if result["error"]:
        call_result["error"] = result["response"]
        call_result["healthy"] = False
        call_result["state"] = CallResult.ERROR
    else:
        call_result["state"] = CallResult.SUCCESS
        call_result["result_json"] = result["response"]
        call_result["healthy"] = result["success"]
        if not call_result["healthy"]:
            if result["timed_out"]:
                call_result["state"] = CallResult.TIMEOUT
            else:
                call_result["state"] = CallResult.INVALID_STATUS
    CallResult.objects.create(**call_result)
    endpoint.recall_at = int(time.time() + endpoint.check_interval)
    endpoint.save()
