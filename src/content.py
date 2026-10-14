"""All site copy and facts live here. Edit this file, then run execution/build_site.py.

Rules followed in this copy (keep them when editing):
- Fair Housing: describe places and housing, never who "should" live there. No
  "family-friendly", "safe", "exclusive", "perfect for young professionals", etc.
  Naming the public school district is factual and fine; ranking schools is not.
- SC advertising (S.C. Code 40-57-135(E)): brokerage name + link on every page.
  Never show another brokerage's listing (photos, address) without written permission.
- No invented reviews, sales counts or market stats. Add real ones when James has them.
"""

AGENT = {
    "name": "James Nowlin",
    "job_title": "Real Estate Agent",
    "phone_display": "(803) 949-0229",
    "phone_e164": "+18039490229",
    "license": "129577",
    "brokerage": "Realty ONE Group Reside",
    "brokerage_url": "https://www.rogreside.com/",
    "office_street": "5300-B Sunset Blvd.",
    "office_city": "Lexington",
    "office_region": "SC",
    "office_zip": "29072",
    "office_phone_display": "(803) 298-0544",
    "office_phone_e164": "+18032980544",
    "facebook": "https://www.facebook.com/JamesNowlinRealtor/",
    "instagram": "https://www.instagram.com/jamesnowlinsc/",
    # His existing Realty ONE Group tools — leads land in his CRM, listings stay IDX-compliant.
    "home_value_url": "https://jamesnowlin.myrealtyonegroup.com/my-home-value",
    "search_url": "https://jamesnowlin.myrealtyonegroup.com/property-search-map/sale/status-active;pending/type-single%20family;condo!townhouse;land;Multi_Family;farm;mobile!manufactured/dsort-n",
    "rog_contact_url": "https://jamesnowlin.myrealtyonegroup.com/contact",
    "app_url": "https://app.realtyonegroup.com/James.Nowlin",
}

SITE_NAME = "James Nowlin Real Estate"
TAGLINE = "Columbia, Lexington and Lake Murray real estate"

