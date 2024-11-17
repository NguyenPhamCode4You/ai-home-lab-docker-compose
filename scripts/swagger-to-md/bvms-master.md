# Entities Documentation

Generated from `bvms-master.md`.

## ArchetypeDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **name:** string (No description provided.)
    - **Type:** string
  - **dataType:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **defaultValue:** string (No description provided.)
    - **Type:** string

---

## ArchetypeDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** ArchetypeDto

---

## ArchetypeDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** ArchetypeDto

---

## ArchetypeDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** ArchetypeDtoPagedResult

---

## BBCLoginDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **rawToken:** string (No description provided.)
    - **Type:** string

---

## BaseSearch

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter

---

## BooleanApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** boolean (No description provided.)
    - **Type:** boolean

---

## BunkerTypeCreateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **bunkerTypeCode:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **isEca:** boolean (No description provided.)
    - **Type:** boolean
  - **co2EmissionsFactor:** number (No description provided.)
    - **Type:** number
  - **ch4EmissionsFactor:** number (No description provided.)
    - **Type:** number
  - **n2oEmissionsFactor:** number (No description provided.)
    - **Type:** number

---

## BunkerTypeDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **bunkerTypeCode:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **isEca:** boolean (No description provided.)
    - **Type:** boolean
  - **co2EmissionsFactor:** number (No description provided.)
    - **Type:** number
  - **ch4EmissionsFactor:** number (No description provided.)
    - **Type:** number
  - **n2oEmissionsFactor:** number (No description provided.)
    - **Type:** number

---

## BunkerTypeDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** BunkerTypeDto

---

## BunkerTypeDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** BunkerTypeDto

---

## BunkerTypeDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** BunkerTypeDtoPagedResult

---

## BunkerTypeFilterBy

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **bunkerTypeCode:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeName:** string (No description provided.)
    - **Type:** string

---

## BunkerTypeSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter
  - **filterBy:** unknown (No description provided.)
    - **Reference:** BunkerTypeFilterBy

---

## BunkerTypeUpdateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **bunkerTypeCode:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **isEca:** boolean (No description provided.)
    - **Type:** boolean
  - **co2EmissionsFactor:** number (No description provided.)
    - **Type:** number
  - **ch4EmissionsFactor:** number (No description provided.)
    - **Type:** number
  - **n2oEmissionsFactor:** number (No description provided.)
    - **Type:** number

---

## BusinessPartnerCreateDtos

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **partnerName:** string (No description provided.)
    - **Type:** string
  - **partnerCode:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **taxNumber:** string (No description provided.)
    - **Type:** string
  - **contacts:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** ContactDto

---

## BusinessPartnerDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **partnerName:** string (No description provided.)
    - **Type:** string
  - **partnerCode:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **taxNumber:** string (No description provided.)
    - **Type:** string
  - **contacts:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** ContactDto

---

## BusinessPartnerDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** BusinessPartnerDto

---

## BusinessPartnerDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** BusinessPartnerDto

---

## BusinessPartnerDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** BusinessPartnerDtoPagedResult

---

## BusinessPartnerFilterBy

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **partnerName:** string (No description provided.)
    - **Type:** string
  - **partnerCode:** string (No description provided.)
    - **Type:** string

---

## BusinessPartnerSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter
  - **filterBy:** unknown (No description provided.)
    - **Reference:** BusinessPartnerFilterBy

---

## BusinessPartnerUpdateDtos

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **partnerName:** string (No description provided.)
    - **Type:** string
  - **partnerCode:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **taxNumber:** string (No description provided.)
    - **Type:** string
  - **contacts:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** ContactDto

---

## CommissionTypeCreateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **commissionTypeName:** string (No description provided.)
    - **Type:** string

---

## CommissionTypeDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **commissionTypeName:** string (No description provided.)
    - **Type:** string

---

## CommissionTypeDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** CommissionTypeDto

---

## CommissionTypeDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** CommissionTypeDto

---

## CommissionTypeDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** CommissionTypeDtoPagedResult

---

## CommissionTypeSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter

---

## CommissionTypeUpdateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **commissionTypeName:** string (No description provided.)
    - **Type:** string

---

## ContactDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **businessPartnerId:** string (No description provided.)
    - **Type:** string
  - **email:** string (No description provided.)
    - **Type:** string
  - **phone:** string (No description provided.)
    - **Type:** string
  - **fax:** string (No description provided.)
    - **Type:** string
  - **address:** string (No description provided.)
    - **Type:** string
  - **cityName:** string (No description provided.)
    - **Type:** string
  - **postalCode:** string (No description provided.)
    - **Type:** string
  - **countryCode:** string (No description provided.)
    - **Type:** string

---

## ContactDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** ContactDto

---

## ContactDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** ContactDto

---

## ContactDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** ContactDtoPagedResult

---

## DynamicFilter

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **fieldName:** string (No description provided.)
    - **Type:** string
  - **operator:** string (No description provided.)
    - **Type:** string
  - **value:** string (No description provided.)
    - **Type:** string
  - **sort:** string (No description provided.)
    - **Type:** string
  - **query:** string (No description provided.)
    - **Type:** string

---

## EstimateVesselConsumptionRateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **vesselId:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeId:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeCode:** string (No description provided.)
    - **Type:** string
  - **consumptionScenario:** string (No description provided.)
    - **Type:** string
  - **speedMode:** string (No description provided.)
    - **Type:** string
  - **speedInKnots:** number (No description provided.)
    - **Type:** number
  - **consumptionPerDayInMetricTons:** number (No description provided.)
    - **Type:** number
  - **isSelected:** boolean (No description provided.)
    - **Type:** boolean

---

## EstimateVesselConsumptionRateDtoListApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** EstimateVesselConsumptionRateDto

---

## FileFormatEnum

**Description:** No description provided.

- **Type:** integer
- **Allowed Values:** 0, 1, 2

---

## InvoiceTypeDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **name:** string (No description provided.)
    - **Type:** string
  - **type:** string (No description provided.)
    - **Type:** string
  - **accountingNumber:** integer (No description provided.)
    - **Type:** integer
  - **defaultValueInUsds:** number (No description provided.)
    - **Type:** number
  - **archetypeId:** string (No description provided.)
    - **Type:** string
  - **archetypeName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **categoryType:** string (No description provided.)
    - **Type:** string

---

## InvoiceTypeDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** InvoiceTypeDto

---

## InvoiceTypeDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** InvoiceTypeDto

---

## InvoiceTypeDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** InvoiceTypeDtoPagedResult

---

## OfficeCreateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **name:** string (No description provided.)
    - **Type:** string
  - **officeCode:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **address:** string (No description provided.)
    - **Type:** string
  - **countryCode:** string (No description provided.)
    - **Type:** string
  - **phone:** string (No description provided.)
    - **Type:** string
  - **email:** string (No description provided.)
    - **Type:** string

---

## OfficeDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **name:** string (No description provided.)
    - **Type:** string
  - **officeCode:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **address:** string (No description provided.)
    - **Type:** string
  - **countryCode:** string (No description provided.)
    - **Type:** string
  - **phone:** string (No description provided.)
    - **Type:** string
  - **email:** string (No description provided.)
    - **Type:** string

---

## OfficeDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** OfficeDto

---

## OfficeDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** OfficeDto

---

## OfficeDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** OfficeDtoPagedResult

---

## OfficeFilterBy

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **name:** string (No description provided.)
    - **Type:** string
  - **officeCode:** string (No description provided.)
    - **Type:** string
  - **countryCode:** string (No description provided.)
    - **Type:** string

---

## OfficeSearch

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter
  - **filterBy:** unknown (No description provided.)
    - **Reference:** OfficeFilterBy

---

## OfficeUpdateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **name:** string (No description provided.)
    - **Type:** string
  - **officeCode:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **address:** string (No description provided.)
    - **Type:** string
  - **countryCode:** string (No description provided.)
    - **Type:** string
  - **phone:** string (No description provided.)
    - **Type:** string
  - **email:** string (No description provided.)
    - **Type:** string

