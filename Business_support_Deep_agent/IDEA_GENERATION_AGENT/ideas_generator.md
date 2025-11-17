# Ideas Generator – Quick‑Start Guide  

## Overview  
This repository contains a lightweight Python utility that:

1. **Accepts a user prompt** (sector, location, optional budget).  
2. **Generates 10 business‑idea suggestions** that can be launched within **6 months**.  
3. Provides a **rough cost estimate in Indian Rupees (₹)** for each idea.  

The script is self‑contained and only requires the standard Python library (no external APIs).  
It is intended for **illustrative/brain‑storming purposes** – the cost figures are **approximate** and should be validated with a detailed feasibility study.

---

## Files  

| File | Description |
|------|-------------|
| `ideas_generator.md` | This documentation file (the one you are reading). |
| `idea_generation_agent.py` | The Python program that implements the idea‑generation logic. |

---

## Prerequisites  

| Requirement | Minimum Version |
|-------------|-----------------|
| Python | 3.8+ |
| (Optional) `tabulate` library – for pretty‑printed tables | `pip install tabulate` |

If you do **not** install `tabulate`, the script will fall back to a simple plain‑text output.

---

## How to Run  

1. **Clone / download** the two files into the same directory.  
2. Open a terminal (or command prompt) and navigate to that directory.  
3. Execute the script:  

   ```bash
   python ideas_generator.py

