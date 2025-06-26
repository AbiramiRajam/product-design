# 🧭 SF Business Survival Analysis – From Data to Product Insight

A San Francisco Registered Business analytical and design workflow that predicts small business survival in San Francisco and visualizes insights via a dynamic, designer-focused Streamlit dashboard.

---

## 📥 1. Data Collection

We collected business license data from the San Francisco Open Data Portal:

- **Source:** [SF Open Data API – Business Registrations](https://data.sfgov.org/resource/g8m3-pdis.json)
- **Method:** Python script with:
  - Pagination handling  
  - Rate-limiting support  
  - Deduplication  
  - Error handling  
  - CSV output for analysis  

> 🎯 **Goal**: Focus on businesses in Supervisor District 3 and prepare a clean dataset for modeling survival and closure risk.

---

## 🧹 2. Data Cleaning & Preprocessing

**Libraries Used:** `pandas`, `datetime`

### Steps:
- Converted `location_start_date`, `location_end_date`, and `data_as_of` to datetime
- Filled missing end dates with `data_as_of` to assume still-active businesses
- Calculated `duration = end_date - start_date` in **years**
- Created `event` column: `1` = closed, `0` = active
- Dropped rows with missing values in key columns (`license`, `neighborhood`, `duration`)

---

## 📊 3. Modeling with Survival Analysis

We applied **Kaplan-Meier** and **Cox Proportional Hazards (CoxPH)** models to predict business longevity.

### Why Survival Analysis?

- Handles **censored data** (ongoing businesses)
- Models **time to event** (closure)
- Provides **risk quantification** using hazard ratios

### Features:
- `duration`, `event`
- `lic_code_description`
- `neighborhoods_analysis_boundaries`
- `transient_occupancy_tax`, `parking_tax`
- `business_zip`, `business_age`

### Advanced Step:
- **PCA + CoxPHFitter** for dimensionality reduction and feature impact interpretation

---

## 📈 4. Exploratory Analysis

We used bar charts and time series to visualize:

- Top license types  
- Business registrations by year  
- Average business age  
- Survival by neighborhood  
- Closures over time

Survival insights showed:
- New businesses close faster  
- Certain licenses and zip codes carry more risk  
- Tax obligations correlate with closure likelihood

---

## 💡 5. Interactive Product Design Dashboard (Streamlit)

An interactive data product that turns survival modeling into **design insights**.

### Features:
- **License & Neighborhood Filter**
- **Colored Bar Charts** by lifespan bucket
- **Dynamic business count by duration**
- **Upload UX/UI mockups** to explore feature ideas
- **Designer-friendly recommendations**

#### Example Filter Logic:
```python
selected_license = st.sidebar.selectbox("Select License Type", sorted(license_list))
filtered_df = df[
    (df['lic_code_description'] == selected_license) &
    (df['neighborhoods_analysis_boundaries'] == selected_neighborhood)
]
