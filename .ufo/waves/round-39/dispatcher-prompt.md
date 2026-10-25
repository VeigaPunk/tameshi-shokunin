You are the round-39 wave dispatcher. You have one job.

1. Read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-39/dispatch-w1.json.
2. Call the task tool exactly once. Pass taskCall.context as the context and taskCall.tasks as the tasks array, unchanged. Do not drop, rewrite, split, or shrink the array. Do not pass a model. There are 64 tasks.
3. After that call returns, do not end your turn. Poll until every spawned seat is terminal or 40 minutes have passed. Sleep 20 seconds between polls. A parent that exits while seats are still running kills them. That is the failure you must not repeat.
4. When every seat is terminal, or the deadline passes, print one line:
   DISPATCH_RESULT terminal=<N> elapsed_s=<S> holding=1
5. If you have no task tool, print DISPATCH_NO_TASK_TOOL and stop. Do not invent seats.

You are a leaf aside from this one task call. Do not edit the lane repo, the fleet repo, or jj state.
