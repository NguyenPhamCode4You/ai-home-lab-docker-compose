# BVMS Voyage Bunker Management and Emission Compliance (ETS and Fuel EU)

## 1. Introduction

This document outlines the comprehensive fuel management feature of BVMS, focusing on fuel planning, emission calculations, and compliance with European Union environmental regulations (EU ETS and FuelEU Maritime).

## 2. The Two-Phase of a Voyage

#### **The Estimate Phase (Chartering)**

- **Objective:** Rapid assessment of voyage profitability and competitive pricing for clients
- **Process:** High-level fuel planning focused on total consumptions & costs
- **Target:** Quick price quotations based on total fuel requirements
- **Limitations:** May not account for realistic senerio when the voyage actually happen.

#### **The Voyage Phase (Operations)**

- **Objective:** Real-world execution of voyage for cost efficiency and compliance
- **Process:** Daily monitoring / updating of voyage data
- **Responsibility:** Converting profitable estimates into feasible operational journeys
- **Focus:** Detailed bunker planning ensuring adequate fuel of correct types throughout the voyage

## 3. Advanced Bunker (Fuel) Management

Bunker fuel represents the largest operational cost component, requiring sophisticated management strategies for profitability and compliance.

### 3.1 Bunker Types

| **Fuel Category** | **Type**                          | **Common Name** | **Key Characteristics**                                                                                                                 |
| :---------------- | :-------------------------------- | :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| **Fossil Fuels**  | MGO (Marine Gas Oil)              | Clean Oil       | Low sulfur content. Mandatory in Emission Control Areas (ECAs). Higher cost, lower emissions.                                           |
|                   | VLSFO (Very Low Sulphur Fuel Oil) | Dirty Oil       | Higher sulfur content for open seas. More economical than MGO.                                                                          |
| **Biofuels**      | Bio-MGO / Bio-VLSFO               | Green Oil       | Plant-based renewable fuels. Significantly lower greenhouse gas emissions. 2-3x more expensive than fossil fuels. Lower energy density. |

### 3.2 Strategic Bunker Planning

#### **Shortage Identification**

The system continuously monitors "Remaining on Board" (ROB) fuel for each itineraries, spotting deficits at specific voyage points where vessels will exhaust any particular fuel types.

#### **Bunker Order Creation**

When deficits are identified, Operations teams initiate bunker orders through a structured process:

1. **Market Research:** Contact suppliers at various ports along the route to choose the best options
2. **Route Integration:** Add refueling stops to vessel itinerary to get the ordered bunkers
3. **Order Lot Creation:** System auto generate bunker lots for each bunker item ordered, that go into the bunker planning phase.

### 3.3 Bunker Lot Management

Maritime fuel management utilizes a "lot-based" tracking system where fuel is segregated into distinct parcels within vessel tanks.

#### **Lot Characteristics**

Each fuel lot contains:

- **Quantity:** Precise tonnage measurements
- **Purchase Price:** Individual cost basis for accurate accounting
- **Fuel Type:** Specific classification (VLSFO, MGO, Bio-variants)

#### **Consumption Logic**

- **FIFO Logics:** First-In, First-Out (FIFO) consumption based on expiry dates
- **Manual Priority:** Operations teams can drag-and-drop bunker lots to optimize consumption priority
- **Cost Calculation:** Weighted average pricing when consumption spans across multiple lots

#### **Example Scenario**

Consider a vessel with two VLSFO lots:

- **Lot 1:** 241 tons @ $542/ton
- **Lot 2:** 200 tons @ $500/ton

If voyage requires 40 tons VLSFO:

- **Default consumption:** Use Lot 1 first → Cost reflects $542/ton
- **Optimized consumption:** Reorder to use Lot 2 first → Cost reflects $500/ton

### 3.4 Operational Aspects: Chartering vs Operations

| **Aspect**               | **Chartering**                           | **Operations**                                   |
| :----------------------- | :--------------------------------------- | :----------------------------------------------- |
| **Focus**                | Total fuel costs for pricing             | Detailed execution feasibility                   |
| **Planning Depth**       | Aggregate total consumption              | Lot-level tracking and management                |
| **Route Considerations** | Usually dont plan for fueling itenraries | Strategic refueling itenraries to optimize costs |
| **System Integration**   | Simplified fuel calculations             | Complex bunker order workflows                   |

## 4. EU Emission Regulations Framework

European maritime operations are subject to two major environmental compliance systems, each with distinct mechanisms and financial implications.

### 4.1 EU Emissions Trading System (EU ETS)

#### **Core Principle**

ETS implements a direct carbon pricing mechanism based on total CO₂ emissions released into the atmosphere during vessel operations within European waters.

#### **Calculation Methodology**

```
ETS Cost = Fuel Consumed × Emission Factor × Regional Scope × Phase-in Factor × EUA Price
```

**Component Breakdown:**

| **Component**        | **Description**              | **Values**                                                                       |
| :------------------- | :--------------------------- | :------------------------------------------------------------------------------- |
| **Emission Factors** | CO₂ produced per fuel ton    | VLSFO: ~3.1 tons CO₂/ton fuel<br>MGO: ~3.2 tons CO₂/ton fuel                     |
| **Regional Scope**   | Coverage percentage by route | EU-to-EU: 100%<br>EU-to-non-EU: 50%<br>Non-EU-to-EU: 50%<br>Non-EU-to-non-EU: 0% |
| **Phase-in Factor**  | Gradual implementation       | 2024: 70%<br>2025: 80%<br>2026+: 100%                                            |
| **EUA Price**        | Market rate per CO₂ ton      | Current: ~€85 ($85)                                                              |

#### **Geographic Application**

