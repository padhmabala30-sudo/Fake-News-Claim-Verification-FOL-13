import re

class ClaimProcessor:
    def __init__(self):
        # ========== PERSON KEYWORDS ==========
        self.person_keywords = {
            "modi": "NarendraModi", "narendra modi": "NarendraModi", "pm modi": "NarendraModi",
            "biden": "JoeBiden", "joe biden": "JoeBiden", "president biden": "JoeBiden",
            "trump": "DonaldTrump", "donald trump": "DonaldTrump",
            "macron": "EmmanuelMacron", "emmanuel macron": "EmmanuelMacron",
            "putin": "VladimirPutin", "vladimir putin": "VladimirPutin",
            "xi jinping": "XiJinping", "xi": "XiJinping", "president xi": "XiJinping",
            "gandhi": "MahatmaGandhi", "mahatma gandhi": "MahatmaGandhi",
            "kalam": "DrAPJAbdulKalam", "abdul kalam": "DrAPJAbdulKalam", "apj abdul kalam": "DrAPJAbdulKalam",
            "nehru": "JawaharlalNehru", "jawaharlal nehru": "JawaharlalNehru",
            "indira gandhi": "IndiraGandhi",
            "elon musk": "ElonMusk", "musk": "ElonMusk",
            "sundar pichai": "SundarPichai", "pichai": "SundarPichai",
            "satya nadella": "SatyaNadella", "nadella": "SatyaNadella",
            "tim cook": "TimCook",
            "einstein": "AlbertEinstein", "albert einstein": "AlbertEinstein",
            "newton": "IsaacNewton", "isaac newton": "IsaacNewton",
            "darwin": "CharlesDarwin", "charles darwin": "CharlesDarwin",
            "cv raman": "CVraman", "c.v. raman": "CVraman", "raman": "CVraman",
            "marie curie": "MarieCurie", "alexander fleming": "AlexanderFleming",
            "galileo": "GalileoGalilei", "copernicus": "NicolausCopernicus",
            "mendeleev": "DmitriMendeleev", "edison": "ThomasEdison",
            "wright brothers": "WrightBrothers",
            "rishi sunak": "RishiSunak", "keir starmer": "KeirStarmer",
            "justin trudeau": "JustinTrudeau", "trudeau": "JustinTrudeau",
            "anthony albanese": "AnthonyAlbanese",
            "olaf scholz": "OlafScholz", "giorgia meloni": "GiorgiaMeloni",
        }

        # ========== PLACE / COUNTRY KEYWORDS ==========
        self.place_keywords = {
            "chennai": "Chennai", "madras": "Chennai",
            "mumbai": "Mumbai", "bombay": "Mumbai",
            "delhi": "Delhi", "new delhi": "Delhi",
            "kolkata": "Kolkata", "calcutta": "Kolkata",
            "bengaluru": "Bengaluru", "bangalore": "Bengaluru",
            "hyderabad": "Hyderabad", "ahmedabad": "Ahmedabad",
            "jaipur": "Jaipur", "lucknow": "Lucknow", "pune": "Pune",
            "paris": "Paris", "tokyo": "Tokyo", "london": "London",
            "beijing": "Beijing", "moscow": "Moscow",
            "washington": "WashingtonDC", "washington dc": "WashingtonDC", "washington d.c.": "WashingtonDC",
            "islamabad": "Islamabad", "dhaka": "Dhaka", "kathmandu": "Kathmandu",
            "berlin": "Berlin", "rome": "Rome", "madrid": "Madrid",
            "seoul": "Seoul", "cairo": "Cairo", "canberra": "Canberra",
            "ottawa": "Ottawa", "brasilia": "Brasilia", "bangkok": "Bangkok",
            "jakarta": "Jakarta", "hanoi": "Hanoi", "manila": "Manila",
            "riyadh": "Riyadh", "abu dhabi": "AbuDhabi", "doha": "Doha",
            "tehran": "Tehran", "ankara": "Ankara", "athens": "Athens",
            "amsterdam": "Amsterdam", "brussels": "Brussels", "vienna": "Vienna",
            "stockholm": "Stockholm", "oslo": "Oslo", "copenhagen": "Copenhagen",
            "helsinki": "Helsinki", "warsaw": "Warsaw", "prague": "Prague",
            "lisbon": "Lisbon", "dublin": "Dublin", "nairobi": "Nairobi",
            "wuhan": "Wuhan", "shanghai": "Shanghai", "dubai": "Dubai",
            "sydney": "Sydney", "melbourne": "Melbourne", "toronto": "Toronto",
            "new york": "NewYork", "los angeles": "LosAngeles",
            "qatar": "Qatar", "rio": "Rio", "rio de janeiro": "Rio",
            "moon": "Moon", "lunar surface": "Moon",
            "india": "India", "bharat": "India",
            "usa": "USA", "america": "USA", "united states": "USA", "u.s.": "USA", "u.s.a.": "USA",
            "uk": "UK", "britain": "UK", "united kingdom": "UK", "england": "UK",
            "france": "France", "japan": "Japan", "china": "China",
            "russia": "Russia", "australia": "Australia", "germany": "Germany",
            "pakistan": "Pakistan", "bangladesh": "Bangladesh", "nepal": "Nepal",
            "sri lanka": "SriLanka", "bhutan": "Bhutan", "maldives": "Maldives",
            "thailand": "Thailand", "indonesia": "Indonesia", "malaysia": "Malaysia",
            "singapore": "Singapore", "vietnam": "Vietnam", "philippines": "Philippines",
            "saudi arabia": "SaudiArabia", "uae": "UAE", "united arab emirates": "UAE",
            "iran": "Iran", "turkey": "Turkey", "greece": "Greece",
            "netherlands": "Netherlands", "holland": "Netherlands",
            "belgium": "Belgium", "switzerland": "Switzerland", "sweden": "Sweden",
            "norway": "Norway", "denmark": "Denmark", "finland": "Finland",
            "poland": "Poland", "portugal": "Portugal", "ireland": "Ireland",
            "italy": "Italy", "spain": "Spain", "brazil": "Brazil",
            "argentina": "Argentina", "chile": "Chile", "peru": "Peru",
            "mexico": "Mexico", "cuba": "Cuba", "south africa": "SouthAfrica",
            "kenya": "Kenya", "ethiopia": "Ethiopia", "nigeria": "Nigeria",
            "south korea": "SouthKorea", "korea": "SouthKorea",
            "canada": "Canada", "new zealand": "NewZealand",
            "europe": "Europe", "asia": "Asia", "africa": "Africa",
        }

        # ========== EVENT KEYWORDS ==========
        self.event_keywords = {
            "olympics 2024": "Olympics2024", "2024 olympics": "Olympics2024", "paris olympics": "Olympics2024",
            "olympics 2020": "Olympics2020", "2020 olympics": "Olympics2020", "tokyo olympics": "Olympics2020",
            "olympics 2016": "Olympics2016", "2016 olympics": "Olympics2016", "rio olympics": "Olympics2016",
            "olympics 2012": "Olympics2012", "2012 olympics": "Olympics2012", "london olympics": "Olympics2012",
            "olympics 2008": "Olympics2008", "2008 olympics": "Olympics2008", "beijing olympics": "Olympics2008",
            "world cup 2022": "WorldCup2022", "fifa 2022": "WorldCup2022", "qatar world cup": "WorldCup2022",
            "world cup 2018": "WorldCup2018", "fifa 2018": "WorldCup2018", "russia world cup": "WorldCup2018",
            "world cup 2014": "WorldCup2014", "brazil world cup": "WorldCup2014",
            "chandrayaan 3": "Chandrayaan3Landing", "chandrayaan-3": "Chandrayaan3Landing",
            "chandrayaan3": "Chandrayaan3Landing", "chandrayaan-3 landing": "Chandrayaan3Landing",
            "g20 2023": "G20Summit2023", "g20 summit 2023": "G20Summit2023", "g20 delhi": "G20Summit2023",
            "g20 2024": "G20Summit2024",
            "covid": "COVID19Outbreak", "covid-19": "COVID19Outbreak", "covid19": "COVID19Outbreak",
            "coronavirus": "COVID19Outbreak", "corona virus": "COVID19Outbreak",
            "berlin wall": "FallOfBerlinWall", "fall of berlin wall": "FallOfBerlinWall",
            "moon landing": "FirstMoonLanding", "apollo 11": "FirstMoonLanding", "first moon landing": "FirstMoonLanding",
            "independence of india": "IndependenceIndia", "indian independence": "IndependenceIndia",
            "independence of usa": "IndependenceUSA", "american independence": "IndependenceUSA",
            "partition of india": "PartitionOfIndia",
            "french revolution": "FrenchRevolution", "american revolution": "AmericanRevolution",
            "russian revolution": "RussianRevolution",
            "hiroshima": "HiroshimaBombing", "september 11": "September11Attacks", "9/11": "September11Attacks",
            "cricket world cup 2023": "CricketWorldCup2023", "t20 world cup 2024": "T20WorldCup2024",
        }

        # ========== DISCOVERY KEYWORDS ==========
        self.discovery_keywords = {
            "gravity": "Gravity", "law of gravity": "Gravity", "universal gravitation": "Gravity",
            "relativity": "Relativity", "theory of relativity": "Relativity", "general relativity": "Relativity",
            "special relativity": "Relativity",
            "penicillin": "Penicillin",
            "radioactivity": "Radioactivity", "radiation": "Radioactivity",
            "evolution": "Evolution", "theory of evolution": "Evolution",
            "raman effect": "RamanEffect", "raman scattering": "RamanEffect",
            "periodic table": "PeriodicTable",
            "electron": "Electron", "proton": "Proton",
            "dna": "DNAStructure", "dna structure": "DNAStructure",
            "heliocentric": "HeliocentricTheory", "heliocentric theory": "HeliocentricTheory",
            "telescope": "Telescope", "electric bulb": "ElectricBulb", "light bulb": "ElectricBulb",
            "telephone": "Telephone", "radio": "Radio", "airplane": "Airplane", "aeroplane": "Airplane",
        }

        # ========== AGENCY KEYWORDS ==========
        
        # ========== LANDMARK KEYWORDS ==========
        self.landmark_keywords = {
            "taj mahal": "TajMahal", "eiffel tower": "EiffelTower",
            "statue of liberty": "StatueOfLiberty", "great wall": "GreatWall",
            "colosseum": "Colosseum", "sydney opera house": "SydneyOperaHouse",
            "christ the redeemer": "ChristTheRedeemer", "pyramids": "PyramidsOfGiza",
            "big ben": "BigBen", "mount fuji": "MountFuji", "burj khalifa": "BurjKhalifa",
            "red fort": "RedFort", "qutub minar": "QutubMinar", "gateway of india": "GatewayOfIndia",
            "charminar": "Charminar", "india gate": "IndiaGate", "lotus temple": "LotusTemple",
        }

        self.agency_keywords = {
            "isro": "ISRO", "indian space research": "ISRO",
            "nasa": "NASA",
            "esa": "ESA", "european space agency": "ESA",
            "cnsa": "CNSA", "chinese space": "CNSA",
            "roscosmos": "Roscosmos", "jaxa": "JAXA",
        }

        # ========== ROLE / RELATION PATTERNS ==========
        self.predicate_patterns = [
            (r"(occurred|happened|held|took place|organised|organized|hosted|conducted|staged|took place).*(in|at|on)", "EventOccurred"),
            (r"(was held in|was hosted by|was organised in|was organized in|took place in)", "EventOccurred"),
            (r"(is the capital|capital of|capital city of|serves as the capital)", "IsCapitalOf"),
            (r"(is capital of|are the capital)", "IsCapitalOf"),
            (r"(is the prime minister|prime minister of|pm of|serves as prime minister)", "PersonIs"),
            (r"(is the chief minister|chief minister of|cm of)", "PersonIs"),
            (r"(is the president|president of|serves as president)", "PersonIs"),
            (r"(is the ceo|ceo of|chief executive of)", "PersonIs"),
            (r"(is the chancellor|chancellor of)", "PersonIs"),
            (r"(is the minister|minister of)", "PersonIs"),
            (r"(space agency of|is the space agency|space research organisation of|space research organization of)", "SpaceAgencyOf"),
            (r"(discovered by|was discovered by|invented by|was invented by|proposed by|developed by)", "DiscoveredBy"),
            (r"(currency of|currency is|official currency of|monetary unit of)", "CurrencyOf"),
            (r"(national animal of|national animal is|official animal of)", "NationalAnimalOf"),
            (r"(official language of|language of|national language of)", "OfficialLanguageOf"),
            (r"(located in|is in|situated in|is situated in|lies in|is based in)", "LocatedIn"),
            (r"(belongs to continent|is in continent|continent of)", "CountryInContinent"),
            (r"(national sport of|national sport is)", "NationalSportOf"),
            (r"(is located in|is in|stands in|situated in).*(city|)", "LandmarkLocatedIn"),
            (r"(capital of|state capital of|is the capital of).*(state|nadu|pradesh|bengal|gujarat|rajasthan)", "StateCapitalOf"),
            (r"(university|iit|iisc|aiims).*(located|in|at)", "UniversityLocatedIn"),
            (r"(headquarters of|hq of|based in).*(company|google|microsoft|apple|infosys|tcs)", "CompanyHeadquartersIn"),
            (r"(holds the record|record for|world record)", "HoldsRecord"),
            (r"(member of|belongs to).*(g20|g7|brics)", "MemberOf"),
        ]

    def _find_keywords(self, text, keyword_dict):
        found = []
        # Longer keys first to avoid partial matches
        for key in sorted(keyword_dict.keys(), key=len, reverse=True):
            if key in text:
                found.append(keyword_dict[key])
                # remove matched part to reduce double matching
                text = text.replace(key, " ")
        return list(dict.fromkeys(found))

    def extract_entities_and_predicates(self, claim: str):
        claim_lower = claim.lower().strip()
        # normalize some punctuation
        claim_lower = re.sub(r"[“”\"']", "", claim_lower)
        claim_lower = re.sub(r"\s+", " ", claim_lower)

        entities = []
        entities += self._find_keywords(claim_lower, self.person_keywords)
        entities += self._find_keywords(claim_lower, self.place_keywords)
        entities += self._find_keywords(claim_lower, self.event_keywords)
        entities += self._find_keywords(claim_lower, self.discovery_keywords)
        entities += self._find_keywords(claim_lower, self.agency_keywords)
        if hasattr(self, 'landmark_keywords'):
            entities += self._find_keywords(claim_lower, self.landmark_keywords)

        predicates = []
        for pattern, pred in self.predicate_patterns:
            if re.search(pattern, claim_lower):
                predicates.append(pred)
        predicates = list(dict.fromkeys(predicates))

        return {
            "original_claim": claim,
            "entities": list(dict.fromkeys(entities)),
            "suggested_predicates": predicates,
            "claim_lower": claim_lower
        }

    def try_map_to_fol(self, claim_info, kb):
        """
        Smarter free-form mapping to FOL predicate + arguments.
        Handles many natural language variations.
        """
        entities = claim_info["entities"]
        predicates = claim_info["suggested_predicates"]
        claim_lower = claim_info["claim_lower"]

        if not entities and not predicates:
            return None, None

        # ---------- StateCapitalOf ----------
        if "StateCapitalOf" in predicates or ("capital" in claim_lower and any(s in claim_lower for s in ["tamil nadu", "maharashtra", "karnataka", "kerala", "gujarat", "rajasthan", "uttar pradesh", "west bengal", "bihar", "punjab"])):
            state_map = {
                "tamil nadu": "TamilNadu", "maharashtra": "Maharashtra", "karnataka": "Karnataka",
                "kerala": "Kerala", "gujarat": "Gujarat", "rajasthan": "Rajasthan",
                "uttar pradesh": "UttarPradesh", "west bengal": "WestBengal", "bihar": "Bihar",
                "punjab": "Punjab", "telangana": "Telangana", "andhra": "AndhraPradesh",
            }
            state = next((state_map[k] for k in state_map if k in claim_lower), None)
            city = next((e for e in entities if e in ["Chennai", "Mumbai", "Bengaluru", "Thiruvananthapuram", "Gandhinagar", "Jaipur", "Lucknow", "Kolkata", "Patna", "Chandigarh", "Hyderabad", "Amaravati"]), None)
            if state and city:
                return "StateCapitalOf", (state, city)
            if state:
                known = {f[0]: f[1] for f in kb.get_facts("StateCapitalOf")}
                claimed = next((e for e in entities if e != state), None)
                if claimed:
                    return "StateCapitalOf", (state, claimed)
                return "StateCapitalOf", (state, known.get(state, "Unknown"))

        # ---------- UniversityLocatedIn ----------
        if "UniversityLocatedIn" in predicates or any(u in claim_lower for u in ["iit", "iisc", "aiims", "harvard", "mit", "stanford", "oxford", "cambridge"]):
            uni_map = {
                "iit madras": "IITMadras", "iit bombay": "IITBombay", "iit delhi": "IITDelhi",
                "iit kanpur": "IITKanpur", "iisc": "IISC", "aiims": "AIIMSDelhi",
                "harvard": "Harvard", "mit": "MIT", "stanford": "Stanford",
                "oxford": "Oxford", "cambridge": "Cambridge",
            }
            uni = next((uni_map[k] for k in uni_map if k in claim_lower), None)
            place = next((e for e in entities if e not in (uni,)), None)
            if uni and place:
                return "UniversityLocatedIn", (uni, place)
            if uni:
                known = {f[0]: f[1] for f in kb.get_facts("UniversityLocatedIn")}
                return "UniversityLocatedIn", (uni, known.get(uni, "Unknown"))

        # ---------- CompanyHeadquartersIn ----------
        if "CompanyHeadquartersIn" in predicates or any(c in claim_lower for c in ["google", "microsoft", "apple", "amazon", "infosys", "tcs", "tesla", "meta"]):
            company_map = {
                "google": "Google", "microsoft": "Microsoft", "apple": "Apple",
                "amazon": "Amazon", "meta": "Meta", "facebook": "Meta",
                "tesla": "Tesla", "infosys": "Infosys", "tcs": "TCS",
                "wipro": "Wipro", "nvidia": "Nvidia", "samsung": "Samsung",
            }
            company = next((company_map[k] for k in company_map if k in claim_lower), None)
            country = next((e for e in entities if e in ["USA", "India", "China", "SouthKorea", "Japan"]), None)
            if company and country:
                return "CompanyHeadquartersIn", (company, country)
            if company:
                known = {f[0]: f[1] for f in kb.get_facts("CompanyHeadquartersIn")}
                claimed = next((e for e in entities if e != company), None)
                if claimed:
                    return "CompanyHeadquartersIn", (company, claimed)
                return "CompanyHeadquartersIn", (company, known.get(company, "Unknown"))

        # ---------- HoldsRecord ----------
        if "HoldsRecord" in predicates or "record" in claim_lower:
            person = next((e for e in entities if e in [f[0] for f in kb.get_facts("HoldsRecord")]), None)
            if person:
                known = {f[0]: f[1] for f in kb.get_facts("HoldsRecord")}
                return "HoldsRecord", (person, known.get(person, "Unknown"))


        # ---------- LandmarkLocatedIn ----------
        if "LandmarkLocatedIn" in predicates or any(lm in claim_lower for lm in ["taj mahal", "eiffel tower", "statue of liberty", "burj khalifa", "red fort", "india gate", "golden temple"]):
            lm_map = {
                "taj mahal": "TajMahal", "eiffel tower": "EiffelTower",
                "statue of liberty": "StatueOfLiberty", "burj khalifa": "BurjKhalifa",
                "red fort": "RedFort", "india gate": "IndiaGate",
                "golden temple": "GoldenTemple", "statue of unity": "StatueOfUnity",
                "gateway of india": "GatewayOfIndia", "qutub minar": "QutubMinar",
            }
            landmark = next((lm_map[k] for k in lm_map if k in claim_lower), None)
            place = next((e for e in entities if e in ["Agra", "Paris", "NewYork", "Dubai", "Delhi", "Amritsar", "Gujarat", "Mumbai", "China", "Rome"]), None)
            if landmark and place:
                return "LandmarkLocatedIn", (landmark, place)
            if landmark:
                known = {f[0]: f[1] for f in kb.get_facts("LandmarkLocatedIn")}
                claimed = next((e for e in entities if e != landmark), None)
                if claimed:
                    return "LandmarkLocatedIn", (landmark, claimed)
                return "LandmarkLocatedIn", (landmark, known.get(landmark, "Unknown"))

        # ---------- 1. EventOccurred ----------
        event_entities = [e for e in entities if e.startswith((
            "Olympics", "WorldCup", "Chandrayaan", "COVID", "G20", "FallOf",
            "FirstMoon", "Independence", "Partition", "French", "American",
            "Russian", "Hiroshima", "September", "Cricket", "T20", "IPL"
        ))]
        place_entities = [e for e in entities if e not in event_entities]

        if event_entities or "EventOccurred" in predicates:
            event = event_entities[0] if event_entities else None
            place = None

            # Prefer known places from EventOccurred facts
            known_event_places = set()
            for f in kb.get_facts("EventOccurred"):
                known_event_places.add(f[1])
            for p in place_entities:
                if p in known_event_places or p in ["Chennai", "Mumbai", "Delhi", "Paris", "Tokyo", "Rio",
                                                     "London", "Beijing", "Qatar", "Russia", "Brazil", "Moon",
                                                     "Wuhan", "NewDelhi", "Berlin", "India", "USA", "Ahmedabad",
                                                     "WestIndies", "Dubai", "UK", "Hiroshima", "NewYork"]:
                    place = p
                    break
            if not place and place_entities:
                place = place_entities[0]

            if event and place:
                return "EventOccurred", (event, place)
            if event and not place:
                # still return so we can show UNKNOWN or match year etc.
                return "EventOccurred", (event, "UnknownPlace")

        # ---------- 2. IsCapitalOf ----------
        if "IsCapitalOf" in predicates or "capital" in claim_lower:
            known_capitals = {f[0]: f[1] for f in kb.get_facts("IsCapitalOf")}
            known_countries = {f[1]: f[0] for f in kb.get_facts("IsCapitalOf")}

            city = next((e for e in entities if e in known_capitals), None)
            country = next((e for e in entities if e in known_countries), None)

            if city and country:
                return "IsCapitalOf", (city, country)
            if city:
                # User claimed a capital but maybe wrong country
                claimed_country = next((e for e in entities if e != city and e in self.place_keywords.values()), None)
                if claimed_country:
                    return "IsCapitalOf", (city, claimed_country)
                # fallback to real one (will be consistent)
                return "IsCapitalOf", (city, known_capitals[city])
            if country:
                real_city = known_countries[country]
                claimed_city = next((e for e in entities if e != country), None)
                if claimed_city:
                    return "IsCapitalOf", (claimed_city, country)
                return "IsCapitalOf", (real_city, country)

        # ---------- 3. PersonIs ----------
        if "PersonIs" in predicates or any(w in claim_lower for w in [
            "prime minister", "chief minister", "president", "ceo", "chancellor", "pm of", "cm of", "leader of", "minister"
        ]):
            known_people = {f[0]: f[1] for f in kb.get_facts("PersonIs")}
            person = next((e for e in entities if e in known_people), None)

            if person:
                # Try to detect claimed role from sentence
                # Detect claimed role (including wrong roles → will become INCONSISTENT)
                if "chief minister" in claim_lower or "cm of" in claim_lower:
                    if "india" in claim_lower:
                        return "PersonIs", (person, "ChiefMinisterOfIndia")
                    return "PersonIs", (person, "ChiefMinister")
                if "prime minister" in claim_lower or "pm of" in claim_lower:
                    if "india" in claim_lower:
                        return "PersonIs", (person, "PrimeMinisterOfIndia")
                    if "uk" in claim_lower or "britain" in claim_lower:
                        return "PersonIs", (person, "PrimeMinisterOfUK")
                    if "australia" in claim_lower:
                        return "PersonIs", (person, "PrimeMinisterOfAustralia")
                    if "canada" in claim_lower:
                        return "PersonIs", (person, "PrimeMinisterOfCanada")
                    if "pakistan" in claim_lower:
                        return "PersonIs", (person, "PrimeMinisterOfPakistan")
                    if "italy" in claim_lower:
                        return "PersonIs", (person, "PrimeMinisterOfItaly")
                    if "japan" in claim_lower:
                        return "PersonIs", (person, "PrimeMinisterOfJapan")
                    return "PersonIs", (person, "PrimeMinister")
                if "president" in claim_lower:
                    if "usa" in claim_lower or "america" in claim_lower or "united states" in claim_lower:
                        return "PersonIs", (person, "PresidentOfUSA")
                    if "france" in claim_lower:
                        return "PersonIs", (person, "PresidentOfFrance")
                    if "russia" in claim_lower:
                        return "PersonIs", (person, "PresidentOfRussia")
                    if "china" in claim_lower:
                        return "PersonIs", (person, "PresidentOfChina")
                    if "south korea" in claim_lower or "korea" in claim_lower:
                        return "PersonIs", (person, "PresidentOfSouthKorea")
                    if "india" in claim_lower:
                        return "PersonIs", (person, "FormerPresidentOfIndia")
                if "ceo" in claim_lower:
                    if "tesla" in claim_lower or "spacex" in claim_lower:
                        return "PersonIs", (person, "CEOOfTeslaAndSpaceX")
                    if "google" in claim_lower:
                        return "PersonIs", (person, "CEOOfGoogle")
                    if "microsoft" in claim_lower:
                        return "PersonIs", (person, "CEOOfMicrosoft")
                    if "apple" in claim_lower:
                        return "PersonIs", (person, "CEOOfApple")
                # Fallback – use the real known role (will be CONSISTENT)
                return "PersonIs", (person, known_people[person])

        # ---------- 4. SpaceAgencyOf ----------
        if "SpaceAgencyOf" in predicates or "space agency" in claim_lower or "space research" in claim_lower:
            agency = next((e for e in entities if e in ["ISRO", "NASA", "ESA", "CNSA", "Roscosmos", "JAXA", "CSA", "ASI", "CNES", "DLR"]), None)
            country = next((e for e in entities if e in ["India", "USA", "Europe", "China", "Russia", "Japan", "Canada", "Italy", "France", "Germany"]), None)
            if agency and country:
                return "SpaceAgencyOf", (agency, country)
            if agency:
                known = {f[0]: f[1] for f in kb.get_facts("SpaceAgencyOf")}
                claimed = next((e for e in entities if e != agency), None)
                if claimed:
                    return "SpaceAgencyOf", (agency, claimed)
                return "SpaceAgencyOf", (agency, known.get(agency, "Unknown"))

        # ---------- 5. DiscoveredBy ----------
        if "DiscoveredBy" in predicates or any(w in claim_lower for w in ["discovered", "invented", "proposed by", "developed by"]):
            discovery = next((e for e in entities if e in [
                "Gravity", "Relativity", "Penicillin", "Radioactivity", "Evolution",
                "RamanEffect", "PeriodicTable", "Electron", "Proton", "DNAStructure",
                "HeliocentricTheory", "Telescope", "ElectricBulb", "Telephone", "Radio", "Airplane"
            ]), None)
            person = next((e for e in entities if e in [
                "IsaacNewton", "AlbertEinstein", "AlexanderFleming", "MarieCurie",
                "CharlesDarwin", "CVraman", "DmitriMendeleev", "JJThomson",
                "ErnestRutherford", "WatsonAndCrick", "NicolausCopernicus",
                "GalileoGalilei", "ThomasEdison", "AlexanderGrahamBell",
                "GuglielmoMarconi", "WrightBrothers"
            ]), None)

            if discovery and person:
                return "DiscoveredBy", (discovery, person)
            if discovery:
                # try to pick any person mentioned, else real one
                known = {f[0]: f[1] for f in kb.get_facts("DiscoveredBy")}
                claimed_person = next((e for e in entities if e != discovery), None)
                if claimed_person:
                    return "DiscoveredBy", (discovery, claimed_person)
                return "DiscoveredBy", (discovery, known.get(discovery, "Unknown"))

        # ---------- 6. CurrencyOf ----------
        if "CurrencyOf" in predicates or "currency" in claim_lower:
            country = next((e for e in entities if e in [f[0] for f in kb.get_facts("CurrencyOf")]), None)
            if country:
                known = {f[0]: f[1] for f in kb.get_facts("CurrencyOf")}
                # We don't extract currency name easily, so return real one (CONSISTENT)
                # or Unknown if user mentioned wrong thing – still useful
                return "CurrencyOf", (country, known.get(country, "Unknown"))

        # ---------- 7. NationalAnimalOf ----------
        if "NationalAnimalOf" in predicates or "national animal" in claim_lower:
            country = next((e for e in entities if e in [f[0] for f in kb.get_facts("NationalAnimalOf")]), None)
            if country:
                known = {f[0]: f[1] for f in kb.get_facts("NationalAnimalOf")}
                return "NationalAnimalOf", (country, known.get(country, "Unknown"))

        # ---------- 8. LocatedIn ----------
        if "LocatedIn" in predicates or any(w in claim_lower for w in ["located in", "situated in", "is in", "lies in"]):
            city = next((e for e in entities if e in [f[0] for f in kb.get_facts("LocatedIn")]), None)
            region = next((e for e in entities if e in [f[1] for f in kb.get_facts("LocatedIn")]), None)
            if city and region:
                return "LocatedIn", (city, region)
            if city:
                known = {f[0]: f[1] for f in kb.get_facts("LocatedIn")}
                return "LocatedIn", (city, known.get(city, "Unknown"))

        # ---------- 9. CountryInContinent ----------
        if "CountryInContinent" in predicates or "continent" in claim_lower:
            country = next((e for e in entities if e in [f[0] for f in kb.get_facts("CountryInContinent")]), None)
            continent = next((e for e in entities if e in ["Asia", "Europe", "NorthAmerica", "SouthAmerica", "Africa", "Oceania"]), None)
            if country and continent:
                return "CountryInContinent", (country, continent)
            if country:
                known = {f[0]: f[1] for f in kb.get_facts("CountryInContinent")}
                return "CountryInContinent", (country, known.get(country, "Unknown"))


        # ---------- StateCapitalOf ----------
        if "StateCapitalOf" in predicates or ("capital" in claim_lower and any(s in claim_lower for s in ["tamil nadu", "maharashtra", "karnataka", "kerala", "gujarat", "rajasthan", "uttar pradesh", "west bengal", "bihar", "punjab"])):
            state_map = {
                "tamil nadu": "TamilNadu", "maharashtra": "Maharashtra", "karnataka": "Karnataka",
                "kerala": "Kerala", "gujarat": "Gujarat", "rajasthan": "Rajasthan",
                "uttar pradesh": "UttarPradesh", "west bengal": "WestBengal", "bihar": "Bihar",
                "punjab": "Punjab", "telangana": "Telangana", "andhra": "AndhraPradesh",
            }
            state = next((state_map[k] for k in state_map if k in claim_lower), None)
            city = next((e for e in entities if e in ["Chennai", "Mumbai", "Bengaluru", "Thiruvananthapuram", "Gandhinagar", "Jaipur", "Lucknow", "Kolkata", "Patna", "Chandigarh", "Hyderabad", "Amaravati"]), None)
            if state and city:
                return "StateCapitalOf", (state, city)
            if state:
                known = {f[0]: f[1] for f in kb.get_facts("StateCapitalOf")}
                claimed = next((e for e in entities if e != state), None)
                if claimed:
                    return "StateCapitalOf", (state, claimed)
                return "StateCapitalOf", (state, known.get(state, "Unknown"))

        # ---------- UniversityLocatedIn ----------
        if "UniversityLocatedIn" in predicates or any(u in claim_lower for u in ["iit", "iisc", "aiims", "harvard", "mit", "stanford", "oxford", "cambridge"]):
            uni_map = {
                "iit madras": "IITMadras", "iit bombay": "IITBombay", "iit delhi": "IITDelhi",
                "iit kanpur": "IITKanpur", "iisc": "IISC", "aiims": "AIIMSDelhi",
                "harvard": "Harvard", "mit": "MIT", "stanford": "Stanford",
                "oxford": "Oxford", "cambridge": "Cambridge",
            }
            uni = next((uni_map[k] for k in uni_map if k in claim_lower), None)
            place = next((e for e in entities if e not in (uni,)), None)
            if uni and place:
                return "UniversityLocatedIn", (uni, place)
            if uni:
                known = {f[0]: f[1] for f in kb.get_facts("UniversityLocatedIn")}
                return "UniversityLocatedIn", (uni, known.get(uni, "Unknown"))

        # ---------- CompanyHeadquartersIn ----------
        if "CompanyHeadquartersIn" in predicates or any(c in claim_lower for c in ["google", "microsoft", "apple", "amazon", "infosys", "tcs", "tesla", "meta"]):
            company_map = {
                "google": "Google", "microsoft": "Microsoft", "apple": "Apple",
                "amazon": "Amazon", "meta": "Meta", "facebook": "Meta",
                "tesla": "Tesla", "infosys": "Infosys", "tcs": "TCS",
                "wipro": "Wipro", "nvidia": "Nvidia", "samsung": "Samsung",
            }
            company = next((company_map[k] for k in company_map if k in claim_lower), None)
            country = next((e for e in entities if e in ["USA", "India", "China", "SouthKorea", "Japan"]), None)
            if company and country:
                return "CompanyHeadquartersIn", (company, country)
            if company:
                known = {f[0]: f[1] for f in kb.get_facts("CompanyHeadquartersIn")}
                claimed = next((e for e in entities if e != company), None)
                if claimed:
                    return "CompanyHeadquartersIn", (company, claimed)
                return "CompanyHeadquartersIn", (company, known.get(company, "Unknown"))

        # ---------- HoldsRecord ----------
        if "HoldsRecord" in predicates or "record" in claim_lower:
            person = next((e for e in entities if e in [f[0] for f in kb.get_facts("HoldsRecord")]), None)
            if person:
                known = {f[0]: f[1] for f in kb.get_facts("HoldsRecord")}
                return "HoldsRecord", (person, known.get(person, "Unknown"))


        return None, None
