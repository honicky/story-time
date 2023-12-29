import contextlib
import time

global timer_invocation_counter
timer_invocation_counter = 0

@contextlib.contextmanager
def HereTimer(name="here"):
    timer_invocation_counter += 1
    start = time.time()
    yield
    end = time.time()
    print(f'{name}-{timer_invocation_counter} {(end-start)/1000:.2f} ms')