- **Full Coverage:** Voyages between European Union ports
- **50% Coverage:** Voyages with one EU port (arrival or departure)
- **No Coverage:** Voyages entirely outside EU waters

### 4.2 Fuel EU Maritime Initiative

#### **Regulatory Objective**

FuelEU Maritime targets greenhouse gas (GHG) intensity reduction by establishing maximum emission limits per unit of energy consumed, driving adoption of cleaner fuel alternatives.

- **Core Mechanism:** It sets an annual GHG intensity target (e.g., 89.3 gCO2/MJ for 2025). This target becomes stricter each year.
- **Compliance Balance (Deficit vs. Surplus):**
  - **Deficit:** Using fossil fuels, which have a high GHG intensity (~90-94 gCO2/MJ), means the vessel operates **above** the target, creating a compliance deficit.
  - **Surplus:** Using biofuels, with a lower GHG intensity (~70-80 gCO2/MJ), means the vessel operates **below** the target, generating a compliance surplus.
- **Annual Reckoning:** The balance is tracked per voyage but is aggregated for the entire ship (or a company's fleet) over the full year. A net deficit at year-end results in a financial penalty.

#### **Fuel GHG Intensity Values**

| **Fuel Type**    | **GHG Intensity** | **Compliance Status**              |
| :--------------- | :---------------- | :--------------------------------- |
| **Fossil Fuels** |
| MGO              | ~90g CO₂/MJ       | Exceeds targets (deficit creation) |
| VLSFO            | ~91g CO₂/MJ       | Exceeds targets (deficit creation) |
| **Biofuels**     |
| Bio-MGO          | ~76g CO₂/MJ       | Below targets (surplus generation) |
| Bio-VLSFO        | ~76g CO₂/MJ       | Below targets (surplus generation) |

#### **Compliance Balance System**

```
Compliance Balance = (Target GHG Intensity - Actual GHG Intensity) × Total Energy Consumed
```

- **Positive Balance:** Surplus credits from using cleaner fuels
- **Negative Balance:** Deficit requiring compliance action
- **Annual Reconciliation:** Company-wide balance assessment at year-end

### 4.3 Fuel EU Compliance Strategies

#### **Strategy 1: Biofuel Utilization**

- **Benefits:** Direct emission reduction, surplus credit generation
- **Challenges:**
  - Cost premium: 2-3x fossil fuel prices
  - Limited availability and supply chain constraints
  - Lower energy density requiring larger storage volumes
- **Application:** Strategic deployment on specific voyages to offset overall fleet deficits

#### **Strategy 2: Pooling System (Recommended Default)**

- **Concept:** Market-based credit trading between vessel operators
- **Mechanism:** Purchase surplus credits from compliant vessels
- **Default Pricing:** ~$185 per ton CO₂ equivalent (significantly below penalty rates)
- **System Logic:** Most cost-effective compliance method for deficit vessels
- **Market Dynamics:** New vessels with mandatory biofuel usage typically generate surplus credits

#### **Strategy 3: Penalty Payment (Last Resort)**

- **Rate:** ~$1,000 per ton CO₂ equivalent deficit
- **Business Impact:** Direct operational cost increase affecting voyage profitability
- **Usage:** Only when pooling options unavailable or economically unviable

### 4.4 Financial Impact Analysis

#### **Cost Structure Comparison**

| **Compliance Method** | **Typical Cost per Ton CO₂** | **Business Advantages**              | **Limitations**                            |
| :-------------------- | :--------------------------- | :----------------------------------- | :----------------------------------------- |
| Biofuel Usage         | $300-900 (fuel premium)      | Direct emissions reduction           | Supply constraints, operational complexity |
| Pooling Purchase      | $185 (market rate)           | Cost-effective, operationally simple | Market availability dependency             |
| Penalty Payment       | $1,000 (regulatory fine)     | Certainty, no operational changes    | Highest cost, regulatory risk              |

## 5. System Integration and Operational Procedures

### 5.1 Fuel Type Requirements by Operating Zone

#### **Clean vs Dirty Fuel Usage**

- **Emission Control Areas (ECAs):** Mandatory MGO or Bio-MGO usage
- **Open Waters:** VLSFO or Bio-VLSFO permitted
- **Route Planning:** System automatically determines fuel type requirements based on itinerary

#### **Fuel Consumption Calculation**

The routing system provides detailed breakdown:

- **Total Distance:** Complete voyage mileage
- **ECA Distance:** Miles requiring clean fuel
- **Open Water Distance:** Miles permitting dirty fuel
- **Fuel Allocation:** Automatic calculation of fuel type requirements per segment

### 5.2 Financial Impact of Fuel Consumptions:

Cost Components:

1. **Fuel Costs**: Prices for different fuel types
2. **ETS Penalties**: Based on total CO₂ emissions
3. **Fuel EU Penalties**: Based on GHG intensity exceedance
   - **Penalty**: Pay directly the penalty for exceeding GHG intensity target
   - **Biofuel Premium**: Extra cost for using biofuels, but dont pay penalty
   - **Pooling Costs**: Co2Eq Credit purchases for reaching compliance

## Conclusion

The maritime industry faces increasing environmental regulations requiring sophisticated fuel management and emission compliance systems. Success depends on:

- **Precise Fuel Planning**: Ensuring adequate fuel while optimizing costs
- **Emission Monitoring**: Real-time calculation of regulatory compliance
- **Strategic Decision Making**: Balancing biofuel costs against penalty payments
- **System Integration**: Coordinating voyage planning with environmental compliance

Organizations must invest in comprehensive systems that manage both operational efficiency and environmental compliance to remain competitive in the evolving regulatory landscape.
