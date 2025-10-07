# Berkeley CalLink Organizations Enhanced Scraper

A comprehensive Go-based scraper that fetches **complete organization data** from UC Berkeley's CalLink, combining API data with detailed page information.

## Features

- **Comprehensive Data Extraction**: Fetches ALL available organization data
- **Two-Phase Scraping**: API list + individual detail pages
- **Concurrent Processing**: Configurable worker pools for optimal performance
- **Progress Tracking**: Resume capability with automatic checkpointing
- **Retry Logic**: Robust error handling with exponential backoff
- **Rate Limiting**: Respectful scraping to avoid overwhelming servers

## Data Captured

### Basic Information
- ID, Name, ShortName, WebsiteKey
- Description (HTML), Summary
- Status, Visibility, Start/End dates
- Last modified timestamp

### Social Media Links (Complete Set)
- External website
- Facebook, Instagram, LinkedIn 
- Twitter (URL and username)
- YouTube, Vimeo, Flickr
- Pinterest, Tumblr, Google+
- Google Calendar integration

### Contact Information
- **Email address** (organization email)
- **Primary Contact Person**:
  - Full name and preferred name
  - Email address
  - Profile image
  - Privacy settings
- **Physical Address**:
  - Street address (line 1 & 2)
  - City, State, ZIP, Country
  - Phone, extension, fax numbers

### Organization Settings
- **Type Configuration**:
  - Member/officer visibility settings
  - Auto-approval preferences
  - Enabled features (events, finance, elections, etc.)
  - Directory and admin settings
- **Categories**: IDs and names
- **Relationships**: Parent org, branch info
- **Features**: Calendar, Facebook wall, Twitter feed

### Technical Details
- Institution and community IDs
- Discussion and wall IDs
- Legacy keys and migration data
- CSS and group type configurations

## Usage

### Run Complete Scraper
```bash
go run main.go
```
*Fetches API data + enriches with detail pages*

### Configure Workers
```bash
go run main.go -workers=20
```
*Increase concurrent workers for faster processing*

### Resume Interrupted Scraping
```bash
go run main.go -resume
```
*Continues from last checkpoint*

## Output Structure

### Individual Files
```
data/org_91415_africanamericanstudentleadershipteam.json
```
*Complete organization data including all social media, contact info, and settings*

### Combined File
```
data/all_organizations_detailed.json
```
*Array of all organizations with complete data*

### Progress Tracking
```
progress.json
```
*Checkpoint file for resume capability*

## Example Data

```json
{
  "id": 91415,
  "name": "African American Student Leadership Team",
  "email": "aasdprogramming@gmail.com",
  "socialMedia": {
    "facebookUrl": "https://www.facebook.com/aasd.berkeley",
    "instagramUrl": "https://www.instagram.com/aasdatcal/",
    "linkedInUrl": "https://www.linkedin.com/company/42301371/"
  },
  "primaryContact": {
    "firstName": "Lezli",
    "lastName": "Waller", 
    "primaryEmailAddress": "ldwaller@berkeley.edu"
  },
  "contactInfo": [{
    "street1": "Hearst Field Annex D3",
    "city": "Berkeley",
    "state": "CA",
    "zip": "94704-1551"
  }],
  "modifiedOn": "2025-10-02T03:09:08-04:00",
  "startDate": "2013-07-29T00:00:00-04:00"
}
```

## Performance

- **Data Completeness**: 100% of available organization data
- **Speed**: Processes ~300-400 orgs per minute with default settings
- **Total Organizations**: 1,307+ from Berkeley CalLink
- **Data Sources**: API + Individual detail pages
- **Reliability**: Automatic retry with exponential backoff
- **Resume Capability**: Never lose progress on interruptions

## Technical Architecture

1. **Phase 1**: Fetch organization list from CalLink API (fast)
2. **Phase 2**: Enrich each org with detail page data (comprehensive)
3. **Data Merging**: Combine API + detail page data intelligently
4. **Concurrent Processing**: Multiple workers process pages simultaneously
5. **Progress Tracking**: Checkpoint completed organizations
6. **Output Generation**: Individual files + combined dataset

This enhanced scraper provides the most complete dataset possible from Berkeley's CalLink system, capturing every available piece of organization information including social media presence, contact details, and administrative settings.