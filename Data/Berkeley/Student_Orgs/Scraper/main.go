package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"math"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"sync"
	"time"
)

// SocialMedia represents social media links
type SocialMedia struct {
	ExternalWebsite   string  `json:"externalWebsite"`
	FacebookUrl       string  `json:"facebookUrl"`
	TwitterUrl        string  `json:"twitterUrl"`
	TwitterUserName   *string `json:"twitterUserName"`
	InstagramUrl      string  `json:"instagramUrl"`
	LinkedInUrl       string  `json:"linkedInUrl"`
	YoutubeUrl        string  `json:"youtubeUrl"`
	FlickrUrl         string  `json:"flickrUrl"`
	GoogleCalendarUrl string  `json:"googleCalendarUrl"`
	GooglePlusUrl     string  `json:"googlePlusUrl"`
	PinterestUrl      string  `json:"pinterestUrl"`
	TumblrUrl         string  `json:"tumblrUrl"`
	VimeoUrl          string  `json:"vimeoUrl"`
}

// PrimaryContact represents the primary contact person
type PrimaryContact struct {
	ID                   string  `json:"id"`
	FirstName            string  `json:"firstName"`
	LastName             string  `json:"lastName"`
	PreferredFirstName   *string `json:"preferredFirstName"`
	PrimaryEmailAddress  string  `json:"primaryEmailAddress"`
	ProfileImageFilePath *string `json:"profileImageFilePath"`
	InstitutionID        int     `json:"institutionId"`
	Privacy              string  `json:"privacy"`
}

// ContactInfo represents contact information
type ContactInfo struct {
	ID           int     `json:"id"`
	AddressType  int     `json:"addressType"`
	PhoneNumber  *string `json:"phoneNumber"`
	Extension    *string `json:"extension"`
	FaxNumber    *string `json:"faxNumber"`
	Street1      *string `json:"street1"`
	Street2      *string `json:"street2"`
	City         *string `json:"city"`
	State        *string `json:"state"`
	Zip          *string `json:"zip"`
	Country      *string `json:"country"`
	Deleted      bool    `json:"deleted"`
}

// OrganizationType represents organization type settings
type OrganizationType struct {
	ID                              int     `json:"id"`
	BranchID                        int     `json:"branchId"`
	Name                            string  `json:"name"`
	ShowMembersToPublic             bool    `json:"showMembersToPublic"`
	ShowOfficersToPublic            bool    `json:"showOfficersToPublic"`
	ShowMembersToLoggedInUsersByDefault bool `json:"showMembersToLoggedInUsersByDefault"`
	ShowOfficersToLoggedInUsersByDefault bool `json:"showOfficersToLoggedInUsersByDefault"`
	AutoApproveRequests             bool    `json:"autoApproveRequests"`
	EventsEnabled                   bool    `json:"eventsEnabled"`
	ServiceHoursEnabled             bool    `json:"serviceHoursEnabled"`
	FinanceEnabled                  bool    `json:"financeEnabled"`
	FinanceRequestsEnabled          bool    `json:"financeRequestsEnabled"`
	FundingRequestsEnabled          bool    `json:"fundingRequestsEnabled"`
	PurchaseRequestsEnabled         bool    `json:"purchaseRequestsEnabled"`
	BudgetingEnabled                bool    `json:"budgetingEnabled"`
	BudgetingRequestsEnabled        bool    `json:"budgetingRequestsEnabled"`
	ElectionsEnabled                bool    `json:"electionsEnabled"`
	FormsEnabled                    bool    `json:"formsEnabled"`
	GalleryEnabled                  bool    `json:"galleryEnabled"`
	OutcomesEnabled                 bool    `json:"outcomesEnabled"`
	RosterEnabled                   bool    `json:"rosterEnabled"`
	DocumentsEnabled                bool    `json:"documentsEnabled"`
	IsShownInPublicDirectory        bool    `json:"shownInPublicDirectory"`
	IsSystemType                    bool    `json:"isSystemType"`
	AdminOnly                       bool    `json:"adminOnly"`
	IsClosed                        bool    `json:"isClosed"`
	ReRegistrationAvailability      *string `json:"reRegistrationAvailabilty"`
}

