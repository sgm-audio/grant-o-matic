# Canadian Grant Databases Research

## Primary Federal Funding Agencies

### 1. Canada Council for the Arts
- Website: https://canadacouncil.ca/
- Key Programs for Musicians:
  - Grants for Professional Musicians
  - Grants for Music Organizations
  - Grants for Collaborative Projects
  - Travel Grants
- Application Cycles: Varies by program (typically 2-4 per year)
- Data Points to Capture:
  - Program name
  - Description
  - Eligibility criteria
  - Deadline dates
  - Funding amount range
  - Required documentation
  - Assessment criteria

### 2. FACTOR (Foundation Assisting Canadian Talent on Recordings)
- Website: https://factor.ca/
- Key Programs:
  - Juried Sound Recording
  - Comprehensive Artist
  - Comprehensive Music Company
  - Marketing Assistance for Labels
  - Showcase Funding
  - Video Program
- Application Cycles: Multiple deadlines throughout year
- Data Points to Capture:
  - Program name
  - Description
  - Eligibility (artist vs company)
  - Deadline dates
  - Maximum funding amounts
  - Matching fund requirements
  - Genre restrictions (if any)

### 3. Musicaction
- Website: https://musicaction.ca/
- Key Programs (Francophone focus):
  - Développement de carrière artistique
  - Développement de l'industrie musicale
  - Soutien à la réalisation d'enregistrements sonores
  - VidéoMusique
  - Chantiers
- Application Cycles: Varies by program
- Data Points to Capture:
  - Program name (French/English)
  - Description
  - Eligibility criteria (Quebec/Francophone focus)
  - Deadline dates
  - Funding amounts
  - Language requirements

## Provincial Funding Agencies

### 4. Ontario Arts Council (OAC)
- Website: https://www.arts.on.ca/
- Key Programs:
  - Music Creation Projects
  - Music Recording Projects
  - Music Performance Projects
  - Music Touring
- Application Cycles: Varies (typically 3-4 per year)
- Data Points to Capture:
  - Program name
  - Description
  - Eligibility (Ontario residents/organizations)
  - Deadline dates
  - Grant amounts
  - Assessment criteria

### 5. BC Arts Council
- Website: https://www.bcartscouncil.ca/
- Key Programs:
  - Project Assistance
  - Career Development
  - Organizational Development
- Application Cycles: Multiple intakes
- Data Points to Capture:
  - Program name
  - Description
  - Eligibility (BC residents)
  - Deadline dates
  - Funding ranges
  - Assessment process

## Federal Film/Media Funding (Relevant for Audio-Visual Work)

### 6. Telefilm Canada
- Website: https://www.telefilm.ca/
- Key Programs Relevant to Musicians:
  - Talent Fund (for emerging creators)
  - Production Programs (for soundtracks/score work)
  - Marketing Programs
- Application Cycles: Varies by program
- Data Points to Capture:
  - Program name
  - Description
  - Eligibility criteria
  - Deadline dates
  - Funding amounts
  - Specific requirements for music/sound work

## Tax Credit Programs (Different Structure - Refundable Credits)

### 7. Canadian Audio Recording Tax Credits
- Administered by: Canada Revenue Agency (CRA)
- Programs:
  - Ontario Sound Recording Tax Credit (OSRTC)
  - British Columbia Production Services Tax Credit (includes music)
  - Quebec Refundable Tax Credit for Musical Production
  - Others (varies by province)
- Data Points to Capture:
  - Program name
  - Province/jurisdiction
  - Eligibility criteria
  - Percentage refundable
  - Maximum claim amounts
  - Required documentation
  - Application process (through tax filing)

## Data Structure for Grant Opportunities

Each grant opportunity should capture:

```json
{
  "id": "unique-identifier",
  "program_name": "Full Program Name",
  "administering_agency": "Canada Council for the Arts",
  "description": "Detailed description of what the grant funds",
  "eligibility_criteria": {
    "artist_type": ["individual", "group", "organization"],
    "residency_requirements": ["Canadian citizen", "Permanent resident"],
    "genre_restrictions": ["All genres" or specific genres],
    "career_stage": ["Emerging", "Established", "Any"],
    "project_type": ["Recording", "Touring", "Creation", "Performance"]
  },
  "deadline_info": {
    "frequency": "Quarterly/Biannual/Annual/Rolling",
    "next_deadline": "YYYY-MM-DD",
    "application_window": "Start date to End date"
  },
  "funding_details": {
    "min_amount": 0,
    "max_amount": 50000,
    "average_award": 15000,
    "funding_type": "Grant/Contribution",
    "requires_matching_funds": true/false,
    "matching_requirements": "Description if applicable"
  },
  "application_requirements": [
    "Project description",
    "Budget",
    "Work samples",
    "Letters of support",
    "Artist CV/bio",
    "Marketing plan"
  ],
  "assessment_criteria": [
    "Artistic merit",
    "Viability",
    "Impact",
    "Feasibility"
  ],
  "url": "Direct link to application guidelines",
  "last_updated": "YYYY-MM-DD",
  "status": "Active/Inactive/Upcoming"
}
```

## Scraping Considerations

1. **Rate Limiting**: Respectful scraping with delays between requests
2. **Data Freshness**: Schedule regular updates (daily/weekly)
3. **Change Detection**: Track when grant programs change significantly
4. **Language Handling**: Handle both English and French content (especially for Musicaction/Quebec programs)
5. **PDF Extraction**: Many guidelines are in PDF format - need PDF parsing capability
6. **Authentication**: Some portals may require login for full details

## Priority Order for Implementation

1. Canada Council for the Arts (most comprehensive)
2. FACTOR (major music-specific funder)
3. Musicaction (important for Francophone market)
4. Provincial arts councils (OAC, BC Arts Council)
5. Telefilm Canada (for audio-visual musicians)
6. Tax credit programs (more complex, may require separate handling)

## Integration Points

The scraped data will feed into:
1. The Grant Matching Algorithm (AI component)
2. The Deadline Tracking/Alert System
3. The Application Assistant (for generating materials)
4. The User Dashboard showing personalized opportunities