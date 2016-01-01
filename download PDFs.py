import odoorpc
odoo = odoorpc.ODOO('172.16.1.146', protocol='jsonrpc', port=8070)
odoo.login('LTS','admin','a')

report = odoo.report.download('account.report_invoice', [1])
from pprint import pprint


with open('sale_orders.pdf', 'w') as report_file:
  report_file.write(report.read())
