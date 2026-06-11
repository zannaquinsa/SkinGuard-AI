from typing import Optional

HOSPITALS_JATIM = {
    # =========================
    # 9 KOTA DI JAWA TIMUR
    # =========================
    "kota batu": [
        {
            "name": "RSUD Karsa Husada Batu",
            "type": "Pemerintah",
            "address": "Jl. Ahmad Yani No.11, Kota Batu",
            "maps": "https://maps.google.com/?q=RSUD+Karsa+Husada+Batu",
        },
        {
            "name": "RS Baptis Batu",
            "type": "Swasta",
            "address": "Jl. Raya Tlekung No.1, Kota Batu",
            "maps": "https://maps.google.com/?q=RS+Baptis+Batu",
        },
    ],
    "kota blitar": [
        {
            "name": "RSUD Mardi Waluyo",
            "type": "Pemerintah",
            "address": "Jl. Kalimantan No.113, Kota Blitar",
            "maps": "https://maps.google.com/?q=RSUD+Mardi+Waluyo+Blitar",
        },
        {
            "name": "RS Syuhada Haji",
            "type": "Swasta",
            "address": "Jl. Tanjung No.100, Kota Blitar",
            "maps": "https://maps.google.com/?q=RS+Syuhada+Haji+Blitar",
        },
    ],
    "kota kediri": [
        {
            "name": "RSUD Gambiran",
            "type": "Pemerintah",
            "address": "Jl. Kapten Pierre Tendean No.16, Kota Kediri",
            "maps": "https://maps.google.com/?q=RSUD+Gambiran+Kediri",
        },
        {
            "name": "RS Bhayangkara Kediri",
            "type": "Swasta",
            "address": "Jl. PB Sudirman No.99, Kota Kediri",
            "maps": "https://maps.google.com/?q=RS+Bhayangkara+Kediri",
        },
    ],
    "kota madiun": [
        {
            "name": "RSUD dr. Soedono",
            "type": "Pemerintah",
            "address": "Jl. Dr. Soetomo No.59, Kota Madiun",
            "maps": "https://maps.google.com/?q=RSUD+dr+Soedono+Madiun",
        },
        {
            "name": "RS Santa Clara",
            "type": "Swasta",
            "address": "Jl. Biliton No.15, Kota Madiun",
            "maps": "https://maps.google.com/?q=RS+Santa+Clara+Madiun",
        },
    ],
    "kota malang": [
        {
            "name": "RSUD Dr. Saiful Anwar",
            "type": "Pemerintah",
            "address": "Jl. Jaksa Agung Suprapto No.2, Kota Malang",
            "maps": "https://maps.google.com/?q=RSUD+Dr+Saiful+Anwar+Malang",
        },
        {
            "name": "RS Lavalette",
            "type": "Swasta",
            "address": "Jl. WR Supratman No.10, Kota Malang",
            "maps": "https://maps.google.com/?q=RS+Lavalette+Malang",
        },
    ],
    "kota mojokerto": [
        {
            "name": "RSUD Dr. Wahidin Sudiro Husodo",
            "type": "Pemerintah",
            "address": "Jl. Raya Surodinawan No.90, Kota Mojokerto",
            "maps": "https://maps.google.com/?q=RSUD+Wahidin+Sudiro+Husodo",
        },
        {
            "name": "RS Gatoel",
            "type": "Swasta",
            "address": "Jl. Raden Wijaya No.56, Kota Mojokerto",
            "maps": "https://maps.google.com/?q=RS+Gatoel+Mojokerto",
        },
    ],
    "kota pasuruan": [
        {
            "name": "RSUD R. Soedarsono",
            "type": "Pemerintah",
            "address": "Jl. DR Soetomo No.46, Kota Pasuruan",
            "maps": "https://maps.google.com/?q=RSUD+R+Soedarsono+Pasuruan",
        },
        {
            "name": "RS Graha Sehat Medika",
            "type": "Swasta",
            "address": "Jl. KH Ahmad Dahlan No.29, Kota Pasuruan",
            "maps": "https://maps.google.com/?q=RS+Graha+Sehat+Medika+Pasuruan",
        },
    ],
    "kota probolinggo": [
        {
            "name": "RSUD dr. Mohamad Saleh",
            "type": "Pemerintah",
            "address": "Jl. Mayjen Panjaitan No.65, Kota Probolinggo",
            "maps": "https://maps.google.com/?q=RSUD+dr+Mohamad+Saleh",
        },
        {
            "name": "RS Dharma Husada",
            "type": "Swasta",
            "address": "Jl. Raya Panglima Sudirman, Kota Probolinggo",
            "maps": "https://maps.google.com/?q=RS+Dharma+Husada+Probolinggo",
        },
    ],
    "kota surabaya": [
        {
            "name": "RSUD Dr. Soetomo",
            "type": "Pemerintah",
            "address": "Jl. Mayjen Prof. Dr. Moestopo No.6-8, Surabaya",
            "maps": "https://maps.google.com/?q=RSUD+Dr+Soetomo+Surabaya",
        },
        {
            "name": "RS Siloam Hospitals Surabaya",
            "type": "Swasta",
            "address": "Jl. Raya Gubeng No.70, Surabaya",
            "maps": "https://maps.google.com/?q=RS+Siloam+Hospitals+Surabaya",
        },
    ],
    # =========================
    # 29 KABUPATEN DI JAWA TIMUR
    # =========================
    "bangkalan": [
        {
            "name": "RSUD Syamrabu Bangkalan",
            "type": "Pemerintah",
            "address": "Jl. Pemuda Kaffa No.9, Bangkalan",
            "maps": "https://maps.google.com/?q=RSUD+Syamrabu+Bangkalan",
        },
        {
            "name": "RS Khusus Bedah Bangkalan",
            "type": "Swasta",
            "address": "Jl. Soekarno Hatta, Bangkalan",
            "maps": "https://maps.google.com/?q=RS+Khusus+Bedah+Bangkalan",
        },
    ],
    "banyuwangi": [
        {
            "name": "RSUD Blambangan",
            "type": "Pemerintah",
            "address": "Jl. Letkol Istiqlah No.49, Banyuwangi",
            "maps": "https://maps.google.com/?q=RSUD+Blambangan",
        },
        {
            "name": "RS Islam Fatimah Banyuwangi",
            "type": "Swasta",
            "address": "Jl. KH Agus Salim No.2, Banyuwangi",
            "maps": "https://maps.google.com/?q=RS+Islam+Fatimah+Banyuwangi",
        },
    ],
    "blitar": [
        {
            "name": "RSUD Ngudi Waluyo Wlingi",
            "type": "Pemerintah",
            "address": "Jl. Raya Sutojayan, Blitar",
            "maps": "https://maps.google.com/?q=RSUD+Ngudi+Waluyo+Wlingi",
        },
        {
            "name": "RS Medika Utama",
            "type": "Swasta",
            "address": "Jl. TGP No.12, Blitar",
            "maps": "https://maps.google.com/?q=RS+Medika+Utama+Blitar",
        },
    ],
    "bojonegoro": [
        {
            "name": "RSUD Dr. R. Sosodoro Djatikoesoemo",
            "type": "Pemerintah",
            "address": "Jl. Dr. Wahidin No.40, Bojonegoro",
            "maps": "https://maps.google.com/?q=RSUD+Sosodoro+Djatikoesoemo",
        },
        {
            "name": "RS Aisyiyah Bojonegoro",
            "type": "Swasta",
            "address": "Jl. Panglima Polim No.24, Bojonegoro",
            "maps": "https://maps.google.com/?q=RS+Aisyiyah+Bojonegoro",
        },
    ],
    "bondowoso": [
        {
            "name": "RSUD Dr. H. Koesnadi",
            "type": "Pemerintah",
            "address": "Jl. Kapten Piere Tendean No.3, Bondowoso",
            "maps": "https://maps.google.com/?q=RSUD+Koesnadi+Bondowoso",
        },
        {
            "name": "RS Mitra Medika",
            "type": "Swasta",
            "address": "Jl. Ahmad Yani No.5, Bondowoso",
            "maps": "https://maps.google.com/?q=RS+Mitra+Medika+Bondowoso",
        },
    ],
    "gresik": [
        {
            "name": "RSUD Ibnu Sina Gresik",
            "type": "Pemerintah",
            "address": "Jl. Dr. Wahidin Sudiro Husodo No.243, Gresik",
            "maps": "https://maps.google.com/?q=RSUD+Ibnu+Sina+Gresik",
        },
        {
            "name": "RS Petrokimia Gresik",
            "type": "Swasta",
            "address": "Jl. Jenderal Ahmad Yani No.69, Gresik",
            "maps": "https://maps.google.com/?q=RS+Petrokimia+Gresik",
        },
    ],
    "jember": [
        {
            "name": "RSUD Dr. Soebandi",
            "type": "Pemerintah",
            "address": "Jl. Dr. Soebandi No.124, Jember",
            "maps": "https://maps.google.com/?q=RSUD+Dr+Soebandi+Jember",
        },
        {
            "name": "RS Bina Sehat",
            "type": "Swasta",
            "address": "Jl. Pangandaran No.18, Jember",
            "maps": "https://maps.google.com/?q=RS+Bina+Sehat+Jember",
        },
    ],
    "jombang": [
        {
            "name": "RSUD Jombang",
            "type": "Pemerintah",
            "address": "Jl. KH Wahid Hasyim No.52, Jombang",
            "maps": "https://maps.google.com/?q=RSUD+Jombang",
        },
        {
            "name": "RS Airlangga Jombang",
            "type": "Swasta",
            "address": "Jl. Dr. Sutomo No.26, Jombang",
            "maps": "https://maps.google.com/?q=RS+Airlangga+Jombang",
        },
    ],
    "kediri": [
        {
            "name": "RSUD Pare Kediri",
            "type": "Pemerintah",
            "address": "Jl. Pahlawan Kusuma Bangsa, Kediri",
            "maps": "https://maps.google.com/?q=RSUD+Pare+Kediri",
        },
        {
            "name": "RS Aura Syifa Kediri",
            "type": "Swasta",
            "address": "Jl. Raya Kandangan No.5, Kediri",
            "maps": "https://maps.google.com/?q=RS+Aura+Syifa+Kediri",
        },
    ],
    "lamongan": [
        {
            "name": "RSUD dr. Soegiri Lamongan",
            "type": "Pemerintah",
            "address": "Jl. Kusuma Bangsa No.7, Lamongan",
            "maps": "https://maps.google.com/?q=RSUD+dr+Soegiri+Lamongan",
        },
        {
            "name": "RS Muhammadiyah Lamongan",
            "type": "Swasta",
            "address": "Jl. Jaksa Agung Suprapto No.76, Lamongan",
            "maps": "https://maps.google.com/?q=RS+Muhammadiyah+Lamongan",
        },
    ],
    "lumajang": [
        {
            "name": "RSUD dr. Haryoto Lumajang",
            "type": "Pemerintah",
            "address": "Jl. A. Yani No.281, Lumajang",
            "maps": "https://maps.google.com/?q=RSUD+dr+Haryoto+Lumajang",
        },
        {
            "name": "RS Bhayangkara Lumajang",
            "type": "Swasta",
            "address": "Jl. Jend. Sudirman No.49, Lumajang",
            "maps": "https://maps.google.com/?q=RS+Bhayangkara+Lumajang",
        },
    ],
    "madiun": [
        {
            "name": "RSUD Caruban Madiun",
            "type": "Pemerintah",
            "address": "Jl. Raya Caruban, Madiun",
            "maps": "https://maps.google.com/?q=RSUD+Caruban+Madiun",
        },
        {
            "name": "RS Islam Siti Aisyah Madiun",
            "type": "Swasta",
            "address": "Jl. Mayjend Panjaitan No.25, Madiun",
            "maps": "https://maps.google.com/?q=RS+Islam+Siti+Aisyah+Madiun",
        },
    ],
    "magetan": [
        {
            "name": "RSUD dr. Sayidiman Magetan",
            "type": "Pemerintah",
            "address": "Jl. Basuki Rahmat No.2, Magetan",
            "maps": "https://maps.google.com/?q=RSUD+dr+Sayidiman+Magetan",
        },
        {
            "name": "RS Paru Dungus Madiun",
            "type": "Pemerintah",
            "address": "Jl. Raya Dungus, Magetan",
            "maps": "https://maps.google.com/?q=RS+Paru+Dungus+Madiun",
        },
    ],
    "malang": [
        {
            "name": "RSUD Kanjuruhan Kepanjen",
            "type": "Pemerintah",
            "address": "Jl. Panji No.100, Kepanjen, Malang",
            "maps": "https://maps.google.com/?q=RSUD+Kanjuruhan+Kepanjen",
        },
        {
            "name": "RS Ben Mari Malang",
            "type": "Swasta",
            "address": "Jl. Raya Kebonagung No.2, Malang",
            "maps": "https://maps.google.com/?q=RS+Ben+Mari+Malang",
        },
    ],
    "mojokerto": [
        {
            "name": "RSUD RA Basoeni Mojokerto",
            "type": "Pemerintah",
            "address": "Jl. Raya Gedeg, Mojokerto",
            "maps": "https://maps.google.com/?q=RSUD+RA+Basoeni+Mojokerto",
        },
        {
            "name": "RS Reksa Waluya Mojokerto",
            "type": "Swasta",
            "address": "Jl. RA Basoeni, Mojokerto",
            "maps": "https://maps.google.com/?q=RS+Reksa+Waluya+Mojokerto",
        },
    ],
    "nganjuk": [
        {
            "name": "RSUD Nganjuk",
            "type": "Pemerintah",
            "address": "Jl. Ahmad Yani No.2, Nganjuk",
            "maps": "https://maps.google.com/?q=RSUD+Nganjuk",
        },
        {
            "name": "RS Islam Nganjuk",
            "type": "Swasta",
            "address": "Jl. Dermojoyo, Nganjuk",
            "maps": "https://maps.google.com/?q=RS+Islam+Nganjuk",
        },
    ],
    "ngawi": [
        {
            "name": "RSUD dr. Soeroto Ngawi",
            "type": "Pemerintah",
            "address": "Jl. Ahmad Yani No.36, Ngawi",
            "maps": "https://maps.google.com/?q=RSUD+dr+Soeroto+Ngawi",
        },
        {
            "name": "RS PKU Muhammadiyah Ngawi",
            "type": "Swasta",
            "address": "Jl. A. Yani No.8, Ngawi",
            "maps": "https://maps.google.com/?q=RS+PKU+Muhammadiyah+Ngawi",
        },
    ],
    "pacitan": [
        {
            "name": "RSUD dr. Darsono Pacitan",
            "type": "Pemerintah",
            "address": "Jl. Letjen Suprapto No.42, Pacitan",
            "maps": "https://maps.google.com/?q=RSUD+dr+Darsono+Pacitan",
        },
        {
            "name": "RS Graha Husada Pacitan",
            "type": "Swasta",
            "address": "Jl. Jend. Ahmad Yani, Pacitan",
            "maps": "https://maps.google.com/?q=RS+Graha+Husada+Pacitan",
        },
    ],
    "pamekasan": [
        {
            "name": "RSUD dr. H. Slamet Martodirdjo",
            "type": "Pemerintah",
            "address": "Jl. Raya Panglegur, Pamekasan",
            "maps": "https://maps.google.com/?q=RSUD+Slamet+Martodirdjo+Pamekasan",
        },
        {
            "name": "RS Nahdlatul Ulama Pamekasan",
            "type": "Swasta",
            "address": "Jl. Kabupaten No.48, Pamekasan",
            "maps": "https://maps.google.com/?q=RS+Nahdlatul+Ulama+Pamekasan",
        },
    ],
    "pasuruan": [
        {
            "name": "RSUD Bangil Pasuruan",
            "type": "Pemerintah",
            "address": "Jl. Raci Bangil, Pasuruan",
            "maps": "https://maps.google.com/?q=RSUD+Bangil+Pasuruan",
        },
        {
            "name": "RS Prima Husada Pasuruan",
            "type": "Swasta",
            "address": "Jl. Raya Pandaan, Pasuruan",
            "maps": "https://maps.google.com/?q=RS+Prima+Husada+Pasuruan",
        },
    ],
    "ponorogo": [
        {
            "name": "RSUD dr. Harjono Ponorogo",
            "type": "Pemerintah",
            "address": "Jl. Raya Ponorogo - Madiun, Ponorogo",
            "maps": "https://maps.google.com/?q=RSUD+dr+Harjono+Ponorogo",
        },
        {
            "name": "RS Aisyiyah Ponorogo",
            "type": "Swasta",
            "address": "Jl. Dr. Sutomo No.17, Ponorogo",
            "maps": "https://maps.google.com/?q=RS+Aisyiyah+Ponorogo",
        },
    ],
    "probolinggo": [
        {
            "name": "RSUD Waluyo Jati Kraksaan",
            "type": "Pemerintah",
            "address": "Jl. Raya Dringu, Kraksaan, Probolinggo",
            "maps": "https://maps.google.com/?q=RSUD+Waluyo+Jati+Kraksaan",
        },
        {
            "name": "RS Wonolangan Probolinggo",
            "type": "Swasta",
            "address": "Jl. Raya Wonolangan, Probolinggo",
            "maps": "https://maps.google.com/?q=RS+Wonolangan+Probolinggo",
        },
    ],
    "sampang": [
        {
            "name": "RSUD Sampang",
            "type": "Pemerintah",
            "address": "Jl. Rajawali No.10, Sampang",
            "maps": "https://maps.google.com/?q=RSUD+Sampang",
        },
        {
            "name": "RS Aisyiyah Sampang",
            "type": "Swasta",
            "address": "Jl. Jaksa Agung Suprapto, Sampang",
            "maps": "https://maps.google.com/?q=RS+Aisyiyah+Sampang",
        },
    ],
    "sidoarjo": [
        {
            "name": "RSUD Sidoarjo",
            "type": "Pemerintah",
            "address": "Jl. Mojopahit No.667, Sidoarjo",
            "maps": "https://maps.google.com/?q=RSUD+Sidoarjo",
        },
        {
            "name": "RS Mitra Keluarga Waru",
            "type": "Swasta",
            "address": "Jl. Raya Waru No.1, Sidoarjo",
            "maps": "https://maps.google.com/?q=RS+Mitra+Keluarga+Waru",
        },
    ],
    "situbondo": [
        {
            "name": "RSUD Abdoer Rahem Situbondo",
            "type": "Pemerintah",
            "address": "Jl. Anggrek No.68, Situbondo",
            "maps": "https://maps.google.com/?q=RSUD+Abdoer+Rahem+Situbondo",
        },
        {
            "name": "RS Elizabeth Situbondo",
            "type": "Swasta",
            "address": "Jl. Basuki Rahmat No.5, Situbondo",
            "maps": "https://maps.google.com/?q=RS+Elizabeth+Situbondo",
        },
    ],
    "sumenep": [
        {
            "name": "RSUD dr. H. Moh. Anwar Sumenep",
            "type": "Pemerintah",
            "address": "Jl. Dr. Cipto No.42, Sumenep",
            "maps": "https://maps.google.com/?q=RSUD+dr+H+Moh+Anwar+Sumenep",
        },
        {
            "name": "RS Asy-Syifa Sumenep",
            "type": "Swasta",
            "address": "Jl. Raya Lenteng, Sumenep",
            "maps": "https://maps.google.com/?q=RS+Asy+Syifa+Sumenep",
        },
    ],
    "trenggalek": [
        {
            "name": "RSUD dr. Soedomo Trenggalek",
            "type": "Pemerintah",
            "address": "Jl. Dr. Soetomo No.5, Trenggalek",
            "maps": "https://maps.google.com/?q=RSUD+dr+Soedomo+Trenggalek",
        },
        {
            "name": "RS Nahdlatul Ulama Trenggalek",
            "type": "Swasta",
            "address": "Jl. Soekarno Hatta, Trenggalek",
            "maps": "https://maps.google.com/?q=RS+Nahdlatul+Ulama+Trenggalek",
        },
    ],
    "tuban": [
        {
            "name": "RSUD dr. R. Koesma Tuban",
            "type": "Pemerintah",
            "address": "Jl. Dr. Wahidin Sudiro Husodo No.800, Tuban",
            "maps": "https://maps.google.com/?q=RSUD+dr+R+Koesma+Tuban",
        },
        {
            "name": "RS Islam Fatimah Tuban",
            "type": "Swasta",
            "address": "Jl. Basuki Rahmat No.4, Tuban",
            "maps": "https://maps.google.com/?q=RS+Islam+Fatimah+Tuban",
        },
    ],
    "tulungagung": [
        {
            "name": "RSUD dr. Iskak Tulungagung",
            "type": "Pemerintah",
            "address": "Jl. Dr. Wahidin Sudiro Husodo No.1, Tulungagung",
            "maps": "https://maps.google.com/?q=RSUD+dr+Iskak+Tulungagung",
        },
        {
            "name": "RS Bhayangkara Tulungagung",
            "type": "Swasta",
            "address": "Jl. Ahmad Yani, Tulungagung",
            "maps": "https://maps.google.com/?q=RS+Bhayangkara+Tulungagung",
        },
    ],
}


def get_hospitals_by_city(city: str) -> list[dict]:
    """Return hospitals for a specific city (case-insensitive lookup)."""
    key = city.strip().lower()
    return HOSPITALS_JATIM.get(key, [])


def get_all_cities() -> list[str]:
    """Return sorted list of all available city keys."""
    return sorted(HOSPITALS_JATIM.keys())


def get_all_hospitals(
    city: Optional[str] = None,
    hospital_type: Optional[str] = None,
) -> list[dict]:
    """
    Return all hospitals, optionally filtered by city and/or type.

    Args:
        city: City name (case-insensitive). If None, returns all cities.
        hospital_type: 'Pemerintah' or 'Swasta'. If None, returns all types.
    """
    if city:
        hospitals = get_hospitals_by_city(city)
        result = [{"city": city.strip().lower(), **h} for h in hospitals]
    else:
        result = []
        for city_key, hospital_list in HOSPITALS_JATIM.items():
            for h in hospital_list:
                result.append({"city": city_key, **h})

    if hospital_type:
        result = [h for h in result if h.get("type", "").lower() == hospital_type.lower()]

    return result
