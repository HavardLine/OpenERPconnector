import odoo, pprint

con = odoo.Connection()

#reads open invoices
obj = 'account.invoice'
terms = [['state', '=', 'open'], ['type','=','out_invoice']]
opts = {'fields': ['move_id', 'date_invoice', 'invoice_line']}
invoices = con.searchRead(obj, terms, opts)

print 'printing one invoice:'
print invoices[0]
print ''

#read relevant invoice lines 
invoice_lines = []
obj = 'account.invoice.line'
opts = {'fields': ['create_date', 'create_uid', 'price_subtotal', 'quantity', 'name', 'product_id']}
for invoice in invoices:
  terms = [['invoice_id', '=', invoice['id']]]
  invoice_lines.extend(con.searchRead(obj, terms, opts))

#pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(invoice_lines)#['display_name'])

for line in invoice_lines:
 print line['create_date'], line['price_subtotal'], line['create_uid'][1], line['product_id']
