## Endpoints:
GET /AiDataSet/PortNames
GET /AiDataSet/VesselNames
GET /AiDataSet/VesselConsumption
POST /Archetype
GET /Archetype/{id}
PUT /Archetype/{id}
DELETE /Archetype/{id}
POST /Archetype/Search
POST /BunkerTypes
GET /BunkerTypes/{id}
PUT /BunkerTypes/{id}
POST /BunkerTypes/Search
DELETE /BunkerTypes/{bunkerTypeId}
POST /api/BusinessPartner
GET /api/BusinessPartner/{id}
PUT /api/BusinessPartner/{id}
DELETE /api/BusinessPartner/{id}
POST /api/BusinessPartner/Search
GET /Claims/Category
GET /CommissionTypes
POST /CommissionTypes
GET /CommissionTypes/{id}
PUT /CommissionTypes/{id}
POST /CommissionTypes/Search
DELETE /CommissionTypes/{Id}
POST /Contact
GET /Contact/{id}
PUT /Contact/{id}
DELETE /Contact/{id}
POST /Contact/Search
POST /InvoiceType
GET /InvoiceType/{id}
PUT /InvoiceType/{id}
DELETE /InvoiceType/{id}
POST /InvoiceType/Search
GET /MicrosoftGraph/ImportAllUsersFromAzure
POST /Offices/Search
GET /Offices/{id}
PUT /Offices/{id}
DELETE /Offices/{id}
POST /Offices
POST /Ports
GET /Ports/{id}
PUT /Ports/{id}
POST /Ports/Search
DELETE /Ports/{portId}
POST /Roles
GET /Roles/{id}
PUT /Roles/{id}
DELETE /Roles/{id}
POST /Roles/Search
POST /SeedData/MasterData
POST /SeedData/VesselConsumptionRates
POST /SeedData/Shipment
POST /SeedData/RandomAllEstimateCodes
POST /SeedData/UserData
POST /SeedData/UpdatePortsTimeZone
POST /SeedData/ValidateBlockCanals
POST /SeedData/RemapEstimateOriginalIds
POST /SeedData/ImportSeaConsumptionRates/Xlsx
POST /SeedData/ImportPortConsumptionRates/Xlsx
POST /SeedData/ImportVesselHireRate/Xlsx
POST /SeedData/ImportRoutingResponses/FromDataLoy
POST /SeedData/ImportRoutingResponses/FromDataLoy/Folder
POST /Terms
GET /Terms/{id}
PUT /Terms/{id}
POST /Terms/Search
DELETE /Terms/{termId}
POST /Users/BBCMicrosoftLogin
POST /Users/RootLogin
GET /Users/NewUserProfile
POST /Users/Login
POST /Users/RefreshToken
POST /Users/Register
POST /Users/Search
GET /Users/UserProfile/{id}
PUT /Users/UserProfile/{id}
GET /Users/UserProfile
POST /Vessels
GET /Vessels/{vesselId}
PUT /Vessels/{vesselId}
DELETE /Vessels/{vesselId}
GET /Vessels/{vesselId}/EstimateSpeedConsumption
POST /Vessels/Search
GET /Vessels/{vesselId}/Specification
PUT /Vessels/{vesselId}/Specification
POST /Vessels/{vesselId}/ConsumptionRates
POST /Vessels/{vesselId}/ConsumptionRates/Search
PUT /Vessels/{vesselId}/ConsumptionRates/{consumptionId}
DELETE /Vessels/{vesselId}/ConsumptionRates/{consumptionId}
POST /Vessels/CreateDuplicate
POST /VesselTypes
GET /VesselTypes/{id}
PUT /VesselTypes/{id}
POST /VesselTypes/Search
DELETE /VesselTypes/{vesselId}
## GET /AiDataSet/PortNames
1. Request: None
2. Response: None

## GET /AiDataSet/VesselNames
1. Request: None
2. Response: None

## GET /AiDataSet/VesselConsumption
1. Request: None
2. Response: None

