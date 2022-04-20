import whois
import pandas as pd
import googlemaps
import pickle
from news import config
from news.db import crud

gid2id = pickle.load(open(config["gis_dir"] / "gid2id.p", "rb"))

country_mappings = pd.read_csv(config["gis_dir"] / "domain2country.csv")
domain2country = {
    domain: country
    for idx, (domain, country) in country_mappings[
        ["TLD", "ISO3166-1-Alpha-3"]
    ].iterrows()
}
iso2_to_iso3 = {
    iso_2: iso_3
    for idx, (iso_2, iso_3) in country_mappings[
        ["ISO3166-1-Alpha-2", "ISO3166-1-Alpha-3"]
    ].iterrows()
}


def get_country_from_source_domain(source_domain):
    if source_domain is None:
        return None

    df = crud.domain.filter(filters=dict(source_domain=source_domain))

    if df.empty:
        country_id = add_source_domain2db(source_domain)
        return country_id
    else:
        country_id = df["country_id"].squeeze()
        country_id = int(country_id) if country_id else None
        return country_id


def add_source_domain2db(source_domain: str):
    country = get_country_from_cctld(source_domain)

    if country is None:
        country = get_country_from_who_is_lookup(source_domain)

    try:
        country_id = gid2id.get(country)
    except:
        print(country)
        country_id = None

    crud.domain.create(dict(source_domain=source_domain, country_id=country_id))

    return country_id


def get_country_from_cctld(source_domain):
    cctld = "." + source_domain.split(".")[-1]
    if cctld in domain2country:
        return domain2country[cctld]
    else:
        return None


def get_country_from_who_is_lookup(source_domain):
    country = None

    try:
        domain_info = whois.whois(source_domain)
    except:
        return None

    country = domain_info["country"] if "country" in domain_info else None
    if country:
        country = domain_info["country"]
        if type(country) == list:
            country = country[0]

        try:
            country = iso2_to_iso3[country]
        except:
            pass
    else:
        for key in domain_info.keys():
            if "address" in key:
                address = domain_info[key]
                if address is not None and address != "REDACTED FOR PRIVACY":
                    country = get_country_from_address(address)

    return country


def get_country_from_address(address):
    gmaps = googlemaps.Client(key=config["GOOGLE_API_KEY"])
    geo = gmaps.geocode(address)

    if geo:
        for addr_comp in geo[0]["address_components"]:
            if "country" in addr_comp["types"]:
                country = addr_comp["short_name"]
                country = iso2_to_iso3[country]
                return country

    return None
