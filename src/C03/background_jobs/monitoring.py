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


def monitor_snapshots(app, freq=1.0):
    state = app.events.State()
    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={'*': state.event})
        with DumpCam(state, freq=freq):
            recv.capture(limit=None, timeout=None)

def realtime_monitoring(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                '*': state.event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

if __name__ == '__main__':
    # monitor_snapshots(app, 10)
    realtime_monitoring(app)