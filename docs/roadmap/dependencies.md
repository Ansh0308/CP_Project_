# Dependencies Between Phases

```
0 -> 1 -> 2 -> 3 -> 4 --+
                         +-> 5 -> 6 -> 7 --+
                         |                  +-> 8 -> 9 -> 10 -> 11 -> 12 -> 13
                         +------------------+
```

- Phase 4 (CI) needs Phase 3 (tests exist) and Phase 2 (repo structure).
- Phase 6 (staging deploy) needs Phase 5 (staging env exists).
- Phase 8 (approval) needs Phase 7 (integration tests exist to approve *against*).
- Phase 10 (prod deploy) needs Phase 9 (prod env exists) and Phase 8 (gate exists).
- Phase 12 (rollback) needs Phase 11 (tags/audit exist to roll back *to*).
- Phase 13 is the capstone — it exercises every prior phase.
