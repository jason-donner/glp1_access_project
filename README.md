# The GLP-1 Divide: Geography, Economics, and the Equity Gap

###  [View the Interactive Tableau Dashboard](https://public.tableau.com/views/GLP-1EquityAnalysisDashboard/GLP-1EquityAnalysis?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

##  Executive Summary
New anti-obesity medications (GLP-1 agonists like Wegovy) offer a clinical breakthrough, but do they reach the patients who need them most? This project integrates pricing data, Census income statistics, and CDC obesity prevalence to visualize the **"Affordability Gap"** across 50 states and 5 education levels.

The analysis reveals a systemic paradox: The states with the highest obesity rates (the South and Midwest) are statistically the least likely to afford the medication. In many low-income states, the monthly cost of treatment exceeds the federal definition of **"Catastrophic Health Expenditure"** (>10% of total income), and this financial barrier is compounded by a lack of Medicaid coverage in the hardest-hit regions.

---

##  Key Insights

### Act 1: The Geography of Need
* **Observation:** Obesity prevalence is not randomly distributed; it is heavily concentrated in the Southern U.S., with rates exceeding 35% in states like Mississippi, West Virginia, and Arkansas.
* **Implication:** Demand is highest in regions with historically lower median household incomes.

### Act 2: The Economic & Policy Wall
* **The "Wedge" Effect:** There is a strong inverse correlation between need and affordability. In the lowest-income states, the list price of treatment consumes **over 27% of a median household's monthly income**—nearly matching the cost of a mortgage.
* **The Medicaid Gap:** The dashboard highlights a critical policy failure: States with the highest "Cost Burden" are predominantly states that have **not** expanded Medicaid coverage for anti-obesity drugs (Visualized by the Orange lines vs. blue lines).

### Act 3: The Education Trap
* **Demographic Determinants:** Obesity rates show a strict gradient based on education. Populations with less than a high school diploma have the highest disease prevalence (~35-40%) but possess the fewest economic resources to access the care they need.
* **Systemic Barrier:** This confirms that the barrier is structural (socioeconomic status) rather than behavioral.

---

##  Methodology

### 1. Data Sourcing
* **Health:** CDC BRFSS (Behavioral Risk Factor Surveillance System) – Obesity prevalence by state and demographic group.
* **Economics:** U.S. Census Bureau (ACS 5-Year Estimates) – Median Household Income by state.
* **Pricing:** Wegovy – Analysis of GLP-1 list prices (Wegovy benchmark) and discounted cash prices.
* **Policy:** State Medicaid coverage policies for weight-loss medications.

### 2. Data Cleaning & Preparation (Python)
* **Structure:** Standardized state names across disparate datasets (CDC uses full names, some pricing data used abbreviations).
* **Aggregation Fix:** The raw CDC data contained overlapping subgroups (Total + Male + Female). These were filtered to prevent double-counting population statistics.
* **Joins:** Merged `GLP1_State_Master` (Income/Price) with `GLP1_Demographics` (Obesity Rates) on the State key.

### 3. Tableau Architecture
**Key Calculated Fields:**
* **`Burden_Pct_List_Price`:** Calculated the monthly cost as a percentage of monthly median income to determine the "Catastrophic" threshold.
    ```tableau
    SUM([List_Price]) / (SUM([Median_Household_Income]) / 12)
    ```
* **`Burden_Pct_Cash_Price`:** Calculated the monthly cost as a percentage of monthly median income to determine the "Catastrophic" threshold.
    ```tableau
    SUM([List_Price]) / (SUM([Median_Household_Income]) / 12)
    ```

---

##  Data Dictionary

| Field Name | Description | Source |
| :--- | :--- | :--- |
| **State** | Geographic identifier (50 U.S. States). | Master |
| **Obesity_Rate** | The prevalence of obesity (BMI > 30) as a percentage of the adult population. | CDC |
| **Median_Household_Income** | The median annual income for a household in that state. | Census |
| **List_Price** | The monthly cost of Wegovy (Semaglutide) without insurance. Benchmark: ~$1,349. | Wegovy |
| **Cash_Price** | The average discounted monthly cost available via coupons/cash payment. | Wegovy |
| **Cost_Burden_Pct** | The drug cost expressed as a % of monthly household income. | Calc |
| **Medicaid_Coverage** | Boolean (Yes/No) indicating if state Medicaid covers weight loss drugs. | Policy |
| **Education_Group** | Demographic breakdown (Less than HS, HS Grad, Some College, College Grad). | CDC |

---

##  Skills Demonstrated
* **Python for Data Engineering (ETL):**
    * Developed a reproducible data pipeline using `pandas` to ingest raw CSVs from disparate sources (CDC, Census, BRFSS).
    * Implemented data cleaning scripts to handle string normalization (State name matching), filter redundant demographic rows, and aggregate gender-split data.
    * Performed left-joins to merge economic indicators with health outcomes, creating a unified master dataset for analysis.
* **Health Equity Analysis:** translating complex socioeconomic datasets into a narrative about access and privilege.
* **Advanced Tableau Visualization:**
    * **Cleveland Dot Plots (Dumbbell Charts):** To visualize the gap between two metrics (Price vs. Income).
    * **Scrollytelling Architecture:** Designing a long-form vertical dashboard that guides the user through a narrative arc.
* **Data Modeling:** Handling one-to-many relationships between State-level economic data and granular demographic data.

---

##  Next Steps
* **Factor in Temporary Programs:** The current administration has proposed a plan that will lower the prices of Ozempic and Wegovy to $350 per month when purchased through *TrumpRX*. Whether this plan is realistic remains to be seen.
* **Insurance Layer:** Add a layer for "Commercial Insurance Coverage" to compare public vs. private access. Data on private insurance plans is not readily available.  
* **Demographic Analysis:** Expand the analysis to examine which groups of Americans are impacted most by the current pricing model. Groups could include race, sex, and age. 