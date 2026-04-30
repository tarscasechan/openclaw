# Resilience Loop

Use this loop for any job that can fail midstream.

## 1. Contract
- What is the goal?
- What is the next slice?
- What counts as done?
- What counts as blocked?

## 2. Execute
- Run one small slice.
- Prefer a slice that can finish in one pass.

## 3. Check
- Is the process still live?
- Did the slice produce a result?
- Did it time out or die?

## 4. Commit state
- Record what changed.
- Record what failed.
- Record the next slice.

## 5. Retry correctly
- Retry only the failed slice.
- If the concept is the problem, restart from concept.
- If the state is wrong, fix the state file first.
