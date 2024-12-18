# Operation Module

# Fuel Zone Setup

- The Fuel Zones is used to specify estimated low sulfur consumption for different ECA Fuel Zones.

### Fuel Zones for Port

**Fuel Grades Consumed in LS Port:**

| Port Type                                            | Configuration               | Fuel Grades Consumed                     |
| ---------------------------------------------------- | --------------------------- | ---------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------- |
| **Not Low Sulfur**                                   | -                           | G and H                                  |
| **Low Sulfur**                                       | Without Configuration flags | All L grades                             |
| **Low Sulfur**                                       | Without Allow `<1% IFO`     | With `CFGLSPortConsumptionDefaultGrades` | L grades specified in `CFGLSPortConsumptionDefaultGrades` |
| **Low Sulfur**                                       | With Allow `<1% IFO`        | With `CFGLSPortConsumptionDefaultGrades` | Without `CFGLSPortConsumptionLSFOGrades`                  | L grades specified in `CFGLSPortConsumptionDefaultGrades` |
| **Low Sulfur**                                       | With Allow `<1% IFO`        | With `CFGLSPortConsumptionLSFOGrades`    | L grades specified in `CFGLSPortConsumptionLSFOGrades`    |
| **Configuration flag with grades not on the vessel** | -                           | No L grades                              |

---

## Fuel Zones for ECA

- **ECA-AUSTRALIA**
- **ECA-BRAZIL**
- **ECA BOHAI SEA**: A zone contained under the **China ECA** zone for propulsion.
- **ECA-CHINA**:
  - When using this fuel zone, set **YANGTZE RIVER DELTA** and **YANGTZE RIVER DELTA 10OCT18** as inactive.
  - **ECA-CHINA** incorporates these zones, and keeping them active will cause duplicate passing points in the itinerary.
- **ECA-KOREA PORTS**
- **ECA-MALAYSIA**
- **ECA-MEDITERRANEAN**
- **ECA-SUEZ CANAL**
- **ECA-TAIWAN**
- **ECA-YANGTZE INNER RIVER**
- **HAWAII 200NM**
- **ICELAND**
- **NORTH SEA**
- **PANAMA CANAL**
- **PUERTO RICO 200NM**
- **USA 200NM**
- **USA 24NM**
- **WORLDWIDE**:
  - This zone is used to set the Fuel Types to be consumed in ports not located in any of these Fuel Zones but have the **Low Sulfur ECA** check box selected.
  - Includes any historic Estimates created without Fuel Zone information.
  - Should include only Fuel Types used for low sulfur consumption before configuring Fuel Zones.
    - Avoid using **cons rate only**; otherwise, consumption rates and types will change for Estimates/Voyages created before Fuel Zones were enabled.
- **YANGTZE RIVER DELTA**
- **YANGTZE RIVER DELTA 1OCT18**

# ECA Routing for Voyage

## Setting ECA Routing

- On the **Estimate** (column or details) or **Voyage Manager**, set ECA Routing:

  - **Default**: Uses the vessel's default routing preferences specified on the Routes tab in the Vessel form.
  - **Disabled**: Uses the most direct route.
  - **Enabled**: Reroutes around all ECA zones.

- On the **Estimate**, **Voyage**, or **Distances map**, select **Minimize ECA Routing**.

- In **Distances Map Settings**, there is a **Minimize ECA** check box. When selected, routes will be calculated to minimize travel through ECA Zones.

- If a port is located within a Fuel Zone, its name appears on the **Properties** panel.
  - A port is assigned to the smallest Fuel Zone within which it is located.
    - For example: HUENEME is assigned to the **USA 25NM zone**, but it is also located in **US 200NM**.

# Bunker Planning

### Key Features

- Proposes bunker prices based on purchase history.
- Consumption calculated per port and sea leg based on vessel-specific parameters.
- Includes heating, cooling, reliquefaction, and idle consumption considerations.

### Optimization Tools

- **Optimize Liftings for Cargo**: Calculates optimal bunker quantities based on price and freight rate trade-offs for cargo.
- **Real-Time Adjustments**: Automatically updates bunker quantities based on price changes until voyage estimate is finalized.

### Specialized Options

- **Use Scrubbers**: Allows high-sulfur fuel consumption within ECA zones while adhering to fuel zone configurations in port.
- **Fuel Zones**: Enables recalculation of bunker consumption and costs based on Fuel Zones.

### Limitations

- Optimizer only for planning purposes
- Fuel consumption calculations rely on pre-configurations