# ---------------------------------------------------------------------------
# Areas. `pin` = (lon, lat) for the map. `label_dx/dy` nudge map labels.
# ---------------------------------------------------------------------------
AREAS = [
    {
        "slug": "columbia-sc",
        "name": "Columbia",
        "county": "Richland County",
        "pin": (-81.0348, 34.0007), "label_dx": 12, "label_dy": 30,
        "photo": "columbia-c",
        "photo_alt": "Downtown Columbia, South Carolina skyline in the fall, seen from Arsenal Hill",
        "title": "Columbia, SC Homes & Neighborhoods | James Nowlin, Real Estate Agent",
        "description": "Buying or selling a home in Columbia, SC? A local guide to Columbia's neighborhoods, housing, schools and commutes from real estate agent James Nowlin.",
        "h1": "Buying and selling a home in Columbia, SC",
        "answer": "Columbia is South Carolina's capital and the center of the Midlands, sitting where the Broad and Saluda rivers meet to form the Congaree. Its housing runs from early-1900s bungalows in historic neighborhoods to downtown condos and newer subdivisions on the northeast side, which gives buyers more range of age, style and price than anywhere else in the region.",
        "sections": [
            ("What living in Columbia is like", [
                "The city is anchored by the State House, the University of South Carolina and Fort Jackson, the Army's largest basic training installation. That mix keeps the economy steady and the rental market busy, which matters if you're weighing a house you might keep as an investment later.",
                "Day to day, Columbia life leans outdoors and local: the Saturday Soda City Market on Main Street, the Three Rivers Greenway along the water, Riverbanks Zoo and Garden, and Congaree National Park a short drive southeast.",
            ]),
            ("Neighborhoods and the homes you'll find", [
                "Shandon, Rosewood, Wales Garden, Melrose Heights and Earlewood are known for older brick and craftsman homes on tree-lined streets. Many have been renovated, and an inspection that looks closely at foundations, wiring and HVAC age is time well spent.",
                "Cottontown and Elmwood Park offer historic homes closer to downtown. The Vista and Main Street have condos and lofts. Northeast Columbia, along the I-77 and Two Notch corridors, is where you'll find newer subdivisions with larger floor plans.",
            ]),
            ("Getting around", [
                "I-20, I-26, I-77 and I-126 all touch the city, so most of the Midlands is within a reasonable drive. Columbia Metropolitan Airport is just across the river in West Columbia.",
            ]),
            ("Schools and services", [
                "Most of the city is served by Richland School District One, with parts of northeast Columbia in Richland School District Two. Because district lines don't follow neighborhood names, James checks the assigned schools for each specific address you're considering.",
            ]),
        ],
        "faq": [
            ("Is Columbia, SC in Richland or Lexington County?",
             "Most of Columbia is in Richland County. A few areas west of the rivers sit in Lexington County, which can change the property tax rate and school district, so it's worth confirming the county for each address."),
            ("What are the historic neighborhoods in Columbia, SC?",
             "Shandon, Rosewood, Wales Garden, Melrose Heights, Earlewood, Cottontown and Elmwood Park are among the best known, with homes dating from the early 1900s through the mid-century."),
            ("How far is Columbia from Lake Murray?",
             "The Lake Murray Dam is roughly 12 to 15 miles west of downtown Columbia, usually a 20 to 25 minute drive depending on traffic."),
        ],
        "nearby": ["forest-acres-sc", "west-columbia-cayce-sc", "blythewood-sc"],
    },
    {
        "slug": "lexington-sc",
        "name": "Lexington",
        "county": "Lexington County",
        "pin": (-81.2362, 33.9815), "label_dx": -16, "label_dy": 7, "label_anchor": "end",
        "photo": "lexington-a",
        "photo_alt": "A roadside farmers market stand in Lexington, South Carolina",
        "title": "Lexington, SC Homes for Sale & Area Guide | James Nowlin",
        "description": "Thinking about Lexington, SC? A practical guide to the Town of Lexington's neighborhoods, housing, schools and commute, from Lexington-based agent James Nowlin.",
        "h1": "Buying and selling a home in Lexington, SC",
        "answer": "Lexington is the county seat of Lexington County, about 13 miles west of downtown Columbia and just south of Lake Murray. It's one of the faster-growing parts of the Midlands, with a mix of newer subdivisions, established neighborhoods and a walkable town center. James's office is on Sunset Boulevard in Lexington.",
        "sections": [
            ("What living in Lexington is like", [
                "The town center has kept its small-town feel, with the Icehouse Amphitheater, Main Street shops and restaurants, and a seasonal farmers market. Lake Murray is a few minutes north for boating and the dam walkway.",
                "Growth means new construction is common here. If you're buying new, James can help you compare builder incentives, lot premiums and what's included, and make sure an independent inspection happens before closing.",
            ]),
            ("The homes you'll find", [
                "Expect a lot of homes built from the 1990s onward, from starter homes to larger two-story plans, plus some older homes near the town center and properties with acreage toward Gilbert and Red Bank.",
                "Sunset Boulevard (US-378), Augusta Road and the US-1 corridor carry most of the commercial activity, so a home's position relative to those roads affects both convenience and traffic noise.",
            ]),
            ("Getting around", [
                "I-20 runs along Lexington's southern edge, and US-378 and US-1 lead toward Columbia. Rush-hour traffic on Sunset Boulevard is the main thing to plan around, so James likes to have buyers try their commute from a home before they commit.",
            ]),
            ("Schools and services", [
                "Most of Lexington is served by Lexington County School District One. Lexington Medical Center's main campus is in nearby West Columbia.",
            ]),
        ],
        "faq": [
            ("What school district is Lexington, SC in?",
             "Most of the Town of Lexington and the surrounding area is in Lexington County School District One. Some addresses near the edges fall in other districts, so check the specific address."),
            ("How far is Lexington, SC from Columbia?",
             "Downtown Lexington is about 13 miles west of downtown Columbia, typically 20 to 30 minutes by car depending on the time of day."),
            ("Is there new construction in Lexington, SC?",
             "Yes. Lexington County has seen steady new-home building, and several builders are active around Lexington. A buyer's agent can help you negotiate with the builder's sales team and review the contract."),
        ],
        "nearby": ["lake-murray-sc", "west-columbia-cayce-sc", "irmo-sc"],
    },
    {
        "slug": "irmo-sc",
        "name": "Irmo",
        "county": "Lexington and Richland counties",
        "pin": (-81.1832, 34.0860), "label_dx": 14, "label_dy": -10,
        "photo": "irmo-a",
        "photo_alt": "Flower beds at Irmo Town Park in Irmo, South Carolina",
        "title": "Irmo, SC Homes & Dutch Fork Area Guide | James Nowlin",
        "description": "A guide to buying and selling in Irmo and the Dutch Fork area of SC: neighborhoods, housing, Lexington-Richland 5 schools and commutes, from agent James Nowlin.",
        "h1": "Buying and selling a home in Irmo, SC",
        "answer": "Irmo sits northwest of Columbia between the Saluda River and the east end of Lake Murray, and straddles Lexington and Richland counties. Together with Ballentine and the wider Dutch Fork area, it offers established neighborhoods, easy I-26 access and short trips to both the lake and the city.",
        "sections": [
            ("What living in Irmo is like", [
                "Irmo is best known locally for the Okra Strut festival each fall. Saluda Shoals Park, Harbison State Forest and the shopping around Columbiana Centre are all close by.",
            ]),
            ("The homes you'll find", [
                "Much of the housing dates from the 1970s through the 2000s, in subdivisions with mature trees and established yards. Toward Ballentine and the lake you'll find newer neighborhoods and some lake-access communities.",
                "Because Irmo crosses a county line, two similar homes a mile apart can carry different tax rates. James pulls the county and millage for each home so you can compare real monthly costs.",
            ]),
            ("Getting around", [
                "I-26 runs through the area toward downtown Columbia and northwest toward Chapin. Harbison Boulevard and St. Andrews Road are the main commercial roads.",
            ]),
            ("Schools and services", [
                "Irmo and the Dutch Fork area are served by School District Five of Lexington and Richland Counties, often called Lexington-Richland 5.",
            ]),
        ],
        "faq": [
            ("What county is Irmo, SC in?",
             "Irmo straddles Lexington County and Richland County. Which one a home sits in affects its property tax rate, so it's worth checking for each address."),
            ("What school district serves Irmo, SC?",
             "School District Five of Lexington and Richland Counties (Lexington-Richland 5) serves Irmo, Ballentine, Chapin and the Dutch Fork area."),
            ("What is the Dutch Fork area?",
             "Dutch Fork is the area between the Broad and Saluda rivers northwest of Columbia, including Irmo, Ballentine and the communities around the east end of Lake Murray."),
        ],
        "nearby": ["chapin-sc", "lake-murray-sc", "columbia-sc"],
    },
    {
        "slug": "chapin-sc",
        "name": "Chapin",
        "county": "Lexington, Richland and Newberry counties",
        "pin": (-81.3498, 34.1660), "label_dx": 14, "label_dy": -10,
        "photo": "chapin-a",
        "photo_alt": "Shops at the corner of Lexington Street in downtown Chapin, South Carolina",
        "title": "Chapin, SC Homes & Lake Murray Living | James Nowlin",
        "description": "Buying or selling in Chapin, SC? Neighborhoods, lake-area homes, Lexington-Richland 5 schools and commute tips for the Capital of Lake Murray, from agent James Nowlin.",
        "h1": "Buying and selling a home in Chapin, SC",
        "answer": "Chapin is a small town on the north side of Lake Murray that calls itself the Capital of Lake Murray. It offers a compact town center, newer neighborhoods, lake-access and waterfront homes, and land toward the countryside, about 25 miles northwest of Columbia off I-26.",
        "sections": [
            ("What living in Chapin is like", [
                "The town center is small and local, with an active calendar of community events. Dreher Island State Park and dozens of marinas and boat ramps put the lake within easy reach.",
            ]),
            ("The homes you'll find", [
                "Chapin has a wide range: newer subdivisions off Amicks Ferry, Dutch Fork and Lexington Avenue, waterfront and water-access homes on the lake, and homes on larger lots further out.",
                "The Chapin 29036 zip code reaches into Lexington, Richland and Newberry counties. County affects taxes and services, so James confirms it for every address rather than going by the mailing address.",
            ]),
            ("Getting around", [
                "I-26 is the main route to Irmo and Columbia. Traffic over the Lake Murray crossings and along Dutch Fork Road at rush hour is worth testing before you buy.",
            ]),
            ("Schools and services", [
                "Chapin is served by School District Five of Lexington and Richland Counties (Lexington-Richland 5).",
            ]),
        ],
        "faq": [
            ("Why is Chapin called the Capital of Lake Murray?",
             "Chapin sits on the lake's north shore with a large share of its marinas, boat ramps and waterfront neighborhoods, and the town has used the name for its lake identity for years."),
            ("What county is Chapin, SC in?",
             "The Town of Chapin is in Lexington County, but the 29036 zip code also covers parts of Richland and Newberry counties. Check the county for each address, because it changes the tax rate."),
            ("How far is Chapin from Columbia?",
             "Chapin is about 25 miles northwest of downtown Columbia, usually 30 to 35 minutes via I-26."),
        ],
        "nearby": ["lake-murray-sc", "irmo-sc", "lexington-sc"],
    },
    {
        "slug": "lake-murray-sc",
        "name": "Lake Murray",
        "county": "Lexington, Richland, Saluda and Newberry counties",
        "list_county": "Four counties", "prep": "on",
        "pin": (-81.4000, 34.0890), "label_dx": 0, "label_dy": 6, "label_anchor": "middle", "is_lake": True,
        "photo": "lake-a",
        "photo_alt": "Lake Murray at sunset, seen from the road across the Saluda Dam",
        "title": "Lake Murray, SC Homes: Waterfront Buying Guide | James Nowlin",
        "description": "Thinking about a Lake Murray home? What to know about waterfront vs. water-access homes, docks and shoreline permits, flood zones and lake levels, from agent James Nowlin.",
        "h1": "Buying and selling a home on Lake Murray",
        "answer": "Lake Murray is a reservoir of about 50,000 acres west of Columbia, created when the Saluda Dam was finished in 1930. It has about 650 miles of shoreline across four counties, and its homes range from full-time waterfront houses with private docks to off-water homes in lake-access neighborhoods.",
        "sections": [
            ("Waterfront, water-access and off-water", [
                "Waterfront means the lot touches the shoreline, though the strip right at the water may be owned by the utility rather than the homeowner. Water-access usually means a community dock, ramp or common lot. Off-water homes are in lake-area neighborhoods without either.",
                "Each one prices very differently, so James helps you sort listings by what you actually get at the water, not just the word in the ad.",
            ]),
            ("Docks, permits and the shoreline", [
                "Dominion Energy South Carolina manages the lake and its shoreline. Docks, boat lifts, seawalls and vegetation clearing near the water need its permits. Before you buy, James helps confirm whether an existing dock is permitted and transferable.",
                "Lake levels are managed seasonally, so a dock that floats well in summer may sit shallower in winter. Asking about water depth at the dock year-round avoids surprises.",
            ]),
            ("Insurance and flood zones", [
                "Some lakefront lots fall partly in FEMA flood zones. A flood zone determination and an early insurance quote should be part of every lake purchase, because they can change your monthly cost.",
            ]),
            ("Where on the lake", [
                "The north shore around Chapin and the Dutch Fork has the most marinas and many established neighborhoods. The south shore toward Lexington and Gilbert offers quick access to I-20. The west end toward Prosperity and Saluda is quieter and more rural.",
            ]),
        ],
        "faq": [
            ("Who controls the shoreline on Lake Murray?",
             "Dominion Energy South Carolina manages the lake and its shoreline. Docks, boat lifts and other work at the water need permits from Dominion Energy, so confirm any existing dock is permitted before you buy."),
            ("How big is Lake Murray?",
             "Lake Murray covers about 50,000 acres with about 650 miles of shoreline across Lexington, Richland, Saluda and Newberry counties."),
            ("What is the difference between waterfront and water-access on Lake Murray?",
             "A waterfront lot borders the shoreline, often with a private dock. A water-access home has shared access, such as a community dock, ramp or common lot. Waterfront usually costs considerably more."),
        ],
        "nearby": ["chapin-sc", "lexington-sc", "irmo-sc"],
    },
    {
        "slug": "west-columbia-cayce-sc",
        "name": "West Columbia & Cayce",
        "map_label": "West Columbia",
        "county": "Lexington County",
        "pin": (-81.0740, 33.9935), "label_dx": -12, "label_dy": -16, "label_anchor": "end",
        "photo": "wcola-a",
        "photo_alt": "The Gervais Street Bridge over the Congaree River, seen from the West Columbia side",
        "title": "West Columbia & Cayce, SC Homes & Area Guide | James Nowlin",
        "description": "A guide to buying and selling in West Columbia and Cayce, SC: riverfront neighborhoods, housing, Lexington Two schools and quick commutes to downtown Columbia.",
        "h1": "Buying and selling a home in West Columbia and Cayce",
        "answer": "West Columbia and Cayce sit right across the Congaree River from downtown Columbia in Lexington County. They offer some of the shortest commutes into the city, older homes with character, the Riverwalk along the water, and easy access to the airport and Lexington Medical Center.",
        "sections": [
            ("What living here is like", [
                "The Riverwalk, part of the Three Rivers Greenway, follows the Congaree on this side of the river. West Columbia's State Street and Meeting Street areas have restaurants and breweries, and Cayce has its own riverfront parks and historic district.",
            ]),
            ("The homes you'll find", [
                "Mill-era cottages, mid-century brick ranches and some newer infill and townhome construction. Older homes can carry great value; plan on a careful inspection and budget for updates.",
                "Springdale and Pine Ridge, just west, offer larger lots and established neighborhoods.",
            ]),
            ("Getting around", [
                "Downtown Columbia is a few minutes across the Gervais Street or Blossom Street bridges. I-26, I-77 and I-126 are all close. Columbia Metropolitan Airport is in West Columbia.",
            ]),
            ("Schools and services", [
                "Most of West Columbia, Cayce, Springdale and Pine Ridge are served by Lexington County School District Two. Lexington Medical Center's main campus is in West Columbia.",
            ]),
        ],
        "faq": [
            ("Is West Columbia part of Columbia, SC?",
             "No. West Columbia is its own city in Lexington County, across the Congaree River from Columbia, which is mostly in Richland County. The two have different city services and tax rates."),
            ("What school district serves West Columbia and Cayce?",
             "Lexington County School District Two serves most of West Columbia, Cayce, Springdale and Pine Ridge."),
            ("How far is West Columbia from downtown Columbia?",
             "Only a couple of miles. Many West Columbia and Cayce neighborhoods are under 10 minutes from the State House."),
        ],
        "nearby": ["columbia-sc", "lexington-sc", "forest-acres-sc"],
    },
    {
        "slug": "blythewood-sc",
        "name": "Blythewood",
        "county": "Richland and Fairfield counties",
        "pin": (-80.9740, 34.2146), "label_dx": -14, "label_dy": 6, "label_anchor": "end",
        "photo": "blythewood-a",
        "photo_alt": "A garden lawn in Old Blythewood, South Carolina",
        "title": "Blythewood, SC Homes & Area Guide | James Nowlin",
        "description": "Buying or selling in Blythewood, SC? Neighborhoods, newer homes and larger lots, Richland Two schools and I-77 commute tips, from Columbia-area agent James Nowlin.",
        "h1": "Buying and selling a home in Blythewood, SC",
        "answer": "Blythewood is a growing town north of Columbia along I-77, mostly in Richland County with parts in Fairfield County. It offers newer subdivisions, homes on larger lots, and quick interstate access to Columbia and Charlotte.",
        "sections": [
            ("What living in Blythewood is like", [
                "Blythewood keeps a small-town center around Doko Meadows Park, which hosts the town's festivals and concerts. Growth in the area has picked up with new employers along the I-77 corridor, including the Scout Motors plant.",
            ]),
            ("The homes you'll find", [
                "Much of the housing is newer construction in planned neighborhoods, alongside older homes and properties with acreage on the rural edges of town.",
                "When an area is growing quickly, knowing what's planned nearby matters. James can help you check zoning and planned development around a home before you commit.",
            ]),
            ("Getting around", [
                "I-77 is the main route south to Columbia and north toward Charlotte. US-21 and Blythewood Road connect the town center to the interstate.",
            ]),
            ("Schools and services", [
                "Most of Blythewood is served by Richland School District Two; homes on the Fairfield County side are in Fairfield County schools.",
            ]),
        ],
        "faq": [
            ("What county is Blythewood, SC in?",
             "Blythewood is mostly in Richland County, with parts in Fairfield County. The county changes property taxes and the school district, so confirm it for each address."),
            ("What school district serves Blythewood?",
             "Most of Blythewood is in Richland School District Two."),
            ("How far is Blythewood from Columbia?",
             "Blythewood is about 20 miles north of downtown Columbia, usually 25 to 30 minutes via I-77."),
        ],
        "nearby": ["columbia-sc", "forest-acres-sc", "irmo-sc"],
    },
    {
        "slug": "forest-acres-sc",
        "name": "Forest Acres",
        "county": "Richland County",
        "pin": (-80.9898, 34.0193), "label_dx": 0, "label_dy": -18, "label_anchor": "middle",
        "photo": "forest-a",
        "photo_alt": "Street in Forest Acres, South Carolina",
        "title": "Forest Acres, SC Homes & Area Guide | James Nowlin",
        "description": "A guide to buying and selling in Forest Acres, SC: mid-century homes on wooded lots, Richland One schools and quick trips to downtown Columbia, from agent James Nowlin.",
        "h1": "Buying and selling a home in Forest Acres, SC",
        "answer": "Forest Acres is a small, independent city surrounded by Columbia, a few miles east of downtown. It's known for mid-century homes on large, wooded lots, the Forest Lake area, and convenient shopping at Trenholm Plaza, all within a short drive of the city center.",
        "sections": [
            ("What living in Forest Acres is like", [
                "Streets are quiet and heavily treed, with Trenholm Plaza and the Forest Drive corridor close by for shopping and dining. Fort Jackson is just to the east.",
            ]),
            ("The homes you'll find", [
                "Brick ranches and split-levels from the 1950s through the 1970s make up much of the housing, often on generous lots. Many have been updated, and some buyers renovate or rebuild.",
                "With older homes and big trees, a good inspection should look at the roof, drainage, sewer line and the trees themselves.",
            ]),
            ("Getting around", [
                "Forest Drive and Trenholm Road connect directly to downtown Columbia, and I-77 is a short drive east.",
            ]),
            ("Schools and services", [
                "Forest Acres is served by Richland School District One. The city has its own police department and city services.",
            ]),
        ],
        "faq": [
            ("Is Forest Acres part of Columbia, SC?",
             "No. Forest Acres is its own incorporated city, surrounded by Columbia, with its own city government and services. Many addresses still use a Columbia mailing address."),
            ("What kind of homes are in Forest Acres?",
             "Mostly mid-century brick ranches and split-levels on large, wooded lots, with some newer and rebuilt homes."),
            ("What school district serves Forest Acres?",
             "Forest Acres is served by Richland School District One."),
        ],
        "nearby": ["columbia-sc", "blythewood-sc", "west-columbia-cayce-sc"],
    },
]

