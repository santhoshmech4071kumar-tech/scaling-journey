import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Descriptive Data Analysis Tool")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        st.write("### Preview of Data")
        st.dataframe(df.head())

        st.write("### Descriptive Statistics")
        st.write(df.describe(include="all"))

        column = st.selectbox("Choose a column to visualize", df.columns)

        if pd.api.types.is_numeric_dtype(df[column]):
            st.write("### Histogram")
            fig, ax = plt.subplots()
            df[column].hist(ax=ax, bins=20)
            st.pyplot(fig)

            st.write("### Boxplot")
            fig2, ax2 = plt.subplots()
            df.boxplot(column=column, ax=ax2)
            st.pyplot(fig2)
        else:
            st.warning("Selected column is not numeric, charts are skipped.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
