import requests
SPECIES = {
    "1": ("Humpback Whale", "Megaptera novaeangliae"),
    "2": ("Blue Whale", "Balaenoptera musculus"),
    "3": ("Sperm Whale", "Physeter macrocephalus"),
    "4": ("Fin Whale", "Balaenoptera physalus"),
    "5": ("Gray Whale", "Eschrichtius robustus")
}

print("=== Whale Tracking Dashboard ===")
for k, (n, s) in SPECIES.items():
    print(f" {k}. {n}")
c = input("Pick (1-5): ").strip()
cn, sci = SPECIES.get(c, ("Humpback Whale", "Megaptera novaeangliae"))
genus, sp = sci.split()

# MODULE 1 - OBIS
print("MODULE 1 - OBIS TRACKER")
try:
    r1 = requests.get("https://api.obis.org/v3/occurrence",
                      params={"scientificname": sci, "size": 10, "hasCoordinate":"true"})
    r1.raise_for_status()
    for s in r1.json().get("results", []):
        print(f"{s.get('decimalLatitude')}, {s.get('decimalLongitude')}")
        print(f"{s.get('eventDate','N/A')} {s.get('depth','N/A')}m")
except Exception as e:
    print(f"Error fetching OBIS data: {e}")
    
# Module 2 - iNaturalist
print("Module 2 - iNATURALIST SPECIES CARD")
try:
    r2  = requests.get("https://api.inaturalist.org/v1/taxa",
                       params={"q": cn, "per_page": 1})
    r2.raise_for_status()
    if (taxa := r2.json().get("results", [])):
        t = taxa[0]
        cs = (t.get('conservation_status') or {}).get('status_name', 'Unknown')
        print(f"SPECIES: {t.get('name')} ({t.get('preferred_common_name', 'N/A')})")
        print(f"Observations: {t.get('observations_count', 0)}")
        print(f"Conservation Status: {cs}")
        print(f"Wikipedia: https://en.wikipedia.org/wiki/{sci.replace(' ', '_')}")
        print(f"photo: {t.get('default_photo', {}).get('medium')}")
except Exception as e:
    print(f"Error fetching iNaturalist data: {e}")

# Module 3 - Wikipedia
print("MODULE 3 - WIKIPEDIA SUMMARY")

# Module 4 - SeaLifeBase
print("MODULE 4 - SEALIFEBASE INFO")
try:
    r4 = requests.get(f"https://www.sealifebase.ca/api.php?genus={genus}&species={sp}")
    r4.raise_for_status()
    if (data := r4.json().get('data')):
        b = data[0]
        print(f"Length: {b.get('Length', 'N/A')} in")
        print(f"Weight: {b.get('Weight', 'N/A')} lb")
        print(f"Habitat: {b.get('Habitat', 'N/A')}")
        print(f"Longevity: {b.get('Longevity', 'N/A')} years")
        print(f" IUCN: {b.get('IUCN_Code', 'N/A')}")
    else:
        print("No SeaLifeBase data found")
except Exception as e:
    print(f"Error fetching SeaLifeBase data: {e}")
        
print("=== Dashboard complete ===")

from urllib.parse import quote_plus

def learning_links(common_name, sci_name):
    print("\nLEARNING RESOURCES:")
    print(f"1. Wikipedia: https://en.wikipedia.org/wiki/{quote_plus(sci_name)}")
    print(f"2. iNaturalist: https://www.inaturalist.org/taxa?query={quote_plus(common_name)}")
    print(f"3. OBIS: https://obis.org/taxon/{quote_plus(sci_name)}")
    print(f"4. SeaLifeBase: https://www.sealifebase.ca/summary/{quote_plus(sci_name)}.html")

learning_links(cn, sci)
