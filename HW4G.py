import xml.etree.ElementTree as ET
import os

xmlfile='D:/sdataprj/Full/Full/4G/HW/4G HW.XML'
ns = {'nons': 'http://www.huawei.com/specs/bsc6000_nrm_forSyn_collapse_1.0.0',
      'xsins': 'http://www.w3.org/2001/XMLSchema-instance',
      'spec': 'http://www.huawei.com/specs/huawei_wl_bulkcm_xml_baseline_syn_1.0.0'}
element_tree = ET.parse(xmlfile)
root = element_tree.getroot()
subroot = root.find('spec:syndata',ns)
classes = root.findall('.//nons:class', ns)
date = root.find('spec:fileFooter', ns)
print(type(subroot))
print(type(classes))
dateTime = date.get('dateTime').split(':')[0]
network = '4G'
MOName = root.find(".//spec:syndata/.[@FunctionType='eNodeBFunction']", ns).get('Id').split('=')[-1]



def createHeader(classTag):
    headerArray = []
    headerArray.append("FileName")
    headerArray.append("MO")

    
    for className in classTag:
        
        attrib = className.find("./*")
        headerNames = attrib.findall("./*")
        if not headerNames:
            continue
        else:
            #create the header array
            
            for headerName in headerNames:
                elements = headerName.findall("./*")
                if not elements:
                    headerArray.append(headerName.tag.split('}')[-1])
                else:
                    currentTagName = headerName.tag.split('}')[-1]
                    for i in range(len(elements)):
                        subHeaderNames = elements[i].findall("./*")
                        if not subHeaderNames:
                            continue
                        else:
                            for subHeaderName in subHeaderNames:
                                columnHeader = currentTagName + "_" + subHeaderName.tag.split('}')[-1] + "[" + str(i) + "]"
                                headerArray.append(columnHeader)
            break
    headerArray.append("\n")
    return headerArray
def WriteData(classTag, exportFile):
    for className in classTag:
        MO = MOName
        attrib = className.find("./*")
        headerNames = attrib.findall("./*")
        if not headerNames:
            continue
        else: 
            dataToWrite = []
            dataToWrite.append(xmlfile.split('/')[-1] + "\t")
            dataToWrite.append(MO + "\t")
            for headerName in headerNames:
                elements = headerName.findall("./*")
                if not elements:
                    if not headerName.text:
                        dataToWrite.append("\t")
                    else:
                        dataToWrite.append(headerName.text + "\t")
                else:
                    for element in elements:
                        subHeaderNames = element.findall("./*")
                        if not subHeaderNames:
                            continue
                        else:
                            for subHeaderName in subHeaderNames:
                                if not subHeaderName.text:
                                    dataToWrite.append("\t")
                                else:
                                    dataToWrite.append(subHeaderName.text+ "\t")
            
            dataToWrite.append("\n")
            strToWrite = ""
            for i in dataToWrite:
                strToWrite += i
            exportFile.write(strToWrite)
            
for classTag in classes:
    nameOfClass = classTag.find("./*").tag.split('}')[-1] #name class to write down
    nameOfOutputFile = "export_" + nameOfClass + "__" + dateTime + ".txt"
    
    locationOfOutputFile ="HW/" + network + "/" + dateTime + "/" + nameOfOutputFile
    if not os.path.exists(os.path.dirname(locationOfOutputFile)):
        try:
            os.makedirs(os.path.dirname(locationOfOutputFile))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    
    exportFile = open(os.path.abspath(locationOfOutputFile), 'w', encoding='utf-8')
    headerArray = createHeader(classTag)
    
    exportFile.write("\t".join(headerArray))
            # write data to it
    WriteData(classTag, exportFile)
    exportFile.close() 