## POST /Archetype
1. Request: Entity=[ArchetypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|dataType:string|description:string|defaultValue:string]
2. Response: Entity=[ArchetypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[ArchetypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|dataType:string|description:string|defaultValue:string])]

## GET /Archetype/{id}
1. Request: None
2. Response: Entity=[ArchetypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[ArchetypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|dataType:string|description:string|defaultValue:string])]

## PUT /Archetype/{id}
1. Request: Entity=[ArchetypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|dataType:string|description:string|defaultValue:string]
2. Response: Entity=[ArchetypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[ArchetypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|dataType:string|description:string|defaultValue:string])]

## DELETE /Archetype/{id}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Archetype/Search
1. Request: Entity=[BaseSearch]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])]
2. Response: Entity=[ArchetypeDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[ArchetypeDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[ArchetypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|dataType:string|description:string|defaultValue:string])])]

## POST /BunkerTypes
1. Request: Entity=[BunkerTypeCreateDto]|Fields=[bunkerTypeCode:string|bunkerTypeName:string|description:string|isEca:boolean|co2EmissionsFactor:number|ch4EmissionsFactor:number|n2oEmissionsFactor:number]
2. Response: Entity=[BunkerTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[BunkerTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|bunkerTypeCode:string|bunkerTypeName:string|description:string|isEca:boolean|co2EmissionsFactor:number|ch4EmissionsFactor:number|n2oEmissionsFactor:number])]

## GET /BunkerTypes/{id}
1. Request: None
2. Response: Entity=[BunkerTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[BunkerTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|bunkerTypeCode:string|bunkerTypeName:string|description:string|isEca:boolean|co2EmissionsFactor:number|ch4EmissionsFactor:number|n2oEmissionsFactor:number])]

## PUT /BunkerTypes/{id}
1. Request: Entity=[BunkerTypeUpdateDto]|Fields=[bunkerTypeCode:string|bunkerTypeName:string|description:string|isEca:boolean|co2EmissionsFactor:number|ch4EmissionsFactor:number|n2oEmissionsFactor:number]
2. Response: Entity=[BunkerTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[BunkerTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|bunkerTypeCode:string|bunkerTypeName:string|description:string|isEca:boolean|co2EmissionsFactor:number|ch4EmissionsFactor:number|n2oEmissionsFactor:number])]

## POST /BunkerTypes/Search
1. Request: Entity=[BunkerTypeSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])|filterBy:object(Entity=[BunkerTypeFilterBy]|Fields=[bunkerTypeCode:string|bunkerTypeName:string])]
2. Response: Entity=[BunkerTypeDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[BunkerTypeDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[BunkerTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|bunkerTypeCode:string|bunkerTypeName:string|description:string|isEca:boolean|co2EmissionsFactor:number|ch4EmissionsFactor:number|n2oEmissionsFactor:number])])]

## DELETE /BunkerTypes/{bunkerTypeId}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /api/BusinessPartner
1. Request: Entity=[BusinessPartnerCreateDtos]|Fields=[partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])]
2. Response: Entity=[BusinessPartnerDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])]

## GET /api/BusinessPartner/{id}
1. Request: None
2. Response: Entity=[BusinessPartnerDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])]

## PUT /api/BusinessPartner/{id}
1. Request: Entity=[BusinessPartnerUpdateDtos]|Fields=[partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])]
2. Response: Entity=[BusinessPartnerDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])]

## DELETE /api/BusinessPartner/{id}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /api/BusinessPartner/Search
1. Request: Entity=[BusinessPartnerSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])|filterBy:object(Entity=[BusinessPartnerFilterBy]|Fields=[partnerName:string|partnerCode:string])]
2. Response: Entity=[BusinessPartnerDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[BusinessPartnerDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])])]

## GET /Claims/Category
1. Request: None
2. Response: Entity=[ClaimCategoryDtoListApiResponse]|Fields=[isSuccess:boolean|result:array(Entity=[ClaimCategoryDto]|Fields=[category:string|description:string|claims:array(Entity=[ClaimDetailDto]|Fields=[id:string|name:string])])]