// Category represents an organization category
type Category struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

// CoverPhoto represents cover photo information
type CoverPhoto struct {
	ID            int    `json:"id"`
	ImageID       string `json:"imageId"`
	ImagePath     string `json:"imagePath"`
	URL           string `json:"url"`
	ThumbnailURL  string `json:"thumbnailUrl"`
	Caption       string `json:"caption"`
	DateCreated   string `json:"dateCreated"`
	InstitutionID int    `json:"institutionId"`
}

// PrimaryContactID represents primary contact ID information
type PrimaryContactID struct {
	CommunityMemberID int    `json:"communityMemberId"`
	AccountID         string `json:"accountId"`
	CampusEmail       string `json:"campusEmail"`
}

// Organization represents the complete structure of an organization
type Organization struct {
	// Core Fields (from API and detail page - using interface{} for flexible types)
	ID                   interface{} `json:"id"`
	InstitutionID        int         `json:"institutionId"`
	ParentOrganizationID interface{} `json:"parentOrganizationId"`
	BranchID             interface{} `json:"branchId"`
	Name                 string      `json:"name"`
	ShortName            *string     `json:"shortName"`
	WebsiteKey           string      `json:"websiteKey"`
	ProfilePicture       string      `json:"profilePicture"`
	ProfilePictureURL    string      `json:"profilePictureURL"`
	Description          string      `json:"description"` 
	Summary              string      `json:"summary"`
	CategoryIDs          []string    `json:"categoryIds"`
	CategoryNames        []string    `json:"categoryNames"`
	Status               string      `json:"status"`
	Visibility           string      `json:"visibility"`

	// Enhanced Fields (from detail page)
	Email                    string           `json:"email"`
	CommunityID              int              `json:"communityId"`
	NameSortKey              string           `json:"nameSortKey"`
	Comment                  *string          `json:"comment"`
	ShowJoin                 bool             `json:"showJoin"`
	StatusChangeDateTime     string           `json:"statusChangeDateTime"`
	StartDate                *string          `json:"startDate"`
	EndDate                  *string          `json:"endDate"`
	ParentID                 *int             `json:"parentId"`
	WallID                   *int             `json:"wallId"`
	DiscussionID             *int             `json:"discussionId"`
	GroupTypeID              *int             `json:"groupTypeId"`
	OrganizationTypeID       int              `json:"organizationTypeId"`
	CssConfigurationID       *int             `json:"cssConfigurationId"`
	Deleted                  bool             `json:"deleted"`
	EnableGoogleCalendar     bool             `json:"enableGoogleCalendar"`
	ModifiedOn               string           `json:"modifiedOn"`
	ShowFacebookWall         bool             `json:"showFacebookWall"`
	ShowTwitterFeed          bool             `json:"showTwitterFeed"`
	IsShownInPublicDirectory bool             `json:"isShownInPublicDirectory"`
	IsAdminOnly              bool             `json:"isAdminOnly"`
	IsBranch                 bool             `json:"isBranch"`
	LegacyKey                interface{}      `json:"legacyKey"`
	ParentLegacyKey          interface{}      `json:"parentLegacyKey"`
	LegacyPrimaryContactKey  interface{}      `json:"legacyPrimaryContactKey"` 

	// Complex nested objects
	SocialMedia       SocialMedia       `json:"socialMedia"`
	PrimaryContact    PrimaryContact    `json:"primaryContact"`
	PrimaryContactID  PrimaryContactID  `json:"primaryContactId"`
	ContactInfo       []ContactInfo     `json:"contactInfo"`
	OrganizationType  OrganizationType  `json:"organizationType"`
	Categories        []Category        `json:"categories"`
	Submissions       []interface{}     `json:"submissions"`
	CoverPhoto        CoverPhoto        `json:"coverPhoto"`
	
	// Additional metadata
	ImageServerBaseURL string `json:"imageServerBaseUrl"`
	BaseURL           string `json:"baseUrl"`
}

