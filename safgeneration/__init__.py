DEFAULT_RIGHTS = "University of Chicago dissertations are covered by copyright." +\
                 " They may be viewed from this source for any purpose," +\
                 "but reproduction or distribution in any format is " +\
                 "prohibited without written permission."


SINGLE_XPATH = [
    ("author", "DISS_authorship/DISS_author[@type='primary']/DISS_name"),
    ("department", "DISS_description/DISS_institution/DISS_inst_contact"),
    ("copyrightdate", "DISS_description/DISS_dates/DISS_accept_date"),
    ("issuedate", "DISS_description/DISS_dates/DISS_accept_date"),
    ("degree", "DISS_description/DISS_degree"),
    ("mimetype", "DISS_content/DISS_binary"),
    ("extent", "DISS_description"),
    ("language", "DISS_description/DISS_categorization/DISS_language"),
    ("license", "DISS_creative_commons_license/DISS_abbreviation"),
    ("title", "DISS_description/DISS_title"),
    ("type", "DISS_description")
]

MULTIPLE_XPATH = [
    ("subject", "DISS_description/DISS_categorization/DISS_keyword"),
    ("advisor", "DISS_description/DISS_advisor/DISS_name"),
]

HARDCODED_VALUES = [
    ("publisher", "University of Chicago"),
    ("rightsurl", "http://doi.org/10.6082/M1CC0XM8")
]

MAPPER = {
    "advisor": {"element":"contributor", "qualifier":"advisor"},
    "author": {"element":"contributor", "qualifier":"author"},
    "department": {"element": "contributor", "qualifier":"department"},
    "copyrightdate": {"element": "date", "qualifier": "copyright"},
    "issuedate": {"element": "date", "qualifier": "issued"},
    "abstract": {"element": "description", "qualifier": "none"},
    "degree": {"element": "description", "qualifier": "degree"},
    "mimetype": {"element": "format", "qualifier": "mimetype"},
    "extent": {"element": "format", "qualifier": "extent"},
    "language": {"element": "language", "qualifier": "iso"},
    "publisher": {"element": "publisher", "qualifier": "none"},
    "license": {"element": "rights", "qualifier": "none",
                "defaultValue": DEFAULT_RIGHTS},
    "rightsurl": {"element": "rights", "qualifier": "uri"},
    "subject": {"element": "subject", "qualifier": "none"},
    "title": {"element": "title", "qualifier": "none"},
    "type": {"element": "type", "qualifier": "none"}
}

