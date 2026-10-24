## 2026-10-24 - React TSX inside app.py with CRLF line endings
**Learning:** `app.py` in this repository is actually a React TypeScript (TSX) component file using CRLF (`\r\n`) line endings. Standard string replacement tools or git diffs can fail if line endings aren't handled explicitly, and Prettier must be invoked with `--parser typescript --end-of-line crlf`.
**Action:** Always specify `--end-of-line crlf --parser typescript` when running Prettier or formatting `app.py` to preserve line endings and formatting.
