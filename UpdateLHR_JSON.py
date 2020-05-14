
import csv
from UpdateLHR_API_JSON_Functions import *
from UpdateLHR_Notes_JSON_Functions import *


###################
#    Main Script
###################

myManualFile = open("OslerNotes_dealManually.csv", "a", newline = "", encoding="utf-8", errors= "ignore")
writer = csv.writer(myManualFile)
myErrorFile = open("OslerNotes_errors.csv", "w", newline = "", encoding="utf-8", errors= "ignore")
errorWriter = csv.writer(myErrorFile)

#File with triaged notes from Bib File extract
myNotesFile = readCsvFile("oslerNotes_test.csv")

##Parse the configuration file to get the base url.
data = parseConfigFile("config.json")

for row in myNotesFile:
    recordArray = []
    notesArray = []
    finalArray = []

    oclcNum = row[0]
    barcode = row[1]
    branch = row[2]
    shelvingLocation = row[3]
    notes = row[4]

    buildRecordArray(oclcNum, recordArray, 0)
    buildRecordArray(barcode, recordArray, 1)
    buildRecordArray(branch, recordArray, 2)
    buildRecordArray(shelvingLocation, recordArray, 3)
    buildNotesArray(notes, recordArray, 4)

    multipleFields = False

    for currentElement in recordArray:
        if len(currentElement) > 1:
            multipleFields = True
    
    if multipleFields == False:
        buildFinalArraySimple(finalArray, recordArray[1][0], recordArray[4][0])
    
    else:

        if len(recordArray[4]) == 1:
            buildFinalArrayOneNote(finalArray, recordArray[3], recordArray[1], recordArray[4][0])
    
        elif len(recordArray[4]) > 1:
            
            robeCount = countRobeInstances(recordArray[3])

            if robeCount > len(recordArray[4]):
                writer.writerow(row)

            elif robeCount == len(recordArray[4]):
                print(finalArray)
                buildFinalArrayWithRobe(finalArray, recordArray[3], recordArray[1], recordArray[4])

            else:
                errorWriter.writerow(row)

    if len(finalArray) > 0 :

        for currentArray in finalArray:

            currentBarcode = currentArray[0]
            currentNote = currentArray[1]
            
            LHRIdentifier = retrieveLHRIdentifier(data["url"], currentBarcode)
            if LHRIdentifier is not None:
                addNoteToLHR(data["url"], LHRIdentifier, currentBarcode, currentNote)
            else:
                writer.writerow(row)
                print(currentBarcode, "No data found")
