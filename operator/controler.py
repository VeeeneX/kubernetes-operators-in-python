import kopf
import logging

@kopf.on.update('deployment')
def my_handler(spec, old, new, diff, **_):
    logging.info(f"A handler is called with body: {spec}")
