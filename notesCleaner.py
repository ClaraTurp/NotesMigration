import csv
import os
import codecs
import string

###################
#    Functions
###################

def readCsvFile(fileName):
    myFile = open(fileName, "r", encoding = "utf-8", errors = "ignore")
    reader = csv.reader(myFile)

    return reader


def createPrintFiles(filename, x):
    myFile = open(filename, x, newline = "", encoding="utf-8", errors= "ignore")
    writer = csv.writer(myFile)

    return writer

def createTextFiles(filename, x):

    myFile = codecs.open(filename, x, "utf-8", errors="ignore")
    
    return myFile


def cleanOclcNum(field35a):
    myFieldArray = field35a.split(";")
    for currentIdentifier in myFieldArray:
        if currentIdentifier.startswith("(OCoLC)"):
            oclcNum = currentIdentifier[7:]
            return oclcNum


def cleanNotes(notes):
    notes = notes.split(";")


    currentNote = notes[0]
    myNote = currentNote.lower()
    translator = str.maketrans("", "", string.punctuation)
    currentNote = myNote.translate(translator)

    if currentNote.startswith("shelved"):
        keptNote = "shelved in/on/with/under: ..."
    elif currentNote.startswith("housed in") :
        keptNote = "housed in ..."
    elif currentNote.startswith("range") :
        keptNote = "range ..."
    elif currentNote.startswith("cancelled") or currentNote.startswith("canceled") :
        keptNote = "cancelled / cancelled after ..."
    elif currentNote.startswith("temporarily housed in") :
        keptNote = "temporarily housed in ..."
    elif currentNote.startswith("intentional") or currentNote.startswith("intention") :
        keptNote = "Intentional duplicate notes ..."
    elif myNote.startswith("od=") :
        keptNote = "od= ..."
    elif currentNote.startswith("osler no") :
        keptNote = "osler no ..."
    elif currentNote.startswith("with dust jacket") or "dust jacket" in currentNote:
        keptNote = "with dust jacket..."
    elif (currentNote.startswith("with") and "jacket" in currentNote) or (currentNote.startswith("with") and "cover" in currentNote):
        keptNote = "with jacket/cover..."
    elif currentNote.startswith("includes educational") or currentNote.startswith("includes public") or "public performance rights" in currentNote :
        keptNote = "includes public performance rights for mcgill ..."
    elif currentNote.startswith("j. patrick lee voltaire collection inventory number") :
        keptNote = "j. patrick lee voltaire collection inventory number: ..."
    elif currentNote.startswith("check first title")  or currentNote.startswith("check serial title"):
        keptNote = "check first/serial title ..." 
    elif currentNote.startswith("sent to binding"):
        keptNote = "sent to binding: ..."
    elif currentNote.startswith("transferred") :
        keptNote = "transferred ..."
    elif currentNote.startswith("cd-rom accompanies") :
        keptNote = "cd-rom accompanies ..."
    elif currentNote.startswith("bound with") or "bound with" in currentNote :
        keptNote = "bound with ..."
    elif currentNote.startswith("accompanied by exercises") :
        keptNote = "accompanied by exercises ..."
    elif "photocopies" in currentNote :
        keptNote = "photocopies ..."
    elif "copies" in currentNote or "copy" in currentNote:
        keptNote = "copies information ..."
    elif "current " in currentNote or "earlier " in currentNote or "later " in currentNote or "latest " in currentNote:
        keptNote = "current/earlier/later information ..."
    elif "reel" in currentNote :
        keptNote = "on x reels ..."
    elif "fiches" in currentNote or "fiche" in currentNote or "microfiches" in currentNote or "microfiche" in currentNote or "microfilms" in currentNote or "microfilm" in currentNote :
        keptNote = "microfiches/microfilms information ..."
    elif "score" in currentNote :
        keptNote = "score information ..."
    elif "disc" in currentNote or "discs" in currentNote or "cd" in currentNote or "cds" in currentNote:
        keptNote = "Disc/Cd information ..."
    elif "dvd" in currentNote or "dvds" in currentNote :
        keptNote = "DVD information ..."
    elif "maps" in currentNote :
        keptNote = "maps information ..."
    elif "consulation use only" in currentNote or "library use only" in currentNote or "home use only" in currentNote:
        keptNote = "consultation/library/home use only ..."
    elif "missing" in currentNote  or "lost" in currentNote or "damaged" in currentNote or "not located" in currentNote:
        keptNote = "physical notes (i.e. missing) ..."
    elif "fragile" in currentNote  or "brittle" in currentNote :
        keptNote = "fragile item ..."
    elif "annotated" in currentNote  or "annotation" in currentNote :
        keptNote = "annotation information ..."
    elif "container" in currentNote  or "box" in currentNote:
        keptNote = "container/box information ..."
    elif "vol" in myNote or "volume" in myNote or "volumes" in myNote or "v." in myNote or "pt." in myNote or "parts" in myNote or "t." in myNote or "no." in myNote:
        keptNote = "volume information ..."
    elif "circulation" in currentNote  or "circulate" in currentNote or "loan" in currentNote or "library holdings" in currentNote or "holdings" in currentNote or "circ" in currentNote:
        keptNote = "circulation/holdings note ..."
    elif "cataloguing" in currentNote  or "catalogued" in currentNote:
        keptNote = "cataloguing note ..."
    elif "collection" in currentNote :
        keptNote = "collection information ..."
    elif "printing" in currentNote  or "reprint" in currentNote:
        keptNote = "printing/reprint information ..."
    else:
        keptNote = currentNote
    return keptNote


