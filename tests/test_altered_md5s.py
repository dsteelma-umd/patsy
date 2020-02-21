import patsy.database
from sqlalchemy import create_engine
from patsy.model import Base
from patsy.perfect_matches import find_perfect_matches
from patsy.altered_md5_matches import find_altered_md5_matches
import unittest
from patsy.model import Accession
from .utils import AccessionBuilder, RestoreBuilder, create_perfect_match

Session = patsy.database.Session


class TestAlteredMd5sMatches(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)

    def test_no_altered_md5_match(self):
        session = Session()

        accession = AccessionBuilder().build()
        restore = RestoreBuilder().build()

        session.add(accession)
        session.add(restore)
        session.commit()

        # Verify that MD5 checksums and filenames are not equal
        self.assertNotEqual(accession.md5, restore.md5)
        self.assertNotEqual(accession.filename, restore.filename)

        accessions = session.query(Accession)
        new_matches_found = find_altered_md5_matches(session, accessions)

        # No perfect match should be found
        self.assertEqual(0, len(new_matches_found))
        self.assertEqual(0, len(accession.altered_md5_matches))
        self.assertEqual(0, len(restore.altered_md5_matches))

    def test_one_altered_md5_match(self):
        session = Session()

        accession = AccessionBuilder().build()
        restore = create_perfect_match(accession)
        restore.md5 = 'altered_md5'

        session.add(accession)
        session.add(restore)
        session.commit()

        self.assertEqual(0, len(accession.altered_md5_matches))

        accessions = session.query(Accession)
        new_matches_found = find_altered_md5_matches(session, accessions)

        self.assertEqual(1, len(new_matches_found))
        self.assertEqual(1, len(accession.altered_md5_matches))
        self.assertEqual(1, len(restore.altered_md5_matches))

    def test_multiple_altered_md_matches_to_one_accession(self):
        session = Session()

        accession = AccessionBuilder().build()
        restore1 = create_perfect_match(accession)
        restore1.md5 = 'altered_md5_1'
        restore2 = create_perfect_match(accession)
        restore2.md5 = 'altered_md5_2'

        session.add(accession)
        session.add(restore1)
        session.add(restore2)
        session.commit()

        accessions = session.query(Accession)
        new_matches_found = find_altered_md5_matches(session, accessions)

        self.assertEqual(2, len(new_matches_found))
        self.assertEqual(2, len(accession.altered_md5_matches))
        self.assertEqual(1, len(restore1.altered_md5_matches))
        self.assertEqual(accession, restore1.altered_md5_matches[0])
        self.assertEqual(1, len(restore2.altered_md5_matches))
        self.assertEqual(accession, restore2.altered_md5_matches[0])

    def test_accession_with_perfect_match_and_altered_md5_match(self):
        session = Session()

        accession = AccessionBuilder().build()
        perfect_restore = create_perfect_match(accession)
        altered_restore = create_perfect_match(accession)
        altered_restore.md5 = 'altered_md5'

        session.add(accession)
        session.add(perfect_restore)
        session.add(altered_restore)
        session.commit()

        accessions = session.query(Accession)
        perfect_matches_found = find_perfect_matches(session, accessions)
        altered_md5_matches_found = find_altered_md5_matches(session, accessions)
        self.assertEqual(1, len(perfect_matches_found))
        self.assertEqual(1, len(altered_md5_matches_found))
        self.assertEqual(perfect_restore, accession.perfect_matches[0])
        self.assertEqual(altered_restore, accession.altered_md5_matches[0])

    def test_altered_md5_match_does_not_include_perfect_match(self):
        # In this test, we are running find_altered_md5_matches without first
        # running find_perfect_matches, to ensure a perfect match is not added
        # to the altered md5 matches
        session = Session()

        accession = AccessionBuilder().build()
        perfect_restore = create_perfect_match(accession)
        altered_restore = create_perfect_match(accession)
        altered_restore.md5 = 'altered_md5'

        session.add(accession)
        session.add(perfect_restore)
        session.add(altered_restore)
        session.commit()

        accessions = session.query(Accession)
        altered_md5_matches_found = find_altered_md5_matches(session, accessions)
        self.assertEqual(0, len(accession.perfect_matches))

        self.assertEqual(1, len(altered_md5_matches_found))
        self.assertEqual(altered_restore, accession.altered_md5_matches[0])

    def test_same_filename_but_different_md5_and_bytes(self):
        session = Session()

        accession = AccessionBuilder().build()
        restore = create_perfect_match(accession)
        restore.md5 = 'altered_md5'
        restore.bytes = restore.bytes + 100
        session.add(accession)
        session.add(restore)
        session.commit()

        # Verify that filenames are the same, but MD5 and bytes differ
        self.assertEqual(accession.filename, restore.filename)
        self.assertNotEqual(accession.md5, restore.md5)
        self.assertNotEqual(accession.bytes, restore.bytes)

        accessions = session.query(Accession)
        new_matches_found = find_altered_md5_matches(session, accessions)

        self.assertEqual(0, len(new_matches_found))
        self.assertEqual(0, len(accession.altered_md5_matches))
        self.assertEqual(0, len(restore.altered_md5_matches))

    def test_same_bytes_but_different_filename_and_md5(self):
        session = Session()

        accession = AccessionBuilder().build()
        restore = create_perfect_match(accession)
        restore.md5 = 'altered_md5'
        restore.filename = 'altered_filename'
        session.add(accession)
        session.add(restore)
        session.commit()

        # Verify that bytes are the same, but MD5 and filenames differ
        self.assertEqual(accession.bytes, restore.bytes)
        self.assertNotEqual(accession.filename, restore.filename)
        self.assertNotEqual(accession.md5, restore.md5)

        accessions = session.query(Accession)
        new_matches_found = find_altered_md5_matches(session, accessions)

        self.assertEqual(0, len(new_matches_found))
        self.assertEqual(0, len(accession.altered_md5_matches))
        self.assertEqual(0, len(restore.altered_md5_matches))

    def test_finding_altered_md5_matches_more_than_once(self):
        session = Session()

        accession = AccessionBuilder().build()
        restore = create_perfect_match(accession)
        restore.md5 = 'altered_md5'

        session.add(accession)
        session.add(restore)
        session.commit()

        accessions = session.query(Accession)
        new_matches_found = find_altered_md5_matches(session, accessions)

        self.assertEqual(1, len(new_matches_found))
        self.assertEqual(1, len(accession.altered_md5_matches))
        self.assertEqual(1, len(restore.altered_md5_matches))

        accessions = session.query(Accession)
        new_matches_found = find_altered_md5_matches(session, accessions)
        self.assertEqual(0, len(new_matches_found))
        self.assertEqual(1, len(accession.altered_md5_matches))
        self.assertEqual(1, len(restore.altered_md5_matches))