// APIResponse represents the structure of the API response
type APIResponse struct {
	Context  string         `json:"@odata.context"`
	Count    int            `json:"@odata.count"`
	Coverage float64        `json:"@search.coverage"`
	Value    []Organization `json:"value"`
}

// DetailPageData represents the structure of the detail page JavaScript data
type DetailPageData struct {
	PreFetchedData struct {
		Organization Organization `json:"organization"`
	} `json:"preFetchedData"`
}

// Progress tracks scraping progress for resume capability
type Progress struct {
	TotalOrgs      int    `json:"totalOrgs"`
	ScrapedOrgs    int    `json:"scrapedOrgs"`
	LastSkip       int    `json:"lastSkip"`
	LastUpdated    string `json:"lastUpdated"`
	CompletedPages []int  `json:"completedPages"`
	CompletedOrgs  []string `json:"completedOrgs"`
}

// ScraperConfig holds configuration for the scraper
type ScraperConfig struct {
	Workers    int
	PageSize   int
	Resume     bool
	BaseURL    string
	UserAgent  string
	MaxRetries int
	RetryDelay time.Duration
}

// Scraper manages the scraping process
type Scraper struct {
	config   ScraperConfig
	client   *http.Client
	progress Progress
	mu       sync.Mutex
}

func main() {
	var workers = flag.Int("workers", 10, "Number of concurrent workers")
	var resume = flag.Bool("resume", false, "Resume from last checkpoint")
	flag.Parse()

	config := ScraperConfig{
		Workers:    *workers,
		PageSize:   100,
		Resume:     *resume,
		BaseURL:    "https://callink.berkeley.edu/api/discovery/search/organizations",
		UserAgent:  "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
		MaxRetries: 3,
		RetryDelay: time.Second * 2,
	}

	scraper := NewScraper(config)

	log.Printf("Starting Berkeley CalLink enhanced scraper with %d workers", config.Workers)

	if err := scraper.Run(); err != nil {
		log.Fatalf("Scraper failed: %v", err)
	}

	log.Println("Enhanced scraping completed successfully!")
}

// NewScraper creates a new scraper instance
func NewScraper(config ScraperConfig) *Scraper {
	client := &http.Client{
		Timeout: 30 * time.Second,
		Transport: &http.Transport{
			MaxIdleConns:        100,
			MaxIdleConnsPerHost: 10,
			IdleConnTimeout:     30 * time.Second,
		},
	}

	return &Scraper{
		config: config,
		client: client,
	}
}

// Run executes the enhanced scraping process
func (s *Scraper) Run() error {
	// Load or initialize progress
	if err := s.loadProgress(); err != nil && !s.config.Resume {
		log.Printf("Could not load progress, starting fresh: %v", err)
		s.progress = Progress{
			CompletedPages: make([]int, 0),
			CompletedOrgs:  make([]string, 0),
		}
	}

	// Get total count first
	if s.progress.TotalOrgs == 0 {
		totalOrgs, err := s.getTotalCount()
		if err != nil {
			return fmt.Errorf("failed to get total count: %w", err)
		}
		s.progress.TotalOrgs = totalOrgs
		log.Printf("Found %d total organizations", totalOrgs)
	}

	// Get all organizations from API first
	log.Println("Fetching organization list from API...")
	allOrgs, err := s.fetchAllOrganizations()
	if err != nil {
		return fmt.Errorf("failed to fetch organizations: %w", err)
	}

	log.Printf("Fetched %d organizations from API, now enriching with detail pages...", len(allOrgs))

	// Create workers for detail page fetching
	orgsChan := make(chan Organization, len(allOrgs))
	resultsChan := make(chan Organization, len(allOrgs))
	var wg sync.WaitGroup

	// Start workers
	for i := 0; i < s.config.Workers; i++ {
		wg.Add(1)
		go s.detailWorker(i, orgsChan, resultsChan, &wg)
	}

	// Queue organizations that haven't been completed
	orgsQueued := 0
	for _, org := range allOrgs {
		if !s.isOrgCompleted(fmt.Sprintf("%v", org.ID)) {
			orgsChan <- org
			orgsQueued++
		}
	}
	close(orgsChan)

	log.Printf("Queued %d organizations for detail enrichment", orgsQueued)

	// Start results collector
	go s.collectDetailResults(resultsChan, orgsQueued)

	// Wait for all workers to complete
	wg.Wait()
	close(resultsChan)

	// Wait a bit for results collector to finish
	time.Sleep(2 * time.Second)

	// Save final combined file
	if err := s.saveCombinedFile(); err != nil {
		log.Printf("Warning: Failed to save combined file: %v", err)
	}

	return nil
}

