# ======== FIXED CONSTANTS =========

# Provinces (short version, expand to 38 total provinces)
PROVINCES = [
    "aceh", "sumatera utara", "sumatera barat", "riau", "jambi",
    "sumatera selatan", "bengkulu", "lampung", "bangka belitung",
    "kepulauan riau", "dki jakarta", "jakarta", "jawa barat", "jawa tengah",
    "di yogyakarta", "jawa timur", "banten", "bali", "ntb", "ntt",
    "kalimantan barat", "kalimantan tengah", "kalimantan selatan",
    "kalimantan timur", "kalimantan utara", "sulawesi utara",
    "sulawesi tengah", "sulawesi selatan", "sulawesi tenggara",
    "gorontalo", "sulawesi barat", "maluku", "maluku utara",
    "papua", "papua barat", "papua tengah", "papua pegunungan",
    "papua selatan", "papua barat daya"
]

PROVINCE_ALIASES = {
    "jakarta": "dki jakarta",
    "dki": "dki jakarta",
    "yogyakarta": "di yogyakarta",
    "jogja": "di yogyakarta",
    "diy": "di yogyakarta",
    "sumut": "sumatera utara",
    "sumbar": "sumatera barat",
    "riau": "riau", # Keeping 'riau' for standardizing other variations
    "sumsel": "sumatera selatan",
    "bengkulu": "bengkulu",
    "babel": "bangka belitung",
    "kepri": "kepulauan riau",
    "jabar": "jawa barat",
    "jateng": "jawa tengah",
    "jatim": "jawa timur",
    "banten": "banten",
    "ntb": "ntb", # Keeping 'ntb' for consistency
    "nusa tenggara barat": "ntb",
    "ntt": "ntt", # Keeping 'ntt' for consistency
    "nusa tenggara timur": "ntt",
    "kalbar": "kalimantan barat",
    "kalteng": "kalimantan tengah",
    "kalsel": "kalimantan selatan",
    "kaltim": "kalimantan timur",
    "kaltara": "kalimantan utara",
    "sulut": "sulawesi utara",
    "sulteng": "sulawesi tengah",
    "sulsel": "sulawesi selatan",
    "sultra": "sulawesi tenggara",
    "gorontalo": "gorontalo",
    "sulbar": "sulawesi barat",
    "maluku": "maluku", # Keeping 'maluku' for consistency
    "malut": "maluku utara",
    "papua": "papua", # Keeping 'papua' for consistency
    "pabar": "papua barat",
    "papua tengah": "papua tengah",
    "papua pegunungan": "papua pegunungan",
    "papua selatan": "papua selatan",
    "papua barat daya": "papua barat daya",
}