---

## PortCreateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **portName:** string (No description provided.)
    - **Type:** string
  - **unLoCode:** string (No description provided.)
    - **Type:** string
  - **tradeArea:** string (No description provided.)
    - **Type:** string
  - **timeZoneOffsetFromUtc:** integer (No description provided.)
    - **Type:** integer
  - **longtitude:** number (No description provided.)
    - **Type:** number
  - **lattitude:** number (No description provided.)
    - **Type:** number
  - **isEca:** boolean (No description provided.)
    - **Type:** boolean
  - **isCanal:** boolean (No description provided.)
    - **Type:** boolean
  - **isPassingPoint:** boolean (No description provided.)
    - **Type:** boolean
  - **canalDistanceInSeaMiles:** number (No description provided.)
    - **Type:** number
  - **canalDefaultTransitTimeInDays:** number (No description provided.)
    - **Type:** number
  - **defaultWaitingTimeInDays:** number (No description provided.)
    - **Type:** number
  - **canalTollInUsds:** number (No description provided.)
    - **Type:** number
  - **countryCode:** string (No description provided.)
    - **Type:** string
  - **area:** number (No description provided.)
    - **Type:** number
  - **note:** string (No description provided.)
    - **Type:** string
  - **portAgentId:** string (No description provided.)
    - **Type:** string
  - **portAgent:** unknown (No description provided.)
    - **Reference:** BusinessPartnerDto

---

## PortDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **portName:** string (No description provided.)
    - **Type:** string
  - **unLoCode:** string (No description provided.)
    - **Type:** string
  - **tradeArea:** string (No description provided.)
    - **Type:** string
  - **timeZoneOffsetFromUtc:** integer (No description provided.)
    - **Type:** integer
  - **longtitude:** number (No description provided.)
    - **Type:** number
  - **lattitude:** number (No description provided.)
    - **Type:** number
  - **isEca:** boolean (No description provided.)
    - **Type:** boolean
  - **portAgentId:** string (No description provided.)
    - **Type:** string
  - **portAgent:** unknown (No description provided.)
    - **Reference:** BusinessPartnerDto
  - **isCanal:** boolean (No description provided.)
    - **Type:** boolean
  - **isPassingPoint:** boolean (No description provided.)
    - **Type:** boolean
  - **canalDistanceInSeaMiles:** number (No description provided.)
    - **Type:** number
  - **canalDefaultTransitTimeInDays:** number (No description provided.)
    - **Type:** number
  - **defaultWaitingTimeInDays:** number (No description provided.)
    - **Type:** number
  - **canalTollInUsds:** number (No description provided.)
    - **Type:** number
  - **countryCode:** string (No description provided.)
    - **Type:** string
  - **area:** number (No description provided.)
    - **Type:** number
  - **note:** string (No description provided.)
    - **Type:** string
  - **timeZone:** string (No description provided.)
    - **Type:** string

---

## PortDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** PortDto

---

## PortDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** PortDto

---

## PortDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** PortDtoPagedResult

---

## PortFilterBy

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **portName:** string (No description provided.)
    - **Type:** string
  - **unLoCode:** string (No description provided.)
    - **Type:** string
  - **tradeArea:** string (No description provided.)
    - **Type:** string
  - **countryCode:** string (No description provided.)
    - **Type:** string
  - **timeZoneOffsetFromUtc:** string (No description provided.)
    - **Type:** string
  - **longtitude:** string (No description provided.)
    - **Type:** string
  - **lattitude:** string (No description provided.)
    - **Type:** string
  - **isEca:** string (No description provided.)
    - **Type:** string
  - **isCanal:** string (No description provided.)
    - **Type:** string
  - **isPassingPoint:** string (No description provided.)
    - **Type:** string
  - **canalDistanceInSeaMiles:** string (No description provided.)
    - **Type:** string
  - **canalDefaultTransitTimeInDays:** string (No description provided.)
    - **Type:** string
  - **defaultWaitingTimeInDays:** string (No description provided.)
    - **Type:** string
  - **canalTollInUsds:** string (No description provided.)
    - **Type:** string
  - **area:** string (No description provided.)
    - **Type:** string
  - **businessPartner:** string (No description provided.)
    - **Type:** string

