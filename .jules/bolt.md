# Bolt's Performance Journal

## 2025-05-18 - Module-level Intl.NumberFormat instantiation for currency formatters
**Learning:** Instantiating `new Intl.NumberFormat()` repeatedly inside utility functions called during React render cycles (e.g. across 10+ receipt rows, sliders, and metric cards) incurs significant overhead (~60x-90x slower than a reused instance) due to locale resolution and internal spec initialization.
**Action:** Always instantiate `Intl.NumberFormat` (and similar Intl formatters like `DateTimeFormat`) once at module level or cache them if locales are dynamic, instead of constructing new instances on every format invocation.
