import os


def get_config(log_dir, logstash_host, logstash_port, log_level="DEBUG"):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": (
                    "[%(asctime)s] %(levelname)s [%(name)s:"
                    " %(funcName)s: %(lineno)s] %(message)s"
                ),
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "null": {"level": log_level, "class": "logging.NullHandler"},
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "django_log_file": {
                "level": log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(log_dir, "django.log"),
                "maxBytes": 16777216,  # 16megabytes
                "formatter": "verbose",
            },
            "apps_log_file": {
                "level": log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(log_dir, "apps.log"),
                "maxBytes": 16777216,  # 16megabytes
                "formatter": "verbose",
            },
            "logstash": {
                # debug info like line numbers are not logged unless it is an error message
                "level": log_level,
                "class": "logstash.TCPLogstashHandler",
                "host": logstash_host,
                "port": logstash_port,
                "version": 1,
                "message_type": "crema",
                "fqdn": False,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["django_log_file", "logstash"],
                "level": log_level,
                "propagate": False,
            },
            "django.request": {
                "handlers": ["django_log_file", "logstash"],
                "level": log_level,
                "propagate": False,
            },
            "kafka": {"handlers": ["django_log_file", "logstash"], "level": log_level,},
            "": {
                "handlers": ["console", "apps_log_file", "logstash"],
                "level": log_level,
                "propagate": False,
            },
        },
    }
