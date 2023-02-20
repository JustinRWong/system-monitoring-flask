# System Monitoring Dashboard (Flask Web App)

A simple, standalone system dashboard to monitor CPU and memory.

Purpose of this is to allow remote monitoring of personal laptops/machines.

Specific intended use case was to enable remore tracking on AI model training. In combination with [ngrok](https://ngrok.com/), this would allow you to monitor jobs currently running so you can easily leave you laptop without worrying about the ai training going wrong.

![ui][ui.png]

Optional query param `truncate=true` will truncate the x axes to the format `HH : MM: SS.SS`.

Resizing also determines if charts are plotted next to each other of stacked vertically.

Only the past 30 intervals are stored as a local in-memory LRU (least recently used) cache.