## GET /CommissionTypes
1. Request: None
2. Response: Entity=[CommissionTypeDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[CommissionTypeDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[CommissionTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|commissionTypeName:string])])]

## POST /CommissionTypes
1. Request: Entity=[CommissionTypeCreateDto]|Fields=[commissionTypeName:string]
2. Response: Entity=[CommissionTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[CommissionTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|commissionTypeName:string])]

## GET /CommissionTypes/{id}
1. Request: None
2. Response: Entity=[CommissionTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[CommissionTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|commissionTypeName:string])]

## PUT /CommissionTypes/{id}
1. Request: Entity=[CommissionTypeUpdateDto]|Fields=[commissionTypeName:string]
2. Response: Entity=[CommissionTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[CommissionTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|commissionTypeName:string])]

## POST /CommissionTypes/Search
1. Request: Entity=[CommissionTypeSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])]
2. Response: Entity=[CommissionTypeDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[CommissionTypeDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[CommissionTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|commissionTypeName:string])])]

## DELETE /CommissionTypes/{Id}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Contact
1. Request: Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string]
2. Response: Entity=[ContactDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])]

## GET /Contact/{id}
1. Request: None
2. Response: Entity=[ContactDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])]

## PUT /Contact/{id}
1. Request: Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string]
2. Response: Entity=[ContactDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])]

## DELETE /Contact/{id}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Contact/Search
1. Request: Entity=[BaseSearch]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])]
2. Response: Entity=[ContactDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[ContactDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])]

## POST /InvoiceType
1. Request: Entity=[InvoiceTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|type:string|accountingNumber:integer|defaultValueInUsds:number|archetypeId:string|archetypeName:string|description:string|categoryType:string]
2. Response: Entity=[InvoiceTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[InvoiceTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|type:string|accountingNumber:integer|defaultValueInUsds:number|archetypeId:string|archetypeName:string|description:string|categoryType:string])]

## GET /InvoiceType/{id}
1. Request: None
2. Response: Entity=[InvoiceTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[InvoiceTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|type:string|accountingNumber:integer|defaultValueInUsds:number|archetypeId:string|archetypeName:string|description:string|categoryType:string])]

## PUT /InvoiceType/{id}
1. Request: Entity=[InvoiceTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|type:string|accountingNumber:integer|defaultValueInUsds:number|archetypeId:string|archetypeName:string|description:string|categoryType:string]
2. Response: Entity=[InvoiceTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[InvoiceTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|type:string|accountingNumber:integer|defaultValueInUsds:number|archetypeId:string|archetypeName:string|description:string|categoryType:string])]

## DELETE /InvoiceType/{id}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /InvoiceType/Search
1. Request: Entity=[BaseSearch]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])]
2. Response: Entity=[InvoiceTypeDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[InvoiceTypeDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[InvoiceTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|type:string|accountingNumber:integer|defaultValueInUsds:number|archetypeId:string|archetypeName:string|description:string|categoryType:string])])]

## GET /MicrosoftGraph/ImportAllUsersFromAzure
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Offices/Search
1. Request: Entity=[OfficeSearch]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])|filterBy:object(Entity=[OfficeFilterBy]|Fields=[name:string|officeCode:string|countryCode:string])]
2. Response: Entity=[OfficeDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[OfficeDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])])]

## GET /Offices/{id}
1. Request: None
2. Response: Entity=[OfficeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])]

## PUT /Offices/{id}
1. Request: Entity=[OfficeUpdateDto]|Fields=[name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string]
2. Response: Entity=[OfficeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])]

## DELETE /Offices/{id}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Offices
1. Request: Entity=[OfficeCreateDto]|Fields=[name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string]
2. Response: Entity=[OfficeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])]

## POST /Ports
1. Request: Entity=[PortCreateDto]|Fields=[portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])]
2. Response: Entity=[PortDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[PortDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|timeZone:string|timeZoneOffsetDisplay:string])]

## GET /Ports/{id}
1. Request: None
2. Response: Entity=[PortDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[PortDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|timeZone:string|timeZoneOffsetDisplay:string])]

