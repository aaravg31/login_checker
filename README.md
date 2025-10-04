# 🔑 Login Checker – COSC 520 (Advanced Algorithms)

This repository contains my project for **COSC 520 – Advanced Algorithms** at UBC Okanagan.  
The problem explored is the **login checker / membership testing problem**, where the task is to efficiently determine whether a given username exists in a dataset.  

The project benchmarks **five different approaches** to membership testing:

- **Linear Search** – exact but slow ($O(n)$ lookups).  
- **Binary Search** – exact and efficient on sorted data ($O(log n)$).  
- **Hashing** – exact, using Python’s built-in `set()` ($O(1)$ expected lookup).  
- **Bloom Filter** – probabilistic, no false negatives but possible false positives (via [`pybloom-live`](https://pypi.org/project/pybloom-live/)).  
- **Cuckoo Filter** – probabilistic, supports deletions but may produce false negatives (via [`cuckoopy`](https://pypi.org/project/cuckoopy/)).  

The final report analyzes runtime, accuracy, and error trade-offs across dataset sizes ranging from **10K up to 100M usernames**, with full discussion of limitations and scalability.  

---

## 📂 Repository Structure

```
login_checker/
│── benchmark.py        # Benchmarking different membership methods
│── synth_dataset.py    # Synthetic dataset generator
│── test_benchmark.py   # Unit tests for benchmark.py
│── main.tex            # LaTeX source of the final report
│── refs.bib            # References file for LaTeX
│── final_report.pdf    # Compiled final report
│── plots/              # Runtime comparison plots
│── logins_*.csv        # Login datasets (10K, 100K, 1M included)
│── queries_*.csv       # Query datasets (matching the above sizes)
│── .gitignore
│── README.md
```
---

## ⚙️ Code Documentation

### `synth_dataset.py`
- Generates synthetic login datasets (`logins_N.csv`) and query datasets (`queries_Q.csv`).  
- Datasets contain randomized usernames with a **50% present / 50% absent** query distribution.  
- Run this to regenerate datasets locally (including very large ones excluded from GitHub).  

### `benchmark.py`
- Loads datasets and runs each membership testing method.  
- Reports runtime, accuracy, false positives (FP), false negatives (FN).  
- Produces two plots:  
  - `linear_plot.png`: runtime of linear search on smaller datasets.  
  - `other_plot.png`: runtime comparison of Binary, Hash, Bloom, and Cuckoo.  

### `test_benchmark.py`
- Unit tests for benchmarking functions.  
- Ensures:
  - Hashing is exact.  
  - Bloom never has false negatives.  
  - Cuckoo behaves reasonably.  

---

## 🚀 How to Run

### 1. Install dependencies (recommend using a virtual environment)
```bash
pip install matplotlib pybloom-live cuckoopy pytest
```

### 2. Generate datasets (if needed)
```bash
python synth_dataset.py
```

- Small datasets (10K, 100K, 1M) are already included in this repo.
- Large datasets (10M, 100M) are not included due to GitHub size limits but can be generated locally with the above script.

### 3. Run benchmarks
```bash
python benchmark.py
```

This will:
- Print runtimes and error stats to the console.
- Open up plots on python window.

### 4. Run tests
```bash
pytest -s test_benchmark.py
```

---

## 📖 Report Files

- `main.tex` – LaTeX source code of the final report.
- `refs.bib` – BibTeX references (including packages and ChatGPT acknowledgement).
- `final_report.pdf `– The compiled version of the report (read this if you just want results & discussion).
- `plots/` – Contains the generated figures used in the report.

---

## 🔎 Notes
- Linear search was only tested up to 1M usernames due to extreme runtime.
- Cuckoo filter was skipped for 100M usernames due to RAM and runtime limitations on the available hardware (MacBook Pro M2).
- A dataset of 1B usernames was not generated, as it would exceed practical time and memory limits.

---

## 👨‍💻 Author

**Aarav Gosalia**
[aaravjgosaliia.com](http://aaravjgosaliia.com)
