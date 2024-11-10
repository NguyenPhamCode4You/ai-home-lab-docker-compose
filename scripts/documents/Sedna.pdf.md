<!-- image -->

## Integration Support Document

## Document Management

| DATE       |   VERSION | AUTHOR       | REASON          |
|------------|-----------|--------------|-----------------|
| 19/09/2023 |         1 | RebeccaPrice | InitialDocument |

## Contents

Contents

Purpose

Business Use Cases

Introduction

Glossary

Event Stream Document Management

Workflow

Technical Guidance

Event Stream End Point

Message Endpoint

Job Reference Endpoint

Job Reference Field Descriptions

Next Step

## Purpose

This document is designed to be a high level overview of leveraging Sedna's API's for Document management purposes. For full reference to SEDNA API: https://developers.sedna.com/reference

## Business Use Cases

- 1. Automate the saving of documents to an alternate system

Save time by allowing the users to complete a simple action to save documents within an alternate system.

- 2. Use the business transaction information to create a repository of documents

Using a common reference you allow ease of filing structure that is consistent across the business.

- 3. Insert Documents into emails

Create a Sedna App to be able to insert documents directly into emails from an alternate system saving time and context switching.

## Introduction

Sedna's APIs allow you to be able to create integrations with your business systems to provide efficiency, accuracy and context gains. Sedna recommends the following 3 options for leveraging these APIs in the Document Management space.

- 1. Save Documents with Job & Category application using the event stream
- 2. Save Documents via a Connected App
- 3. Insert Documents in the composer with Connected App

## Glossary

Throughout this document we will use terms that are used within Sedna. Please see below table for terms and definitions as we mean them.

| Term              | Definition                                                                                                                                                                                                                                                                                         |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Job Reference Tag | A green tag within Sedna used to group messages that relate to a business transaction, such as Vessel - Voyage or Linkage ID.                                                                                                                                                                      |
| Category Tag      | A blue tag within Sedna that is used to add additional context to a message, such as Recap, Final Documents or Certificates.                                                                                                                                                                       |
| Attributes        | This is the meta data held within a Job Reference, such as Vessel Name, Voyage Reference, Linkage ID or CP Date, that is used for different actions, such as providing a guiding path for integration & auto tagging. The end user cannot see this data but it is required to create the tag. This |
| Message ID        | This is a unique number that each message inside Sedna is given upon ingest. Messages can be found and actions can be taken to messages using this ID number.                                                                                                                                      |
| Job Reference ID  | This is a unique number that each Job Reference Tag is given upon creation                                                                                                                                                                                                                         |
| Category Tag ID   | This is a unique number that each Category Tag is given upon creation                                                                                                                                                                                                                              |

| Message Shared Within Sedna a message can be visible to multiple different mailboxes. Sharing a message allows the message to be visible to another mailbox as specified.   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Event An event is something that is triggered by an action in your Sedna system                                                                                             |
| Event Stream This is a list of current events happening within your Sedna System. This can                                                                                  |
| End Point This is a specific access point to an entity within your Sedna System.                                                                                            |

## Event Stream Document Management

Using Sedna's Event Stream API we allow users to control the saving of documentation in a simple quick action. This aligns with the business case goals 1 & 2. You can use this to save documents into an alternate system and also create a repository of documents.

Sedna should be set up with two things to allow this method to be efficient:

- 1. Job Reference Tags that are linked to a business transaction (or reference in your alternate system) - for example Vessel Name - Voyage Number
- 2. Category Tags that align with where you would like to categorise the Document - eg Certificates, Final Documents, Recap

You will use the Job Reference and its attributes (further detail on attributes in Job Reference section below) plus the Category Tag to be able to retrieve the message ID for download and the information to guide where it should be uploaded into your alternate system.

## Workflow

Below is a high level overview of the flow of this use case.

The coloured flow is related to the end user and the grey flow is related to the flow of the automation.

<!-- image -->

## Technical Guidance

## Event Stream End Point

Use the event endpoint to capture real time events. An event is something that is triggered by an action in your tenant such as sending a message or adding a tag. This endpoint is designed to catch events in real time as they occur. Sedna preserves one month of events so actions to be completed based on events should be taken within this timeframe.

Note that the event endpoint allows you to retrieve data for specific messages that meet a given criteria in a set order. It is not possible to retrieve messages in bulk in the same order via the API at this time.

Events are triggered on the event endpoint as follows:

- ● Message received - event.message.received
- ● Message scheduled (for sending) - event.message.message\_scheduled
- ● Message sent - event.message.sent
- ● Message shared - event.message.shared
- ● Category tag added - event.message.tag.added.category

- ● Category tag removed - event.message.tag.removed.category
- ● Job reference added - event.message.tag.added.job-reference
- ● Job reference removed - event.message.tag.removed.job-reference
- ● Draft edited - event.message.draft.edited

In the situation where you want to save a document to an alternate system based on the application of a category tag, you would use:

- ● Category tag added endpoint looking for the specific Category tag ID identified

You would use this to identify the Sedna Message ID for the mail that the tag has been applied to.

A n example on how to loop specific message events:

- ● Read latest events endpoint [GET] {{baseUrl}}/platform/2019-01-01/event/latest
- ● Read the 'next' link

```
"links": { "self": "https://demo01.sednanetwork.com/platform/2019-01-01/event/latest", "first": "https://demo01.sednanetwork.com/platform/2019-01-01/event/latest", "next": "https://demo01.sednanetwork.com/platform/2019-01-01/event/latest?page[cursor]=00001gcrf3et4000000007q5 310000000000g00" }
```

- ● Loop on the 'next' links. Check on each iteration if anything has changed.

