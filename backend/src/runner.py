from .models import Task
from .runner_db import Session
import dramatiq
from dramatiq.brokers.redis import RedisBroker
import os
from datetime import datetime
from dramatiq_abort import Abort, Abortable, backends

# Configure Redis broker
redis_broker = RedisBroker(url=os.getenv("REDIS_URL"))
dramatiq.set_broker(redis_broker)

event_backend = backends.RedisBackend(client=redis_broker.client)
abortable = Abortable(backend=event_backend)
redis_broker.add_middleware(abortable)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_nth_prime(n, progress_update):
    count = 0
    num = 1
    last_progress = -1

    while count < n:
        num += 1

        if is_prime(num):
            count += 1
            progress = int((count / n) * 100)
            if progress > last_progress:
                progress_update(progress)
                last_progress = progress
    return num

@dramatiq.actor(max_retries=0, queue_name="prime_calculator")
def calculate_prime(task_id):
    session = Session()
    try:
        task = session.query(Task).get(task_id)
        if not task:
            return
        
        task.status = "running"
        session.commit()

        def progress_update(progress):
            task.progress = progress
            session.commit()
        
        result = find_nth_prime(task.n, progress_update)

        task.result = result
        task.status = "done"
        task.completed_at = datetime.utcnow()
        task.progress = 100
        session.commit()
    except Abort:
        pass
    except Exception as e:
        task.status = "error"
        task.error = str(e)
        task.completed_at = datetime.utcnow()
        session.commit()
    finally:
        session.close() 