CATEGORY_MAP = {
    # Existing Categories from Prompt Analysis
    "angka kelahiran": "birth_rate",
    "angka kematian": "mortality_rate",
    "pajak reklame": "reklame_tax",
    "pajak restoran": "restaurant_tax",
    "pajak rokok": "cigarette_tax",
    "pajak kendaraan bermotor": "motor_vehicle_tax",
    "retribusi sampah/kebersihan": "waste_retribution",
    "pajak hotel": "hotel_tax",
    "retribusi parkir": "parking_retribution",
    "limbah cair": "liquid_waste_regulation",
    "pajak penghasilan": "income_tax",
    "retribusi pasar": "market_retribution",
    "izin usaha": "business_license",
    "transportasi online": "online_transport_regulation",
    "tenaga kerja asing": "foreign_worker_regulation",
    "izin mendirikan bangunan (imb)": "building_permit_regulation",
    "uu no 28 tahun 2009": "law_28_2009_local_tax_retribution",
    "retribusi jalan tol": "toll_road_retribution",
    "pajak kendaraan listrik": "electric_vehicle_tax",
    "pajak karbon": "carbon_tax",
    "dana desa": "village_fund_regulation",
    "pajak hiburan": "entertainment_tax",
    "retribusi air": "water_retribution",
    "perizinan sumber daya alam (tambang, hutan, laut)": "natural_resource_permits",
    "pajak bumi dan bangunan (pbb)": "land_and_building_tax",
    "pajak cukai": "excise_tax",
    "perbedaan pajak dan retribusi": "tax_vs_retribution_difference",
    "prosedur npwp": "npwp_procedure",
    "jenis pajak indonesia": "types_of_tax_in_indonesia",
    "prosedur spt tahunan": "annual_tax_return_procedure",
    "ppn dan ppnbm": "vat_and_luxury_sales_tax",
    "pajak daerah dan retribusi daerah": "local_tax_and_retribution_definition",
    "pph 21": "pph_21_calculation",
    "pajak tontonan/bioskop": "cinema_tax",
    "pajak properti": "property_tax",
    "restitusi pajak": "tax_refund_procedure",
    "tarif pajak progresif": "progressive_tax_rate",
    "sanksi pajak kendaraan bermotor": "motor_vehicle_tax_sanction",
    "e-faktur": "e_invoicing_procedure",
    "umkm": "msme_tax_exemption",
    "pedagang online (e-commerce)": "e_commerce_tax_regulation",
    "dana hibah": "grant_taxation",
    "uu cipta kerja": "omnibus_law_tax_provisions",

    # New Categories from the provided list
    "administrasi, kearsipan, & tata naskah": "administration_archiving_and_script_management",
    "agraria, pertanahan, & tata ruang": "agrarian_land_affairs_and_spatial_planning",
    "anggaran pendapatan & belanja (apbn/apbd)": "state_regional_budget",
    "aset, utang, & hibah negara/daerah": "state_regional_assets_debt_and_grants",
    "badan layanan umum (blu)": "public_service_agencies_blu",
    "badan usaha milik negara & daerah (bumn/bumd)": "state_and_regional_owned_enterprises",
    "dasar & informasi hukum (jdih)": "legal_basis_and_information_network_jdih",
    "energi & sumber daya mineral": "energy_and_mineral_resources",
    "hak asasi manusia (ham)": "human_rights",
    "hak kekayaan intelektual (haki)": "intellectual_property_rights",
    "hubungan & kerjasama internasional": "international_relations_and_cooperation",
    "hukum (pidana, perdata, dagang)": "law_criminal_civil_commercial",
    "ilmu pengetahuan & teknologi": "science_and_technology",
    "informasi geospasial": "geospatial_information",
    "investasi & penanaman modal": "investment_and_capital_planting",
    "jabatan, profesi, & sertifikasi": "position_profession_and_certification",
    "jasa keuangan, pasar modal, & asuransi": "financial_services_capital_market_and_insurance",
    "keagamaan & penyelenggaraan haji": "religious_affairs_and_hajj_organization",
    "kelautan & perikanan": "marine_affairs_and_fisheries",
    "kepegawaian & aparatur negara": "personnel_and_state_apparatus",
    "kepemudaan & olah raga": "youth_and_sports",
    "kependudukan & keluarga": "population_and_family_affairs",
    "kepolisian": "police_affairs",
    "kerjasama pemerintah & badan usaha (kpbu)": "government_and_business_entity_cooperation_kpbu",
    "kesehatan & penanganan wabah": "health_and_epidemic_management",
    "kesejahteraan & penanggulangan bencana": "welfare_and_disaster_management",
    "ketatanegaraan & kebijakan publik": "constitutional_law_and_public_policy",
    "ketenagakerjaan & cipta kerja": "labor_and_omnibus_law",
    "keterbukaan informasi publik": "public_information_disclosure",
    "kewarganegaraan & imigrasi": "citizenship_and_immigration",
    "kode etik & protokoler": "code_of_ethics_and_protocol",
    "komunikasi, informatika, & siber": "communication_informatics_and_cyber",
    "konstruksi & infrastruktur": "construction_and_infrastructure",
    "koperasi & umkm": "cooperatives_and_msmes",
    "lingkungan hidup & kehutanan": "environment_and_forestry",
    "meteorologi, klimatologi, & geofisika": "meteorology_climatology_and_geophysics",
    "narkotika & terorisme": "narcotics_and_terrorism",
    "otonomi & pemerintahan daerah": "autonomy_and_local_government",
    "pajak & retribusi": "tax_and_retribution",
    "pakaian dinas": "official_uniforms",
    "pariwisata & kebudayaan": "tourism_and_culture",
    "pembangunan berkelanjutan (sdgs)": "sustainable_development_sdgs",
    "pembangunan ikn": "ikn_development",
    "pelayanan publik, perizinan, & pengaduan": "public_service_licensing_and_complaints",
    "pemerintahan desa": "village_government",
    "pemilu, partai politik, & kepala daerah": "election_political_parties_and_regional_heads",
    "pencegahan korupsi & gratifikasi": "corruption_and_gratification_prevention",
    "pendidikan & pelatihan": "education_and_training",
    "penerimaan negara bukan pajak (pnbp)": "non_tax_state_revenue_pnbp",
    "pengadaan barang/jasa": "procurement_of_goods_and_services",
    "pengawasan internal & audit": "internal_oversight_and_audit",
    "pengelolaan keuangan negara/daerah": "state_regional_financial_management",
    "pengelolaan sumber daya air": "water_resources_management",
    "penyelesaian kerugian negara/daerah": "settlement_of_state_regional_losses",
    "perdagangan internasional": "international_trade",
    "perekonomian & pembangunan ekonomi": "economy_and_economic_development",
    "perindustrian & perdagangan": "industry_and_trade",
    "pers, pos, & periklanan": "press_post_and_advertising",
    "persaingan usaha & perlindungan konsumen": "business_competition_and_consumer_protection",
    "pertahanan & keamanan": "defense_and_security",
    "pertanian, pangan, & peternakan": "agriculture_food_and_livestock",
    "perumahan & permukiman": "housing_and_settlement",
    "reformasi birokrasi": "bureaucracy_reform",
    "sistem peradilan & hukum acara": "judicial_system_and_procedural_law",
    "spbe & satu data indonesia": "spbe_and_one_data_indonesia",
    "standar biaya, gaji, dan honorarium": "cost_salary_and_honorarium_standards",
    "standar, pedoman, & proses bisnis": "standards_guidelines_and_business_processes",
    "struktur organisasi & kelembagaan negara": "state_organizational_and_institutional_structure",
    "transmigrasi & daerah tertinggal": "transmigration_and_underdeveloped_regions",
    "transportasi & lalu lintas": "transportation_and_traffic",
    "yayasan": "foundations"
} 


# Regex for years (1900–2100)
YEAR_REGEX = r"\b(19\d{2}|20\d{2}|2100)\b"


# Intent keywords (for fast detection)
INTENT_KEYWORDS = {
    "sql": 
    [
        "berapa", "jumlah", "persentase", "nilai", "angka", "tren", "total", 
        "tarif", "pasal", "perbedaan", "kesamaan", "isi", "definisi", "contoh"
    ],
    "rag": 
    [
        "aturan", "peraturan", "undang-undang", "uu", "kebijakan", "regulasi", 
        "ketentuan", "prosedur", "tata cara", "cara", "syarat", "apa", 
        "bagaimana", "adakah", "apakah", "jelaskan"
    ],
}


# --- Retrieval defaults ---
TOP_K = 5              # how many docs to retrieve in RAG
CHUNK_SIZE = 400       # tokens per chunk for legal text (RAG ingestion)
OVERLAP = 50           # overlap tokens to preserve context between chunks