---

## PortSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter
  - **filterBy:** unknown (No description provided.)
    - **Reference:** PortFilterBy
  - **alternativeOf:** string (No description provided.)
    - **Type:** string

---

## PortUpdateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **portName:** string (No description provided.)
    - **Type:** string
  - **unLoCode:** string (No description provided.)
    - **Type:** string
  - **tradeArea:** string (No description provided.)
    - **Type:** string
  - **timeZoneOffsetFromUtc:** integer (No description provided.)
    - **Type:** integer
  - **longtitude:** number (No description provided.)
    - **Type:** number
  - **lattitude:** number (No description provided.)
    - **Type:** number
  - **isEca:** boolean (No description provided.)
    - **Type:** boolean
  - **isCanal:** boolean (No description provided.)
    - **Type:** boolean
  - **isPassingPoint:** boolean (No description provided.)
    - **Type:** boolean
  - **canalDistanceInSeaMiles:** number (No description provided.)
    - **Type:** number
  - **canalDefaultTransitTimeInDays:** number (No description provided.)
    - **Type:** number
  - **defaultWaitingTimeInDays:** number (No description provided.)
    - **Type:** number
  - **canalTollInUsds:** number (No description provided.)
    - **Type:** number
  - **countryCode:** string (No description provided.)
    - **Type:** string
  - **area:** number (No description provided.)
    - **Type:** number
  - **note:** string (No description provided.)
    - **Type:** string
  - **portAgentId:** string (No description provided.)
    - **Type:** string
  - **portAgent:** unknown (No description provided.)
    - **Reference:** BusinessPartnerDto

---

## RoutingImportResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **totalCount:** integer (No description provided.)
    - **Type:** integer
  - **importedCount:** integer (No description provided.)
    - **Type:** integer
  - **failedCount:** integer (No description provided.)
    - **Type:** integer
  - **existingCount:** integer (No description provided.)
    - **Type:** integer

---

## RoutingImportResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** RoutingImportResult

---

## StringApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** string (No description provided.)
    - **Type:** string

---

## TermCreateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **termCode:** string (No description provided.)
    - **Type:** string
  - **termType:** string (No description provided.)
    - **Type:** string
  - **termName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **factor:** number (No description provided.)
    - **Type:** number

---

## TermDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **termCode:** string (No description provided.)
    - **Type:** string
  - **termType:** string (No description provided.)
    - **Type:** string
  - **termName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **factor:** number (No description provided.)
    - **Type:** number

---

## TermDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** TermDto

---

## TermDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** TermDto

---

## TermDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** TermDtoPagedResult

---

## TermFilterBy

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **termCode:** string (No description provided.)
    - **Type:** string
  - **termType:** string (No description provided.)
    - **Type:** string
  - **termName:** string (No description provided.)
    - **Type:** string

---

## TermSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter
  - **filterBy:** unknown (No description provided.)
    - **Reference:** TermFilterBy

---

## TermUpdateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **termCode:** string (No description provided.)
    - **Type:** string
  - **termType:** string (No description provided.)
    - **Type:** string
  - **termName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string
  - **factor:** number (No description provided.)
    - **Type:** number

---

## UserDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **fullName:** string (No description provided.)
    - **Type:** string
  - **userName:** string (No description provided.)
    - **Type:** string
  - **email:** string (No description provided.)
    - **Type:** string
  - **officeId:** string (No description provided.)
    - **Type:** string
  - **office:** unknown (No description provided.)
    - **Reference:** OfficeDto

---

## UserDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** UserDto

---

## UserLogin

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **email:** string (No description provided.)
    - **Type:** string
  - **password:** string (No description provided.)
    - **Type:** string

---

## UserLoginRequestDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **username:** string (No description provided.)
    - **Type:** string
  - **password:** string (No description provided.)
    - **Type:** string

---

## UserLoginResponseDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **data:** unknown (No description provided.)
    - **Reference:** UserProfileDto
  - **token:** string (No description provided.)
    - **Type:** string

