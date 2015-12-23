from time import gmtime, strftime
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas

output = PdfFileWriter()
#Look for PDF in folders here...
input1 = PdfFileReader(open("PDF1.pdf", "rb"))
input2 = PdfFileReader(open("PDF2.pdf", "rb"))
input3 = PdfFileReader(open("PDF3.pdf", "rb"))

 
# Test print to check number of pages
print "PDF1.pdf has %d pages." % input1.getNumPages()
print "PDF2.pdf has %d pages." % input2.getNumPages()
print "PDF3.pdf has %d pages." % input3.getNumPages()

#Make pdf with current date
strDato = strftime("%Y-%m-%d", gmtime())
def dato(c):
    c.drawString(50,50,str(strDato))
c = canvas.Canvas("DatoStempel.pdf")
dato(c)
c.showPage()
c.save()

#Make variable with new date-pdf
inputDato = PdfFileReader(open("DatoStempel.pdf", "rb"))


#For-loops to add all pages from several pdf-files to one output
for page_num in range(input1.numPages):
    output.addPage(input1.getPage(page_num))
    page = input1.getPage(page_num)
    page.mergePage(inputDato.getPage(0))
    
for page_num in range(input2.numPages):
    output.addPage(input2.getPage(page_num))
    page = input2.getPage(page_num)
    page.mergePage(inputDato.getPage(0))
    
for page_num in range(input3.numPages):
    output.addPage(input3.getPage(page_num))
    page = input3.getPage(page_num)
    page.mergePage(inputDato.getPage(0))


#Put all pages together to one file
output.write(file('TESTPDF.pdf','wb'))
