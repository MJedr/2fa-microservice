import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.PrintLoggerFactory(),  # You can change this based on your needs
)

LOGGER = structlog.get_logger()