## PUT /Ports/{id}
1. Request: Entity=[PortUpdateDto]|Fields=[portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])]
2. Response: Entity=[PortDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[PortDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|timeZone:string|timeZoneOffsetDisplay:string])]

## POST /Ports/Search
1. Request: Entity=[PortSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])|filterBy:object(Entity=[PortFilterBy]|Fields=[portName:string|unLoCode:string|tradeArea:string|countryCode:string|timeZoneOffsetFromUtc:string|longtitude:string|lattitude:string|isEca:string|isCanal:string|isPassingPoint:string|canalDistanceInSeaMiles:string|canalDefaultTransitTimeInDays:string|defaultWaitingTimeInDays:string|canalTollInUsds:string|area:string|businessPartner:string])|alternativeOf:string]
2. Response: Entity=[PortDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[PortDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[PortDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|timeZone:string|timeZoneOffsetDisplay:string])])]

## DELETE /Ports/{portId}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Roles
1. Request: Entity=[RoleCreateDto]|Fields=[name:string|description:string|claims:array[string]]
2. Response: Entity=[RoleDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[RoleDto]|Fields=[id:string|name:string|description:string|claims:array[string]])]

## GET /Roles/{id}
1. Request: None
2. Response: Entity=[RoleDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[RoleDto]|Fields=[id:string|name:string|description:string|claims:array[string]])]

## PUT /Roles/{id}
1. Request: Entity=[RoleUpdateDto]|Fields=[name:string|description:string|claims:array[string]]
2. Response: Entity=[RoleDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[RoleDto]|Fields=[id:string|name:string|description:string|claims:array[string]])]

## DELETE /Roles/{id}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Roles/Search
1. Request: Entity=[RoleSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])]
2. Response: Entity=[RoleReducedDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[RoleReducedDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[RoleReducedDto]|Fields=[id:string|name:string|description:string])])]

## POST /SeedData/MasterData
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/VesselConsumptionRates
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/Shipment
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/RandomAllEstimateCodes
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/UserData
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/UpdatePortsTimeZone
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/ValidateBlockCanals
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/RemapEstimateOriginalIds
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/ImportSeaConsumptionRates/Xlsx
1. Request: Entity=[AnonymousEntity]|Fields=[ContentType:string|ContentDisposition:string|Headers:object|Length:integer|Name:string|FileName:string]
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/ImportPortConsumptionRates/Xlsx
1. Request: Entity=[AnonymousEntity]|Fields=[ContentType:string|ContentDisposition:string|Headers:object|Length:integer|Name:string|FileName:string]
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/ImportVesselHireRate/Xlsx
1. Request: Entity=[AnonymousEntity]|Fields=[ContentType:string|ContentDisposition:string|Headers:object|Length:integer|Name:string|FileName:string]
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /SeedData/ImportRoutingResponses/FromDataLoy
1. Request: None
2. Response: Entity=[RoutingImportResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[RoutingImportResult]|Fields=[totalCount:integer|importedCount:integer|failedCount:integer|existingCount:integer])]

## POST /SeedData/ImportRoutingResponses/FromDataLoy/Folder
1. Request: None
2. Response: Entity=[RoutingImportResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[RoutingImportResult]|Fields=[totalCount:integer|importedCount:integer|failedCount:integer|existingCount:integer])]

## POST /Terms
1. Request: Entity=[TermCreateDto]|Fields=[termCode:string|termType:string|termName:string|description:string|factor:number]
2. Response: Entity=[TermDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[TermDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|termCode:string|termType:string|termName:string|description:string|factor:number])]

## GET /Terms/{id}
1. Request: None
2. Response: Entity=[TermDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[TermDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|termCode:string|termType:string|termName:string|description:string|factor:number])]

## PUT /Terms/{id}
1. Request: Entity=[TermUpdateDto]|Fields=[termCode:string|termType:string|termName:string|description:string|factor:number]
2. Response: Entity=[TermDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[TermDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|termCode:string|termType:string|termName:string|description:string|factor:number])]

