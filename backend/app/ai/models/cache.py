from functools import lru_cache


@lru_cache(maxsize=10)
def cached_model(name: str):
    """
    Future cache for expensive AI models.
    """
    return name