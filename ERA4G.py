import xml.etree.ElementTree as ET
import os

xmlfile='D:/sdataprj/Full/Full/4G/ERA/4G ERA.xml'
ns = {'es': 'EricssonSpecificAttributes.17.08.xsd',
      'un': 'utranNrm.xsd',
      'xn': 'genericNrm.xsd',
      'gn': 'geranNrm.xsd',
      'nons': 'configData.xsd'}
element_tree = ET.parse(xmlfile)

root = element_tree.getroot()

date = root.find('nons:fileFooter', ns)
dateTime = date.get('dateTime').split(':')[0]
network = '4G'

Type = root.findall('.//xn:vsDataType', ns)
typeArray = []
for name in Type:
    typeArray.append(name.text)
print(len(set(typeArray)))