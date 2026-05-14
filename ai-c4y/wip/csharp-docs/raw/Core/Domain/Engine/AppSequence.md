# AppSequence

## Purpose
Models the persisted state for a named numeric sequence used to generate unique identifiers across bounded contexts. Exists to decouple sequence tracking from calculation logic, providing a single source of truth for current values and step increments.

## Business Responsibility
Owns the domain entity for application and module-specific number sequences. Critical to all identifier generation paths (voyages, invoices, app IDs) because it prevents duplicate ID issuance across distributed or retry scenarios. The configurable step size enables non-consecutive numbering schemes while defaulting to standard incrementation for out-of-the-box behavior