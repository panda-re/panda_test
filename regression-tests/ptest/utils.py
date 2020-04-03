import os
import tempfile

def get_tempfile_name(some_id):
    return os.path.join(tempfile.gettempdir(),
    next(tempfile._get_candidate_names()) + "_" + some_id)
