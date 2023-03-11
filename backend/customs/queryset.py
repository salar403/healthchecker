def get_object_or_none(Class, *args, **kwargs):
    queryset = (
        Class._default_manager.all() if hasattr(Class, "_default_manager") else Class
    )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
