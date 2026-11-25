# Menu tools

`menu.json` is the single source of truth for the menu (names, prices, descriptions, thumbnails, Sunday roast, allergy note).

1. Edit `tools/menu.json`.
2. `python3 tools/build_menu.py`  - rebuilds the menu page and its Google structured data.
3. `python3 tools/build_pdf.py`   - rebuilds `six-hills-cafe-menu.pdf` (needs `pip install reportlab pillow numpy fonttools brotli`).

To swap an icon for a real photo, save a square 128x128 WebP in `images/thumbs/` and point the item's `"thumb"` at it.
Add `"veg": true` to mark an item vegetarian. Do not upload the `tools/` folder to the live site if you prefer to keep it private.