// fetchAllOrganizations fetches all organizations from the API
func (s *Scraper) fetchAllOrganizations() ([]Organization, error) {
	totalPages := int(math.Ceil(float64(s.progress.TotalOrgs) / float64(s.config.PageSize)))
	var allOrgs []Organization

	for page := 0; page < totalPages; page++ {
		skip := page * s.config.PageSize
		orgs, err := s.fetchOrganizations(skip)
		if err != nil {
			return nil, fmt.Errorf("failed to fetch page %d: %w", page+1, err)
		}
		allOrgs = append(allOrgs, orgs...)
		
		if page%5 == 0 {
			log.Printf("Fetched page %d/%d (%d orgs)", page+1, totalPages, len(allOrgs))
		}
	}

	return allOrgs, nil
}

// detailWorker processes organizations to fetch their detail pages
func (s *Scraper) detailWorker(id int, orgs <-chan Organization, results chan<- Organization, wg *sync.WaitGroup) {
	defer wg.Done()

	for org := range orgs {
		log.Printf("Worker %d: Enriching org %v (%s)", id, org.ID, org.WebsiteKey)

		enrichedOrg, err := s.enrichOrganization(org)
		if err != nil {
			log.Printf("Worker %d: Failed to enrich org %v: %v", id, org.ID, err)
			// Still save the basic org data
			enrichedOrg = org
		}

		results <- enrichedOrg

		// Mark org as completed
		s.markOrgCompleted(fmt.Sprintf("%v", org.ID))

		// Update progress
		s.mu.Lock()
		s.progress.ScrapedOrgs++
		s.progress.LastUpdated = time.Now().Format(time.RFC3339)
		s.mu.Unlock()

		// Save progress periodically
		if s.progress.ScrapedOrgs%10 == 0 {
			s.saveProgress()
		}

		// Rate limiting
		time.Sleep(200 * time.Millisecond)
	}
}

// enrichOrganization fetches detail page data and merges it with API data
func (s *Scraper) enrichOrganization(org Organization) (Organization, error) {
	if org.WebsiteKey == "" {
		return org, fmt.Errorf("no websiteKey available")
	}

	url := fmt.Sprintf("https://callink.berkeley.edu/organization/%s", org.WebsiteKey)

	var detailOrg Organization

	// Retry logic
	for attempt := 0; attempt <= s.config.MaxRetries; attempt++ {
		if attempt > 0 {
			waitTime := time.Duration(attempt) * s.config.RetryDelay
			time.Sleep(waitTime)
		}

		req, err := http.NewRequest("GET", url, nil)
		if err != nil {
			continue
		}

		req.Header.Set("User-Agent", s.config.UserAgent)
		req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")

		resp, err := s.client.Do(req)
		if err != nil {
			if attempt == s.config.MaxRetries {
				return org, fmt.Errorf("HTTP request failed after %d attempts: %w", s.config.MaxRetries+1, err)
			}
			continue
		}

		body, err := io.ReadAll(resp.Body)
		resp.Body.Close()

		if err != nil {
			if attempt == s.config.MaxRetries {
				return org, fmt.Errorf("failed to read response body: %w", err)
			}
			continue
		}

		if resp.StatusCode != 200 {
			if attempt == s.config.MaxRetries {
				return org, fmt.Errorf("detail page returned status %d", resp.StatusCode)
			}
			continue
		}

		// Extract and parse the JavaScript data
		detailOrg, err = s.parseDetailPage(string(body))
		if err != nil {
			if attempt == s.config.MaxRetries {
				return org, fmt.Errorf("failed to parse detail page: %w", err)
			}
			continue
		}

		// Success!
		break
	}

	// Merge API data with detail page data
	mergedOrg := s.mergeOrganizationData(org, detailOrg)
	return mergedOrg, nil
}

