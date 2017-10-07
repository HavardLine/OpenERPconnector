from drivers import odoo_connector, api_connector
import pandas, io, requests

#Establish conections
con_odoo = odoo_connector.Connection()
con_api = api_connector.Connection()

#Find all project tags
categories = con_odoo.searchRead('project.category', opts={'fields': ['id', 'display_name']})

#attachment_account_invoice = con_odoo.searchRead('ir.attachment', [[['description','<>', '']]], {'fields': ['date_start', 'description', 'categ_ids']})
tasks = con_odoo.searchRead('project.task', [[['description','<>', '']]], {'fields': ['date_start', 'description', 'id', 'categ_ids', 'child_ids']})

data = []
for task in tasks:
    tag = ''
    for categ_id in task['categ_ids']:
        for category in categories:
            if category['id'] == categ_id:
                tag = tag + category['display_name'] + ', '
    if task['description'][:8] == '@lts.no ':
        data.append({
            'date': task['date_start'],
            'description': task['description'][8:],
            'tag': tag.strip(', ')
            })
  
pandas.set_option('display.max_colwidth', 100)
df = pandas.DataFrame(data)
df = df.sort_values('date', ascending=False)
df['year'] = df['date'].astype(str).str[:4]
#Changing place
df2 = df[['year', 'description', 'tag']]
df2.columns = ['År', 'Beskrivelse', 'Tag']
#Save file
buffer = io.StringIO()
df2.to_html(buf=buffer,index=False, justify='left')
print(buffer.getvalue())

#defining api-call
headers ={'X-Dreamfactory-API-Key': con_api.params['api-key']}
data={"introtext": buffer.getvalue()}
url=con_api.params['url']
#executing patch command
response = requests.patch(url=url, headers=headers, data=data)
#printing status-code of the response
print(str(response.status_code))
buffer.close()