# Bunkers Expense Calculation Method

You buy 1,000 MT of IFO at $400 (= $400,000), then 600 MT at $500 (= $300,000). You consume 700 MT on a voyage. How are costs allocated to the voyage?

- **AVE = Average method**: The weighted average cost is **(Total Initial Bunker Cost + Total Lifted Bunker Cost) / (Initial Qty + Lifted Qty)**. In this scenario, $700,000 / 1600 = $437.50/MT. Multiplied by 700, your voyage bunker expense is $306,250. Many companies use this method, but it is not fair if bunker prices are high during a voyage when that voyage might not even use those bunkers.
- **TBM = Tramper Business Method**: With this method, you buy all the inventory at the beginning of the voyage and sell all at the end, so you know the exact cost for the voyage. The consumption is calculated. You might use this method for a Time Charter In or Out that is delivered and redelivered with the same amount, or if you just want to override all values.
- **FIFO = First In First Out** (default for new Voyage Estimates and Fixtures): FIFO treats bunkers as an asset and depletes the first asset before going on to the next. Starting with the oldest, you use 700 MT at $400/MT, for a total cost of $280,000. This is the most common method.
- **LIFO = Last In First Out**: Starting with the most recent, you use all 600 MT at $500/MT (= $300,000) and 100 MT at $400/MT (= $40,000), for a total cost of $340,000. The reason for using this method is that it defers revenues when prices are going up, so you can maximize expenses currently and defray savings until later, for a tax advantage.



As the voyage progresses, you might buy more fuel; if you do not use it on this voyage, it does not affect this voyage's costs.

If you change the voyage, the change in fuel needed is estimated. When the voyage is completed, and the **Completed** check box is selected, the accounts can be reconciled.

# Create New Voyage

When you open the Create New Voyage form, some fields might be completed. Complete the remaining fields according to the voyage.

- **Note:** You cannot reuse Vessel/Voy No. combinations.

## Voyage Type

Type of voyage being scheduled. The following default types are available:

- **OVOV**: Owned Vessel, Own Voyage
- **OVTO**: Owned Vessel, TC Out
- **RELT**: Cargo Relet
- **SPOT**: Charter of Vessel for Single Voyage
- **TCOV**: TC In Vessel, Own Voyage
- **TCTO**: TC In Vessel, TC Out
- **VCOV**: VC In Vessel, Own Voyage (must be enabled for you by Veson Nautical)

**Note:**  
Time Charter contracts and Fixtures must be specified for Time Charter Opr Type voyages and cannot be removed once the voyage has been scheduled.

## Consecutive Voyage
Of course, you do not start a voyage empty, so previous inventory is also taken into account; this is a continuous process. For that reason, you want to set this option once and not change it, even though there might be an advantage one way or another if the market goes up or down.

Select this check box if there is already a previous voyage for the vessel. The following apply:

- The completing date of the previous voyage becomes the commencing date of the new voyage (displayed in the **Commencing** field).
- The last port of the previous voyage becomes the commencing port of the next voyage.
- The ending bunker inventory of the previous voyage becomes the beginning bunker inventory of the next voyage.

## Initial Bunkers

After creating a non-consecutive voyage, the **Initial Bunkers** form appears to track bunker inventories. Enter the appropriate **Quantity** and **Price** information for each fuel type. This is particularly useful for voyages using the FIFO bunker calculation method.

- If you do not know these values at scheduling, adjust Initial Bunkers later from the **Voyage Bunkers** form.
- After closing the form, the voyage appears.

## Backup Bunkers

- Within the voyage bunkers, make sure there is enough Primary fuel to complete the voyage.
- If there is not, the system with calculating with a backup fuel unless there is not enough fuel for the backup Fuel to complete the voyage or the disable backup fuel checkbox has been selected.
- In this case, the system will have the Primary fuel consume the entire voyage and the backup fuel quantity will be untouched.

# Voyage Functional Tools

- **Estimate**: Open the Estimate module to manage voyage estimates.
- **Freight**: Access the Freight Invoice or Expenses Rebill Management.
- **Commission**: View and manage:
  - Freight/Relet Commission
  - TC In or Out Commission
  - Claim Commission Payments
- **Other Rev/Exp**: Open the following modules:
  - Voyage Other Revenues and Expenses
  - Rebills for Off Hire and Port Expenses (enabled by configuration flag **CFGRebillForOffhire**)
  - Deviation Analysis
  - Profit Share