## POST /Terms/Search
1. Request: Entity=[TermSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])|filterBy:object(Entity=[TermFilterBy]|Fields=[termCode:string|termType:string|termName:string])]
2. Response: Entity=[TermDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[TermDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[TermDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|termCode:string|termType:string|termName:string|description:string|factor:number])])]

## DELETE /Terms/{termId}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Users/BBCMicrosoftLogin
1. Request: Entity=[BBCLoginDto]|Fields=[rawToken:string]
2. Response: Entity=[UserLoginResponseDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[UserLoginResponseDto]|Fields=[data:object(Entity=[UserProfileDto]|Fields=[id:string|fullName:string|userName:string|email:string|officeId:string|office:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])|policies:array[string]])|token:string])]

## POST /Users/RootLogin
1. Request: Entity=[UserLoginRequestDto]|Fields=[username:string|password:string]
2. Response: Entity=[UserLoginResponseDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[UserLoginResponseDto]|Fields=[data:object(Entity=[UserProfileDto]|Fields=[id:string|fullName:string|userName:string|email:string|officeId:string|office:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])|policies:array[string]])|token:string])]

## GET /Users/NewUserProfile
1. Request: None
2. Response: Entity=[UserLoginResponseDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[UserLoginResponseDto]|Fields=[data:object(Entity=[UserProfileDto]|Fields=[id:string|fullName:string|userName:string|email:string|officeId:string|office:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])|policies:array[string]])|token:string])]

## POST /Users/Login
1. Request: Entity=[UserLogin]|Fields=[email:string|password:string]
2. Response: Entity=[StringApiResponse]|Fields=[isSuccess:boolean|result:string]

## POST /Users/RefreshToken
1. Request: Entity=[AnonymousEntity]|Fields=[]
2. Response: Entity=[StringApiResponse]|Fields=[isSuccess:boolean|result:string]

## POST /Users/Register
1. Request: Entity=[UserRegister]|Fields=[email:string|password:string|fullName:string]
2. Response: Entity=[StringApiResponse]|Fields=[isSuccess:boolean|result:string]

## POST /Users/Search
1. Request: Entity=[UserSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])]
2. Response: Entity=[UserReducedDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[UserReducedDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[UserReducedDto]|Fields=[id:string|fullName:string|userName:string|department:string|region:string|email:string|officeId:string|office:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])])])]

## GET /Users/UserProfile/{id}
1. Request: None
2. Response: Entity=[UserDetailDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[UserDetailDto]|Fields=[id:string|fullName:string|userName:string|department:string|region:string|email:string|officeId:string|office:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])|roles:array[string]|userClaims:array[string]])]

## PUT /Users/UserProfile/{id}
1. Request: Entity=[GrantUserPermissionRequest]|Fields=[roles:array[string]|claims:array[string]]
2. Response: Entity=[UserDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[UserDto]|Fields=[id:string|fullName:string|userName:string|department:string|region:string|email:string|officeId:string|office:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])])]

## GET /Users/UserProfile
1. Request: None
2. Response: Entity=[UserDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[UserDto]|Fields=[id:string|fullName:string|userName:string|department:string|region:string|email:string|officeId:string|office:object(Entity=[OfficeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|name:string|officeCode:string|description:string|address:string|countryCode:string|phone:string|email:string])])]

## POST /Vessels
1. Request: Entity=[VesselCreateDto]|Fields=[vesselName:string|imoNumber:integer|vesselCode:string|flag:string|vesselTypeId:string|vesselType:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])|vesselSpecification:object(Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string])|openingPositionPortId:string|openingDate:string|vesselStatus:string|vesselOwnershipType:string|subjectedToIceClass:boolean|vesselConsumptionRates:array(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])|vesselOwnerId:string|vesselOwner:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean]
2. Response: Entity=[VesselDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselName:string|imoNumber:integer|vesselCode:string|flag:string|vesselTypeId:string|vesselType:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])|vesselSpecification:object(Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string])|openingPositionPortId:string|openingPositionPort:object(Entity=[PortDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|timeZone:string|timeZoneOffsetDisplay:string])|openingDate:string|vesselStatus:string|vesselOwnershipType:string|subjectedToIceClass:boolean|vesselConsumptionRates:array(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])|vesselOwnerId:string|vesselOwner:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])]

