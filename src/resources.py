"""Resource directory data. Every URL is verified by execution/check_links.py before publishing.

county: "richland", "lexington", "fairfield", or "all" (statewide / serves both).
"""

# Ordered checklist for people moving to the area — this order is required by how SC works:
# vehicle tax -> DMV registration -> SC license -> then the 4% application needs both.
NEW_RESIDENT_STEPS = [
    ("Pay the county vehicle property tax",
     "South Carolina collects property tax on cars and trucks, and the DMV won't register your vehicle until it's paid. Contact your county auditor for the bill, then pay the treasurer.",
     [("Richland County Auditor", "https://www.richlandcountysc.gov/Government/Elected-Offices/Auditor"),
      ("Lexington County Auditor", "https://lex-co.sc.gov/departments/auditor")]),
    ("Register your vehicles with the SC DMV",
     "New residents have 45 days to title and register vehicles. Bring the paid tax receipt, your out-of-state title, insurance details and the odometer reading.",
     [("SC DMV", "https://dmv.sc.gov/")]),
    ("Get your SC driver's license",
     "You can drive on your old state's license for up to 90 days. Use your new address, because the next step depends on it.",
     [("SC DMV driver's licenses", "https://dmv.sc.gov/Driver-Services")]),
    ("Apply for the 4% legal residence rate",
     "This is the big one. Your primary home is taxed on 4% of its value instead of 6%, but only after you apply. You'll need your SC license and vehicle registration showing the new address. Apply by the first penalty date on your tax notice.",
     [("Richland County application", "https://www7.richlandcountysc.gov/AssessorApps/LegalResidence"),
      ("Lexington County application", "https://www.lex-co.com/lra-pub/")]),
    ("Register to vote",
     "Update your voter registration to your new address.",
     [("SC Votes", "https://www.scvotes.gov/")]),
]

# Official sites that refuse scripted requests (403 / unreachable from the build machine) but were
# confirmed as live official pages via search results or a browser. The checker skips them.
VERIFIED_MANUALLY = {
    "https://www.richlandcountysc.gov/Government/Elected-Offices/Auditor",
    "https://www.richlandcountysc.gov/Government/Elected-Offices/Treasurer",
    "https://www.richlandcountysc.gov/Property-Business/Mapping-and-Records/Register-of-Deeds",
    "https://www.richlandcountysc.gov/Government/Organization/Departments/Planning-and-Development-Services",
    "https://www.richlandcountysc.gov/Utilities-Services/Trash-and-Recycling",
    "https://www.richlandcountysc.gov/Property-Business/Mapping-and-Records/Geographic-Information-Systems",
    "https://richlandcountysc.gov/government/departments/taxes/assessor",
    "https://richlandcountysc.gov/Residents/Information-for-Residents/Local-Utility-Providers",
    "https://www.richlandcountysc.gov/",
    "https://lex-co.sc.gov/departments/solid-waste-management",
    "https://www.lcjmwsc.com/", "https://www.lex2.org/", "https://lexcolibrary.com/locations",
    "https://www.richlandlibrary.com/", "https://broadbandmap.fcc.gov/",
    "https://lexingtoncountyusa.sc.gov/doing-business/utilities/",
}

