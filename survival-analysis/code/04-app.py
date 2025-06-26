import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="SF Business Survival Dashboard", layout="wide")


# ---------------------
# Load Data
# ---------------------
st.title("📊 San Francisco Business Survival Insights: Driving Product Design Solutions")

df = pd.read_csv("../data/modeling_dataset_full.csv")

# ---------------------
# Data Preprocessing
# ---------------------
df['location_start_date'] = pd.to_datetime(df['location_start_date'], errors='coerce')
df['location_end_date'] = pd.to_datetime(df['location_end_date'], errors='coerce')
df['data_as_of'] = pd.to_datetime(df['data_as_of'], errors='coerce')

df['end_date_filled'] = df['location_end_date'].fillna(df['data_as_of'])
df['duration'] = (df['end_date_filled'] - df['location_start_date']).dt.days / 365.25
df['event'] = df['location_end_date'].notna().astype(int)

df = df.dropna(subset=['duration', 'event', 'lic_code_description', 'neighborhoods_analysis_boundaries'])

# ---------------------
# Sidebar Filters
# ---------------------
st.sidebar.header("Filter Data")
df['lic_code_description'] = df['lic_code_description'].str.title()
license_list = df['lic_code_description'].dropna().unique().tolist()
neighborhood_list = df['neighborhoods_analysis_boundaries'].dropna().unique().tolist()

selected_license = st.sidebar.selectbox("Select License Type", sorted(license_list))
selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", sorted(neighborhood_list))

filtered_df = df[
    (df['lic_code_description'] == selected_license) &
    (df['neighborhoods_analysis_boundaries'] == selected_neighborhood)
]

# ---------------------
# Bar Chart With Colored Bars
# ---------------------
st.subheader(f"📊 Business Lifespan Distribution: {selected_license} in {selected_neighborhood}")

if len(filtered_df) < 5:
    st.warning("Not enough data for this combination. Try a different filter.")
else:
    # Create duration buckets
    bins = [0, 1, 3, 5, 10, 15, 20, 100]
    labels = ['<1 yr', '1–3 yrs', '3–5 yrs', '5–10 yrs', '10–15 yrs', '15–20 yrs', '20+ yrs']
    filtered_df['duration_bucket'] = pd.cut(filtered_df['duration'], bins=bins, labels=labels, right=False)

    # Count businesses in each bucket
    bucket_counts = filtered_df['duration_bucket'].value_counts().sort_index()

    # Define a color for each bar
    color_map = {
        '<1 yr': '#FF9999',
        '1–3 yrs': '#FFCC99',
        '3–5 yrs': '#FFFF99',
        '5–10 yrs': '#CCFF99',
        '10–15 yrs': '#99FFCC',
        '15–20 yrs': '#99CCFF',
        '20+ yrs': '#C299FF',
    }
    bar_colors = [color_map[label] for label in bucket_counts.index]

    # Plotting
    fig, ax = plt.subplots()
    bucket_counts.plot(kind='bar', color=bar_colors, ax=ax, edgecolor='black')

    ax.set_xlabel("Business Lifespan", fontdict={'size': 18})
    ax.set_ylabel("Number of Businesses", fontdict={'size': 18})
    ax.set_title(f"Lifespan Distribution: {selected_license} in {selected_neighborhood}", fontsize=20)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    st.pyplot(fig)

    st.markdown(f"""
    **Insights:**  
    - Most common lifespan: **{bucket_counts.idxmax()}**  
    - Sample size: {len(filtered_df)} businesses  
    """)

# ---------------------
# Design Samples
# ---------------------
st.subheader("🎨 Design Solutions Based on Insights")

st.markdown("⬆️ Use the uploaders below to add your UI/UX Mockups.")

uploaded_web = st.file_uploader("Upload Web UI Mockup", type=["png", "jpg"], key="web")
uploaded_mobile = st.file_uploader("Upload Mobile UI Mockup", type=["png", "jpg"], key="mobile")

col1, col2 = st.columns(2)
with col1:
    if uploaded_web:
        st.image(uploaded_web, caption="Web Design Proposal", use_column_width=True)
with col2:
    if uploaded_mobile:
        st.image(uploaded_mobile, caption="Mobile Design Proposal", use_column_width=True)

st.markdown("---")
st.markdown("🔍 **Design Opportunity: Insights into business durability reveal key areas for design and product management focus:")
st.markdown("""
- Personalized onboarding during early-stage business years  
- Mid-life check-ins to offer targeted support  
- Outreach to long-standing businesses for mentorship programs
""")


