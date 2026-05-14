# CurrencyExchangeRateDto, CurrencyDto, CurrencyUpdateDto

## Purpose
Thin data-transfer contracts for the Finance domain that standardize currency master data and exchange rate records across API boundaries, internal business handlers, and AutoMapper projections.

## Business Responsibility
Owned by the Finance/Currency aggregate boundary. `CurrencyExchangeRateDto` carries conversion rates with effective date ranges for lookup and calculation workflows. `CurrencyDto` defines master currency metadata alongside the latest USD-equivalent rate. `CurrencyUpdateDto` provides a constrained input shape for modifying currency definitions. Critical for all rate retrieval