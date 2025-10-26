"""
Configuration for UCOP scraper system.
"""

# Organization definitions
# UCOP Organizations (in ucop/ directory)
UCOP_ORGANIZATIONS = {
    "ucop/academic_affairs": {
        "name": "Academic Affairs",
        "main_url": "https://www.ucop.edu/academic-affairs/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/academic-affairs/staff/index.html"
        }
    },
    "ucop/ethics_compliance_audit_services": {
        "name": "Ethics, Compliance and Audit Services",
        "main_url": "https://www.ucop.edu/ethics-compliance-audit-services/index.html",
        "staff_urls": {
            "leadership": "https://www.ucop.edu/ethics-compliance-audit-services/staff/leadership/index.html",
            "compliance": "https://www.ucop.edu/ethics-compliance-audit-services/staff/compliance/index.html",
            "audit": "https://www.ucop.edu/ethics-compliance-audit-services/staff/audit/index.html",
            "investigations": "https://www.ucop.edu/ethics-compliance-audit-services/staff/investigations/index.html",
            "policy": "https://www.ucop.edu/ethics-compliance-audit-services/staff/policy/index.html"
        }
    },
    "ucop/external_relations_communications": {
        "name": "External Relations and Communications",
        "main_url": "https://ucop.edu/external-relations-communications/index.html",
        "staff_urls": {
            "main": "https://ucop.edu/external-relations-communications/staff/index.html"
        }
    },
    "ucop/uc_finance": {
        "name": "UC Finance",
        "main_url": "https://www.ucop.edu/finance-office/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/finance-office/staff/index.html"
        }
    },
    "ucop/uc_investments": {
        "name": "UC Investments",
        "main_url": "https://www.ucop.edu/investment-office/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/investment-office/staff/index.html"
        }
    },
    "ucop/uc_legal": {
        "name": "UC Legal - Office of the General Counsel",
        "main_url": "https://www.ucop.edu/uc-legal/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/uc-legal/staff/index.html"
        }
    },
    "ucop/uc_national_laboratories": {
        "name": "UC National Laboratories",
        "main_url": "https://www.ucop.edu/laboratory-management/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/laboratory-management/staff/index.html"
        }
    },
    "ucop/uc_operations": {
        "name": "UC Operations",
        "main_url": "https://www.ucop.edu/uc-operations/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/uc-operations/staff/index.html"
        }
    },
    "ucop/university_of_california_health": {
        "name": "University of California Health",
        "main_url": "https://www.ucop.edu/uc-health/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/uc-health/staff/index.html"
        }
    },
    "ucop/systemwide_office_of_civil_rights": {
        "name": "Systemwide Office of Civil Rights",
        "main_url": "https://www.ucop.edu/office-civil-rights/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/office-civil-rights/staff/index.html"
        }
    }
}

# Other UC Organizations (to be configured as scrapers are added)
OTHER_ORGANIZATIONS = {
    # Academic Senate - to be added
    # Board of Regents - to be added
    # Campuses - to be added
    # Labs - to be added
}

# Combined organizations dictionary (for backwards compatibility)
ORGANIZATIONS = {**UCOP_ORGANIZATIONS, **OTHER_ORGANIZATIONS}

# Scraper settings
SCRAPER_SETTINGS = {
    "user_agent": "UCOP-Scraper/1.0 (Educational Research)",
    "delay_between_requests": 2,  # seconds
    "max_retries": 3,
    "timeout": 10,  # seconds
    "respect_robots_txt": True
}

# Flask settings
FLASK_CONFIG = {
    "DEBUG": True,
    "HOST": "0.0.0.0",
    "PORT": 5000,
    "SECRET_KEY": "ucop-scraper-secret-key-change-in-production"
}
