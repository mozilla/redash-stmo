import os

from redash.settings.helpers import parse_boolean, set_from_string


# Frequency of health query runs in minutes (12 hours by default)
HEALTH_QUERIES_REFRESH_SCHEDULE = int(
    os.environ.get("REDASH_HEALTH_QUERIES_REFRESH_SCHEDULE", 720)
)

# When enabled this will match the given remote groups request header with a
# configured list of allowed user groups.
REMOTE_GROUPS_ENABLED = parse_boolean(
    os.environ.get("REDASH_REMOTE_GROUPS_ENABLED", "false")
)
REMOTE_GROUPS_HEADER = os.environ.get(
    "REDASH_REMOTE_GROUPS_HEADER", "X-Forwarded-Remote-Groups"
)
REMOTE_GROUPS_ALLOWED = set_from_string(
    os.environ.get("REDASH_REMOTE_GROUPS_ALLOWED", "")
)

# Iodide API key for creating new notebooks
IODIDE_API_KEY = os.environ.get(
    "REDASH_IODIDE_API_KEY"
)

# The Redash API key that Iodide uses
REDASH_OWN_API_KEY_FOR_IODIDE = os.environ.get(
    "REDASH_OWN_API_KEY_FOR_IODIDE"
)
