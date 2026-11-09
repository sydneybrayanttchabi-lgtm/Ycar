# Bolt's Performance Journal

## 2025-05-18 - Module-level Intl.NumberFormat caching in React render tree
**Learning:** `new Intl.NumberFormat(...)` performs locale data resolution and object construction, making it ~90x slower than reusing a pre-created formatter instance. In components with high-frequency updates (e.g. range sliders controlling freight / customs calculations) or receipt tables mapping multiple line items, reconstructing formatters in utility functions directly degrades frame rate and UI responsiveness.
**Action:** Always instantiate `Intl.NumberFormat` (and other `Intl.*` formatters) at module scope or via memoization rather than allocating new instances inside formatting helper functions called during render.
