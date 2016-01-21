import Rest, xlrd
con = Rest.Connection()


with open("config.yml", "r") as f:
    params = yaml.load(f)
params = params['productCatalog']

class Manager:
  def importPXC(self, filename='ShoppingCart.xls'):
    """Charts at phoenixcontact.com can be exported to excel.
    This method imports data into ODOO.
    TODO: check for existing product before importing"""
    
    template = con.search('product.template', ['default_code', '=', 'LTS.part'])
    if len(template)==1:
      template = template[0]
    else:
      template = False
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(template)
      
    book = xlrd.open_workbook(filename)
    sh = book.sheet_by_index(0)
    row = 4
    while sh.cell_value(rowx=row, colx=0)!='':
      #list*(1-discount)/(1+margin)
      discount = sh.cell_value(rowx=row, colx=9)/100
      margin = 0.2
      print discount
      cost = sh.cell_value(rowx=row, colx=7)*(1-discount)
      out_price = cost/(1-margin)
      print cost
      print out_price
      new_template = {
        'active': template['active'],
        'default_code': 'PXC.'+sh.cell_value(rowx=row, colx=0), #input field
        'name': sh.cell_value(rowx=row, colx=2), #input field
        'standard_price': cost, #input field
        'list_price': out_price, #input field
        'mes_type': template['mes_type'],
        'uom_id': template['uom_id'][0],
        'uom_po_id': template['uom_po_id'][0],
        'type': template['type'],
        'cost_method': template['cost_method'],
        'categ_id': template['categ_id'][0],
        }
      new_template_id = con.setProductTemplate(new_template)
      print 'new_template_id =', new_template_id
      import pprint
      pp.pprint(new_template)
      print ''
      row += 1

  def find(self):
    print con.search('product.product', ['name', '=', 'Software - STARTUP+'], {'fields' : ['display_name', 'id']})

  def readActive(self):
    """ Returns all products that are marked as active
    """
    #data = con.searchRead('product.product', ['code', 'like', 'PXC.'], {})
    return con.searchRead('product.product', ['default_code', 'like', 'PXC.'])
	
  def createCatalog(self, dataset, catalogParams = params):
    import time
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
 
    doc = SimpleDocTemplate(catalogParams['reportfile'],
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]
    formatted_time = time.ctime()

    im = Image(catalogParams['logo_path'], catalogParams['logo_width']*mm, catalogParams['logo_height']*mm)
    Story.append(im)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
      
    
    for item in dataset:
      #display name
      ptext = '<font size=12>%s</font>' % item['display_name']
      Story.append(Paragraph(ptext, styles["Normal"]))
      Story.append(Spacer(1, 12))
      #description
      ptext = '<font size=12>%s</font>' % item['description']
      Story.append(Paragraph(ptext, styles["Normal"]))
      Story.append(Spacer(1, 12))

    doc.build(Story)
    return True
  
if __name__ == '__main__':
  product = Manager()
  dataset = product.readActive()
  print product.createCatalog(dataset)
  
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(dataset[0])
