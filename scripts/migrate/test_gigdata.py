"""Tests for the one-time live.md migration helpers.

Run: python3 -m unittest discover -s scripts/migrate -v
"""
import unittest
from datetime import date

from gigdata import (
    Gig,
    build_venues,
    gig_filename,
    gig_front_matter,
    parse_blocks,
    select_gigs,
    slugify,
    venue_yaml,
)

STANDARD = """+++
title = 'Live'
+++
<div class="live-events">

# Friday, July 10, 2026

6 pm - 9 pm ET

[Feathered Friend Brewery](https://www.featheredfriendbrewing.com/) \\
231 S Main Street \\
Concord, NH 03301 ([map](https://maps.app.goo.gl/ZumFMie1GaUm37VJ9))

# Wednesday, July 15, 2026

6:30 pm - 8 pm ET

[Canal Street Riverfront Park](https://www.concordnh.gov/1964/Canal-Street-Riverfront-Park/) \\
11 Canal Street \\
Penacook, NH 03303 ([map](https://maps.app.goo.gl/7uhx4DKSs8vnkKoeA))

</div>
"""

BR_VARIANT = """# Saturday, March 22, 2025

8 pm - 12 am ET

[Penuche's Ale House](https://www.facebook.com/penuches.concord/)<br>\\
16 Bicentennial Square<br>\\
Concord, NH ([map](https://maps.app.goo.gl/XkijJT2VbstW4yV49))
"""

PLAYHOUSE = """# Sunday, February 1, 2026

11 am - 12 pm ET (Doors: 10:30 am ET)

[Rock &amp; Roll Playhouse: Music of the Grateful Dead](https://www.ccanh.com/show/25000585) \\
Capitol Center for the Arts \\
Bank of New Hampshire Stage \\
16 S. Main Street \\
Concord, NH 03301 ([map](https://maps.app.goo.gl/UsCRTuYicBsv5tyn9))
"""


class ParseBlocksTest(unittest.TestCase):
    def test_standard_blocks(self):
        gigs = parse_blocks(STANDARD)
        self.assertEqual(len(gigs), 2)
        first = gigs[0]
        self.assertEqual(first.date, date(2026, 7, 10))
        self.assertEqual((first.start, first.end), ("6 pm", "9 pm"))
        self.assertEqual(first.venue_name, "Feathered Friend Brewery")
        self.assertEqual(first.venue_url, "https://www.featheredfriendbrewing.com/")
        self.assertEqual(first.street, "231 S Main Street")
        self.assertEqual((first.city, first.state, first.zip), ("Concord", "NH", "03301"))
        self.assertEqual(first.map_url, "https://maps.app.goo.gl/ZumFMie1GaUm37VJ9")
        self.assertEqual(first.notes, [])
        self.assertEqual(gigs[1].start, "6:30 pm")

    def test_br_tags_and_city_without_zip(self):
        (gig,) = parse_blocks(BR_VARIANT)
        self.assertEqual(gig.venue_name, "Penuche's Ale House")
        self.assertEqual(gig.street, "16 Bicentennial Square")
        self.assertEqual((gig.city, gig.state, gig.zip), ("Concord", "NH", ""))
        self.assertEqual(gig.end, "12 am")

    def test_doors_note_entities_and_extra_lines(self):
        (gig,) = parse_blocks(PLAYHOUSE)
        self.assertEqual(gig.venue_name, "Rock & Roll Playhouse: Music of the Grateful Dead")
        self.assertEqual(gig.street, "16 S. Main Street")
        self.assertEqual(
            gig.notes,
            ["Doors: 10:30 am ET", "Capitol Center for the Arts", "Bank of New Hampshire Stage"],
        )

    def test_skips_block_with_unparseable_date(self):
        text = "# Friday, Juuly 10, 2026\n\n6 pm - 9 pm ET\n\n# Friday, July 10, 2026\n\n7 pm - 9 pm ET\n"
        gigs = parse_blocks(text)
        self.assertEqual([(g.date, g.start) for g in gigs], [(date(2026, 7, 10), "7 pm")])


class SelectGigsTest(unittest.TestCase):
    def test_keeps_gigs_listed_on_their_day_and_drops_removed_ones(self):
        played = Gig(date=date(2025, 5, 1), venue_name="Old Name")
        played_v2 = Gig(date=date(2025, 5, 1), venue_name="New Name")
        cancelled = Gig(date=date(2025, 5, 10), venue_name="Gone")
        revisions = [  # chronological
            (date(2025, 4, 1), [played, cancelled]),
            (date(2025, 4, 20), [played_v2]),       # cancelled removed before its date
            (date(2025, 5, 15), []),                 # past shows cleaned up
        ]
        kept, dropped = select_gigs(revisions)
        self.assertEqual([g.venue_name for g in kept], ["New Name"])
        self.assertEqual([g.venue_name for g in dropped], ["Gone"])


class VenuesTest(unittest.TestCase):
    def test_groups_by_url_and_fills_fields_from_newest(self):
        old = Gig(date=date(2025, 1, 1), venue_name="Feather Friend Brewing",
                  venue_url="https://www.featheredfriendbrewing.com/", street="231 S Main Street",
                  city="Concord", state="NH", zip="03301")
        new = Gig(date=date(2026, 7, 10), venue_name="Feathered Friend Brewery",
                  venue_url="https://featheredfriendbrewing.com", map_url="https://maps.example/x")
        venues, gig_venue, names = build_venues([old, new])
        self.assertEqual(list(venues), ["feathered-friend-brewery"])
        v = venues["feathered-friend-brewery"]
        self.assertEqual(v["name"], "Feathered Friend Brewery")
        self.assertEqual(v["street"], "231 S Main Street")
        self.assertEqual(v["map_url"], "https://maps.example/x")
        self.assertEqual(gig_venue, {0: "feathered-friend-brewery", 1: "feathered-friend-brewery"})
        self.assertEqual(names["feathered-friend-brewery"],
                         {"Feather Friend Brewing", "Feathered Friend Brewery"})


class WritersTest(unittest.TestCase):
    def test_slugify_matches_pages_cms_style(self):
        self.assertEqual(slugify("Biederman's Deli"), "biedermans-deli")
        self.assertEqual(slugify("Rock & Roll"), "rock-and-roll")
        self.assertEqual(slugify("6:30 pm"), "6-30-pm")

    def test_gig_filename(self):
        gig = Gig(date=date(2026, 7, 15), start="6:30 pm")
        self.assertEqual(gig_filename(gig, "canal-street-riverfront-park"),
                         "2026-07-15-canal-street-riverfront-park-6-30-pm.md")

    def test_front_matter_quotes_text(self):
        gig = Gig(date=date(2026, 2, 1), start="11 am", end="12 pm",
                  notes=['Doors: 10:30 am ET', 'Say "hi"'])
        text = gig_front_matter(gig, "biedermans-deli", "/images/posters/2026-02-01.jpg")
        self.assertEqual(text, "\n".join([
            "+++",
            "date = 2026-02-01",
            'start = "11 am"',
            'end = "12 pm"',
            'venue = "biedermans-deli"',
            'poster = "/images/posters/2026-02-01.jpg"',
            'notes = "Doors: 10:30 am ET; Say \\"hi\\""',
            "cancelled = false",
            "+++",
            "",
        ]))

    def test_venue_yaml_keeps_zip_as_string(self):
        text = venue_yaml({"name": "Biederman's Deli", "zip": "03264"})
        self.assertEqual(text, 'name: "Biederman\'s Deli"\nzip: "03264"\n')


if __name__ == "__main__":
    unittest.main()
