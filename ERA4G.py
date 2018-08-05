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
nameOfObj = list(set(typeArray))
#print(len(nameOfObj))
print(Type[0].text)
#pa = Type[10].find("..")
#print(root.find('.//nons:configData', ns).tag)
"""
pa = root.find('.//%s/..' % Type[0].tag)
pb = root.find('.//%s/..' % Type[1].tag)
print(pa.tag == pb.tag)"""

def CreateMO(xmlfile, elementObject):
    
    arrayOfParent = []
    
    parent = root.find('.//%s/../..' % elementObject.tag)
   # print(currentAtrrib.tag)
   # parent = root.find('.//%s/..' % currentAtrrib.tag)
    print(parent.tag)
    while parent.tag != root.find('.//nons:configData', ns).tag:
        if parent.tag == root.find('.//xn:VsDataContainer', ns).tag:
            attribOfparent = parent.find('./xn:attributes/xn:vsDataType', ns)
            arrayOfParent.append(attribOfparent.text.split('vsData')[-1] + "=" + parent.get('id'))
        else:
            arrayOfParent.append(parent.tag + "=" + parent.get('id'))
        parent = root.find('.//%s/..' % parent.tag)
    
    #arrayOfParent = arrayOfParent[::-1]
    return ",".join(arrayOfParent)

a = CreateMO(xmlfile, Type[0])
print(a)