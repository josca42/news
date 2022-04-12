from wikidataintegrator import wdi_core
import pandas as pd


def map_rdf_subject2wikidata_link(rdf_subjects: pd.Series) -> pd.Series:
    def get_wikidata_link(search_text):
        result = wdi_core.WDItemEngine.get_wd_search_results(search_text, max_results=1)
        return f"https://www.wikidata.org/wiki/{result[0]}" if result else None

    rdf_subject2wikidata_link = {
        search_text: get_wikidata_link(search_text)
        for search_text in rdf_subjects.unique()
    }
    return rdf_subjects.map(rdf_subject2wikidata_link)