- **Laytime**: Access tools related to laytime, including:
  - Estimated Demurrage
  - New Laytime Calculation Setup
  - Laytime Notes (to record notes related to the Laytime Calculation)
- **Delays**: Open the Delay module.
- **Bunkers**: Manage voyage bunkers:
  - Open Voyage Bunkers
  - Access Bunker Liftings
  - Add fuel types from the vessel that are not already present in the voyage.
- **Reports**: Generate and access:
  - Voyage Reports
  - Voyage XML Export

# Voyage PL

### Estimated

- **Source**: Derived from the Estimate that initiated the voyage. If no Estimate exists, these figures are calculated from the initial voyage data.
- **Purpose**: Serves as the baseline for expected revenues and expenses.

### Actual

- **Initial Population**: Estimated figures transfer to Actual upon voyage scheduling, reflecting the best available knowledge at the time.
- **Updates**: Changes during the voyage, such as deviations or adjustments in bunker consumption, update the Actual column. Updates continue until the **Voyage Status** is set to Completed.
- **Discrepancies**: Differences between Estimated and Actual can occur if data is altered on the Voyage Fixture or before the voyage begins (e.g., different commencing port).

### Posted

- **Definition**: Contains amounts posted to P&L via the Transaction Data Entry form.
- **Exclusions**: Proforma port expense invoices appear in Actual but are not included here since they are typically posted to Balance Sheet accounts.

### Cash

- **Definition**: Reflects payments and receipts related to the amounts listed in the Posted column.

### Variance

- **Act - Est**: The difference between Actual and Estimated values.
- **Act - Est %**: \((\text{Act} - \text{Est}) / |\text{Est}|\), ensuring consistency in variance interpretation when values are negative.
- **Act - Pst**: The difference between Actual and Posted values.
- **Act - Pst %**: \((\text{Act} - \text{Pst}) / |\text{Act}|\), ensuring consistency in variance interpretation when values are negative.

---

# Snapshot and Period Comparison

### Snapshot Comparison

- **Basis (Default: Actual)**: Displays Actual values from the selected Basis snapshot. Snapshot dates appear under the column title when a selection other than Actual is made.
- **Compare (Default: Posted)**: Displays values from the selected Compare snapshot. The column title changes to Compare, with the snapshot's short name under it.

### Period Comparison

- **Selection**: Allows monthly accrual-based comparison. Estimated and Actual values are prorated to the selected month's end, while Posted and Cash columns reflect full transactions until that date.

---

# Revenues and Expenses

### Structure

- Organized in a tree format, with Revenues and Expenses as main categories. Running Costs can appear as a separate category if enabled by a configuration flag.
- **Details**: Expand items to view calculations or related invoices. Invoice Numbers link directly to their respective invoices.

### Totals

- **Voyage Result**:

  - **Net Daily (TCE)**: \[
    \text{Net Daily (TCE)} = \frac{\text{Net Income} - (\text{Total Expenses} - (\text{Vessel Expenses} + \text{Ballast Bonus} + \text{TC In Common Voyage Expenses} - \text{Address Commission}))}{\text{Voyage Days}}
    \]
  - For Type G (Gas Carrier) vessels, **Net Monthly (TCE)** is also displayed.

- **Profit (Loss)**:

  - Market Profit (Loss): Calculated if a Market Hire value is provided.
  - **Net Voyage Days**: Total Voyage Days minus Off Hire Days and Waiting Days.
    - **Important**: Continuous Off Hire requires exact "To" and "From" time matching to avoid calculation errors.

- **Daily Profit (Loss)**:
  - Reflects profit/loss with adjustments for Profit Sharing, Waiting for Laycan, and Waiting for Orders (if applicable).

---

# P&L Calculation Options

P&L calculation options are available when you have enabled the configuration flag `CFGShowPNLCalcOptions`. By selecting these options, you can modify certain areas of the P&L calculation, typically using a pro-rata calculation or a more specific calculation for certain values.

With the **Modify P&L Calculation Options Module Right** selected under **Financials Actions in Security**, you can toggle the P&L calculation options on the **Monthly Accruals**, **Voyage Period Journals**, and **Voyage P&L Summary Report** forms. Without it, you can only use these forms with the P&L Options as set by the configuration flags beginning with **Default P&L Calc**.

## Option Descriptions

Each of the following options has one or more possible configurations; for more information, see **Related Configuration Flags** on this page. These flags can be used to set the default states of the checkboxes.

