from .app import start_proxy

from importlib import reload

# while True:
#     # Do some things.
#     if is_changed(foo):
#         foo = reload(foo)

start_proxy('0.0.0.0', 8080)
