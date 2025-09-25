# Maritime Fuel Management and EU Environmental Compliance

## Overview

This document outlines the comprehensive fuel management system for maritime vessels, focusing on fuel planning, emission calculations, and compliance with European Union environmental regulations (EU ETS and FuelEU Maritime).

## 1. Voyage Management System

### 1.1 Estimate vs Voyage

- **Estimate**: Initial target version used for rating and quotation purposes
- **Voyage**: Actual operational transaction with real data, created when an estimate is nominated
- **Operations Team**: Continuously monitors and updates voyage data to ensure profit margins remain acceptable

### 1.2 Voyage Planning Components

- **Itinerary**: Route planning with port locations and timing
- **Cargo Details**: Cargo lots and discharge information
- **Duration**: Total journey time and port stays
- **Fuel Requirements**: Critical for bunker calculations

## 2. Fuel (Bunker) Management

### 2.1 Fuel Types

#### Fossil Fuels

- **MGO (Marine Gas Oil)**: Clean fuel, more expensive, lower emissions
- **VLSFO (Very Low Sulfur Fuel Oil)**: "Dirty" fuel, cheaper, higher emissions

#### Biofuels

- **Bio-MGO**: Clean biofuel alternative
- **Bio-VLSFO**: Biofuel alternative to traditional VLSFO
- **Characteristics**:
  - More expensive (up to 3x cost of fossil fuels)
  - Lower CO₂ emissions
  - Less energy density than fossil fuels
  - Environmentally friendly

### 2.2 Fuel Planning Process

#### Bunker Tab Overview

- Displays fuel quantities at each port
- Shows "Remaining on Board" (ROB) calculations
- Tracks fuel consumption between ports
- Identifies fuel shortages requiring additional orders

#### Bunker Lot Management

- **Lot-Level Tracking**: Individual fuel batches with different prices and specifications
- **FIFO Usage**: First-in, first-out consumption based on expiry dates
- **Price Averaging**: Automatic calculation of weighted average prices
- **Order Sequence**: Configurable priority for fuel consumption

### 2.3 Bunker Order Process

1. **Shortage Identification**: System flags insufficient fuel levels
2. **Port Selection**: Choose optimal refueling locations based on price and availability
3. **Price Negotiation**: Contact port suppliers for quotations
4. **Order Creation**: Generate bunker orders with quantities and specifications
5. **Route Planning**: Integrate refueling stops into voyage itinerary

### 2.4 Key Differences: Chartering vs Operations

- **Chartering**: Simplified fuel calculations for pricing purposes
- **Operations**: Detailed fuel management ensuring voyage completion
- **Planning Depth**: Operations requires precise lot-level tracking and order management

## 3. EU Environmental Regulations

### 3.1 EU Emissions Trading System (ETS)

#### Core Concept

- **Principle**: Pay for total CO₂ emissions released into the environment
- **Scope**: All emissions within European waters
- **Calculation**: Based on fuel consumption and emission factors

#### ETS Calculation Method

```
Emission Factor × Fuel Consumed × Regional Factor × Phase-in Factor × Price per Ton
```

**Key Components:**

- **Emission Factors**:
  - VLSFO: ~3.1 tons CO₂ per ton fuel
  - MGO: ~3.2 tons CO₂ per ton fuel
- **Regional Factors**:
  - Europe to Europe: 1.0
  - Europe to Non-Europe: 0.5
  - Non-Europe to Europe: 0.5
  - Non-Europe to Non-Europe: 0.0
- **Phase-in Factor**: Gradually increasing (2024: 0.7, 2025: 0.8, eventually 1.0)
- **Current Price**: ~$85 per ton CO₂

### 3.2 FuelEU Maritime Regulation

#### Objective

Reduce CO₂ intensity by setting maximum greenhouse gas (GHG) emission limits per unit of energy consumed.

#### Key Metrics

- **2024 Target**: 89.3g CO₂ per megajoule (MJ) of energy
- **Annual Reduction**: Target decreases yearly to drive further emission reductions
- **GHG Intensity**: Measured in grams CO₂ per MJ

#### Fuel GHG Intensities

- **Fossil Fuels**:
  - MGO: ~90g CO₂/MJ (exceeds target)
  - VLSFO: ~91g CO₂/MJ (exceeds target)
- **Biofuels**:
  - Bio-MGO: ~76g CO₂/MJ (below target)
  - Bio-VLSFO: ~76g CO₂/MJ (below target)

#### Compliance Calculation

```
(Actual GHG Intensity - Target) × Total Energy Consumed × Fine Rate
```

### 3.3 Compliance Strategies

#### Strategy 1: Biofuel Usage

- **Benefits**: Lower GHG intensity, potential credit generation
- **Challenges**: Higher cost, limited availability
- **Impact**: Direct emission reduction at source

#### Strategy 2: Pooling System

- **Concept**: Purchase emission credits from vessels with surplus
- **Default Price**: ~$185 per ton CO₂ equivalent
- **Participants**: Newer vessels often generate credits due to mandatory biofuel usage
- **Benefits**: Cost-effective compliance without operational changes

#### Strategy 3: Penalty Payment

- **Last Resort**: Pay fines for non-compliance
- **Rate**: ~$1,000 per ton CO₂ equivalent excess
- **Business Impact**: Direct cost increase affecting voyage profitability

## 4. System Integration and Testing

### 4.1 Calculation Verification

- **Bunker Tab**: Overall fuel consumption summary
- **Bunker Lot**: Detailed batch-level consumption tracking
- **Cross-Validation**: Ensure lot totals match bunker tab figures
- **Route Integration**: Verify fuel requirements against route planning data

### 4.2 Emission Calculation Testing

- **ETS Verification**: Check regional factors and phase-in multipliers
- **FuelEU Validation**: Confirm GHG intensity calculations
- **Cost Impact**: Verify penalty calculations and compliance costs

### 4.3 Operational Considerations

- **Clean vs Dirty Fuel**: Route-based fuel type requirements
- **EU Waters**: Specific zones requiring clean fuel usage
- **Fuel Quality**: MGO for sensitive areas, VLSFO for open waters

## 5. Financial Impact

### 5.1 Cost Components

1. **Base Fuel Costs**: Procurement prices for different fuel types
2. **ETS Penalties**: Based on total CO₂ emissions
3. **FuelEU Penalties**: Based on GHG intensity exceedance
4. **Pooling Costs**: Credit purchases for compliance
5. **Operational Costs**: Additional port calls for refueling

### 5.2 Annual Compliance

- **Year-End Reconciliation**: All emissions and credits balanced annually
- **Fleet Management**: Company-wide emission trading and optimization
- **Regulatory Reporting**: Mandatory submission to EU authorities

## Conclusion

The maritime industry faces increasing environmental regulations requiring sophisticated fuel management and emission compliance systems. Success depends on:

- **Precise Fuel Planning**: Ensuring adequate fuel while optimizing costs
- **Emission Monitoring**: Real-time calculation of regulatory compliance
- **Strategic Decision Making**: Balancing biofuel costs against penalty payments
- **System Integration**: Coordinating voyage planning with environmental compliance

Organizations must invest in comprehensive systems that manage both operational efficiency and environmental compliance to remain competitive in the evolving regulatory landscape.
