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
print(Type[100].text)


parent_map = dict((c, p) for p in root.getiterator() for c in p)
def CreateMO(xmlfile, elementObject):
    
    arrayOfParent = []
    
  
    parent = parent_map[parent_map[elementObject]]
    


    print(parent.tag)
    while parent.tag != root.find('.//nons:configData', ns).tag:
        print(parent.attrib)
        if parent.tag == root.find('.//xn:VsDataContainer', ns).tag:
            attribOfparent = parent.find('./xn:attributes/xn:vsDataType', ns)
            arrayOfParent.append(attribOfparent.text.split('vsData')[-1] + "=" + parent.get('id'))
        else:
            if parent.tag.split('}')[-1] != elementObject.text.split('vsData')[-1]:
                arrayOfParent.append(parent.tag.split('}')[-1] + "=" + parent.get('id'))
       
        parent = parent_map[parent]

    arrayOfParent = arrayOfParent[::-1]
    return ",".join(arrayOfParent)

a = CreateMO(xmlfile, Type[100])
print(a)