---

## UserLoginResponseDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** UserLoginResponseDto

---

## UserProfileDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **fullName:** string (No description provided.)
    - **Type:** string
  - **userName:** string (No description provided.)
    - **Type:** string
  - **email:** string (No description provided.)
    - **Type:** string
  - **officeId:** string (No description provided.)
    - **Type:** string
  - **office:** unknown (No description provided.)
    - **Reference:** OfficeDto
  - **policies:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Type:** string

---

## UserReducedDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **fullName:** string (No description provided.)
    - **Type:** string
  - **userName:** string (No description provided.)
    - **Type:** string
  - **email:** string (No description provided.)
    - **Type:** string
  - **officeId:** string (No description provided.)
    - **Type:** string
  - **office:** unknown (No description provided.)
    - **Reference:** OfficeDto

---

## UserReducedDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** UserReducedDto

---

## UserReducedDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** UserReducedDtoPagedResult

---

## UserRegister

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **email:** string (No description provided.)
    - **Type:** string
  - **password:** string (No description provided.)
    - **Type:** string
  - **fullName:** string (No description provided.)
    - **Type:** string

---

## UserSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter

---

## VesselConsumptionRateCreateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselId:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeId:** string (No description provided.)
    - **Type:** string
  - **consumptionScenario:** string (No description provided.)
    - **Type:** string
  - **speedMode:** string (No description provided.)
    - **Type:** string
  - **speedInKnots:** number (No description provided.)
    - **Type:** number
  - **consumptionPerDayInMetricTons:** number (No description provided.)
    - **Type:** number

---

## VesselConsumptionRateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **vesselId:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeId:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeCode:** string (No description provided.)
    - **Type:** string
  - **consumptionScenario:** string (No description provided.)
    - **Type:** string
  - **speedMode:** string (No description provided.)
    - **Type:** string
  - **speedInKnots:** number (No description provided.)
    - **Type:** number
  - **consumptionPerDayInMetricTons:** number (No description provided.)
    - **Type:** number

---

## VesselConsumptionRateDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** VesselConsumptionRateDto

---

## VesselConsumptionRateDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** VesselConsumptionRateDto

---

## VesselConsumptionRateDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** VesselConsumptionRateDtoPagedResult

---

## VesselConsumptionRateFilterBy

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **bunkerTypeId:** string (No description provided.)
    - **Type:** string
  - **speedMode:** string (No description provided.)
    - **Type:** string
  - **consumptionScenario:** string (No description provided.)
    - **Type:** string

---

## VesselConsumptionRateSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter
  - **filterBy:** unknown (No description provided.)
    - **Reference:** VesselConsumptionRateFilterBy

---

## VesselConsumptionRateUpdateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselId:** string (No description provided.)
    - **Type:** string
  - **bunkerTypeId:** string (No description provided.)
    - **Type:** string
  - **consumptionScenario:** string (No description provided.)
    - **Type:** string
  - **speedMode:** string (No description provided.)
    - **Type:** string
  - **speedInKnots:** number (No description provided.)
    - **Type:** number
  - **consumptionPerDayInMetricTons:** number (No description provided.)
    - **Type:** number

---

## VesselCreateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselName:** string (No description provided.)
    - **Type:** string
  - **imoNumber:** integer (No description provided.)
    - **Type:** integer
  - **vesselCode:** string (No description provided.)
    - **Type:** string
  - **flag:** string (No description provided.)
    - **Type:** string
  - **vesselTypeId:** string (No description provided.)
    - **Type:** string
  - **vesselType:** unknown (No description provided.)
    - **Reference:** VesselTypeDto
  - **vesselSpecification:** unknown (No description provided.)
    - **Reference:** VesselSpecificationDto
  - **openingPositionPortId:** string (No description provided.)
    - **Type:** string
  - **openingDate:** string (No description provided.)
    - **Type:** string
  - **vesselStatus:** string (No description provided.)
    - **Type:** string
  - **vesselOwnershipType:** string (No description provided.)
    - **Type:** string
  - **subjectedToIceClass:** boolean (No description provided.)
    - **Type:** boolean
  - **vesselConsumptionRates:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** VesselConsumptionRateDto
  - **vesselOwnerId:** string (No description provided.)
    - **Type:** string
  - **vesselOwner:** unknown (No description provided.)
    - **Reference:** BusinessPartnerDto

