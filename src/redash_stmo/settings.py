import os

# Frequency of health query runs in minutes (12 hours by default)
HEALTH_QUERIES_REFRESH_SCHEDULE = int(os.environ.get("REDASH_HEALTH_QUERIES_REFRESH_SCHEDULE", 720))
