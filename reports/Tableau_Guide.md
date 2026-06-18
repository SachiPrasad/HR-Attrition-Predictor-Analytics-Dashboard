# Tableau HR Analytics Dashboard Guide

This guide details how to build the interactive HR Analytics dashboards in Tableau using the exported CSV dataset: `dataset/cleaned_employee_attrition.csv`.

---

## 1. Connecting Data
1. Open Tableau (Desktop or Public).
2. Under **Connect / To a File**, select **Text File**.
3. Choose the exported file `cleaned_employee_attrition.csv`.
4. Go to **Sheet 1** to start building sheets.

---

## 2. Creating KPI Calculations
To show KPIs on the Executive Dashboard, create the following calculated fields:

- **Attrition Rate**:
  - Click the drop-down on the data pane and select **Create Calculated Field**.
  - Name it `Attrition Rate`.
  - Enter the formula:
    ```sql
    SUM(IF [Attrition] = 'Yes' THEN 1 ELSE 0 END) / COUNT([EmployeeNumber])
    ```
  - Right-click the newly created field, go to **Default Properties > Number Format**, and choose **Percentage** (1 decimal place).

---

## 3. Building Sheets for Dashboard 1 (Executive Summary)

### KPI Cards
- **Total Employees**: Drag the number of records or `EmployeeNumber` (change aggregation to Count) to **Text** on the Marks card.
- **Attrition Rate**: Drag the calculated `Attrition Rate` field to **Text** on the Marks card.
- **Average Salary**: Drag `MonthlyIncome` to **Text** and change its aggregation to **Average**. Format as Currency ($).
- **Average Age**: Drag `Age` to **Text** and change its aggregation to **Average**.

---

## 4. Building Sheets for Dashboard 2 (Attrition Analysis)

### Sheet A: Department vs Attrition (Grouped Bar Chart)
1. Drag `Department` to **Columns**.
2. Drag `EmployeeNumber` (Count) to **Rows**.
3. Drag `Attrition` to **Color** (on the Marks card).
4. In the Analysis menu, select **Percentage of > Cell** or use a table calculation to show percentages if you want relative distributions.

### Sheet B: Salary vs Attrition (Box Plot)
1. Drag `Attrition` to **Columns**.
2. Drag `MonthlyIncome` to **Rows**.
3. Change `MonthlyIncome` to a dimension (uncheck **Aggregate Measures** under the Analysis menu), or drag `EmployeeNumber` to **Detail** to disaggregate the marks.
4. Go to the **Analytics** pane on the left, drag **Box Plot** onto the view, and drop it.

### Sheet C: Overtime vs Attrition (Stacked Bar Chart)
1. Drag `OverTime` to **Columns**.
2. Drag `EmployeeNumber` (Count) to **Rows**.
3. Drag `Attrition` to **Color**.

### Sheet D: Job Satisfaction vs Attrition (Stacked Bar Chart)
1. Drag `JobSatisfaction` (ensure it is set as a Dimension) to **Columns**.
2. Drag `EmployeeNumber` (Count) to **Rows**.
3. Drag `Attrition` to **Color**.

### Sheet E: Age Group vs Attrition (Histogram)
1. Right-click `Age` in the Data pane, go to **Create > Bins**.
2. Set the bin size to `5` or `10`. Name the field `Age (Bins)`.
3. Drag `Age (Bins)` to **Columns**.
4. Drag `EmployeeNumber` (Count) to **Rows**.
5. Drag `Attrition` to **Color**.

---

## 5. Building Sheets for Dashboard 3 (Prediction Insights)

### Sheet F: Top Attrition Predictors
1. Connect to `dataset/feature_importances.csv` as a new data source.
2. Drag `Feature` to **Rows**.
3. Drag `Importance` to **Columns**.
4. Sort descending by clicking the sort icon on the toolbar.
5. Drag `Importance` to **Color** for a gradient look.

---

## 6. Assembly & Dashboard Formatting
1. Click the **New Dashboard** icon at the bottom.
2. Under **Size**, set to **Generic Desktop (1000x800)** or custom.
3. Drag sheet components onto the workspace. Use containers (Horizontal and Vertical) to organize cards and charts.
4. To add global filters, right-click any chart in the dashboard, select **Filters**, and choose a dimension (e.g. `Department`, `Gender`, `JobRole`).
5. Select the filter drop-down, choose **Apply to Worksheets > All Using This Data Source** to make the filter interactive across all charts.