---

## VesselCreateDuplicateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselIds:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Type:** string

---

## VesselDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **vesselName:** string (No description provided.)
    - **Type:** string
  - **imoNumber:** integer (No description provided.)
    - **Type:** integer
  - **vesselCode:** string (No description provided.)
    - **Type:** string
  - **flag:** string (No description provided.)
    - **Type:** string
  - **vesselTypeId:** string (No description provided.)
    - **Type:** string
  - **vesselType:** unknown (No description provided.)
    - **Reference:** VesselTypeDto
  - **vesselSpecification:** unknown (No description provided.)
    - **Reference:** VesselSpecificationDto
  - **openingPositionPortId:** string (No description provided.)
    - **Type:** string
  - **openingPositionPort:** unknown (No description provided.)
    - **Reference:** PortDto
  - **openingDate:** string (No description provided.)
    - **Type:** string
  - **vesselStatus:** string (No description provided.)
    - **Type:** string
  - **vesselOwnershipType:** string (No description provided.)
    - **Type:** string
  - **subjectedToIceClass:** boolean (No description provided.)
    - **Type:** boolean
  - **vesselConsumptionRates:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** VesselConsumptionRateDto
  - **vesselOwnerId:** string (No description provided.)
    - **Type:** string
  - **vesselOwner:** unknown (No description provided.)
    - **Reference:** BusinessPartnerDto

---

## VesselDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** VesselDto

---

## VesselDtoListApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** VesselDto

---

## VesselFilterBy

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselName:** string (No description provided.)
    - **Type:** string
  - **imoNumber:** integer (No description provided.)
    - **Type:** integer
  - **vesselCode:** string (No description provided.)
    - **Type:** string
  - **flag:** string (No description provided.)
    - **Type:** string
  - **vesselTypeId:** string (No description provided.)
    - **Type:** string
  - **vesselStatus:** string (No description provided.)
    - **Type:** string
  - **vesselOwnershipType:** string (No description provided.)
    - **Type:** string

---

## VesselReducedDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **vesselName:** string (No description provided.)
    - **Type:** string
  - **imoNumber:** integer (No description provided.)
    - **Type:** integer
  - **vesselCode:** string (No description provided.)
    - **Type:** string
  - **flag:** string (No description provided.)
    - **Type:** string
  - **vesselStatus:** string (No description provided.)
    - **Type:** string
  - **vesselOwnershipType:** string (No description provided.)
    - **Type:** string
  - **vesselTypeId:** string (No description provided.)
    - **Type:** string
  - **vesselTypeName:** string (No description provided.)
    - **Type:** string
  - **openingPositionPortId:** string (No description provided.)
    - **Type:** string
  - **openingPositionPortName:** string (No description provided.)
    - **Type:** string
  - **openingDate:** string (No description provided.)
    - **Type:** string
  - **hireCostPerDayInUsds:** number (No description provided.)
    - **Type:** number
  - **dwtInMetricTons:** number (No description provided.)
    - **Type:** number
  - **liftingCapacityInMetricTons:** number (No description provided.)
    - **Type:** number
  - **intendedCargoType:** string (No description provided.)
    - **Type:** string
  - **subjectedToIceClass:** boolean (No description provided.)
    - **Type:** boolean
  - **builtYear:** string (No description provided.)
    - **Type:** string

---

## VesselReducedDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** VesselReducedDto

---

## VesselReducedDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** VesselReducedDtoPagedResult

---

## VesselSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter
  - **filterBy:** unknown (No description provided.)
    - **Reference:** VesselFilterBy

---

## VesselSpecificationDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **hireCostPerDayInUsds:** number (No description provided.)
    - **Type:** number
  - **dwtInMetricTons:** number (No description provided.)
    - **Type:** number
  - **liftingCapacityInMetricTons:** number (No description provided.)
    - **Type:** number
  - **auxillaryEngineDescription:** string (No description provided.)
    - **Type:** string
  - **mainEngineDescription:** string (No description provided.)
    - **Type:** string
  - **intendedCargoType:** string (No description provided.)
    - **Type:** string
  - **otherInformation:** string (No description provided.)
    - **Type:** string
  - **builtYear:** string (No description provided.)
    - **Type:** string

---

## VesselSpecificationDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** VesselSpecificationDto

---

## VesselTypeCreateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselTypeCode:** string (No description provided.)
    - **Type:** string
  - **vesselTypeName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string

---

## VesselTypeDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **id:** string (No description provided.)
    - **Type:** string
  - **createdOn:** string (No description provided.)
    - **Type:** string
  - **createdById:** string (No description provided.)
    - **Type:** string
  - **createdByName:** string (No description provided.)
    - **Type:** string
  - **modifiedOn:** string (No description provided.)
    - **Type:** string
  - **modifiedById:** string (No description provided.)
    - **Type:** string
  - **modifiedByName:** string (No description provided.)
    - **Type:** string
  - **tenantId:** string (No description provided.)
    - **Type:** string
  - **isDeleted:** boolean (No description provided.)
    - **Type:** boolean
  - **vesselTypeCode:** string (No description provided.)
    - **Type:** string
  - **vesselTypeName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string

---

## VesselTypeDtoApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** VesselTypeDto

---

## VesselTypeDtoPagedResult

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **totalCounts:** integer (No description provided.)
    - **Type:** integer
  - **items:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** VesselTypeDto

---

## VesselTypeDtoPagedResultApiResponse

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **isSuccess:** boolean (No description provided.)
    - **Type:** boolean
  - **result:** unknown (No description provided.)
    - **Reference:** VesselTypeDtoPagedResult

---

## VesselTypeFilterBy

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselTypeCode:** string (No description provided.)
    - **Type:** string
  - **vesselTypeName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string

---

## VesselTypeSearchDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **keySearch:** string (No description provided.)
    - **Type:** string
  - **currentPage:** integer (No description provided.)
    - **Type:** integer
  - **pageSize:** integer (No description provided.)
    - **Type:** integer
  - **filters:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** DynamicFilter
  - **filterBy:** unknown (No description provided.)
    - **Reference:** VesselTypeFilterBy

---

## VesselTypeUpdateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselTypeCode:** string (No description provided.)
    - **Type:** string
  - **vesselTypeName:** string (No description provided.)
    - **Type:** string
  - **description:** string (No description provided.)
    - **Type:** string

---

## VesselUpdateDto

**Description:** No description provided.

- **Type:** object
- **Properties:**
  - **vesselName:** string (No description provided.)
    - **Type:** string
  - **imoNumber:** integer (No description provided.)
    - **Type:** integer
  - **vesselCode:** string (No description provided.)
    - **Type:** string
  - **flag:** string (No description provided.)
    - **Type:** string
  - **vesselTypeId:** string (No description provided.)
    - **Type:** string
  - **vesselType:** unknown (No description provided.)
    - **Reference:** VesselTypeDto
  - **vesselSpecification:** unknown (No description provided.)
    - **Reference:** VesselSpecificationDto
  - **openingPositionPortId:** string (No description provided.)
    - **Type:** string
  - **openingDate:** string (No description provided.)
    - **Type:** string
  - **vesselStatus:** string (No description provided.)
    - **Type:** string
  - **vesselOwnershipType:** string (No description provided.)
    - **Type:** string
  - **subjectedToIceClass:** boolean (No description provided.)
    - **Type:** boolean
  - **vesselConsumptionRates:** array (No description provided.)
    - **Type:** array
    - **Items:**
        - **Reference:** VesselConsumptionRateDto
  - **vesselOwnerId:** string (No description provided.)
    - **Type:** string
  - **vesselOwner:** unknown (No description provided.)
    - **Reference:** BusinessPartnerDto

---