def arrayShouldBeUpdated(field, array):
    if field != "" and field not in array:
        return True
    else:
        return False

def updateArrays(row, notesList_852, notesList_866, notesList_867, notesList_868, notesList_876):

    field852_withZ = row[6]
    field866_withZ = row[7]
    field867_withZ = row[8]
    field868_withZ = row[9]
    field876_withZ = row[10]

    #Clean Notes
    if field852_withZ != "":
        field852_withZ = cleanNotes(field852_withZ)
    if field866_withZ != "":
        field866_withZ = cleanNotes(field866_withZ)
    if field867_withZ != "":
        field867_withZ = cleanNotes(field867_withZ)
    if field868_withZ != "":
        field868_withZ = cleanNotes(field868_withZ)
    if field876_withZ != "":
        field876_withZ = cleanNotes(field876_withZ)
    

    # Update Arrays
    if arrayShouldBeUpdated(field852_withZ, notesList_852):
        notesList_852.append(field852_withZ)
    if arrayShouldBeUpdated(field866_withZ, notesList_866):
        notesList_866.append(field866_withZ)
    if arrayShouldBeUpdated(field867_withZ, notesList_867):
        notesList_867.append(field867_withZ)
    if arrayShouldBeUpdated(field868_withZ, notesList_868):
        notesList_868.append(field868_withZ)
    if arrayShouldBeUpdated(field876_withZ, notesList_876):
        notesList_876.append(field876_withZ)

def printArray(myArray, myText, myFile):
    if len(myArray) > 0:
        #notesWriter.write("\n" + myText + "\n" + "\n")
        
        myArray.sort()
        for currentNote in myArray:
            myFile.write(currentNote+ "\n")

###################
#    Main Code   
###################
notesList_852 = []
notesList_866 = []
notesList_867 = []
notesList_868 = []
notesList_876 = []
notesList_Lande = []

bibWriter = createPrintFiles("NotesFromBibFiles.csv", "w")
bibWriter.writerow(["OCLC Number", "Field 245", "Field 852", "Field 866", "Field 867", "Field 868", "Field 876", "Notes with a Subfield Z"])
notesWriter = csv.writer(bibWriter)

currentDir = os.getcwd()
filesDir = currentDir + "\\allFiles\\"

for filename in os.listdir(filesDir):
    print(filename)

    myBibFile = readCsvFile(filesDir + filename)
    for row in myBibFile:    
        
        oclcNum = cleanOclcNum(row[0])
        field852_withZ = row[6]
        field866_withZ = row[7]
        field867_withZ = row[8]
        field868_withZ = row[9]
        field876_withZ = row[10]
        allFieldsWithZ = [field852_withZ, field866_withZ, field867_withZ, field868_withZ, field876_withZ]

        if any(currentSlot != "" for currentSlot in allFieldsWithZ):
            
            updateArrays(row, notesList_852, notesList_866, notesList_867, notesList_868, notesList_876)

printArray(notesList_852, "Notes in the 852 field", notesWriter)
printArray(notesList_866, "Notes in the 866 field", notesWriter)
printArray(notesList_867, "Notes in the 867 field", notesWriter)
printArray(notesList_868, "Notes in the 868 field", notesWriter)
printArray(notesList_876, "Notes in the 876 field", notesWriter)


