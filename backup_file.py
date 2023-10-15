import shutil
import datetime

def backup_file(file_path):
    """
    Create a backup of the given file with a datestamp suffix.
    """
    datestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup_path = f"{file_path}_{datestamp}"
    shutil.copy(file_path, backup_path)
    return backup_path
