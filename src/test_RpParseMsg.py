import os
import unittest
from RPParseMsg import main

class test_RpParseMsg(unittest.TestCase):
    """Tests for `rp-parse-msg.py`."""

    def test_with_default_files(self):
        """Does output file get written?"""
        archiveFile = "/Users/morgans/lisa/projects/rp-parse-msg/resources/sampleEmailstar.gz"
        resultsFile = "/Users/morgans/lisa/projects/rp-parse-msg/resources/results/results.json"

        if os.path.isfile(resultsFile):
            os.remove(resultsFile)

        self.assertFalse(os.path.isfile(resultsFile))
        argv = ["rp-parse-msg.py", archiveFile, resultsFile]
        main(argv)

        assert(os.path.isfile(resultsFile))

if __name__ == '__main__':
    unittest.main()