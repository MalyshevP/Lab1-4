from .data_base import ReadAll, Write, Delete, Purge
from .status import StatusView

VIEWS = [
    StatusView,
    ReadAll,
    Write,
    Delete,
    Purge
]
