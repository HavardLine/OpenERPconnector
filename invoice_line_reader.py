import odoo, pprint

con = odoo.Connection()
obj = 'account.invoice.line'

terms = []
#terms = [['date', 'like', '2016-0']]
opts = {}
dataset = con.searchRead(obj, terms, opts)

#print dataset[0]

#pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(dataset[0]['display_name'])

for data in dataset:
 print data['invoice_id']
 print data['write_uid']
 print data['price_subtotal']
 print ''


#print dataset['display_name'])
#invoice_line

#task_ids = []
#for data in dataset:
#  task_ids.append(data['task_id'][1])
#active_tasks = set(task_ids)
#print 'active tasks:',list(active_tasks)

#for task in active_tasks:
#  print ''
#  print 'Task name:', task
#  total_hours = 0
#  for data in dataset:
#    if data['task_id'][1]==task:
#      print data['date'][:10], '  ', str(data['hours'])+'t', '  ',data['display_name']
#      total_hours += data['hours']
#  print 'Total: '+str(total_hours)+'t'
