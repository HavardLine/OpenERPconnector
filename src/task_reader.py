
import d_odoo

con = d_odoo.Connection()

terms = [['date', 'like', '2016-09']]

dataset = con.searchRead('project.task.work', terms, {})

task_ids = []
for data in dataset:
  task_ids.append(data['task_id'][1])
active_tasks = set(task_ids)
print 'active tasks:',list(active_tasks)

for task in active_tasks:
  print ''
  print 'Task name:', task.encode(encoding='UTF-8')
  total_hours = 0
  for data in dataset:
    if data['task_id'][1]==task:
      print data['date'][:10], \
        '  ', \
        str(data['hours'])+'t', \
        '  ', \
        data['display_name'].encode(encoding='UTF-8')
      total_hours += data['hours']
  print 'Total: '+str(total_hours)+'t'
