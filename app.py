import streamlit as st
import pandas as pd

from pdf_reader import extract_text_from_pdf
from analyzer import analyze_report


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🩺",
    layout="wide"
)


# ---------------- TITLE ----------------
st.title("🩺 Medical Report Analyzer")
st.write("Upload a medical report and analyze Normal and Abnormal results.")

st.divider()


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📋 Patient Information")

    patient_name = st.text_input("Patient Name")

    patient_age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=25
    )

    patient_gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    st.divider()

    st.info(
        "This software provides an automated report analysis. "
        "Always consult a qualified healthcare professional for "
        "medical diagnosis or treatment."
    )


# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📤 Upload Medical Report",
    type=["pdf", "txt"]
)


# ---------------- ANALYSIS ----------------
if uploaded_file is not None:

    report_text = ""

    # Read PDF
    if uploaded_file.name.lower().endswith(".pdf"):
        try:
            report_text = extract_text_from_pdf(uploaded_file)

        except Exception as error:
            st.error(f"Error reading PDF: {error}")

    # Read TXT
    elif uploaded_file.name.lower().endswith(".txt"):
        try:
            report_text = uploaded_file.read().decode("utf-8")

        except Exception as error:
            st.error(f"Error reading text file: {error}")

    # Continue if text was found
    if report_text.strip():

        st.success("Report uploaded successfully!")

        # ---------------- EXTRACTED TEXT ----------------
        with st.expander("📄 View Extracted Report Text"):
            st.text_area(
                "Report Content",
                report_text,
                height=300
            )

        # ---------------- ANALYZE REPORT ----------------
        results = analyze_report(
            report_text,
            patient_gender
        )

        normal_results = results["normal"]
        abnormal_results = results["abnormal"]
        unknown_results = results["unknown"]

        # ---------------- METRICS ----------------
        st.divider()
        st.subheader("📊 Analysis Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🟢 Normal Results",
                len(normal_results)
            )

        with col2:
            st.metric(
                "🔴 Abnormal Results",
                len(abnormal_results)
            )

        with col3:
            st.metric(
                "⚪ Unknown / Not Analyzed",
                len(unknown_results)
            )

        st.divider()

        # ---------------- NORMAL AND ABNORMAL RESULTS ----------------
        col1, col2 = st.columns(2)

        # Normal
        with col1:
            st.subheader("🟢 Normal Results")

            if normal_results:
                normal_df = pd.DataFrame(normal_results)

                st.dataframe(
                    normal_df,
                    use_container_width=True
                )

            else:
                st.info("No normal results found.")

        # Abnormal
        with col2:
            st.subheader("🔴 Abnormal Results")

            if abnormal_results:
                abnormal_df = pd.DataFrame(abnormal_results)

                st.dataframe(
                    abnormal_df,
                    use_container_width=True
                )

            else:
                st.success("No abnormal results found.")

        # ---------------- UNKNOWN RESULTS ----------------
        if unknown_results:

            st.divider()
            st.subheader("⚪ Results Not Automatically Analyzed")

            unknown_df = pd.DataFrame(unknown_results)

            st.dataframe(
                unknown_df,
                use_container_width=True
            )

        # ---------------- SUMMARY ----------------
        st.divider()
        st.subheader("📝 Analysis Summary")

        total_analyzed = (
            len(normal_results)
            + len(abnormal_results)
        )

        summary = f"""
MEDICAL REPORT ANALYSIS SUMMARY

Patient Name: {patient_name if patient_name else "Not Provided"}
Age: {patient_age}
Gender: {patient_gender}

Total Results Analyzed: {total_analyzed}
Normal Results: {len(normal_results)}
Abnormal Results: {len(abnormal_results)}
Not Automatically Analyzed: {len(unknown_results)}

"""

        # Normal findings
        if normal_results:

            summary += "NORMAL FINDINGS:\n"

            for result in normal_results:
                summary += (
                    f"- {result['Test']}: "
                    f"{result['Value']} "
                    f"({result['Status']})\n"
                )

        summary += "\n"

        # Abnormal findings
        if abnormal_results:

            summary += "ABNORMAL FINDINGS:\n"

            for result in abnormal_results:
                summary += (
                    f"- {result['Test']}: "
                    f"{result['Value']} "
                    f"({result['Status']})\n"
                )

        else:
            summary += "No abnormal results were automatically detected.\n"

        # Disclaimer
        summary += """
IMPORTANT:
This is an automated analysis based on configured reference ranges.
It is not a medical diagnosis. Please consult a qualified healthcare
professional for medical advice, diagnosis, or treatment.
"""

        # ---------------- DISPLAY SUMMARY ----------------
        st.text_area(
            "Generated Summary",
            summary,
            height=350
        )

        # ---------------- DOWNLOAD SUMMARY ----------------
        st.download_button(
            label="⬇️ Download Summary",
            data=summary,
            file_name="medical_report_summary.txt",
            mime="text/plain"
        )

    else:
        st.error(
            "No readable text was found in the uploaded report."
        )

else:
    st.info(
        "👆 Please upload a PDF or TXT medical report to start the analysis."
    )