If no P&L calculation options are changed from their defaults, all P&L items will be calculated according to configuration flag settings. Off Hire will be included in voyage duration and thus reflected in the Portion %.

### Option List

| Option                                   | Description                                                                                                                                              |
|------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Apply TC Hire to Period**              | TC Hire will not be prorated; instead, TC Hire will be calculated based on the hire rate and actual voyage days in the period. CVE and commissions will be applied only to the period in which they occur. In Monthly Accruals, TC Commission will be applied to period when set as a percentage of the Hire in the contract. |
| **Apply Additional Hire to Period**      | For Time Charter voyages, 100% of an XHIRE (additional hire) amount is allocated to period based on TCIP (Time Charter In Payment) or TCOB (Time Charter Out Bill) Invoice Date. |
| **Apply Off Hire/Waiting to Period**     | Off Hire will be allocated to the actual period, that is, full deduction of Off Hire in the period when the Off Hire occurred.                            |
| **Apply Ballast Bonus to Period**        | Ballast Bonus and Ballast Bonus Commission for TCI and TCO will be allocated to period of voyage commencement. The P&L Period Range will begin before the voyage commences. |
| **Apply TC Bunker Adjustment to Period** | For Time Charter voyages, 100% of a Bunker Adjustment amount is allocated to period based on operations ETA for delivery (TCO) or redelivery (TCI). For Time Charter Out Voyages, if the TCO Contract is set to Bunkers on Consumption, the Bunker Adjustment will be allocated to the period containing the departure from the Z port. |
| **Apply TC Expenses to Period**          | For TCIP and TCOB INTHC (Intermediate Hold Cleaning), ILOHC (In Lieu of Hold Cleaning), and VOYEX (Voyage Expenses), 100% of the line item amount is allocated to period based on the Invoice Date of the invoice in which it is included. Items included on incremental invoices will still be allocated based on their original invoice's date. |
| **Apply Bunker Consumption to Period**   | Bunker expense will not be prorated but calculated based on the actual consumed amount in the period.                                                    |
| **Apply Other Revenues/Expenses to Period** | For invoice types VEXP (Voyage Other Expense, Lumpsum) and VREV (Voyage Other Revenue, Lumpsum), 100% of the invoice amount, including linked non-freight rebills, is allocated to period based on a specific date, determined by configuration. |
| **Apply Port Expenses to Period**        | 100% of a Port Expense amount, including linked non-freight rebills, is allocated to period based on a specific date, determined by configuration.         |
| **Apply Demurrage to Period**            | When this option appears on a form, its effect depends on the values of configuration flags `CFGDefaultPnlCalcApplyDemurrage` and `CFGDefaultPnlCalcAdjustForDemurrageDays`; for more information, see **Compliance with IFRS 15 & 16 Regulations**. |
| **Apply TC Rebills to Period**           | When this flag is enabled, any TC Rebill line items will be recognized in the month of the accounting date of the original expense item when that expense is posted. When the original expense is not yet posted, the TC Rebill item will be recognized in the month of the invoice date of the original expense item. |
| **Adjust Portion for Demurrage Days**    | The portion percentage for other P&L items is adjusted based on the demurrage days in the period.                                                         |
| **Adjust Portion for Off Hire**          | Off-hire time is considered when determining the percentage. For example, if you have a 2-month voyage, and it is off-hire for the entire first month, the voyage will be considered 0% complete after the first month and 100% after the second month. If the check box is cleared, the system will consider the voyage 50% complete after the first month and 100% complete after the second month. |
| **Adjust Portion for Waiting Time**      | Waiting Time is considered when determining the percentage. For example, if you have a 2-month voyage, and it is waiting for the entire first month, the voyage will be considered 0% complete after the first month and 100% after the second month. If the check box is cleared, the system will consider the voyage 50% complete after the first month and 100% complete after the second month. |
| **Adjust Portion for Ballast Days**      | Load-to-discharge or delivery-to-redelivery is used as P&L recognition basis when the check box is selected. Otherwise, the full voyage duration is used as the basis. Voyage revenues and expenses will be allocated within the L/D period (for voyage charters) or Y/Z period (for TC Out voyages). Note that this does not impact revenues/expenses that are applied to the period; these will still be allocated to the period in which they were incurred. |
| **Reconcile Bunker ROB for Current Voyages** | Accrual includes ROB rows up until the accrual period with new bill codes of the format ROB_FuelType in current voyages. The accrual basis is based on the ROB from the most current Activity Report in the accrual period rather than based on bunker planning estimation. |
| **Exclude Running Costs for Long Term TCI/OV** | There will be no accrual for Running Cost on OV vessels and vessels on Long Term TCI contract.                                                              |
| **Exclude Hire Related Items for Long Term TCO** | For long-term Time Charter Out contracts (which is something that can only be defined via inter-company mirroring), exclude hire-related items, such as Hire, Off Hire, CVE, Hire Commissions, Off Hire Commissions, and Off Hire CVE, from P&L calculations. |
| **Accrue Linked Trades Upon Settlement** | Only settled periods of trades linked to the Voyage P&L will be included in Monthly Accruals; exposed periods will be excluded.                           |
| **Prorate Freight Revenue on a Per Cargo Basis** | When selected, the accruals program will use the BL Date for the individual cargo(s) and the BL qty for the cargo to calculate the accrual percentage and amount to accrue for freight when there are multiple cargoes on the voyage. |
| **Apply Internal Freight Revenue to Period** | When selected, freight revenue with an internal counterparty on the voyage, excluding demurrage, will be 100% allocated to the period based on the BL Date for the contract. Demurrage will still be allocated according to the Apply Demurrage to Period option. |
| **Accruals for Closed Voyages**           | When selected, the system will run accruals only for voyages that are marked as Closed during the specified Accrual Month.                                  |
| **Capitalize/Amortize Costs Prior to Performing Period** | When selected, the costs incurred between the Nomination Date and the Start of the First Load port will be capitalized and then amortized over the performing period as defined by the Start of First Load to the end of Last Discharge on the voyage. |
| **Apply Carbon Expenses to Period**      | When selected, this will look at the actualized emissions recorded on the voyage based on the bunker consumption details actualized on the voyage and accrue based on that information instead of prorating across the voyage. |

