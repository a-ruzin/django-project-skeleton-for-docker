__all__ = ["model_repr"]

"""
взято здесь:
https://github.com/getsentry/sentry/blob/120d06aab39749b388de8a85a0fe9b9163838948/src/sentry/db/models/base.py
"""


def model_repr(*attrs):
    if "id" not in attrs and "pk" not in attrs:
        attrs = ("id",) + attrs

    def new_repr(self):
        cls = type(self).__name__

        pairs = (f"{attr}={getattr(self, attr, None)!r}" for attr in attrs)

        return "<{} at 0x{:x}: {}>".format(cls, id(self), ", ".join(pairs))

    return new_repr
