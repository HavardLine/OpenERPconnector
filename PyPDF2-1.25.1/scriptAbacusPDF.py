from time import gmtime, strftime
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
import glob, os
from os.path import expanduser

#Make variables for output PDF and array for input PDFs
output = PdfFileWriter()
files = []

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

#Change directories to find PDFs in alle the folders
os.chdir(expanduser("~")+r"\server\LTS\bedrift\ABACUS_arbeidsmappe\bilag")
for findPDF in glob.glob("*.pdf"):
    files = PdfFileReader(open(findPDF, "rb"))
    print findPDF
    print files, "has %d pages." % files.getNumPages()

    #For-loops to add all pages from several pdf-files to one output
    for page_num in range(files.numPages):
        output.addPage(files.getPage(page_num))
        page = files.getPage(page_num)
        page.mergePage(inputDato.getPage(0))

os.chdir(expanduser("~")+r"\server\LTS\bedrift\ABACUS_arbeidsmappe\faktura_til_betaling")
for findPDF in glob.glob("*.pdf"):
    files = PdfFileReader(open(findPDF, "rb"))
    print findPDF
    print files, "has %d pages." % files.getNumPages()

    #For-loops to add all pages from several pdf-files to one output
    for page_num in range(files.numPages):
        output.addPage(files.getPage(page_num))
        page = files.getPage(page_num)
        page.mergePage(inputDato.getPage(0))

os.chdir(expanduser("~")+r"\server\LTS\bedrift\ABACUS_arbeidsmappe\loenn")
for findPDF in glob.glob("*.pdf"):
    files = PdfFileReader(open(findPDF, "rb"))
    print findPDF
    print files, "has %d pages." % files.getNumPages()
    
    #For-loops to add all pages from several pdf-files to one output
    for page_num in range(files.numPages):
        output.addPage(files.getPage(page_num))
        page = files.getPage(page_num)
        page.mergePage(inputDato.getPage(0))


#Put all pages together to one file
os.chdir(r"C:\Users\Anfinn\server\LTS\bedrift\ABACUS_arbeidsmappe")
output.write(file('ABACUS.pdf','wb'))
