import json
import logging
import tarfile
from email.parser import Parser
from sys import argv


def main(argv):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # Default files for easy command line testing
    archiveFile = "/Users/morgans/lisa/projects/rp-parse-msg/resources/sampleEmailstar.gz"
    resultsFile = "/Users/morgans/lisa/projects/rp-parse-msg/resources/results/results.json"

    # use command line args if provided
    if len(argv) > 1:
        archiveFile = argv[1]
        logging.info("Processing messages for archive file %s" % archiveFile)
    else:
        logging.info("No archive file specified. Processing messages for default file %s" % archiveFile)

    if len(argv) == 3:
        resultsFile = argv[2]
    else:
        logging.info("No results file specified. Using default file: %s" % resultsFile)

    class MessageDetails:
        def __init__(self, dateSent, fromAddress, subject):
            self.dateSent = dateSent
            self.fromAddress = fromAddress
            self.subject = subject

    # decompress archive and write info for each message to output file
    try:
        decompressedDirectory = tarfile.open(archiveFile)
    except IOError:
        logging.error("Could not open archive file %s" % archiveFile)
        exit(1)

    try:
        outputFile = open(resultsFile, 'w')
    except IOError:
        logging.error("Could not open results file %s" % results)
        exit(1)

    outputFile.write("{messages:")
    fileCounter = 0

    for member_info in decompressedDirectory.getmembers():
        # assumes all messages will conform to this naming convention
        fileName = member_info.name
        if fileName.endswith(".msg"):
            try:
                if fileCounter > 0:
                    outputFile.write(",")

                if fileCounter%100 == 0:
                    logging.info("Processed %d files" % fileCounter)

                inputFile = decompressedDirectory.extractfile(fileName)
                headers = Parser().parse(inputFile)
                messageDetail = MessageDetails(headers['date'], headers['from'], headers['subject'])
                outputFile.write("%s" % json.dumps(messageDetail.__dict__))
                fileCounter += 1
            except KeyError:
                logging.error("Did not find %s in tar archive" % fileName)
        else:
            logging.info("%s is not a .msg file and will be ignored" % fileName)

    outputFile.write("}")
    outputFile.close()

    logging.info("Processing complete. Results file can be found at: %s" % resultsFile)


if __name__ == "__main__":
    main(argv)


# Questions: what is the resulting file used for?
# How many files do we need to process?
# How fast does it need to be?
# Will the archive always be .gz or do we need to handle multiple compression formats?
