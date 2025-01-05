# gunicorn_config.py

# Server Socket
bind = '0.0.0.0:8000'  # Bind to all network interfaces on port 8000

# Worker Processes
workers = 3  # Number of worker processes

# Worker Class
worker_class = 'sync'  # Synchronous workers

# Logging
accesslog = '-'  # Access log - '-' means log to stdout
errorlog = '-'  # Error log - '-' means log to stderr
loglevel = 'info'  # Log level

# Timeout
timeout = 30  # Workers silent for more than this many seconds are killed and restarted

# Debugging
reload = True  # Restart workers when code changes (useful for development)