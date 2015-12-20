import Rest
from os.path import expanduser
from openpyxl import load_workbook


con = Rest.Connection()

#1: asking for every task_id, 2: asking for every work-record
ids = con.search('project.task.work')
print ids
works = con.get('project.task.work', [ids])
#print works[1]



basePath = expanduser("~")+'\\server\\LTS\\grunndata\\'
templatePath = basePath+'timesheets.xlsx'
outPath = basePath+'timesheets2.xlsx'

wb = load_workbook(templatePath) 
shResult = wb.get_sheet_by_name('result')

#loop all work records
for index, item in enumerate(works):
  print item['date'], index
  shResult.cell(row = index+1, column = 1).value=item['date']
  shResult.cell(row = index+1, column = 2).value=item['user_id'][1]
  shResult.cell(row = index+1, column = 3).value=item['hours']
  shResult.cell(row = index+1, column = 4).value=item['task_id'][1]
  shResult.cell(row = index+1, column = 5).value=item['display_name']

wb.save(outPath)