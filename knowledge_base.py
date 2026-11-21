"""
Advanced & Vast FOL Knowledge Base
----------------------------------
Large structured fact collection with metadata for an advanced
Fake News Claim Verification System using First-Order Logic.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum


class FactCategory(Enum):
    POLITICS = "Politics"
    GEOGRAPHY = "Geography"
    HISTORY = "History"
    SCIENCE = "Science"
    SPACE = "Space"
    SPORTS = "Sports"
    BUSINESS = "Business"
    ORGANIZATION = "Organization"
    CULTURE = "Culture"
    TECHNOLOGY = "Technology"
    EDUCATION = "Education"
    ECONOMY = "Economy"
    HEALTH = "Health"
    ENVIRONMENT = "Environment"


@dataclass
class Fact:
    predicate: str
    arguments: Tuple[str, ...]
    category: FactCategory
    confidence: float = 1.0
    source: str = "Verified KB"
    year: Optional[int] = None
    description: str = ""

    def as_fol(self) -> str:
        return f"{self.predicate}({', '.join(self.arguments)})"


@dataclass
class LogicalRule:
    name: str
    description: str
    rule_type: str
    predicate: str
    key_arity: int = 1


class KnowledgeBase:
    def __init__(self):
        self.facts: List[Fact] = []
        self.rules: List[LogicalRule] = []
        self._index: Dict[str, List[Fact]] = {}
        self._build()

    def get_facts(self, predicate: str) -> List[Tuple]:
        return [f.arguments for f in self._index.get(predicate, [])]

    def get_fact_objects(self, predicate: str) -> List[Fact]:
        return self._index.get(predicate, [])

    def total_facts(self) -> int:
        return len(self.facts)

    def predicates(self) -> List[str]:
        return list(self._index.keys())

    def show_all_facts(self):
        print(f"\n===== VAST KNOWLEDGE BASE ({self.total_facts()} facts) =====")
        for pred in sorted(self._index.keys()):
            print(f"  {pred}: {len(self._index[pred])} facts")
        print(f"Rules: {len(self.rules)}")
        print("=" * 50)

    def _f(self, pred, args, cat, conf=1.0, source="Verified KB", year=None, desc=""):
        self.facts.append(Fact(pred, tuple(args), cat, conf, source, year, desc))

    def _build(self):
        self._add_events()
        self._add_people()
        self._add_capitals()
        self._add_locations()
        self._add_years()
        self._add_continents()
        self._add_discoveries()
        self._add_space()
        self._add_organizations()
        self._add_currency_language()
        self._add_symbols()
        self._add_landmarks()
        self._add_indian_states()
        self._add_universities()
        self._add_tech_companies()
        self._add_awards()
        self._add_economy()
        self._add_health_env()
        self._add_sports_records()
        self._add_rules()
        for f in self.facts:
            self._index.setdefault(f.predicate, []).append(f)

    # ===================== EVENTS =====================
    def _add_events(self):
        C, H, S, P = FactCategory.SPORTS, FactCategory.HISTORY, FactCategory.SPACE, FactCategory.POLITICS
        events = [
            ("Olympics2024", "Paris", C, 2024, "IOC"), ("Olympics2020", "Tokyo", C, 2021, "IOC"),
            ("Olympics2016", "Rio", C, 2016, "IOC"), ("Olympics2012", "London", C, 2012, "IOC"),
            ("Olympics2008", "Beijing", C, 2008, "IOC"), ("Olympics2004", "Athens", C, 2004, "IOC"),
            ("Olympics2000", "Sydney", C, 2000, "IOC"), ("Olympics1996", "Atlanta", C, 1996, "IOC"),
            ("Olympics1984", "LosAngeles", C, 1984, "IOC"), ("Olympics1980", "Moscow", C, 1980, "IOC"),
            ("WorldCup2022", "Qatar", C, 2022, "FIFA"), ("WorldCup2018", "Russia", C, 2018, "FIFA"),
            ("WorldCup2014", "Brazil", C, 2014, "FIFA"), ("WorldCup2010", "SouthAfrica", C, 2010, "FIFA"),
            ("WorldCup2006", "Germany", C, 2006, "FIFA"), ("WorldCup2002", "JapanKorea", C, 2002, "FIFA"),
            ("CricketWorldCup2023", "India", C, 2023, "ICC"), ("CricketWorldCup2019", "England", C, 2019, "ICC"),
            ("CricketWorldCup2015", "Australia", C, 2015, "ICC"), ("CricketWorldCup2011", "India", C, 2011, "ICC"),
            ("T20WorldCup2024", "WestIndies", C, 2024, "ICC"), ("T20WorldCup2022", "Australia", C, 2022, "ICC"),
            ("IPL2024Final", "Chennai", C, 2024, "BCCI"), ("IPL2023Final", "Ahmedabad", C, 2023, "BCCI"),
            ("IndependenceIndia", "India", H, 1947, "Historical"), ("IndependenceUSA", "USA", H, 1776, "Historical"),
            ("IndependencePakistan", "Pakistan", H, 1947, "Historical"), ("IndependenceBangladesh", "Bangladesh", H, 1971, "Historical"),
            ("COVID19Outbreak", "Wuhan", H, 2019, "WHO"), ("Chandrayaan3Landing", "Moon", S, 2023, "ISRO"),
            ("Chandrayaan2", "Moon", S, 2019, "ISRO"), ("Apollo11Landing", "Moon", S, 1969, "NASA"),
            ("Apollo13", "Space", S, 1970, "NASA"), ("G20Summit2023", "NewDelhi", P, 2023, "G20"),
            ("G20Summit2024", "Rio", P, 2024, "G20"), ("COP28", "Dubai", P, 2023, "UN"),
            ("COP27", "SharmElSheikh", P, 2022, "UN"), ("BrexitReferendum", "UK", P, 2016, "UKGov"),
            ("FallOfBerlinWall", "Berlin", H, 1989, "Historical"), ("September11Attacks", "NewYork", H, 2001, "Historical"),
            ("HiroshimaBombing", "Hiroshima", H, 1945, "Historical"), ("NagasakiBombing", "Nagasaki", H, 1945, "Historical"),
            ("FirstHumanInSpace", "Space", S, 1961, "Roscosmos"), ("FirstWomanInSpace", "Space", S, 1963, "Roscosmos"),
            ("PartitionOfIndia", "India", H, 1947, "Historical"), ("FrenchRevolution", "France", H, 1789, "Historical"),
            ("AmericanRevolution", "USA", H, 1776, "Historical"), ("RussianRevolution", "Russia", H, 1917, "Historical"),
            ("WorldWar1Start", "Europe", H, 1914, "Historical"), ("WorldWar2Start", "Europe", H, 1939, "Historical"),
            ("WorldWar2End", "Europe", H, 1945, "Historical"), ("DDayLanding", "Normandy", H, 1944, "Historical"),
            ("IndianConstitutionAdopted", "India", P, 1950, "Historical"), ("RepublicDayIndia", "India", P, 1950, "Historical"),
            ("MarsOrbiterInsertion", "Mars", S, 2014, "ISRO"), ("JamesWebbLaunch", "Space", S, 2021, "NASA"),
            ("Demo2Launch", "Space", S, 2020, "SpaceX"), ("FirstiPhoneLaunch", "USA", FactCategory.TECHNOLOGY, 2007, "Apple"),
        ]
        for e, place, cat, year, src in events:
            self._f("EventOccurred", (e, place), cat, 1.0, src, year)

    # ===================== PEOPLE =====================
    def _add_people(self):
        P, S, B = FactCategory.POLITICS, FactCategory.SCIENCE, FactCategory.BUSINESS
        people = [
            # Politics - India
            ("NarendraModi", "PrimeMinisterOfIndia", P, 0.99),
            ("DroupadiMurmu", "PresidentOfIndia", P, 0.99),
            ("AmitShah", "HomeMinisterOfIndia", P, 0.98),
            ("NirmalaSitharaman", "FinanceMinisterOfIndia", P, 0.98),
            ("JawaharlalNehru", "FirstPrimeMinisterOfIndia", P, 1.0),
            ("IndiraGandhi", "FirstWomanPrimeMinisterOfIndia", P, 1.0),
            ("RajivGandhi", "FormerPrimeMinisterOfIndia", P, 1.0),
            ("AtalBihariVajpayee", "FormerPrimeMinisterOfIndia", P, 1.0),
            ("ManmohanSingh", "FormerPrimeMinisterOfIndia", P, 1.0),
            ("DrAPJAbdulKalam", "FormerPresidentOfIndia", P, 1.0),
            ("DrRajendraPrasad", "FirstPresidentOfIndia", P, 1.0),
            ("MahatmaGandhi", "FatherOfNationIndia", P, 1.0),
            ("SardarPatel", "FirstDeputyPrimeMinisterOfIndia", P, 1.0),
            ("BabaSahebAmbedkar", "ArchitectOfIndianConstitution", P, 1.0),
            ("SubhasChandraBose", "FreedomFighter", P, 1.0),
            ("BhagatSingh", "FreedomFighter", P, 1.0),
            ("MKStalin", "ChiefMinisterOfTamilNadu", P, 0.98),
            ("YogiAdityanath", "ChiefMinisterOfUttarPradesh", P, 0.98),
            ("MamataBanerjee", "ChiefMinisterOfWestBengal", P, 0.98),
            # World leaders
            ("JoeBiden", "PresidentOfUSA", P, 0.99), ("DonaldTrump", "FormerPresidentOfUSA", P, 1.0),
            ("EmmanuelMacron", "PresidentOfFrance", P, 0.99), ("KeirStarmer", "PrimeMinisterOfUK", P, 0.98),
            ("RishiSunak", "FormerPrimeMinisterOfUK", P, 0.98), ("XiJinping", "PresidentOfChina", P, 0.99),
            ("VladimirPutin", "PresidentOfRussia", P, 0.99), ("AnthonyAlbanese", "PrimeMinisterOfAustralia", P, 0.98),
            ("JustinTrudeau", "PrimeMinisterOfCanada", P, 0.98), ("OlafScholz", "ChancellorOfGermany", P, 0.98),
            ("GiorgiaMeloni", "PrimeMinisterOfItaly", P, 0.98), ("VolodymyrZelenskyy", "PresidentOfUkraine", P, 0.99),
            ("MohammedBinSalman", "CrownPrinceOfSaudiArabia", P, 0.98), ("RecepTayyipErdogan", "PresidentOfTurkey", P, 0.98),
            ("CyrilRamaphosa", "PresidentOfSouthAfrica", P, 0.98), ("LuizInacioLula", "PresidentOfBrazil", P, 0.98),
            ("ShehbazSharif", "PrimeMinisterOfPakistan", P, 0.97), ("SheikhHasina", "FormerPrimeMinisterOfBangladesh", P, 0.97),
            # Scientists
            ("AlbertEinstein", "Physicist", S, 1.0), ("IsaacNewton", "Physicist", S, 1.0),
            ("MarieCurie", "Scientist", S, 1.0), ("StephenHawking", "Physicist", S, 1.0),
            ("CVraman", "Physicist", S, 1.0), ("HomiBhabha", "NuclearScientist", S, 1.0),
            ("VikramSarabhai", "SpaceScientist", S, 1.0), ("SatishDhawan", "SpaceScientist", S, 1.0),
            ("CharlesDarwin", "Biologist", S, 1.0), ("AlexanderFleming", "Biologist", S, 1.0),
            ("GalileoGalilei", "Astronomer", S, 1.0), ("NicolausCopernicus", "Astronomer", S, 1.0),
            ("DmitriMendeleev", "Chemist", S, 1.0), ("ThomasEdison", "Inventor", S, 1.0),
            ("NikolaTesla", "Inventor", S, 1.0), ("WrightBrothers", "AviationPioneers", S, 1.0),
            ("AlanTuring", "ComputerScientist", S, 1.0), ("AdaLovelace", "ComputerScientist", S, 1.0),
            # Business
            ("ElonMusk", "CEOOfTeslaAndSpaceX", B, 0.99), ("SundarPichai", "CEOOfGoogle", B, 0.99),
            ("SatyaNadella", "CEOOfMicrosoft", B, 0.99), ("TimCook", "CEOOfApple", B, 0.99),
            ("MukeshAmbani", "ChairmanOfReliance", B, 0.99), ("RatanTata", "FormerChairmanOfTata", B, 1.0),
            ("JeffBezos", "FounderOfAmazon", B, 1.0), ("MarkZuckerberg", "CEOOfMeta", B, 0.99),
            ("JensenHuang", "CEOOfNvidia", B, 0.99), ("GautamAdani", "ChairmanOfAdaniGroup", B, 0.98),
            ("NandanNilekani", "CoFounderOfInfosys", B, 0.98), ("AzimPremji", "FormerChairmanOfWipro", B, 0.98),
            ("BillGates", "FounderOfMicrosoft", B, 1.0), ("WarrenBuffett", "CEOOfBerkshireHathaway", B, 0.99),
        ]
        for person, role, cat, conf in people:
            self._f("PersonIs", (person, role), cat, conf)

    # ===================== CAPITALS =====================
    def _add_capitals(self):
        G = FactCategory.GEOGRAPHY
        capitals = [
            ("Delhi", "India"), ("Paris", "France"), ("WashingtonDC", "USA"), ("London", "UK"),
            ("Tokyo", "Japan"), ("Beijing", "China"), ("Moscow", "Russia"), ("Canberra", "Australia"),
            ("Ottawa", "Canada"), ("Berlin", "Germany"), ("Rome", "Italy"), ("Madrid", "Spain"),
            ("Brasilia", "Brazil"), ("Cairo", "Egypt"), ("Seoul", "SouthKorea"), ("Islamabad", "Pakistan"),
            ("Dhaka", "Bangladesh"), ("Kathmandu", "Nepal"), ("Colombo", "SriLanka"), ("Thimphu", "Bhutan"),
            ("Male", "Maldives"), ("Bangkok", "Thailand"), ("Jakarta", "Indonesia"), ("KualaLumpur", "Malaysia"),
            ("Singapore", "Singapore"), ("Hanoi", "Vietnam"), ("Manila", "Philippines"), ("Riyadh", "SaudiArabia"),
            ("AbuDhabi", "UAE"), ("Doha", "Qatar"), ("Tehran", "Iran"), ("Ankara", "Turkey"),
            ("Athens", "Greece"), ("Amsterdam", "Netherlands"), ("Brussels", "Belgium"), ("Vienna", "Austria"),
            ("Bern", "Switzerland"), ("Stockholm", "Sweden"), ("Oslo", "Norway"), ("Copenhagen", "Denmark"),
            ("Helsinki", "Finland"), ("Warsaw", "Poland"), ("Prague", "CzechRepublic"), ("Budapest", "Hungary"),
            ("Lisbon", "Portugal"), ("Dublin", "Ireland"), ("Pretoria", "SouthAfrica"), ("Nairobi", "Kenya"),
            ("AddisAbaba", "Ethiopia"), ("Abuja", "Nigeria"), ("BuenosAires", "Argentina"), ("Santiago", "Chile"),
            ("Lima", "Peru"), ("MexicoCity", "Mexico"), ("Havana", "Cuba"), ("Wellington", "NewZealand"),
            ("Kyiv", "Ukraine"), ("Baghdad", "Iraq"), ("Damascus", "Syria"), ("Amman", "Jordan"),
            ("Beirut", "Lebanon"), ("Jerusalem", "Israel"), ("KuwaitCity", "Kuwait"), ("Muscat", "Oman"),
            ("Manama", "Bahrain"), ("Kabul", "Afghanistan"), ("Tashkent", "Uzbekistan"), ("Astana", "Kazakhstan"),
            ("Ulaanbaatar", "Mongolia"), ("Pyongyang", "NorthKorea"), ("Taipei", "Taiwan"),
            ("Yangon", "Myanmar"), ("PhnomPenh", "Cambodia"), ("Vientiane", "Laos"),
        ]
        for city, country in capitals:
            self._f("IsCapitalOf", (city, country), G, 1.0, "Geographical authority")

    # ===================== LOCATIONS =====================
    def _add_locations(self):
        G = FactCategory.GEOGRAPHY
        locs = [
            ("Chennai", "TamilNadu"), ("Mumbai", "Maharashtra"), ("Kolkata", "WestBengal"),
            ("Bengaluru", "Karnataka"), ("Hyderabad", "Telangana"), ("Ahmedabad", "Gujarat"),
            ("Pune", "Maharashtra"), ("Jaipur", "Rajasthan"), ("Lucknow", "UttarPradesh"),
            ("Kanpur", "UttarPradesh"), ("Nagpur", "Maharashtra"), ("Indore", "MadhyaPradesh"),
            ("Bhopal", "MadhyaPradesh"), ("Patna", "Bihar"), ("Ranchi", "Jharkhand"),
            ("Bhubaneswar", "Odisha"), ("Thiruvananthapuram", "Kerala"), ("Kochi", "Kerala"),
            ("Coimbatore", "TamilNadu"), ("Madurai", "TamilNadu"), ("Chandigarh", "Punjab"),
            ("Guwahati", "Assam"), ("Shimla", "HimachalPradesh"), ("Dehradun", "Uttarakhand"),
            ("Srinagar", "JammuAndKashmir"), ("Leh", "Ladakh"), ("Panaji", "Goa"),
            ("Raipur", "Chhattisgarh"), ("Gandhinagar", "Gujarat"), ("Dispur", "Assam"),
            ("Amaravati", "AndhraPradesh"), ("Itanagar", "ArunachalPradesh"), ("Imphal", "Manipur"),
            ("Shillong", "Meghalaya"), ("Aizawl", "Mizoram"), ("Kohima", "Nagaland"),
            ("Agartala", "Tripura"), ("Gangtok", "Sikkim"),
            ("Paris", "France"), ("Tokyo", "Japan"), ("NewYork", "USA"), ("LosAngeles", "USA"),
            ("London", "UK"), ("Wuhan", "China"), ("Shanghai", "China"), ("Dubai", "UAE"),
            ("Sydney", "Australia"), ("Melbourne", "Australia"), ("Toronto", "Canada"),
            ("Berlin", "Germany"), ("Munich", "Germany"), ("Rome", "Italy"), ("Milan", "Italy"),
            ("Madrid", "Spain"), ("Barcelona", "Spain"), ("Moscow", "Russia"), ("RioDeJaneiro", "Brazil"),
            ("CapeTown", "SouthAfrica"), ("SingaporeCity", "Singapore"), ("HongKongCity", "HongKong"),
        ]
        for city, region in locs:
            self._f("LocatedIn", (city, region), G, 1.0)

    # ===================== YEARS =====================
    def _add_years(self):
        H = FactCategory.HISTORY
        years = [
            ("Olympics2024", 2024), ("Olympics2020", 2021), ("Olympics2016", 2016),
            ("Olympics2012", 2012), ("Olympics2008", 2008), ("WorldCup2022", 2022),
            ("WorldCup2018", 2018), ("WorldCup2014", 2014), ("CricketWorldCup2023", 2023),
            ("CricketWorldCup2011", 2011), ("IndependenceIndia", 1947), ("IndependenceUSA", 1776),
            ("COVID19Outbreak", 2019), ("Chandrayaan3Landing", 2023), ("Apollo11Landing", 1969),
            ("FallOfBerlinWall", 1989), ("September11Attacks", 2001), ("HiroshimaBombing", 1945),
            ("FirstHumanInSpace", 1961), ("BrexitReferendum", 2016), ("G20Summit2023", 2023),
            ("FrenchRevolution", 1789), ("WorldWar2End", 1945), ("IndianConstitutionAdopted", 1950),
            ("InternetPublic", 1991), ("FirstiPhoneLaunch", 2007), ("GoogleFounded", 1998),
            ("MicrosoftFounded", 1975), ("AppleFounded", 1976), ("FacebookLaunch", 2004),
            ("TeslaFounded", 2003), ("ISROFounded", 1969), ("NASAFounded", 1958),
        ]
        for event, year in years:
            self._f("HappenedInYear", (event, str(year)), H, 1.0, year=year)

    # ===================== CONTINENTS =====================
    def _add_continents(self):
        G = FactCategory.GEOGRAPHY
        mapping = [
            ("India", "Asia"), ("China", "Asia"), ("Japan", "Asia"), ("Pakistan", "Asia"),
            ("Bangladesh", "Asia"), ("Nepal", "Asia"), ("SriLanka", "Asia"), ("Bhutan", "Asia"),
            ("Thailand", "Asia"), ("Indonesia", "Asia"), ("Malaysia", "Asia"), ("Singapore", "Asia"),
            ("Vietnam", "Asia"), ("Philippines", "Asia"), ("SouthKorea", "Asia"), ("NorthKorea", "Asia"),
            ("SaudiArabia", "Asia"), ("UAE", "Asia"), ("Qatar", "Asia"), ("Iran", "Asia"),
            ("Iraq", "Asia"), ("Turkey", "Asia"), ("Afghanistan", "Asia"), ("Israel", "Asia"),
            ("Myanmar", "Asia"), ("Cambodia", "Asia"), ("Laos", "Asia"), ("Mongolia", "Asia"),
            ("France", "Europe"), ("Germany", "Europe"), ("UK", "Europe"), ("Italy", "Europe"),
            ("Spain", "Europe"), ("Russia", "Europe"), ("Ukraine", "Europe"), ("Poland", "Europe"),
            ("Netherlands", "Europe"), ("Belgium", "Europe"), ("Switzerland", "Europe"), ("Sweden", "Europe"),
            ("Norway", "Europe"), ("Portugal", "Europe"), ("Ireland", "Europe"), ("Greece", "Europe"),
            ("USA", "NorthAmerica"), ("Canada", "NorthAmerica"), ("Mexico", "NorthAmerica"), ("Cuba", "NorthAmerica"),
            ("Brazil", "SouthAmerica"), ("Argentina", "SouthAmerica"), ("Chile", "SouthAmerica"), ("Peru", "SouthAmerica"),
            ("Australia", "Oceania"), ("NewZealand", "Oceania"),
            ("Egypt", "Africa"), ("SouthAfrica", "Africa"), ("Kenya", "Africa"), ("Nigeria", "Africa"),
            ("Ethiopia", "Africa"), ("Morocco", "Africa"), ("Ghana", "Africa"),
        ]
        for country, cont in mapping:
            self._f("CountryInContinent", (country, cont), G, 1.0)

    # ===================== DISCOVERIES =====================
    def _add_discoveries(self):
        S = FactCategory.SCIENCE
        discs = [
            ("Gravity", "IsaacNewton", 1687), ("Relativity", "AlbertEinstein", 1905),
            ("Penicillin", "AlexanderFleming", 1928), ("Radioactivity", "MarieCurie", 1898),
            ("Evolution", "CharlesDarwin", 1859), ("RamanEffect", "CVraman", 1928),
            ("PeriodicTable", "DmitriMendeleev", 1869), ("Electron", "JJThomson", 1897),
            ("DNAStructure", "WatsonAndCrick", 1953), ("XRays", "WilhelmRoentgen", 1895),
            ("ElectricBulb", "ThomasEdison", 1879), ("Telephone", "AlexanderGrahamBell", 1876),
            ("Airplane", "WrightBrothers", 1903), ("HeliocentricTheory", "NicolausCopernicus", 1543),
            ("Telescope", "GalileoGalilei", 1609), ("ComputerScience", "AlanTuring", 1936),
            ("WorldWideWeb", "TimBernersLee", 1989), ("Radio", "GuglielmoMarconi", 1895),
            ("Vaccination", "EdwardJenner", 1796), ("CirculationOfBlood", "WilliamHarvey", 1628),
            ("QuantumTheory", "MaxPlanck", 1900), ("PhotoelectricEffect", "AlbertEinstein", 1905),
            ("Neutron", "JamesChadwick", 1932), ("Proton", "ErnestRutherford", 1917),
        ]
        for disc, person, year in discs:
            self._f("DiscoveredBy", (disc, person), S, 1.0, "Scientific consensus", year)

    # ===================== SPACE =====================
    def _add_space(self):
        S = FactCategory.SPACE
        for agency, country in [
            ("ISRO", "India"), ("NASA", "USA"), ("ESA", "Europe"), ("CNSA", "China"),
            ("Roscosmos", "Russia"), ("JAXA", "Japan"), ("CSA", "Canada"), ("CNES", "France"),
            ("DLR", "Germany"), ("UKSA", "UK"), ("KARI", "SouthKorea"), ("Suparco", "Pakistan"),
        ]:
            self._f("SpaceAgencyOf", (agency, country), S, 1.0)
        for m in ["Chandrayaan3", "Apollo11", "MarsOrbiterMission", "MarsPerseverance",
                  "JamesWebbTelescope", "HubbleTelescope", "Voyager1", "Voyager2",
                  "AdityaL1", "GaganyaanTest", "CassiniHuygens", "NewHorizons", "ParkerSolarProbe"]:
            self._f("MissionSuccess", (m, "True"), S, 1.0)

    # ===================== ORGANIZATIONS =====================
    def _add_organizations(self):
        O = FactCategory.ORGANIZATION
        orgs = [
            ("UnitedNations", "NewYork"), ("WHO", "Geneva"), ("IMF", "WashingtonDC"),
            ("WorldBank", "WashingtonDC"), ("EuropeanUnion", "Brussels"), ("NATO", "Brussels"),
            ("WTO", "Geneva"), ("UNESCO", "Paris"), ("ICJ", "TheHague"), ("ICC", "TheHague"),
            ("FIFA", "Zurich"), ("IOC", "Lausanne"), ("ICC_Cricket", "Dubai"),
            ("ISROHeadquarters", "Bengaluru"), ("NASAHeadquarters", "WashingtonDC"),
            ("ASEAN", "Jakarta"), ("SAARC", "Kathmandu"), ("AfricanUnion", "AddisAbaba"),
            ("OPEC", "Vienna"), ("RedCross", "Geneva"), ("AmnestyInternational", "London"),
            ("BCCI", "Mumbai"), ("RBI", "Mumbai"), ("SEBI", "Mumbai"),
        ]
        for org, place in orgs:
            self._f("OrganizationLocatedIn", (org, place), O, 1.0)

    # ===================== CURRENCY & LANGUAGE =====================
    def _add_currency_language(self):
        G = FactCategory.GEOGRAPHY
        for c, cur in [
            ("India", "IndianRupee"), ("USA", "USDollar"), ("UK", "PoundSterling"),
            ("Japan", "Yen"), ("China", "Yuan"), ("Eurozone", "Euro"), ("Russia", "Ruble"),
            ("Australia", "AustralianDollar"), ("Canada", "CanadianDollar"), ("Switzerland", "SwissFranc"),
            ("SaudiArabia", "SaudiRiyal"), ("UAE", "Dirham"), ("Singapore", "SingaporeDollar"),
            ("SouthKorea", "Won"), ("Brazil", "Real"), ("SouthAfrica", "Rand"),
            ("Turkey", "Lira"), ("Mexico", "Peso"), ("Indonesia", "Rupiah"), ("Thailand", "Baht"),
            ("Pakistan", "PakistaniRupee"), ("Bangladesh", "Taka"),
        ]:
            self._f("CurrencyOf", (c, cur), G, 1.0)
        for c, lang in [
            ("India", "Hindi"), ("USA", "English"), ("UK", "English"), ("France", "French"),
            ("Germany", "German"), ("Japan", "Japanese"), ("China", "Mandarin"), ("Russia", "Russian"),
            ("Spain", "Spanish"), ("Brazil", "Portuguese"), ("SaudiArabia", "Arabic"), ("Italy", "Italian"),
            ("Pakistan", "Urdu"), ("Bangladesh", "Bengali"), ("Portugal", "Portuguese"),
            ("Netherlands", "Dutch"), ("SouthKorea", "Korean"), ("Turkey", "Turkish"), ("Iran", "Persian"),
        ]:
            self._f("OfficialLanguageOf", (c, lang), G, 0.95)

    # ===================== SYMBOLS =====================
    def _add_symbols(self):
        C = FactCategory.CULTURE
        for c, a in [
            ("India", "Tiger"), ("USA", "BaldEagle"), ("Australia", "Kangaroo"), ("China", "GiantPanda"),
            ("Russia", "BrownBear"), ("Canada", "Beaver"), ("SouthAfrica", "Springbok"), ("UK", "Lion"),
            ("France", "GallicRooster"), ("Japan", "GreenPheasant"), ("Germany", "FederalEagle"),
            ("Brazil", "Jaguar"), ("Mexico", "GoldenEagle"), ("NewZealand", "Kiwi"), ("Pakistan", "Markhor"),
        ]:
            self._f("NationalAnimalOf", (c, a), C, 1.0)
        for c, s in [
            ("India", "Hockey"), ("USA", "Baseball"), ("Canada", "IceHockey"), ("Japan", "Sumo"),
            ("Brazil", "Football"), ("England", "Cricket"), ("Australia", "Cricket"), ("China", "TableTennis"),
            ("Pakistan", "FieldHockey"), ("Bangladesh", "Kabaddi"),
        ]:
            self._f("NationalSportOf", (c, s), C, 0.95)

    # ===================== LANDMARKS =====================
    def _add_landmarks(self):
        C = FactCategory.CULTURE
        for lm, place in [
            ("TajMahal", "Agra"), ("EiffelTower", "Paris"), ("StatueOfLiberty", "NewYork"),
            ("GreatWall", "China"), ("Colosseum", "Rome"), ("SydneyOperaHouse", "Sydney"),
            ("ChristTheRedeemer", "RioDeJaneiro"), ("PyramidsOfGiza", "Cairo"), ("BigBen", "London"),
            ("BurjKhalifa", "Dubai"), ("RedFort", "Delhi"), ("QutubMinar", "Delhi"),
            ("GatewayOfIndia", "Mumbai"), ("Charminar", "Hyderabad"), ("IndiaGate", "Delhi"),
            ("LotusTemple", "Delhi"), ("MachuPicchu", "Peru"), ("Petra", "Jordan"),
            ("MountFuji", "Japan"), ("Stonehenge", "UK"), ("GoldenTemple", "Amritsar"),
            ("MeenakshiTemple", "Madurai"), ("HawaMahal", "Jaipur"), ("VictoriaMemorial", "Kolkata"),
            ("HowrahBridge", "Kolkata"), ("MarinaBeach", "Chennai"), ("MysorePalace", "Mysore"),
            ("StatueOfUnity", "Gujarat"), ("KonarkSunTemple", "Odisha"), ("AjantaEllora", "Maharashtra"),
        ]:
            self._f("LandmarkLocatedIn", (lm, place), C, 1.0)

    # ===================== INDIAN STATES =====================
    def _add_indian_states(self):
        G = FactCategory.GEOGRAPHY
        states = [
            ("TamilNadu", "Chennai"), ("Maharashtra", "Mumbai"), ("Karnataka", "Bengaluru"),
            ("Kerala", "Thiruvananthapuram"), ("AndhraPradesh", "Amaravati"), ("Telangana", "Hyderabad"),
            ("Gujarat", "Gandhinagar"), ("Rajasthan", "Jaipur"), ("UttarPradesh", "Lucknow"),
            ("WestBengal", "Kolkata"), ("Bihar", "Patna"), ("MadhyaPradesh", "Bhopal"),
            ("Odisha", "Bhubaneswar"), ("Punjab", "Chandigarh"), ("Haryana", "Chandigarh"),
            ("Assam", "Dispur"), ("Jharkhand", "Ranchi"), ("Chhattisgarh", "Raipur"),
            ("HimachalPradesh", "Shimla"), ("Uttarakhand", "Dehradun"), ("Goa", "Panaji"),
            ("Manipur", "Imphal"), ("Meghalaya", "Shillong"), ("Mizoram", "Aizawl"),
            ("Nagaland", "Kohima"), ("Tripura", "Agartala"), ("Sikkim", "Gangtok"),
            ("ArunachalPradesh", "Itanagar"),
        ]
        for state, capital in states:
            self._f("StateCapitalOf", (state, capital), G, 1.0, "Government of India")

    # ===================== UNIVERSITIES =====================
    def _add_universities(self):
        E = FactCategory.EDUCATION
        unis = [
            ("IITMadras", "Chennai"), ("IITBombay", "Mumbai"), ("IITDelhi", "Delhi"),
            ("IITKanpur", "Kanpur"), ("IITKharagpur", "Kharagpur"), ("IISC", "Bengaluru"),
            ("AIIMSDelhi", "Delhi"), ("JNU", "Delhi"), ("DU", "Delhi"),
            ("AnnaUniversity", "Chennai"), ("UniversityOfMadras", "Chennai"),
            ("Harvard", "CambridgeMA"), ("MIT", "CambridgeMA"), ("Stanford", "California"),
            ("Oxford", "Oxford"), ("Cambridge", "CambridgeUK"), ("Yale", "NewHaven"),
            ("Princeton", "NewJersey"), ("Caltech", "California"), ("NUS", "Singapore"),
        ]
        for uni, place in unis:
            self._f("UniversityLocatedIn", (uni, place), E, 1.0)

    # ===================== TECH COMPANIES =====================
    def _add_tech_companies(self):
        T = FactCategory.TECHNOLOGY
        companies = [
            ("Google", "USA"), ("Microsoft", "USA"), ("Apple", "USA"), ("Amazon", "USA"),
            ("Meta", "USA"), ("Tesla", "USA"), ("Nvidia", "USA"), ("Netflix", "USA"),
            ("Infosys", "India"), ("TCS", "India"), ("Wipro", "India"), ("HCL", "India"),
            ("RelianceJio", "India"), ("Flipkart", "India"), ("Paytm", "India"),
            ("Samsung", "SouthKorea"), ("Sony", "Japan"), ("Huawei", "China"),
            ("Alibaba", "China"), ("Tencent", "China"), ("SpaceX", "USA"),
        ]
        for company, country in companies:
            self._f("CompanyHeadquartersIn", (company, country), T, 0.98)

    # ===================== AWARDS =====================
    def _add_awards(self):
        C = FactCategory.CULTURE
        awards = [
            ("NobelPrizePhysics", "Sweden"), ("NobelPrizePeace", "Norway"),
            ("BharatRatna", "India"), ("PadmaVibhushan", "India"), ("PadmaBhushan", "India"),
            ("Oscar", "USA"), ("Grammy", "USA"), ("BookerPrize", "UK"),
            ("FieldsMedal", "International"), ("TuringAward", "USA"),
            ("PulitzerPrize", "USA"), ("RamonMagsaysay", "Philippines"),
        ]
        for award, place in awards:
            self._f("AwardOriginatesFrom", (award, place), C, 1.0)

    # ===================== ECONOMY =====================
    def _add_economy(self):
        E = FactCategory.ECONOMY
        for country, org in [
            ("India", "G20"), ("USA", "G7"), ("China", "G20"), ("Japan", "G7"),
            ("Germany", "G7"), ("UK", "G7"), ("France", "G7"), ("Italy", "G7"),
            ("Canada", "G7"), ("Brazil", "BRICS"), ("Russia", "BRICS"),
            ("SouthAfrica", "BRICS"), ("India", "BRICS"), ("China", "BRICS"),
        ]:
            self._f("MemberOf", (country, org), E, 1.0)
        for country, status in [
            ("India", "Developing"), ("USA", "Developed"), ("China", "Developing"),
            ("Japan", "Developed"), ("Germany", "Developed"), ("UK", "Developed"),
            ("Bangladesh", "Developing"), ("Norway", "Developed"),
        ]:
            self._f("EconomyStatus", (country, status), E, 0.9)

    # ===================== HEALTH & ENVIRONMENT =====================
    def _add_health_env(self):
        H = FactCategory.HEALTH
        Env = FactCategory.ENVIRONMENT
        for disease, org in [
            ("COVID19", "WHO"), ("Polio", "WHO"), ("Tuberculosis", "WHO"),
            ("Malaria", "WHO"), ("HIV", "WHO"),
        ]:
            self._f("MonitoredBy", (disease, org), H, 1.0)
        for site, country in [
            ("AmazonRainforest", "Brazil"), ("GreatBarrierReef", "Australia"),
            ("Sundarbans", "India"), ("WesternGhats", "India"),
            ("Yellowstone", "USA"), ("Serengeti", "Tanzania"),
        ]:
            self._f("HeritageSiteIn", (site, country), Env, 1.0)

    # ===================== SPORTS RECORDS =====================
    def _add_sports_records(self):
        C = FactCategory.SPORTS
        for person, record in [
            ("SachinTendulkar", "MostInternationalRunsCricket"),
            ("ViratKohli", "FastestTo8000ODIRuns"),
            ("MSDhoni", "WorldCupWinningCaptain2011"),
            ("UsainBolt", "FastestMan100m"),
            ("MichaelPhelps", "MostOlympicGolds"),
            ("SerenaWilliams", "MostGrandSlamSinglesWomen"),
            ("RogerFederer", "MultipleGrandSlamChampion"),
            ("LionelMessi", "MultipleBallonDorWinner"),
            ("CristianoRonaldo", "AllTimeTopInternationalScorer"),
            ("PVSindhu", "OlympicMedalistBadminton"),
            ("NeerajChopra", "OlympicGoldJavelin"),
            ("MaryKom", "WorldChampionBoxer"),
        ]:
            self._f("HoldsRecord", (person, record), C, 0.95)

    # ===================== RULES =====================
    def _add_rules(self):
        self.rules = [
            LogicalRule("UniqueEventLocation", "An event can occur in only one primary location", "uniqueness", "EventOccurred", 1),
            LogicalRule("UniqueCapital", "A country has exactly one official capital", "uniqueness", "IsCapitalOf", 2),
            LogicalRule("UniquePersonRole", "A person holds at most one primary high office at a time", "uniqueness", "PersonIs", 1),
            LogicalRule("UniqueDiscovery", "A scientific discovery is attributed to one primary scientist/team", "uniqueness", "DiscoveredBy", 1),
            LogicalRule("UniqueCurrency", "A country has one primary official currency", "uniqueness", "CurrencyOf", 1),
            LogicalRule("UniqueAgencyCountry", "A space agency belongs to one primary country/region", "uniqueness", "SpaceAgencyOf", 1),
            LogicalRule("LandmarkUniqueness", "A landmark is located in one primary place", "uniqueness", "LandmarkLocatedIn", 1),
            LogicalRule("UniqueStateCapital", "An Indian state has one official capital", "uniqueness", "StateCapitalOf", 1),
            LogicalRule("UniqueUniversityLocation", "A university has one primary campus location", "uniqueness", "UniversityLocatedIn", 1),
            LogicalRule("UniqueCompanyHQ", "A company has one primary headquarters country", "uniqueness", "CompanyHeadquartersIn", 1),
        ]
