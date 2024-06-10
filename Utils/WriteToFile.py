from datetime import datetime

class WriteToFile():
        
    def LogErrorToFile(errorText):

        with open('log/error.txt', 'a') as errorFile:
                        errorFile.write(f"{datetime.now()} - {errorText}\n")