// parseDetailPage extracts organization data from the detail page HTML
func (s *Scraper) parseDetailPage(html string) (Organization, error) {
	// Extract the JavaScript object using regex
	re := regexp.MustCompile(`window\.initialAppState\s*=\s*({.*?});`)
	matches := re.FindStringSubmatch(html)
	
	if len(matches) < 2 {
		return Organization{}, fmt.Errorf("could not find initialAppState in HTML")
	}

	var pageData DetailPageData
	if err := json.Unmarshal([]byte(matches[1]), &pageData); err != nil {
		return Organization{}, fmt.Errorf("failed to parse initialAppState JSON: %w", err)
	}

	org := pageData.PreFetchedData.Organization
	
	// Extract additional data from the full JSON structure
	var fullData map[string]interface{}
	if err := json.Unmarshal([]byte(matches[1]), &fullData); err == nil {
		// Extract imageServerBaseURL if available
		if prefetchedData, ok := fullData["preFetchedData"].(map[string]interface{}); ok {
			if imageServerBaseURL, ok := prefetchedData["imageServerBaseUrl"].(string); ok {
				org.ImageServerBaseURL = imageServerBaseURL
			}
			
			// Extract cover photo data from organization
			if orgData, ok := prefetchedData["organization"].(map[string]interface{}); ok {
				if coverPhotoData, ok := orgData["coverPhoto"].(map[string]interface{}); ok {
					org.CoverPhoto = extractCoverPhoto(coverPhotoData)
				}
				
				// Extract primaryContactId data
				if primaryContactIdData, ok := orgData["primaryContactId"].(map[string]interface{}); ok {
					org.PrimaryContactID = extractPrimaryContactID(primaryContactIdData)
				}
			}
		}
	}

	return org, nil
}

// extractCoverPhoto extracts cover photo data from raw interface{} data
func extractCoverPhoto(data map[string]interface{}) CoverPhoto {
	coverPhoto := CoverPhoto{}
	
	if id, ok := data["id"].(float64); ok {
		coverPhoto.ID = int(id)
	}
	if imageId, ok := data["imageId"].(string); ok {
		coverPhoto.ImageID = imageId
	}
	if imagePath, ok := data["imagePath"].(string); ok {
		coverPhoto.ImagePath = imagePath
	}
	if url, ok := data["url"].(string); ok {
		coverPhoto.URL = url
	}
	if thumbnailUrl, ok := data["thumbnailUrl"].(string); ok {
		coverPhoto.ThumbnailURL = thumbnailUrl
	}
	if caption, ok := data["caption"].(string); ok {
		coverPhoto.Caption = caption
	}
	if dateCreated, ok := data["dateCreated"].(string); ok {
		coverPhoto.DateCreated = dateCreated
	}
	if institutionId, ok := data["institutionId"].(float64); ok {
		coverPhoto.InstitutionID = int(institutionId)
	}
	
	return coverPhoto
}

