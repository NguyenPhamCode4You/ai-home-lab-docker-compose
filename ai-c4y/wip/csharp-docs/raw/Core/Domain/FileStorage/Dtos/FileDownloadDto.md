# FileDownloadDto, FilesDownloadDto

## Purpose
These DTOs define the data contracts for file download operations, specifically for transferring file identifiers and authentication tokens between the application layer and file storage services.

## Business Responsibility
These DTOs support the temporary URL generation workflow identified in `GetTempUrlFileById.cs`. `FileDownloadDto` couples a file's identity with its generated security token, enabling secure, time-limited direct downloads. `FilesDownloadDto` aggregates multiple file IDs to support batch download requests, optimizing network overhead by grouping identifiers.

## Members
No members require documentation; all properties are simple auto-properties (`Token`, `FileId`, `FileIds`) with no computed logic, fallback chains, or domain calculations.

## Dependencies
None. No injected services or external type references beyond standard collections.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]