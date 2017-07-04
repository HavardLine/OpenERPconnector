import d_odoo
import pandas

con = d_odoo.Connection()

terms = [['date', 'like', '2017-0']]

#Get all lines from tasks in this period
dataset = con.searchRead('project.task.work', terms, {})
test = pandas.Series(dataset)


#Loop all lines to extract active_tasks
active_task_ids = []
active_task_names = []
for data in dataset:
  active_task_ids.append(data['task_id'][0])
  active_task_names.append(data['task_id'][1])
  print(data)
  print()

#active_tasks = unique tasks in this period
active_task_ids = set(active_task_ids)
active_task_names = set(active_task_names)
print('active task ids:',list(active_task_ids))
print('active task names:',list(active_task_names))

for task in active_task_names:
  print()
  print('Task name:', task)
  total_hours = 0
  for data in dataset:
    if data['task_id'][1]==task:
      print(
        data['date'][:10], \
        '  ', \
        str(data['hours'])+'t', \
        '  ', \
        data['display_name'],
        '  ', \
        data['user_id'][1]
        )
      total_hours += data['hours']
  print('Total: '+str(total_hours)+'t')
