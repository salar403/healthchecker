from backend.customs.exceptions import CustomException


def get_object_or_none(Class, *args, **kwargs):
    queryset = (
        Class._default_manager.all() if hasattr(Class, "_default_manager") else Class
    )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_object_or_404(Class, *args, **kwargs):
    result = get_object_or_none(Class, *args, **kwargs)
    if not result:
        raise CustomException(code="not_found", status_code=404)
    return result
