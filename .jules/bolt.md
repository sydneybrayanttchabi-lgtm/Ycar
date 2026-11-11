# Bolt's Journal - Critical Learnings Only

## 2025-05-18 - Hoisting Intl.NumberFormat out of Hot Render Paths
**Learning:** Instantiating `new Intl.NumberFormat()` inside utility helper functions called repeatedly during React rendering (such as table rows, calculation breakdown items, or range input updates) is computationally expensive (~60x slower than reusing an instance). Each instantiation constructs locale-specific formatters and generates garbage collection overhead on high-frequency events like slider adjustments.
**Action:** Always instantiate `Intl.NumberFormat` instances once at module or file scope, and reuse them across format helper calls.