## GET /Vessels/{vesselId}
1. Request: None
2. Response: Entity=[VesselDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselName:string|imoNumber:integer|vesselCode:string|flag:string|vesselTypeId:string|vesselType:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])|vesselSpecification:object(Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string])|openingPositionPortId:string|openingPositionPort:object(Entity=[PortDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|timeZone:string|timeZoneOffsetDisplay:string])|openingDate:string|vesselStatus:string|vesselOwnershipType:string|subjectedToIceClass:boolean|vesselConsumptionRates:array(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])|vesselOwnerId:string|vesselOwner:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])]

## PUT /Vessels/{vesselId}
1. Request: Entity=[VesselUpdateDto]|Fields=[vesselName:string|imoNumber:integer|vesselCode:string|flag:string|vesselTypeId:string|vesselType:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])|vesselSpecification:object(Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string])|openingPositionPortId:string|openingDate:string|vesselStatus:string|vesselOwnershipType:string|subjectedToIceClass:boolean|vesselConsumptionRates:array(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])|vesselOwnerId:string|vesselOwner:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean]
2. Response: Entity=[VesselDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselName:string|imoNumber:integer|vesselCode:string|flag:string|vesselTypeId:string|vesselType:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])|vesselSpecification:object(Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string])|openingPositionPortId:string|openingPositionPort:object(Entity=[PortDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|timeZone:string|timeZoneOffsetDisplay:string])|openingDate:string|vesselStatus:string|vesselOwnershipType:string|subjectedToIceClass:boolean|vesselConsumptionRates:array(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])|vesselOwnerId:string|vesselOwner:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])]

## DELETE /Vessels/{vesselId}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## GET /Vessels/{vesselId}/EstimateSpeedConsumption
1. Request: None
2. Response: Entity=[EstimateVesselConsumptionRateDtoListApiResponse]|Fields=[isSuccess:boolean|result:array(Entity=[EstimateVesselConsumptionRateDto]|Fields=[id:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number|isSelected:boolean])]

## POST /Vessels/Search
1. Request: Entity=[VesselSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])|filterBy:object(Entity=[VesselFilterBy]|Fields=[vesselName:string|imoNumber:integer|vesselCode:string|flag:string|vesselTypeId:string|vesselStatus:string|vesselOwnershipType:string])]
2. Response: Entity=[VesselReducedDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselReducedDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[VesselReducedDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselName:string|imoNumber:integer|vesselCode:string|flag:string|vesselStatus:string|vesselOwnershipType:string|vesselTypeId:string|vesselTypeName:string|openingPositionPortId:string|openingPositionPortName:string|openingDate:string|hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|intendedCargoType:string|subjectedToIceClass:boolean|builtYear:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])])]

## GET /Vessels/{vesselId}/Specification
1. Request: None
2. Response: Entity=[VesselSpecificationDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string])]

## PUT /Vessels/{vesselId}/Specification
1. Request: Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string]
2. Response: Entity=[VesselSpecificationDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string])]

## POST /Vessels/{vesselId}/ConsumptionRates
1. Request: Entity=[VesselConsumptionRateCreateDto]|Fields=[vesselId:string|bunkerTypeId:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number]
2. Response: Entity=[VesselConsumptionRateDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])]

## POST /Vessels/{vesselId}/ConsumptionRates/Search
1. Request: Entity=[VesselConsumptionRateSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])|filterBy:object(Entity=[VesselConsumptionRateFilterBy]|Fields=[bunkerTypeId:string|speedMode:string|consumptionScenario:string])]
2. Response: Entity=[VesselConsumptionRateDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselConsumptionRateDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])])]

## PUT /Vessels/{vesselId}/ConsumptionRates/{consumptionId}
1. Request: Entity=[VesselConsumptionRateUpdateDto]|Fields=[vesselId:string|bunkerTypeId:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number]
2. Response: Entity=[VesselConsumptionRateDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])]

