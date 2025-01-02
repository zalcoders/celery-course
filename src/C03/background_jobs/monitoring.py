from pprint import pformat
import datetime as dt

from celery.events.snapshot import Polaroid

from background_jobs.celery import app

class DumpCam(Polaroid):
    clear_after = True  # clear after flush (incl, state.event_count).
    

    def on_shutter(self, state):
        if not len(state.tasks):
            # No new events since last snapshot.
            print(f"No new event: {dt.datetime.now()}")
            return
        print('Workers: {0}'.format(pformat(state.workers, indent=4)))
        print('Tasks: {0}'.format(pformat(state.tasks, indent=4)))
        print('Total: {0.event_count} events, {0.task_count} tasks'.format(
            state))
        print("-"*50)


        failed_tasks = 0
        for task_id, task in state.tasks.items():
            if task.failed is not None:
                failed_tasks += 1

        print(f"{failed_tasks / len(state.tasks) * 100}% Of tasks failed")


def main(app, freq=1.0):
    state = app.events.State()
    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={'*': state.event})
        with DumpCam(state, freq=freq):
            recv.capture(limit=None, timeout=None)

if __name__ == '__main__':
    main(app, 10)