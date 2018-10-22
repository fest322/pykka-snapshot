from examples.example_1 import Incrementor
from pykka import ActorRegistry
from pykka.exceptions import ActorDeadError
import inspect
import sys
import time

from snapshotting import Message

ACTOR_PROXIES = []

def run_example_1():
    print("Setting up example 1")

    inc1 = Incrementor.start(0.2)
    inc2 = Incrementor.start(0.8)
    inc_proxies = [inc1.proxy(), inc2.proxy()]

    ACTOR_PROXIES.extend(inc_proxies)

    for i, p in enumerate(inc_proxies):
        proxies_to_send = [ip for j, ip in enumerate(inc_proxies) if j != i]
        p.save_neighbors(proxies_to_send).get()

    print("Starting example 1")
    start_msg = { "start": True, "logical_clock": 0 }
    start_msg = Message(0, 0, start_msg).as_sendable()
    inc1.tell(start_msg)

    time.sleep(1)
    snapshot_msg = { "init_snapshot": True }
    snapshot_msg = Message(0, 0, snapshot_msg).as_sendable()
    inc1.tell(snapshot_msg)

def cleanup():
    print("\nCleaning up example")

    ActorRegistry.stop_all()

    # for a in ACTOR_PROXIES:
    #     try:
    #         print("Stopping", a.id.get())
    #         a.stop()
    #     except (ActorDeadError):
    #         print("Dead actor:", a)
    #         continue

    print("Done!")

def get_available_examples():
    return [name for name, obj in inspect.getmembers(sys.modules[__name__])
            if inspect.isfunction(obj) and "run_example_" in name]

def run_example(n):
    example_target = "run_example_{}".format(n)
    if example_target in get_available_examples():
        try:
            exec(example_target + "()")
            while True:
                time.sleep(100)
        except (KeyboardInterrupt):
            cleanup()
    else:
        print("Example not implemented")