## DELETE /Vessels/{vesselId}/ConsumptionRates/{consumptionId}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

## POST /Vessels/CreateDuplicate
1. Request: Entity=[VesselCreateDuplicateDto]|Fields=[vesselIds:array[string]]
2. Response: Entity=[VesselDtoListApiResponse]|Fields=[isSuccess:boolean|result:array(Entity=[VesselDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselName:string|imoNumber:integer|vesselCode:string|flag:string|vesselTypeId:string|vesselType:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])|vesselSpecification:object(Entity=[VesselSpecificationDto]|Fields=[hireCostPerDayInUsds:number|dwtInMetricTons:number|liftingCapacityInMetricTons:number|auxillaryEngineDescription:string|mainEngineDescription:string|intendedCargoType:string|otherInformation:string|builtYear:string])|openingPositionPortId:string|openingPositionPort:object(Entity=[PortDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|portName:string|unLoCode:string|tradeArea:string|timeZoneOffsetFromUtc:integer|longtitude:number|lattitude:number|isEca:boolean|portAgentId:string|portAgent:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|isCanal:boolean|isPassingPoint:boolean|canalDistanceInSeaMiles:number|canalDefaultTransitTimeInDays:number|defaultWaitingTimeInDays:number|canalTollInUsds:number|countryCode:string|area:number|note:string|timeZone:string|timeZoneOffsetDisplay:string])|openingDate:string|vesselStatus:string|vesselOwnershipType:string|subjectedToIceClass:boolean|vesselConsumptionRates:array(Entity=[VesselConsumptionRateDto]|Fields=[id:string|createdOn:string|createdById:string|modifiedOn:string|modifiedById:string|vesselId:string|bunkerTypeId:string|bunkerTypeCode:string|consumptionScenario:string|speedMode:string|speedInKnots:number|consumptionPerDayInMetricTons:number])|vesselOwnerId:string|vesselOwner:object(Entity=[BusinessPartnerDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|partnerName:string|partnerCode:string|description:string|taxNumber:string|contacts:array(Entity=[ContactDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|businessPartnerId:string|email:string|phone:string|fax:string|address:string|cityName:string|postalCode:string|countryCode:string])])|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])]

## POST /VesselTypes
1. Request: Entity=[VesselTypeCreateDto]|Fields=[vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean]
2. Response: Entity=[VesselTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])]

## GET /VesselTypes/{id}
1. Request: None
2. Response: Entity=[VesselTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])]

## PUT /VesselTypes/{id}
1. Request: Entity=[VesselTypeUpdateDto]|Fields=[vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean]
2. Response: Entity=[VesselTypeDtoApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])]

## POST /VesselTypes/Search
1. Request: Entity=[VesselTypeSearchDto]|Fields=[keySearch:string|currentPage:integer|pageSize:integer|filters:array(Entity=[DynamicFilter]|Fields=[fieldName:string|operator:string|value:string|sort:string|query:string])|filterBy:object(Entity=[VesselTypeFilterBy]|Fields=[vesselTypeCode:string|vesselTypeName:string|description:string])]
2. Response: Entity=[VesselTypeDtoPagedResultApiResponse]|Fields=[isSuccess:boolean|result:object(Entity=[VesselTypeDtoPagedResult]|Fields=[currentPage:integer|pageSize:integer|totalCounts:integer|items:array(Entity=[VesselTypeDto]|Fields=[id:string|createdOn:string|createdById:string|createdByName:string|modifiedOn:string|modifiedById:string|modifiedByName:string|tenantId:string|isDeleted:boolean|vesselTypeCode:string|vesselTypeName:string|description:string|blockSuez:boolean|blockPanama:boolean|blockKiel:boolean|blockCorinth:boolean|blockTorres:boolean|blockNorthEast:boolean|blockNorthWest:boolean])])]

## DELETE /VesselTypes/{vesselId}
1. Request: None
2. Response: Entity=[BooleanApiResponse]|Fields=[isSuccess:boolean|result:boolean]

