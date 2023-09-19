import streamlit as st
import pandas as pd
import plotly.express as px


def create_info_section(title, info_text):
    with st.expander(f"{title} - Know More?"):
        st.info(info_text)


# Load the CSV file with the "institute" column
# publication_df = pd.read_csv("modified_publicationRecord_with_institute.csv")
publication_df = pd.read_csv("modified_publicationRecord_with_institute_no_depart.csv", usecols=lambda column: column != 'creators')
publication_df = publication_df[publication_df["date"] <= 2022.00]
publication_df = publication_df[publication_df["date"] >= 1930.00]
publication_df = publication_df.sort_values(by="date")


# Streamlit Dashboard
st.title("BORIS Dashboard")
st.sidebar.title("Select Institute ")

# Dropdowns for selecting institute and security
unique_institutes = publication_df["institute"].unique()
selected_institute = st.sidebar.selectbox("Type or Select Institute", ["All"] + sorted(list(unique_institutes)))
# selected_security = st.sidebar.selectbox("Select Security", ["All", "Open", "Closed"])

# Display selected options
selected_security = "All" # recently added
st.success(f"Showing results for {selected_institute}.")

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

info_text_oar = "Open Access Rate (OAR): percentage of Open-Access publications among total publications -> OA-Publications / Total Publications"
create_info_section("Open Access Rate", info_text_oar)

# Calculate publication count based on date and security status
count_df = filtered_df.groupby(["date", "full_text_status"]).size().reset_index(name="count")
st.markdown("---")
filtered_df_no_index = filtered_df.reset_index(drop=True)
st.dataframe(filtered_df_no_index)
st.markdown("---")

st.title("Data Plots")
# Plot scatter graph
scatter_fig = px.scatter(
    count_df,
    x="date",
    y="count",
    title="Publication Frequency",
    labels={"date": "Date", "count": "count"},
    color="full_text_status"
)

# Update color for each marker

scatter_fig.update_traces(marker=dict(color="green"), selector=dict(name="open"))
scatter_fig.update_traces(marker=dict(color="red"), selector=dict(name="closed"))

scatter_fig.update_layout(legend_title_text=None)

# Display the scatter plot
st.plotly_chart(scatter_fig)

# Calculate publication count based on year and security status

yearly_count_df = filtered_df.groupby(["date"]).size().reset_index(name="count")


# bar_fig = px.scatter(
#     yearly_count_df,
#     x="date",
#     y="count",
#     title="Total Publication Count by Year",
#     labels={"year": "Year", "count": "Publication Count"},
# )

# st.plotly_chart(bar_fig)


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
    labels = {"date":"Year", "oar":"OA-Rate"},
    hover_name='year',
    hover_data=['closed', 'open', 'total'],
    trendline='lowess',#ols
    trendline_color_override='rgba(226, 85, 158, 0.41)',
    color_discrete_sequence=['rgba(239, 61, 98, 0.72)']
)

st.plotly_chart(fig)



st.markdown("---")

modified_df = pd.read_csv("modified_publicationRecord_with_institute_no_depart.csv")
unibe_df = pd.read_csv("unibe_data.csv")

merged_df = pd.merge(modified_df, unibe_df, on="institute", how="left")
grouped = merged_df.groupby("faculty")
faculty_projects = grouped.agg(
    total_projects=("institute", "count"),
    open_projects=("full_text_status", lambda x: (x == "open").sum())
)
faculty_projects = faculty_projects.reset_index()
faculty_projects["oar"] = (faculty_projects["open_projects"] / faculty_projects["total_projects"]).round(2)
faculty_projects = faculty_projects.sort_values(by="oar", ascending=False)

faculty_projects_filtered = faculty_projects[faculty_projects['oar'] > 0]

fig = px.bar(
    faculty_projects_filtered,
    x="faculty",
    y="oar",
    title="Open Access Rate by Faculty (Excluding OAR = 0)",
    labels={"faculty": "Faculty", "oar": "OA-Rate"},
    hover_data=["total_projects", "open_projects"]
)
st.plotly_chart(fig)
# Create info button and section for Open Access Ratio by Faculty

