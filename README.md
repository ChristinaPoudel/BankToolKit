# 🏦 BANKDATA TOOLKIT

Local GUI toolkit made with Python, Pandas, Streamlit and Matplotlib.

## GUI features
- Upload CSV or XLSX files.
- Preview up to 200 rows in an interactive table.
- Clean duplicate/empty rows and trim text.
- Analyze numeric expense columns and optionally group them by category.
- Dedicated **Plot Dashboard** with histogram, box plot, trend plot, category bar chart and correlation heatmap.
- Export the processed dataset as CSV.

## Run locally
1. Install Python 3.10 or newer.
2. Extract `BANKDATA_TOOLKIT.zip`.
3. Open Terminal/Command Prompt in the extracted `BANKDATA_TOOLKIT` folder.
4. Create a virtual environment:

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Launch the GUI:
```bash
streamlit run app.py
```

7. If a browser does not open automatically, visit the local address printed by Streamlit, normally `http://localhost:8501`.

## How to use
1. **Upload**: Choose CSV/XLSX in the left sidebar.
2. **Preview**: Open the Preview tab to inspect rows and dataset size.
3. **Clean**: Open Cleaner, choose your options and click `Clean Data`.
4. **Analyze**: Open Expense Analyzer and choose an amount column and optional category.
5. **View plots**: Open Plot Dashboard, select a numeric column and optional category. Multiple charts appear together for easy comparison.
6. **Export**: Click `Export Report (CSV)` at the bottom.

A `sample_bank_data.csv` file is supplied for a quick test.
