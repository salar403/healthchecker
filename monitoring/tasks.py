from celery import shared_task
from time import time

from .models import Endpoint
from .services.outbound import call_endpoint


@shared_task(queue="outbound")
def call_async_endpoint(endpoint_id: int):
    call_endpoint(endpoint_id=endpoint_id)


@shared_task
def check_for_intervals():
    for endpoint in Endpoint.objects.filter(
        is_deleted=False, recall_at__lte=time.time()
    ):
        call_async_endpoint.apply_async(kwargs={"endpoint_id": endpoint.id})
