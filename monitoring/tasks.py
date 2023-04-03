from celery import shared_task
import time

from .models import Endpoint
from .services.outbound import call_endpoint


@shared_task(queue="outbound")
def call_endpoint_task(endpoint_id: int):
    call_endpoint(endpoint_id=endpoint_id)


@shared_task
def check_for_intervals():
    for endpoint in Endpoint.objects.filter(
        is_deleted=False, recall_at__lte=time.time()
    ):
        call_endpoint_task.apply_async(kwargs={"endpoint_id": endpoint.id})
