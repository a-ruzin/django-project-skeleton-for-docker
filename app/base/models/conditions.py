from typing import overload, Union, TypeVar, Callable

from django.db.models import Q, Model

T = TypeVar("T", bound=Model)


def condition(func: Callable[[Union[T, None]], Union[bool, Q]]) -> Callable[[Union[T, None]], Union[bool, Q]]:
    """Decorator that adds type overloads for dual-purpose condition functions.

    Decorates functions that:
    - Return bool when called with a model instance
    - Return Q when called with None

    Usage:
        @condition
        def is_expired(model_instance: Union[Model, None] = None) -> Union[bool, Q]:
            if model_instance is not None:
                return model_instance.expires_at < timezone.now()
            else:
                return Q(expires_at__lt=timezone.now())
    """
    @overload
    def wrapper(model_instance: None = None) -> Q: ...

    @overload
    def wrapper(model_instance: T) -> bool: ...

    def wrapper(model_instance: Union[T, None] = None) -> Union[bool, Q]:
        return func(model_instance)

    return wrapper


__all__ = ["condition"]
