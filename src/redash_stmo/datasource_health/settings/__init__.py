import os
import json

def dict_from_string(s):
    try:
        return json.loads(s)
    except ValueError:
        return {}

# Allow for a map of custom queries to test data source performance and availability.
# A sample map may look like:
# {
#    "1": "select 1;",
#    "5": "select 1;"
# }
CUSTOM_HEALTH_QUERIES = dict_from_string(os.environ.get("REDASH_CUSTOM_HEALTH_QUERIES", ""))

# Frequency of health query runs in minutes (12 hours by default)
HEALTH_QUERIES_REFRESH_SCHEDULE = int(os.environ.get("REDASH_HEALTH_QUERIES_REFRESH_SCHEDULE", 720))