---

# Apply & Adjust Portion Off Hire Calculation

When it comes to reporting hire in the month-end accruals, there are four ways in which the system accounts and adjusts for off hire. Depending on the P&L Calculation Options chosen for off hire related calculations, the following are the four scenarios:

- **No Options Selected**
- **Apply Off Hire / Waiting to Period Selected**
- **Adjust Portion Off Hire Selected**
- **Both Apply and Adjust Portion Off Hire Selected**

### Assumptions:
- Accrual is run for July 2020 Month End.
- This is an ongoing voyage where off hire occurred entirely in the month of July 2020.

## Scenarios

### No Options Selected
By default, the system will take the total net hire and prorate it. 

The general formula for prorating is:
- **Voyage Days Performed / Total Voyage Days**,  
Where **Voyage Days Performed** = No. of days sailed from Voyage Commencement to Accrual Month End Date (e.g. 31 July 2020).

When no option is selected, the system calculates based on the following logic:
- **(Total Hire - Off Hire) * (Voyage Days Performed / Total Voyage Days)**  
Where **Total Hire** = expected hire for the entire duration of the voyage.

### Apply Off Hire to Period
This option builds upon the earlier one. Instead of prorating net hire, the system will now allocate the full off hire deduction to the period in which it occurred. Since the off hire occurred in July, the full amount will be deducted from the accrued hire.

When **Apply Off Hire to Period** is selected, the system calculates based on the following logic:
- **[Total Hire * (Voyage Days Performed / Total Voyage Days)] - Off Hire**

#### Note:
- If the off hire crosses two months, the system will apply the amounts to each month according to the proportion in which they occurred.
- If the off hire took place outside of the period in which the accrual is run, there will be no off hire deducted. The formula will be:
  - **[Total Hire * (Voyage Days Performed / Total Voyage Days)] - 0**

### Adjust Portion Off Hire
For this option, the system will exclude the off hire entirely when performing accruals. Hence, it follows a different prorating logic.

Adjusted Prorate %:
- **(Voyage Days Performed - Off Hire Days) / (Total Voyage Days - Off Hire Days)**

With the above logic for Adjusted Prorate %, the system deducts the off hire from the total hire and then prorates it based on the following logic:
- **(Total Hire - Off Hire) * Adjusted Prorate %**

### Adjust Portion & Apply Off Hire
When both options are selected, the system will first perform an adjusted prorate and then deduct the off hire. 

The logic is as follows:
- **(Total Hire * Adjusted Prorate %) - Off Hire**

#### Note:
- If the off hire took place outside of the period in which the accrual is run, there will be no off hire deducted. The formula will be:
  - **(Total Hire * Adjusted Prorate %) - 0**

---



