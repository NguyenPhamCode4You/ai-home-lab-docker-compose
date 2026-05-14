# InvoiceConstants

## Purpose
Provides mapping and translation logic between BVMS invoice types/sources and legacy Imos bill sources, handling dual-system data migration and laytime-specific invoice routing.

## Business Responsibility
Owns the critical translation layer for invoice ingestion and export. Ensures BVMS invoice generation correctly targets legacy systems (Imos) or internal BVMS formats during the transition period. A failure here results in misrouted invoices, incorrect billing sources in downstream financial reports, or data loss during DA desk imports.

---

## Dependencies
- `LaytimeGroupEntity` — Required to extract `GetLaytimeType` for determining laytime invoice sources.
- `ProfitAndLossIdentifierEnum` — Referenced in P&L list definitions and laytime type checks for routing logic.
- `TransactionTypeEnum` — Used in `GetInvoiceType` to determine default invoice type based on transaction direction.
- `DAInvoiceTypesEnum` — Used in `GetInvoiceSourceEnumFromInvoiceType` to map DA desk invoice types to BVMS sources.

## Members

### USE_IMOS_INVOICE_SOURCE — Toggle for legacy mapping strategy
```csharp
static bool USE_IMOS_INVOICE_SOURCE = false;
```
**Explanation**: Controls the routing strategy in `MapInvoiceSource`. When `true`, the system maps to legacy `BillSourceEnum` strings (Imos format). When `false`, it uses native `InvoiceSourceEnum` strings. Currently defaults to `false` in code, but comments indicate `true` is the runtime expectation during migration until legacy data is fully migrated.

### GetInvoiceSourceFromInvoiceType — Maps InvoiceType to string source
```csharp
var invoiceSourceEnum = GetInvoiceSourceEnumFromInvoiceType(invoiceType);
var invoiceSource = MapInvoiceSource(invoiceSourceEnum.ToString());
return invoiceSource;
```
**Explanation**: Public entry point to resolve the string source for a given invoice type. Delegates to enum resolution and then applies the migration toggle (`MapInvoiceSource`). Used by invoice builders to populate source fields.

### GetLaytimeInvoiceSource — Specialized routing for laytime groups
```csharp
var invoiceSource = string.Empty;
if (laytimeGroup.GetLaytimeType() == ProfitAndLossIdentifierEnum.Demurrage.ToString() ||
    laytimeGroup.GetLaytimeType() == ProfitAndLossIdentifierEnum.Detention.ToString())
{
    invoiceSource = InvoiceSourceEnum.BVMS_DEMURRAGE.ToString();
}
else if (laytimeGroup.GetLaytimeType() == ProfitAndLossIdentifierEnum.Despatch.ToString())
{
    invoiceSource = InvoiceSourceEnum.BVMS_DESPATCH.ToString();
}

invoiceSource = MapInvoiceSource(invoiceSource);
return invoiceSource;
```
**Explanation**: Handles special business rule where both Demurrage and Detention map to the same invoice source (`BVMS_DEMURRAGE`), while Despatch maps separately. Applies the migration toggle at the end. Prevents undefined behavior for unsupported laytime types by returning empty string before mapping.

### MapInvoiceSource — Central router based on migration flag
```csharp
if (USE_IMOS_INVOICE_SOURCE)
{
    return GetBillSourceFromInvoiceSource(invoiceSource).ToString();
}
return invoiceSource;
```
**Explanation**: Branches logic based on `USE_IMOS_INVOICE_SOURCE`. If legacy mode is active, performs a strict reverse lookup to `BillSourceEnum`; otherwise passes through the BVMS source. The `GetBillSourceFromInvoiceSource` method throws on unrecognized values, enforcing strict mapping integrity for legacy output.

### GetInvoiceType — Maps source to type with transaction-aware fallback
```csharp
switch (billSource)
{
    case nameof(BillSourceEnum.BINV):
        return InvoiceTypeEnum.BunkerInvoice.ToString();
    case nameof(BillSourceEnum.FCOM):
        return InvoiceTypeEnum.FreightCommission.ToString();
    // ... other cases ...
    default:
        if (transType == TransactionTypeEnum.AR.ToString())
        {
            return InvoiceTypeEnum.Miscellaneous.ToString();
        }
        else
        {
            return InvoiceTypeEnum.VoyageExpense.ToString();
        }
}
```
**Explanation**: Resolves invoice type from bill source. Handles both legacy `BillSourceEnum` and BVMS `InvoiceSourceEnum` namespaces in the same switch. The `default` block implements critical fallback logic: Credit Transactions (`AR`) become `Miscellaneous`, while all other unknown sources default to `VoyageExpense`. This prevents null types during ingestion of unexpected data.