# ---------------------------------------------------------------------------
# Main FAQ. Each answer opens with a direct one-sentence answer (good for
# search snippets and AI answers), then gives detail.
# ---------------------------------------------------------------------------
FAQ = [
    ("Buying in South Carolina", [
        ("Do I need an attorney to buy a house in South Carolina?",
         "Yes. South Carolina requires a licensed attorney to conduct real estate closings. The attorney handles the title search, prepares the closing documents and disburses funds. As the buyer, you usually choose the closing attorney, and James can recommend a few to compare."),
        ("What is a due diligence period in South Carolina?",
         "It's a set number of days after your offer is accepted when you can inspect the home, check the survey, insurance and neighborhood, and walk away for any reason. Many SC contracts also include a non-refundable due diligence fee paid to the seller. The length and fee are negotiable, and James helps you set both to fit the home and the market."),
        ("Do I have to sign an agreement with a buyer's agent?",
         "Yes, in most cases. Since August 2024, agents who use the MLS need a written agreement with a buyer before touring homes together. The agreement spells out what the agent does and how they're paid, and the compensation is negotiable. James walks through it with you before your first showing."),
        ("How much do I need for a down payment?",
         "It depends on the loan. VA and USDA loans can require no down payment, FHA loans start at 3.5%, and some conventional loans start at 3%. You'll also need money for the due diligence fee, earnest money, inspections and closing costs. Down payment assistance is available through SC Housing for qualifying buyers. A lender can give you exact numbers, and James can recommend a few."),
        ("How long does it take to close on a house in SC?",
         "About 30 to 45 days with financing is typical, and two to three weeks is common for cash. The timeline depends on the lender, the appraisal and the due diligence period you negotiate."),
    ]),
    ("Taxes and costs", [
        ("How do property taxes work in Lexington and Richland counties?",
         "Your primary home is taxed on 4% of its assessed value, while second homes and rentals are taxed on 6%, so the primary residence rate saves a lot. The 4% rate isn't automatic: you have to apply with the county assessor, ideally right after you close. The tax rate (millage) also varies by county, school district and city, which is why two similar homes can have different tax bills."),
        ("Is there a property tax break for seniors in South Carolina?",
         "Yes. Homeowners who are 65 or older, totally disabled or legally blind can qualify for the homestead exemption, which removes the first $50,000 of the home's value from property taxes. You apply through the county auditor."),
        ("How much does it cost to sell a house in South Carolina?",
         "Sellers typically pay the real estate commission (which is negotiable), the deed recording fee of $3.70 per $1,000 of sale price, their share of the attorney's fees, any loan payoff and prorated property taxes. James gives you a written estimate of your net proceeds before you list."),
    ]),
    ("Selling your home", [
        ("Do sellers have to disclose problems in South Carolina?",
         "Yes. Most sellers must complete the South Carolina Residential Property Condition Disclosure Statement, which covers known issues with the roof, structure, systems and more. Some sales, like certain estate and foreclosure sales, are exempt. Being upfront protects you and helps the deal hold together."),
        ("What is my home worth?",
         "The best answer is a comparative market analysis based on recent nearby sales. You can get an instant estimate from James's home value tool, then ask James for a detailed review that accounts for your home's condition and updates."),
        ("When is the best time to sell a home in the Columbia area?",
         "Spring usually brings the most buyers in the Midlands, but a well-priced, well-prepared home sells in any season. Fewer competing listings in the fall and winter can work in your favor."),
    ]),
    ("Working with James", [
        ("What areas does James Nowlin serve?",
         "James works across the Columbia, SC metro area: Columbia, Lexington, Irmo, Chapin, Lake Murray, West Columbia and Cayce, Blythewood and Forest Acres, plus the surrounding Midlands."),
        ("How does James's mortgage background help buyers and sellers?",
         "James worked in mortgage finance before real estate, so he knows how lenders look at income, credit, appraisals and closing timelines. That helps buyers make offers their loans can actually close on, and helps sellers judge which offers are strongest."),
        ("Can I search every home for sale in the area?",
         "Yes. James's home search shows MLS listings across the Midlands with daily updates, and his ONE app lets you save homes and message him directly."),
        ("How do I contact James Nowlin?",
         "Call or text James at (803) 949-0229. His office is at Realty ONE Group Reside, 5300-B Sunset Blvd., Lexington, SC 29072."),
    ]),
]
