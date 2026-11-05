# Bolt's Journal - Critical Learnings Only

## 2025-05-18 - Caching Intl.NumberFormat in React Components
**Learning:** Instantiating `new Intl.NumberFormat(...)` on every render inside utility functions called repeatedly (such as within table/receipt loops) causes heavy ICU initialization overhead (~600ms per 12k calls vs ~8ms when cached).
**Action:** Always instantiate and reuse `Intl.NumberFormat` instances at module level when locales and format options are static.
