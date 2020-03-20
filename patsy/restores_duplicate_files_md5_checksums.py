from .database import Session
from .model import Restore
from .progress_notifier import ProgressNotifier
from .utils import get_accessions


def find_restore_duplicate_files_with_md5_checksums(filename):
    session = Session()

    with open(filename, 'r') as file_handle:
        filename = file_handle.readline().strip()

        while True:
            if not filename:
                break

            result = check_md5s(session, filename)

            if not result.startswith("No MD5 mismatch"):
                print(result)

            filename = file_handle.readline().strip()


def check_md5s(session, filename):
    restores = session.query(Restore) \
        .filter(Restore.filename == filename).all()

    if len(restores) == 0:
        return f"ERROR - '#{filename} not found in restores table."

    if len(restores) == 1:
        return f"ERROR - '#{filename} occurs only once."

    md5 = None
    for restore in restores:
        if md5 is None:
            md5 = restore.md5
            continue

        if restore.md5 != md5:
            return f"MD5 Mismatch found for {filename}"

    return f"No MD5 mismatch for {filename}"
