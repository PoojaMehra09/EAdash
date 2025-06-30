import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("EA.csv")

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_department = st.sidebar.multiselect("Department", options=df["Department"].unique(), default=df["Department"].unique())
selected_gender = st.sidebar.multiselect("Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
selected_attrition = st.sidebar.multiselect("Attrition", options=df["Attrition"].unique(), default=df["Attrition"].unique())
age_range = st.sidebar.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (20, 60))

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Demographics", "Job Metrics", "Satisfaction", "Advanced"])
with tab1:
    st.title("Employee Attrition Dashboard")
    st.markdown("""
        This dashboard provides insights into employee attrition and workforce statistics 
        to support HR leadership in strategic decision-making.
    """)

    st.subheader("Attrition Breakdown")
    st.write("Pie chart showing the proportion of employees who left vs. stayed.")
    st.write(\"Checking if px is defined:\", px)
    fig1 = px.pie(filtered_df, names='Attrition', title='Attrition Rate')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Department-wise Count")
    st.write("Bar chart showing employee count per department.")
    dept_counts = filtered_df["Department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Count"]
    fig2 = px.bar(dept_counts, x="Department", y="Count", title="Employees per Department")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("KPI Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Employees", len(filtered_df))
    with col2:
        attrition_rate = (filtered_df['Attrition'] == 'Yes').mean() * 100
        st.metric("Attrition Rate", f"{attrition_rate:.1f}%")
    with col3:
        avg_income = filtered_df['MonthlyIncome'].mean()
        st.metric("Avg. Monthly Income", f"${avg_income:,.0f}")

    with col1:
        st.metric("Total Employees", len(filtered_df))
    with col2:
        st.metric("Attrition Rate", f"{(filtered_df['Attrition']=='Yes').mean()*100:.1f}%")
    with col3:
        st.metric("Avg. Monthly Income", f"${filtered_df['MonthlyIncome'].mean():,.0f}")

with tab2:
    st.header("Demographics")

    st.subheader("Age Distribution by Attrition")
    st.write("Boxplot showing how age varies between those who stayed vs. left.")
    fig3 = px.box(filtered_df, x='Attrition', y='Age')
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Gender Distribution")
    st.write("Count plot of gender distribution by attrition.")
    fig4 = px.histogram(filtered_df, x='Gender', color='Attrition', barmode='group')
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.header("Job Metrics")

    st.subheader("Attrition by Overtime")
    st.write("Bar chart shows more attrition among employees working overtime.")
    fig5 = px.bar(filtered_df.groupby(['OverTime', 'Attrition']).size().reset_index(name='Count'), x='OverTime', y='Count', color='Attrition', barmode='group')
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Income vs Years at Company")
    st.write("Scatter plot to show how monthly income changes with tenure.")
    fig6 = px.scatter(filtered_df, x='YearsAtCompany', y='MonthlyIncome', color='Attrition', trendline='ols')
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("Job Role Distribution")
    st.write("Count of employees in each job role split by attrition.")
    fig7 = px.histogram(filtered_df, x='JobRole', color='Attrition', barmode='group')
    st.plotly_chart(fig7, use_container_width=True)

with tab4:
    st.header("Satisfaction & Ratings")

    st.subheader("Job Satisfaction by Attrition")
    st.write("Distribution of job satisfaction levels among employees.")
    fig8 = px.histogram(filtered_df, x='JobSatisfaction', color='Attrition', barmode='group')
    st.plotly_chart(fig8, use_container_width=True)

    st.subheader("Environment Satisfaction")
    st.write("Similar analysis for environment satisfaction.")
    fig9 = px.histogram(filtered_df, x='EnvironmentSatisfaction', color='Attrition', barmode='group')
    st.plotly_chart(fig9, use_container_width=True)

    st.subheader("Work-Life Balance")
    fig10 = px.histogram(filtered_df, x='WorkLifeBalance', color='Attrition', barmode='group')
    st.plotly_chart(fig10, use_container_width=True)

with tab5:
    st.header("Advanced Analytics")

    st.subheader("Correlation Heatmap")
    st.write("Correlation between numeric features to find key attrition drivers.")
    corr_df = filtered_df.select_dtypes(include='number')
    fig11, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(corr_df.corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    st.pyplot(fig11)

    st.subheader("Pivot Table")
    st.write("Create custom groupings to explore deeper insights.")
    col_x = st.selectbox("Select Column for Rows", options=df.columns)
    col_y = st.selectbox("Select Column for Values", options=df.select_dtypes(include='number').columns)
    if col_x and col_y:
        pivot_table = pd.pivot_table(filtered_df, index=col_x, values=col_y, aggfunc='mean').reset_index()
        st.dataframe(pivot_table)
        fig12 = px.bar(pivot_table, x=col_x, y=col_y)
        st.plotly_chart(fig12, use_container_width=True)