### GetBillSourceFromInvoiceSource — Strict BVMS to legacy source mapping
```csharp
switch (invoiceSource)
{
    case nameof(InvoiceSourceEnum.BVMS_FREIGHT):
        return BillSourceEnum.FINV;
    // ... exhaustive cases ...
    default:
        throw new ArgumentOutOfRangeException(nameof(invoiceSource), invoiceSource, null);
}
```
**Explanation**: Reverse mapper used when `USE_IMOS_INVOICE_SOURCE` is `true`. Throws on any unrecognized BVMS source, ensuring that only fully mapped legacy sources reach downstream systems. Used internally by `MapInvoiceSource`.

### GetInvoiceSourceEnumFromInvoiceType — Type to BVMS source mapping
```csharp
switch (invoiceType)
{
    case nameof(InvoiceTypeEnum.Freight):
        return InvoiceSourceEnum.BVMS_FREIGHT;
    case nameof(InvoiceTypeEnum.Laytime):
        return InvoiceSourceEnum.BVMS_DEMURRAGE;
    // ... DA invoice type cases ...
    default:
        throw new ArgumentOutOfRangeException(nameof(invoiceType), invoiceType, null);
}
```
**Explanation**: Maps invoice types to BVMS sources. Groups multiple DA desk types (`PDA`, `APR`, `ADR`, etc.) into a single source (`BVMS_PORT_DA_ADVANCE`). Throws on unsupported types to catch configuration gaps early.

### getPaymentBasisName — Formatting for display
```csharp
switch (paymentBasis)
{
    case nameof(PaymentBasisEnum.Percentage):
        return "Percentage";
    case nameof(PaymentBasisEnum.CPQuantity):
        return "CP Quantity";
    // ... other cases ...
    default:
        return "Unknown";
}
```
**Explanation**: Converts payment basis enums to human-readable strings for UI or report display. Returns "Unknown" for unmapped values rather than throwing, suitable for presentation layers.

### ShipmentTypeDefaultPlItems.ListType — Default P&L items for shipments
```csharp
public static readonly List<string> ListType =
[
    ProfitAndLossIdentifierEnum.FreightAdjustment.ToString(),
    ProfitAndLossIdentifierEnum.MiscellaneousRevenue.ToString(),
    ProfitAndLossIdentifierEnum.MiscellaneousExpense.ToString(),
    ProfitAndLossIdentifierEnum.AddressCommission.ToString(),
    ProfitAndLossIdentifierEnum.PortExpense.ToString(),
    ProfitAndLossIdentifierEnum.CargoExpense.ToString(),
    ProfitAndLossIdentifierEnum.Freight.ToString(),
    ProfitAndLossIdentifierEnum.InternalCommission.ToString(),
    ProfitAndLossIdentifierEnum.BrokerCommission.ToString()
];
```
**Explanation**: Defines the standard set of P&L items available for shipment invoicing. Used by invoice builders to validate or populate available line items.

### ShipmentTypeKeepPlItems.ListType — Protected P&L items
```csharp
public static readonly List<string> ListType = new List<string>
{
    ProfitAndLossIdentifierEnum.Freight.ToString(),
};
```
**Explanation**: Defines P&L items that must be retained/maintained during shipment operations. Currently contains only `Freight`, indicating core freight revenue is immutable during certain workflows.

### CommissionTypePlItems.ListType — Standard commission categories
```csharp
public static readonly List<string> ListType = new List<string>
{
    ProfitAndLossIdentifierEnum.InternalCommission.ToString(),
    ProfitAndLossIdentifierEnum.BrokerCommission.ToString(),
    ProfitAndLossIdentifierEnum.AddressCommission.ToString(),
    ProfitAndLossIdentifierEnum.BrokerCommForMiscRev.ToString(),
    ProfitAndLossIdentifierEnum.AddressCommForMiscRev.ToString(),
};
```
**Explanation**: Enumerates supported commission types for standard voyage invoicing.

### CommissionTypePlItems.TCOListType — TCO-specific commission categories
```csharp
public static readonly List<string> TCOListType = new List<string>
{
    ProfitAndLossIdentifierEnum.InternalTCOCommission.ToString(),
    ProfitAndLossIdentifierEnum.TCOHireAddComm.ToString(),
    ProfitAndLossIdentifierEnum.TCOHireBrokerComm.ToString()
};
```
**Explanation**: Enumerates commission types specific to TCO (Time Charter Out) invoicing, separating them from standard voyage commissions.

---

## Impact Scope
[PLACEHOLDER — will be filled in Phase 3]