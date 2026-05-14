# CompanyBankDto

## Purpose
Data transfer objects for company bank account management. `CompanyBankDto` serves as the read-side representation (inheriting `BaseDto` for system metadata), while `CompanyBankUpdateDto` acts as the explicit write-side payload for update operations.

## Business Responsibility
These DTOs decouple the finance domain’s company bank entity from the API and application layers. They are low-impact, high-frequency models routed through CRUD handlers (`CreateCompanyBank`, `UpdateCompanyBank