Note - SEDNA plans to implement webhooks for events in the future. This will eliminate the need for a polling loop on events.

## Code example

```
public function loop\_events() { $loop\_wait = 1; //Seconds //Get the latest event $url = $this->base\_url . "/event/latest"; $r = $this->api\_get($url); $url = $r['links']['next']; //This sets us on the current cursor which we'll loop $last\_id = ''; do { $r = $this->api\_get($url); foreach($r['data'] as $ix=>$data) { $id = $data['id']; //If not a new message wait a sec and restart the loop if ($id == $last\_id) {sleep($loop\_wait); continue;}
```

```
//Get basic event metadata $atts = $data['attributes']; $time = $atts['time']; $eventType = $atts['eventType']; //Only deal with incoming messages using the below //if ($eventType <> 'event.message.received') continue; //Get the message subject $msg\_id = $data['relationships']['message']['data']['id']; $msg = $this->get\_message($msg\_id); $subject = $msg['data']['attributes']['subject']; echo "$time $eventType $id $subject "; } $last\_id = $id; $url = $r['links']['next']; sleep($loop\_wait); } while (true); }
```

## Message Endpoint

Once you have the Message ID you can get message information that you need. This is broken down into two pieces.

- 1. The job reference applied to the message
- a. [GET] /platform/2019-01-01/message/{{MessageID}}/relationships/job-reference/
- 2. The documents attached to the message
- a. [GET] /platform/2019-01-01/message/{{MessageID}}/relationships/document

You can also use this to find the category tags applied if you wish to use them to add extra information for the file path for example, save - final documents, save - recap. This can be done using:

- 1. [GET] /platform/2019-01-01/message/{{MessageID}}/relationships/category-tag/

Once you have these two pieces of information you can move onto the next step.

Using the same document endpoint above you would then download the attachments (documents)

## An example below:

```
public function download\_document($in\_document\_id, $in\_file\_loc = '/tmp/sedna\_merge') { //Create destination $in\_file\_loc if it doesn't exists if (!file\_exists($in\_file\_loc)) mkdir($in\_file\_loc,0777); //Download the file to the directory given by $in\_file\_loc $url = $this->base\_url . "/download/document/$in\_document\_id"; $output\_file = "$in\_file\_loc/$in\_document\_id.pdf"; $r = $this->api\_download($url,$output\_file); //api\_download in appendix below return $output\_file; }
```

## Job Reference Endpoint

The job reference is related to the business transaction so should give you the path to finding the record to upload to. This means once you have a result you should then move on to the next step using the

- ● Job Reference Endpoint [GET] {{baseurl}}/platform/2019-01-01/job-reference

## Example job Reference

```
{ "data": { "type": "job-reference", "attributes": { "name": "Vessel Name. - 2202", "archived": false , "date": null , "type": "voyage", "foreignKey": "1667622", "attributes": { "type": "DEFAULT", "vesselName": "Vessel Name", "displayName": "Vessel Name - 2202", "voyageNumber": "2202", "imo": "930215" } } } }
```

## Job Reference Field Descriptions

| Field ref   | Field Name   | Description                                                                                                                                   | Format                                                                       | Examples                                                                                                                | Source      |
|-------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------|
| jr -f1      | data         | Container for al lfie lds                                                                                                                     | n/a                                                                          | n/a                                                                                                                     | n/a         |
| jr-f2       | attribute s  | All Job Reference attributes                                                                                                                  | string                                                                       | n/a                                                                                                                     | System      |
| jr-f3       | name         | Job Reference name                                                                                                                            | String                                                                       | Cape Alaska - 12345                                                                                                     | System      |
| jr-f4       | date         | Created Date associated with transaction                                                                                                      | Iso 8601                                                                     | 2020-02-06T 12:51:47Z                                                                                                   | System      |
| jr-f5       | type         | Job Reference type                                                                                                                            | String value                                                                 | Voyage                                                                                                                  | Fixed value |
| jr-f6       | foreign key  | Unique id relating to alternate system                                                                                                        | String                                                                       | 1667622                                                                                                                 | System      |
| jr-f7       | attribute s  | These are self describing key value pairs. N.B. Other key value pairs may be included for future use, see format for string length constraint | String (Example) Vessel Name Reference Number Port ETA Vessel Email Operator | Vessel Name, Cape Alaska Reference Number, 54323445 Port, Barcelona ETA, 23.08.01 Vessel Email, StarAlaska@ sednashippi | System      |
| jr-f8       | archived     | Two values expected. "True" means Job Reference will not be                                                                                   | String                                                                       | Allowed values "true" or "false"                                                                                        | n/a         |

| jr-f9   |      | considered by Auto-taggers; "False" means Job Reference will be considered by Auto-taggers   |        |                      |     |
|---------|------|----------------------------------------------------------------------------------------------|--------|----------------------|-----|
|         | type | Refers to all Data provided to API                                                           | String | Fixed value "string" | n/a |

## For Reference

- ● The lowest level attributes section can be varied and attributes can be added in this section to support the customer's configuration.
- ● The data.attributes.name value is what shows as the job reference in SEDNA.
- ● The data.type value should indicate the type of job reference. This can be useful when more than one job reference is applied and, for example, an application needs to identify the correct job reference to use for lookups in the alternate system.

## Next Step

These 3 pieces of information should give you the ability to save the documents to your alternate system.

- 1. The category tag event is the trigger that indicates the message or documents should be saved. If you have multiple file structures in your system you can use multiple tags to save under the correct structure, eg. Save - Recap, Save - Certificate, Save Final Documents
- 2. The message id allows you to find the job reference id and the documents to be downloaded.
- 3. The job reference attributes gives you the information to guide you to where the document should be saved for example, using the Vessel name and the reference number.