RESOURCES = [
    ("Property taxes and records", "Look up a property, pay taxes, or find a deed.", [
        ("Richland County Assessor", "https://richlandcountysc.gov/government/departments/taxes/assessor", "richland", "Property values, the 4% legal residence application and appeals."),
        ("Richland County Auditor", "https://www.richlandcountysc.gov/Government/Elected-Offices/Auditor", "richland", "Tax bills, vehicle taxes and the over-65 homestead exemption."),
        ("Richland County Treasurer", "https://www.richlandcountysc.gov/Government/Elected-Offices/Treasurer", "richland", "Pay real estate and vehicle taxes."),
        ("Richland County Register of Deeds", "https://www.richlandcountysc.gov/Property-Business/Mapping-and-Records/Register-of-Deeds", "richland", "Deeds, mortgages and plats on record."),
        ("Lexington County Assessor", "https://lex-co.sc.gov/departments/assessor", "lexington", "Property values, the 4% legal residence rate and appeals."),
        ("Lexington County Auditor", "https://lex-co.sc.gov/departments/auditor", "lexington", "Tax bills, vehicle taxes and the over-65 homestead exemption."),
        ("Lexington County Treasurer", "https://lex-co.sc.gov/treasurer", "lexington", "Pay real estate and vehicle taxes."),
        ("Lexington County Register of Deeds", "https://lex-co.sc.gov/departments/register-deeds", "lexington", "Deeds, mortgages and plats on record."),
        ("SC Department of Revenue, property tax", "https://dor.sc.gov/property", "all", "How SC property tax works, including assessment ratios and exemptions."),
    ]),
    ("Maps, zoning and flood zones", "Check what's around a property before you buy.", [
        ("Richland County GIS maps", "https://www.richlandcountysc.gov/Property-Business/Mapping-and-Records/Geographic-Information-Systems", "richland", "Parcel lines, zoning, aerial photos and owner of record."),
        ("Lexington County GIS maps", "https://lex-co.sc.gov/planning-gis", "lexington", "Parcel lines, zoning and aerial photos."),
        ("FEMA Flood Map Service Center", "https://msc.fema.gov/portal/home", "all", "Official flood zone maps by address. Check before you buy near water."),
        ("Richland County Community Planning", "https://www.richlandcountysc.gov/Government/Organization/Departments/Planning-and-Development-Services", "richland", "Zoning, permits and planned development in unincorporated Richland County."),
        ("Lexington County Community Development", "https://lex-co.sc.gov/departments/community-development", "lexington", "Zoning, building permits and inspections in unincorporated Lexington County."),
        ("SC 811", "https://sc811.com/", "all", "Free utility line marking before you dig for a fence, deck or garden."),
    ]),
    ("Power and natural gas", "Who provides electricity depends on the address, not the town. Check the listing or ask James.", [
        ("Dominion Energy South Carolina", "https://www.dominionenergy.com/south-carolina", "all", "Electricity and natural gas across much of the Midlands."),
        ("Mid-Carolina Electric Cooperative", "https://www.mcecoop.com/", "all", "Electric co-op serving parts of Lexington, Richland, Newberry and Saluda counties."),
        ("Tri-County Electric Cooperative", "https://www.tcec.coop/", "all", "Electric co-op serving parts of Lexington, Richland and Calhoun counties."),
    ]),
    ("Water, sewer and trash", "Water and sewer providers change from one neighborhood to the next. Many rural homes have a well and septic system instead.", [
        ("Richland County utility providers", "https://richlandcountysc.gov/Residents/Information-for-Residents/Local-Utility-Providers", "richland", "The county's own list of water, sewer, power and gas providers. Start here if you're not sure who serves an address."),
        ("Lexington County utility providers", "https://lexingtoncountyusa.sc.gov/doing-business/utilities/", "lexington", "An overview of the utility providers across Lexington County."),
        ("City of Columbia Water", "https://columbiascwater.net/", "richland", "Water and sewer for Columbia and many surrounding areas."),
        ("Joint Municipal Water and Sewer Commission", "https://www.lcjmwsc.com/", "lexington", "Water and sewer for much of Lexington County."),
        ("Town of Lexington Utilities", "https://www.lexsc.gov/793/Residential-Water-Sewer-Service", "lexington", "Water and sewer for the Town of Lexington area."),
        ("City of West Columbia Utilities", "https://westcolumbiasc.gov/water-sewer/", "lexington", "Water and sewer for West Columbia."),
        ("City of Cayce Utilities", "https://caycesc.gov/water.php", "lexington", "Water and sewer for Cayce."),
        ("Richland County Solid Waste and Recycling", "https://www.richlandcountysc.gov/Utilities-Services/Trash-and-Recycling", "richland", "Curbside pickup in unincorporated Richland County, plus drop-off centers."),
        ("Lexington County Solid Waste", "https://lex-co.sc.gov/departments/solid-waste-management", "lexington", "Drop-off sites and collection details. Many areas use private haulers."),
        ("FCC National Broadband Map", "https://broadbandmap.fcc.gov/", "all", "See which internet providers serve a specific address."),
    ]),
    ("Schools", "School assignment goes by address, and district lines don't follow town names. Use each district's lookup tool.", [
        ("Richland School District One", "https://www.richlandone.org/", "richland", "Most of Columbia and Forest Acres."),
        ("Richland School District Two", "https://www.richland2.org/", "richland", "Northeast Columbia and Blythewood."),
        ("Lexington-Richland School District Five", "https://www.lexrich5.org/", "all", "Irmo, Chapin, Ballentine and the Dutch Fork area."),
        ("Lexington County School District One", "https://www.lexington1.net/", "lexington", "Lexington, Gilbert, Pelion and Red Bank."),
        ("Lexington County School District Two", "https://www.lex2.org/", "lexington", "West Columbia, Cayce, Springdale and Pine Ridge."),
        ("Fairfield County School District", "https://www.fairfield1.org/", "fairfield", "Homes on the Fairfield County side of Blythewood."),
        ("SC School Report Cards", "https://screportcards.com/", "all", "The state's official data on every public school."),
    ]),
    ("Buying help", "Programs and lookups for buyers.", [
        ("SC Housing homebuyer programs", "https://schousing.sc.gov/", "all", "Down payment assistance and mortgage programs for qualifying buyers."),
        ("SC Real Estate Commission", "https://llr.sc.gov/re/", "all", "The state board that licenses agents, with a license lookup for checking any agent."),
        ("HUD-approved housing counselors", "https://www.hud.gov/findacounselor", "all", "Free or low-cost homebuyer counseling."),
        ("Dominion Energy Lake Murray shoreline", "https://www.dominionenergy.com/lakemurray", "all", "Dock and shoreline permit rules for Lake Murray homes."),
    ]),
    ("Towns and cities", "Local government pages for city services, events and council meetings.", [
        ("City of Columbia", "https://columbiasc.gov/", "richland", ""),
        ("City of Forest Acres", "https://www.forestacres.net/", "richland", ""),
        ("Town of Blythewood", "https://www.townofblythewoodsc.gov/", "richland", ""),
        ("Town of Lexington", "https://www.lexsc.gov/", "lexington", ""),
        ("Town of Irmo", "https://www.townofirmosc.com/", "all", ""),
        ("Town of Chapin", "https://www.chapinsc.com/", "lexington", ""),
        ("City of West Columbia", "https://westcolumbiasc.gov/", "lexington", ""),
        ("City of Cayce", "https://caycesc.gov/", "lexington", ""),
        ("Richland County", "https://www.richlandcountysc.gov/", "richland", ""),
        ("Lexington County", "https://lex-co.sc.gov/", "lexington", ""),
    ]),
    ("Libraries, parks and getting out", "The good stuff once you've moved in.", [
        ("Richland Library", "https://www.richlandlibrary.com/", "richland", "Branches across Richland County, plus events and classes."),
        ("Lexington County Public Library", "https://lexcolibrary.com/locations", "lexington", "Branches across Lexington County."),
        ("Irmo Chapin Recreation Commission", "https://www.icrc.net/", "all", "Parks, Saluda Shoals Park and youth sports in the Dutch Fork area."),
        ("Lexington County Recreation and Aging Commission", "https://www.lcrac.com/", "lexington", "Parks, sports leagues and senior programs."),
        ("Richland County Recreation Commission", "https://www.richlandcountyrecreation.com/", "richland", "Parks, centers and programs across Richland County."),
        ("Experience Columbia SC", "https://www.experiencecolumbiasc.com/", "all", "Events, restaurants and things to do across the region."),
        ("Riverbanks Zoo and Garden", "https://www.riverbanks.org/", "all", ""),
        ("Congaree National Park", "https://www.nps.gov/cong/index.htm", "all", ""),
    ]),
]
