import logging

# Start logging module.
log = logging.getLogger()
log.setLevel(logging.DEBUG)
format_ = logging.Formatter('%(levelname)s: %(message)s\n')

# Stdout stream handler.
stream_handle = logging.StreamHandler()
stream_handle.setFormatter(format_)
stream_handle.setLevel(logging.INFO)

# Log file handler.
file_handle = logging.FileHandler("exec.log", "w", encoding = None, delay = "true")
file_handle.setFormatter(format_)
file_handle.setLevel(logging.DEBUG)

log.addHandler(stream_handle)
log.addHandler(file_handle)