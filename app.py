import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
import io

st.title("📊 Final Marks Uploader")
st.write("Upload a PDF with student marks and an Excel file with student numbers. Get a merged Excel file!")

pdf_file = st.file_uploader("Upload PDF Result File", type="pdf")
excel_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if pdf_file and excel_file:
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "".join([page.get_text() for page in doc])
    pattern = r"(\d{6})\s+\d{5}\s+(\d+)\s*/\s*100\s+(\d+\.\d+)"
    matches = re.findall(pattern, text)
    marks_dict = {int(sid): float(score) for sid, _, score in matches}

    df = pd.read_excel(excel_file)
    student_col = next((col for col in df.columns if df[col].astype(str).str.match(r"^\d{4,6}$").sum() > 5), None)

    if student_col is None:
        st.error("❌ Could not detect student number column.")
    else:
        df["Final Marks (100%)"] = df[student_col].map(marks_dict)
        st.success("✅ Marks added successfully!")
        st.dataframe(df)

        output = io.BytesIO()
        df.to_excel(output, index=False)
        st.download_button("📥 Download Updated Excel", output.getvalue(), file_name="updated_marks.xlsx")
