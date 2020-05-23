def singleton(cls):
    """
    This decorator make sure that there is only 1 instance of the class.
    Args:
        cls:

    Returns:

    """
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper
