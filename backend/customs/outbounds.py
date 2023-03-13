import requests, json, time
from backend.customs.exceptions import FailedRequestException


def send(
    url: str,
    method: str,
    good_status_code: int = 200,
    parameters: dict = None,
    headers: str = None,
    body: dict = None,
    convert_body_to_json: bool = False,
    parse_to_json: bool = True,
    auth: tuple = None,
    verify: bool = True,
    proxies: dict = None,
    raise_if_fail: bool = False,
):
    starting_time = int(time.time() * 1000)
    try:
        if convert_body_to_json:
            body = json.dumps(body)
        response = requests.request(
            method=method,
            url=url,
            params=parameters,
            headers=headers,
            auth=auth,
            data=body,
            verify=verify,
            proxies=proxies,
        )
    except Exception as error:
        ending_time = int(time.time() * 1000)
        elapsed_time = ending_time - starting_time
        status = False
        final = str(error)
        code = 0
    else:
        elapsed_time = int(response.elapsed.microseconds / 1000)
        if response.status_code == good_status_code:
            code = good_status_code
            status = True
            if parse_to_json:
                final = response.json()
            else:
                final = response.text
        else:
            status = False
            code = response.status_code
            final = response.text
    if raise_if_fail and not status:
        raise FailedRequestException(detail=final)
    return {"success": status, "response": final, "code": code, "elapsed": elapsed_time}
