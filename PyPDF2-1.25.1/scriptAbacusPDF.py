from time import gmtime, strftime
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
import glob, os
from os.path import expanduser

#Make variables for output PDF and array for input PDFs
output = PdfFileWriter()


#Make pdf with current date
os.chdir(expanduser("~")+'\Documents\GitHub\OpenERPconnector')
strDato = strftime("%Y-%m-%d", gmtime())
def dato(c):
    c.drawString(50,50,str(strDato))
c = canvas.Canvas("DatoStempel.pdf")
dato(c)
c.showPage()
c.save()

#Make variable with new date-pdf
inputDato = PdfFileReader(open("DatoStempel.pdf", "rb"))

#Make array with filepaths
folderlist = ([r"\server\LTS\bedrift\ABACUS_arbeidsmappe\bilag",
                r"\server\LTS\bedrift\ABACUS_arbeidsmappe\faktura_til_betaling",
                r"\server\LTS\bedrift\ABACUS_arbeidsmappe\loenn"])

#Define function for searching after PDF in folder from folderlist-array
def searchFolder(folderlist):
    os.chdir(expanduser("~")+folderlist)
    for findPDF in glob.glob("*.pdf"):
        files = PdfFileReader(open(findPDF, "rb"))
        print findPDF, "has %d pages." % files.getNumPages()
        print 'Found file %s'  %files
        print 'in folder %s:\n' %folderlist

        #For-loops to add all pages from several pdf-files to one output
        for page_num in range(files.numPages):
            output.addPage(files.getPage(page_num))
            page = files.getPage(page_num)
            page.mergePage(inputDato.getPage(0))

    return

#Define function for writing to output PDF
def writePDF(outputPDF):
    os.chdir(expanduser("~")+r"\server\LTS\bedrift\ABACUS_arbeidsmappe")
    output.write(file(outputPDF + '.pdf','wb'))

    return
    
#Calling functions for search and write PDFs
for i in range(len(folderlist)):
    searchFolder(folderlist[i])

writePDF('ABACUS PDF')

