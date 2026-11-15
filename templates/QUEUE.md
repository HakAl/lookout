# Local queue

Instance file. Copy to `QUEUE.md` at the instance root. This is the
authoritative local task ledger. If the instance adopts an issue tracker, move
the tasks once, keep their ID mapping, and make this file a pointer instead of
maintaining two queues. A task may need more than one execution.

| ID | Work | State | Owner / next action |
| --- | --- | --- | --- |
| <TASK-001> | <short description, linked to `reviews/<task-id>/report.md` once it exists> | <ready, in progress, reviewed, done> | <who acts next and on what> |
