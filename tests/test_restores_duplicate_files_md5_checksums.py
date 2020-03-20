import patsy.database
from patsy.restore import RestoreCsvLoader
from sqlalchemy import create_engine
from patsy.model import Base
import unittest
from patsy.model import Restore
from patsy.restores_duplicate_files_md5_checksums import check_md5s
from .utils import RestoreBuilder

Session = patsy.database.Session


class TestRestore(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)

    def test_check_md5s_no_record(self):
        session = Session()

        filename = "filename_does_not_exist"
        result = check_md5s(session, filename)
        self.assertEqual(f"ERROR - '#{filename} not found in restores table.", result)

    def test_check_md5s_one_record(self):
        session = Session()

        filename = "filename_one_restore"
        restore = RestoreBuilder().set_filename(filename).build()
        session.add(restore)
        session.commit()

        result = check_md5s(session, filename)
        self.assertEqual(f"ERROR - '#{filename} occurs only once.", result)

    def test_check_md5s_two_records_same_md5(self):
        session = Session()

        filename = "filename_restore"
        md5 = "SAMPLE_MD5"
        restore1 = RestoreBuilder().set_filename(filename).set_filepath(f"path1/#{filename}").set_md5(md5).build()
        restore2 = RestoreBuilder().set_filename(filename).set_filepath(f"path2/#{filename}").set_md5(md5).build()
        session.add(restore1)
        session.add(restore2)
        session.commit()

        result = check_md5s(session, filename)
        self.assertEqual(f"No MD5 mismatch for {filename}", result)

    def test_check_md5s_two_records_different_md5(self):
        session = Session()

        filename = "filename_restore"
        md5_1 = "SAMPLE_MD5"
        md5_2= "DIFFERENT_MD5"
        restore1 = RestoreBuilder().set_filename(filename).set_filepath(f"path1/#{filename}").set_md5(md5_1).build()
        restore2 = RestoreBuilder().set_filename(filename).set_filepath(f"path2/#{filename}").set_md5(md5_2).build()
        session.add(restore1)
        session.add(restore2)
        session.commit()

        result = check_md5s(session, filename)
        self.assertEqual(f"MD5 Mismatch found for #{filename}", result)
