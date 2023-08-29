import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file with the "institute" column
# publication_df = pd.read_csv("modified_publicationRecord_with_institute.csv")
publication_df = pd.read_csv("modified_publicationRecord_with_institute_no_depart.csv", usecols=lambda column: column != 'creators')
publication_df = publication_df[publication_df["date"] <= 2024.00]
publication_df = publication_df[publication_df["date"] >= 1930.00]
publication_df = publication_df.sort_values(by="date")

# Streamlit Dashboard
st.title("BORIS Dashboard")
st.sidebar.title("Select Institute ")

# Dropdowns for selecting institute and security
unique_institutes = publication_df["institute"].unique()
selected_institute = st.sidebar.selectbox("Select Institute", ["All"] + list(unique_institutes))
# selected_security = st.sidebar.selectbox("Select Security", ["All", "Open", "Closed"])

# Display selected options
selected_security = "All" # recently added
st.success(f"Institute: {selected_institute} & Security: open and closed")

# Filter the data based on selected options
filtered_df = publication_df.copy()


if selected_institute != "All":
    filtered_df = filtered_df[filtered_df["institute"] == selected_institute]

# if selected_security == "Open":
#     filtered_df = filtered_df[filtered_df["full_text_status"] == "open"]

# if selected_security == "Closed":
#     filtered_df = filtered_df[filtered_df["full_text_status"] == "closed"]

total_entries = len(filtered_df)
public_entries = len(filtered_df[filtered_df["full_text_status"] == "open"])
restricted_entries = len(filtered_df[filtered_df["full_text_status"] == "closed"])

if total_entries > 0:
    oar = public_entries / total_entries
else:
    oar = 0.0
st.markdown("---")

# Create cards to display OAR, counts, and total entries
col1, col2, col3, col5 = st.columns(4)
col1.metric("Open Access Rate", f"{oar:.2%}")
col2.metric("Open Entries", public_entries)
col3.metric("Closed Entries", restricted_entries)
col5.metric("Total Entries", total_entries)

# Calculate publication count based on date and security status
count_df = filtered_df.groupby(["date", "full_text_status"]).size().reset_index(name="count")
st.markdown("---")
st.dataframe(filtered_df)
st.markdown("---")

st.title("Data Plots")
# Plot scatter graph
scatter_fig = px.scatter(
    count_df,
    x="date",
    y="count",
    title="Scatter Plot of Publication Frequency",
    labels={"date": "Date", "count": "Publication Count"},
    color="full_text_status"
)

# Update color for each marker
scatter_fig.update_traces(marker=dict(color="green"), selector=dict(name="open"))
scatter_fig.update_traces(marker=dict(color="red"), selector=dict(name="closed"))

# Display the scatter plot
st.plotly_chart(scatter_fig)

# Calculate publication count based on year and security status

yearly_count_df = filtered_df.groupby(["date"]).size().reset_index(name="count")


bar_fig = px.scatter(
    yearly_count_df,
    x="date",
    y="count",
    title="Total Publication Count by Year",
    labels={"year": "Year", "count": "Publication Count"},
)

st.plotly_chart(bar_fig)



if selected_security == "All":

    st.markdown("---")
    st.title("OAR(Open Access Rate) Data.")



    grouped = filtered_df.groupby(['date', 'full_text_status']).size().unstack(fill_value=0)
    grouped['total'] = grouped['closed'] + grouped['open']
    grouped['oar'] = (grouped['open'] / grouped['total']).round(4)  
    grouped = grouped.reset_index()
    grouped.columns = ['year', 'closed', 'open', 'total', 'oar']
    # st.dataframe(grouped)

    fig = px.scatter(
        grouped,
        x = "year",
        y = "oar",
        title = "Open Access Rate per Year",
        labels = {"date":"Year", "oar":"Open Access Rate"},
        hover_name='year',
        hover_data=['closed', 'open', 'total'],
        trendline='lowess',#ols
        trendline_color_override='rgba(226, 85, 158, 0.41)',
        color_discrete_sequence=['rgba(239, 61, 98, 0.72)']
    )

    st.plotly_chart(fig)

else:
    st.warning("Open Access Trends are only visible when your security is configured as 'All'.")
