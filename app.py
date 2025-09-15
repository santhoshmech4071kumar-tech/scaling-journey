import streamlit as st
import pandas as pd

# Try importing plotting libraries
try:
    import plotly.express as px
    USE_PLOTLY = True
except ImportError:
    USE_PLOTLY = False

try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    USE_SEABORN = True
except ImportError:
    USE_SEABORN = False


st.title("📊 Descriptive Data Analysis Tool")

# File upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read CSV or Excel
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("🔍 Preview of Data")
    st.dataframe(df.head())

    st.subheader("📈 Descriptive Statistics")
    st.write(df.describe(include="all"))

    # Select column for visualization
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        col = st.selectbox("Choose a numeric column to visualize", numeric_cols)

        if USE_PLOTLY:
            st.write("✅ Using Plotly for interactive chart")
            fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}")
            st.plotly_chart(fig)

        elif USE_SEABORN:
            st.write("✅ Using Seaborn for visualization")
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

        else:
            st.write("✅ Using Matplotlib fallback")
            fig, ax = plt.subplots()
            ax.hist(df[col], bins=30, color="skyblue", edgecolor="black")
            ax.set_title(f"Distribution of {col}")
            st.pyplot(fig)
    else:
        st.warning("No numeric columns found in your dataset.")

    # Correlation Heatmap
    if len(numeric_cols) > 1:
        st.subheader("🔗 Correlation Heatmap")
        corr = df[numeric_cols].corr()

        if USE_PLOTLY:
            fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
            st.plotly_chart(fig)

        elif USE_SEABORN:
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

        else:
            fig, ax = plt.subplots()
            cax = ax.matshow(corr, cmap="coolwarm")
            plt.colorbar(cax)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=90)
            ax.set_yticklabels(corr.columns)
            st.pyplot(fig)

    # Trend Line Plot
    st.subheader("📉 Trend Line Plot")
    if numeric_cols:
        trend_col = st.selectbox("Choose a numeric column for trend plot", numeric_cols)
        if USE_PLOTLY:
            fig = px.line(df, y=trend_col, title=f"Trend of {trend_col}")
            st.plotly_chart(fig)

        elif USE_SEABORN:
            fig, ax = plt.subplots()
            sns.lineplot(data=df, y=trend_col, x=df.index, ax=ax)
            st.pyplot(fig)

        else:
            fig, ax = plt.subplots()
            ax.plot(df.index, df[trend_col], marker="o", color="blue")
            ax.set_title(f"Trend of {trend_col}")
            ax.set_xlabel("Index")
            ax.set_ylabel(trend_col)
            st.pyplot(fig)

else:
    st.info("👆 Upload a CSV or Excel file to get started.")