// extractPrimaryContactID extracts primary contact ID data from raw interface{} data
func extractPrimaryContactID(data map[string]interface{}) PrimaryContactID {
	contactID := PrimaryContactID{}
	
	if communityMemberId, ok := data["communityMemberId"].(float64); ok {
		contactID.CommunityMemberID = int(communityMemberId)
	}
	if accountId, ok := data["accountId"].(string); ok {
		contactID.AccountID = accountId
	}
	if campusEmail, ok := data["campusEmail"].(string); ok {
		contactID.CampusEmail = campusEmail
	}
	
	return contactID
}

// mergeOrganizationData merges API data with detail page data
func (s *Scraper) mergeOrganizationData(apiOrg, detailOrg Organization) Organization {
	// Start with detail page data (more complete)
	merged := detailOrg

	// Preserve API fields that might be missing from detail page
	if merged.CategoryIDs == nil && len(apiOrg.CategoryIDs) > 0 {
		merged.CategoryIDs = apiOrg.CategoryIDs
	}
	if merged.CategoryNames == nil && len(apiOrg.CategoryNames) > 0 {
		merged.CategoryNames = apiOrg.CategoryNames
	}

	// Build full profile picture URL if we have the filename and base URL
	if merged.ProfilePicture != "" && merged.ImageServerBaseURL != "" {
		merged.ProfilePictureURL = fmt.Sprintf("%s/%s", merged.ImageServerBaseURL, merged.ProfilePicture)
	} else if merged.ProfilePicture != "" {
		// Fallback to CalLink's standard image server URL
		merged.ProfilePictureURL = fmt.Sprintf("https://se-images.campuslabs.com/clink/images/%s", merged.ProfilePicture)
	}

	// Set base URL for reference
	merged.BaseURL = "https://callink.berkeley.edu"

	return merged
}

// collectDetailResults saves enriched organizations to files
func (s *Scraper) collectDetailResults(results <-chan Organization, expectedOrgs int) {
	orgCount := 0
	for org := range results {
		if err := s.saveOrganization(org); err != nil {
			log.Printf("Failed to save organization %v: %v", org.ID, err)
		}
		orgCount++
		if orgCount%25 == 0 {
			log.Printf("Saved %d/%d enriched organizations", orgCount, expectedOrgs)
		}
	}
	log.Printf("Results collector finished. Saved %d enriched organizations", orgCount)
}

// fetchOrganizations fetches a page of organizations from the API
func (s *Scraper) fetchOrganizations(skip int) ([]Organization, error) {
	url := fmt.Sprintf("%s?orderBy%%5B0%%5D=UpperName%%20asc&top=%d&filter=&query=&skip=%d",
		s.config.BaseURL, s.config.PageSize, skip)

	var resp APIResponse

	// Retry logic
	for attempt := 0; attempt <= s.config.MaxRetries; attempt++ {
		if attempt > 0 {
			waitTime := time.Duration(attempt) * s.config.RetryDelay
			time.Sleep(waitTime)
		}

		req, err := http.NewRequest("GET", url, nil)
		if err != nil {
			continue
		}

		req.Header.Set("User-Agent", s.config.UserAgent)
		req.Header.Set("Accept", "application/json")

		httpResp, err := s.client.Do(req)
		if err != nil {
			if attempt == s.config.MaxRetries {
				return nil, fmt.Errorf("HTTP request failed after %d attempts: %w", s.config.MaxRetries+1, err)
			}
			continue
		}

		body, err := io.ReadAll(httpResp.Body)
		httpResp.Body.Close()

		if err != nil {
			if attempt == s.config.MaxRetries {
				return nil, fmt.Errorf("failed to read response body: %w", err)
			}
			continue
		}

		if httpResp.StatusCode != 200 {
			if attempt == s.config.MaxRetries {
				return nil, fmt.Errorf("API returned status %d: %s", httpResp.StatusCode, string(body))
			}
			continue
		}

		if err = json.Unmarshal(body, &resp); err != nil {
			if attempt == s.config.MaxRetries {
				return nil, fmt.Errorf("failed to parse JSON response: %w", err)
			}
			continue
		}

		// Success!
		break
	}

	return resp.Value, nil
}

