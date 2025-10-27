import xml.etree.ElementTree as ET
from models import models
from database import database

category_map = {
    "Retailers - supermarkets/hypermarkets": "grocery",
    "Retailers - other": "grocery",
    "Takeaway/sandwich shop": "restaurant",
    "Restaurant/Cafe/Canteen": "restaurant",
    "Mobile caterer": "restaurant",
    "Pub/bar/nightclub": "restaurant",
    "Butchers": "butcher",
    "Farmers/growers": "produce",
}

def load_fhrs_xml(xml_path: str):
    db = database.session_local()

    tree = ET.parse(xml_path)
    root = tree.getroot()

    count = 0

    # This finds ALL EstablishmentDetail elements in the entire XML tree
    for est in root.findall(".//EstablishmentDetail"):
        name = est.findtext("BusinessName")
        business_type_raw = est.findtext("BusinessType") or "Unknown"
        business_type = category_map.get(business_type_raw, "other")

        lat = est.findtext("Geocode/Latitude")
        lon = est.findtext("Geocode/Longitude")

        # Build full address string
        address_parts = [
            est.findtext("AddressLine1"),
            est.findtext("AddressLine2"),
            est.findtext("AddressLine3"),
            est.findtext("AddressLine4"),
            est.findtext("PostCode"),
        ]
        address = ", ".join([a for a in address_parts if a])

        if not lat or not lon:
            continue  # skip entries with no coordinates

        store = models.Store(
            name=name,
            type=business_type,
            region="Nottingham",
            latitude=float(lat),
            longitude=float(lon),
            address=address,
        )

        db.add(store)
        count += 1

    db.commit()
    db.close()
    print(f"Loaded {count} establishments into the database.")

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=database.engine)
    load_fhrs_xml("nottingham.xml")