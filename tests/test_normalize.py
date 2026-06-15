import unittest

from arb.config import CategoryConfig
from arb.models import Listing
from arb.normalize import build_identity_key, normalize


def _listing(title, **kw):
    base = dict(source="t", source_id="1", url="", title=title, current_bid=10.0)
    base.update(kw)
    return Listing(**base)


CAT = CategoryConfig(key="cards", sold_comp_window=10, min_comps=5)


class TestNormalize(unittest.TestCase):
    def test_extracts_grade_from_title(self):
        l = normalize(_listing("2018 Panini Prizm Luka Doncic #280 PSA 10"), CAT)
        self.assertEqual(l.grade_company, "PSA")
        self.assertEqual(l.grade, "10")

    def test_extracts_half_grade(self):
        l = normalize(_listing("2020 Prizm Herbert #325 BGS 9.5"), CAT)
        self.assertEqual(l.grade_company, "BGS")
        self.assertEqual(l.grade, "9.5")

    def test_extracts_year_and_card_number(self):
        l = normalize(_listing("2003 Topps Chrome LeBron #111 PSA 9"), CAT)
        self.assertEqual(l.year, "2003")
        self.assertEqual(l.card_number, "111")

    def test_identity_key_from_structured_fields(self):
        l = _listing("anything", year="2018", set_name="Panini Prizm",
                     player="Luka Doncic", card_number="280")
        self.assertEqual(build_identity_key(l), "2018|panini_prizm|luka_doncic|280")

    def test_identity_key_falls_back_to_title(self):
        l = _listing("2018 Panini Prizm Luka Doncic #280 PSA 10")
        # grade token removed, slugified
        key = build_identity_key(l)
        self.assertIn("luka_doncic", key)
        self.assertNotIn("psa", key)

    def test_category_assigned(self):
        l = normalize(_listing("2018 Prizm Luka #280 PSA 10"), CAT)
        self.assertEqual(l.category, "cards")


if __name__ == "__main__":
    unittest.main()