// getTotalCount gets the total number of organizations
func (s *Scraper) getTotalCount() (int, error) {
	url := fmt.Sprintf("%s?orderBy%%5B0%%5D=UpperName%%20asc&top=1&filter=&query=&skip=0", s.config.BaseURL)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return 0, err
	}

	req.Header.Set("User-Agent", s.config.UserAgent)
	req.Header.Set("Accept", "application/json")

	resp, err := s.client.Do(req)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return 0, err
	}

	var apiResp APIResponse
	if err = json.Unmarshal(body, &apiResp); err != nil {
		return 0, err
	}

	return apiResp.Count, nil
}

// saveOrganization saves an individual organization to a JSON file
func (s *Scraper) saveOrganization(org Organization) error {
	filename := fmt.Sprintf("org_%v.json", org.ID)
	if org.WebsiteKey != "" && org.WebsiteKey != "null" {
		filename = fmt.Sprintf("org_%v_%s.json", org.ID, sanitizeFilename(org.WebsiteKey))
	}

	filepath := filepath.Join("data", filename)

	data, err := json.MarshalIndent(org, "", "  ")
	if err != nil {
		return err
	}

	return os.WriteFile(filepath, data, 0644)
}

// saveCombinedFile saves all organizations to a single combined file
func (s *Scraper) saveCombinedFile() error {
	log.Println("Creating combined organizations file...")

	files, err := filepath.Glob("data/org_*.json")
	if err != nil {
		return err
	}

	var allOrgs []Organization

	for _, file := range files {
		data, err := os.ReadFile(file)
		if err != nil {
			log.Printf("Warning: Could not read %s: %v", file, err)
			continue
		}

		var org Organization
		if err := json.Unmarshal(data, &org); err != nil {
			log.Printf("Warning: Could not parse %s: %v", file, err)
			continue
		}

		allOrgs = append(allOrgs, org)
	}

	log.Printf("Combined %d organizations into single file", len(allOrgs))

	combinedData, err := json.MarshalIndent(allOrgs, "", "  ")
	if err != nil {
		return err
	}

	return os.WriteFile(filepath.Join("data", "all_organizations_detailed.json"), combinedData, 0644)
}

// Progress tracking functions
func (s *Scraper) loadProgress() error {
	if !s.config.Resume {
		return fmt.Errorf("resume not enabled")
	}

	data, err := os.ReadFile("progress.json")
	if err != nil {
		return err
	}

	return json.Unmarshal(data, &s.progress)
}

func (s *Scraper) saveProgress() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	data, err := json.MarshalIndent(s.progress, "", "  ")
	if err != nil {
		return err
	}

	return os.WriteFile("progress.json", data, 0644)
}

func (s *Scraper) isPageCompleted(page int) bool {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, completedPage := range s.progress.CompletedPages {
		if completedPage == page {
			return true
		}
	}
	return false
}

func (s *Scraper) markPageCompleted(page int) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, completedPage := range s.progress.CompletedPages {
		if completedPage == page {
			return
		}
	}

	s.progress.CompletedPages = append(s.progress.CompletedPages, page)
}

func (s *Scraper) isOrgCompleted(orgID string) bool {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, completedOrg := range s.progress.CompletedOrgs {
		if completedOrg == orgID {
			return true
		}
	}
	return false
}

func (s *Scraper) markOrgCompleted(orgID string) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, completedOrg := range s.progress.CompletedOrgs {
		if completedOrg == orgID {
			return
		}
	}

	s.progress.CompletedOrgs = append(s.progress.CompletedOrgs, orgID)
}

// sanitizeFilename removes or replaces invalid characters for filenames
func sanitizeFilename(s string) string {
	invalid := []string{"/", "\\", ":", "*", "?", "\"", "<", ">", "|", " "}
	result := s
	for _, char := range invalid {
		result = strings.ReplaceAll(result, char, "_")
	}

	if len(result) > 50 {
		result = result[:50]
	}

	return result
}