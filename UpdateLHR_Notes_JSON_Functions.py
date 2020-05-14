import csv

###################
#    Functions
###################

def readCsvFile(fileName):

    myFile = open(fileName, "r", encoding = "utf-8", errors = "ignore")
    reader = csv.reader(myFile)

    return reader

def buildRecordArray(myField, myArray, myArrayIndex):

    myFieldArray = myField.split("/")
    myArray.insert(myArrayIndex, myFieldArray)

def buildNotesArray(myField, myArray, myArrayIndex):
    notesArray = []
    myFieldArray = myField.split("/")

    for currentElement in myFieldArray:
        currentElement = currentElement.lower()
        currentElement = currentElement.strip()
        if currentElement not in notesArray:
            notesArray.append(currentElement)
    
    myArray.insert(myArrayIndex, notesArray)

def buildFinalArraySimple(finalArray, currentBarcode, currentNote):
    finalArray.append([currentBarcode, currentNote])

def buildFinalArrayOneNote(finalArray, shelvingLocArray, currentBarcodeArray, currentNote):
	for x in range(0, len(shelvingLocArray)):
		if shelvingLocArray[x] == "ROBE":
			currentBarcode = currentBarcodeArray[x]
			finalArray.append([currentBarcode, currentNote])

def buildFinalArrayWithRobe(finalArray, shelvingLocArray, currentBarcodeArray, currentNoteArray):
	for x in range(0, len(shelvingLocArray)):
		if shelvingLocArray[x] == "ROBE":
			currentBarcode = currentBarcodeArray[x]
			currentNote = currentNoteArray[x]
			finalArray.append([currentBarcode, currentNote])

def countRobeInstances(shelvingLocArray):
	robeCount = 0
    
	for x in range(0, len(shelvingLocArray)):
		if shelvingLocArray[x] == "ROBE":robeCount = robeCount + 1
	
	return robeCount
	

