# Bolt's Journal - Critical Learnings

## 2025-05-18 - Intl.NumberFormat instantiation in render paths
**Learning:** `new Intl.NumberFormat()` constructor incurs heavy initialization overhead (~50-65x slower) compared to reusing an instance. When formatting currency in loops or frequent render callbacks, instantiating `Intl.NumberFormat` on each call creates unnecessary CPU spikes and GC pressure.
**Action:** Always hoist `Intl.NumberFormat` instances to module-level scope or memoize them when locale and formatting options are constant.
