# -*- coding=gbk -*-
import sys  
reload(sys)  
sys.setdefaultencoding('gbk')   
import csv
from xml.etree.ElementTree import iterparse
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
import markdown2
import codecs
import re
class XML_CSV():
    #去掉xml文件中的HTML标签
    def strip_tags(self,htmlStr):
        htmlStr = re.sub("[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\\x7f]","",htmlStr)
        htmlStr = re.sub(codecs.BOM_UTF8,"",htmlStr)
        htmlStr = re.sub("\\xef\\xbb\\xbf","",htmlStr)
        
        htmlStr = htmlStr.strip()
        htmlStr = htmlStr.strip("\n")

        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(htmlStr)
        parser.close()
        return  ''.join(result)
    def recursion(self, parent, _p_num):
        for child in parent:
            if child.tag == "testsuite":
                self.p_num = self.p_num + 1
                suite_list = ['', '', '', '']
                suite_list[0] = '%s_%s' % (parent.attrib['name'], str(_p_num))
                suite_list[1] = child.attrib['name']
                #suite_list[2] = child.attrib['detail']
                suite_list[3] = '%s_%s' % (child.attrib['name'], str(self.p_num))
                self.return_list[0].append(suite_list)
                self.recursion(child, self.p_num)
            if child.tag == "testcase":
                case_list = ['', '', '', '', '', '']
                case_list[0] = '%s_%s' % (parent.attrib['name'], str(_p_num))
                case_list[1] = child.attrib['name']
                case_list[5] = child.attrib['internalid'] 
                for sub_elem in child:
                    if sub_elem.tag == "summeary":
                        case_list[2] = markdown2.markdown(str(sub_elem.text).decode('gbk'))
                    if sub_elem.tag == "steps":
                        try:
                            case_list[3] =  sub_elem.text
                        except Exception, e:
                            print e
                    if sub_elem.tag == "expectedresults":
                        try:
                            case_list[4] = sub_elem.text
                        except Exception, e:
                            print e
                self.return_list[1].append(case_list)
        return self.return_list


    def read_xml(self, xml_obj):
        self.p_num = 0
        self.return_list = ([],[])
        tree = ET.ElementTree(file=xml_obj)
        root_node = tree.getroot()
        root_name = root_node.attrib['name']
        self.return_list[0].append(["root_node", root_name, '', '%s_%s'%(root_name,0)]) 
        
        self.recursion(root_node, 0)
        print self.return_list
        return self.return_list
    #先用iter方法获取所有目录节点，之后遍历每一个目录节点的子节点，把目录节点的名字送给子节点的列表。
    def read_xml_bak(self, xmlobj):
        return_list = ([],[])
        tree = ET.ElementTree(file=xmlobj)
        #up_suite = 'root'
        p_num = 0
        root_node = tree.getroot()
        _root = "root_node"
        _name = root_node.attrib['name']
        internalid = '%s_%s'% (_name,str(p_num))
        _detail = ''
        for child in root_node:
            if child.tag == "detail":
                _detail = child.text
        return_list[0].append([_root, _name, _detail,internalid])
        
        for parent_elem in tree.iter():
            
        #for i in range(len(tree.iter())):
            #parent_elem = tree.iter()[i]
            #suite_list = ['','','']
            '''
            if i == 0:
                if parent_elem.tag == "testsuite": 
                    suite_list[0] = "root"
                    suite_list[1] = parent_elem.attrib['name']
                    for child in parent_elem:
                        if child.tag == "details":
                            suite_list[2] = child.text
                    return_list[0].append(suite_list)
            '''
            if parent_elem.tag == "testsuite":
                for elem in parent_elem:
                    if elem.tag == "testsuite":
                        suite_list = ['','','','']
                        suite_list[0] = '%s_%s'% (parent_elem.attrib['name'],str(p_num))
                        suite_list[1] = elem.attrib['name']
                        suite_list[3] = '%s_%s'% (elem.attrib['name'], str(p_num+1))
                        for child in elem:
                            if child.tag == "details":
                                suite_list[2] = child.text
                        #print suite_list
                        return_list[0].append(suite_list)
                    if elem.tag == "testcase":
                        case_list = ['','','','','','']
                        # case_list[0] = parent_elem.attrib['name']
                        case_list[0] = '%s_%s'% (parent_elem.attrib['name'],str(p_num))    
                        case_list[1] = elem.attrib['name']
                        case_list[5] = elem.attrib['internalid'] 
                        for child in elem:
                            if child.tag == "summeary":
                                case_list[2] = markdown2.markdown(str(child.text).decode('gbk'))
                            if child.tag == "steps":
                                try:
                                    case_list[3] = self.strip_tags(str(child.text)).decode('gbk')
                                except Exception,e:
                                    print e
                                    case_list[3] = ""
                            if child.tag == "expectedresults":
                                case_list[4] = self.strip_tags(str(child.text).decode('GBK'))
                        #print case_list
                        return_list[1].append(case_list)
                p_num = p_num + 1
        print return_list[0]
        return return_list
    def read_xml_to_csv(self,csv_file,xmlfile):  
        csvfile = open(csv_file, 'wb')
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(['tag', 'name', 'node_order', 'details', 'internalid','externalid','summary','steps','expectedresults'])
        #逐行解析XML文件，将每行的内容存入列表，之后逐行写入CSV文件中
        for (event,node) in iterparse(xmlfile,events=['start']):
            if node.tag == "testsuite":
                suite_list = ['','','','','','','','','']
                print node.attrib['name']
                suite_list[0] = node.attrib['name']
                for child in node:
                    if child.tag == "node_order":
                        print child.text
                        suite_list[2] = child.text
                    if child.tag == "details":
                        print child.text
                        suite_list[3] = self.strip_tags(str(child.text))
                spamwriter.writerow(suite_list)
            if node.tag == "testcase":
                case_list = ['testcase','','','','','','','','']
                print node.attrib['internalid']
                print node.attrib['name']
                case_list[1] = node.attrib['name']
                case_list[4] = node.attrib['internalid']
                for child in node:
                    if child.tag == "node_order":
                        print child.text
                        case_list[2] = child.text
                    if child.tag == "externalid":
                        print child.text
                        case_list[5] = child.text
                    if child.tag == "summary":
                        print self.strip_tags(str(child.text))
                        case_list[6] = self.strip_tags(str(child.text))
                    if child.tag == "steps":
                        print self.strip_tags(str(child.text))
                        case_list[7] = self.strip_tags(str(child.text))
                    if child.tag == "expectedresults":
                        #print child.text
                        print self.strip_tags(str(child.text))
                        case_list[8] = self.strip_tags(str(child.text))
                spamwriter.writerow(case_list)
        csvfile.close()
    
    def read_csv_to_xml(self,csv_file,xmlfile):
        #逐行读取CSV文件的内容，将内容写进以internalid为键，name，sumary，steps，expectresult为值得字典
        csv_file = file(csv_file,'rb')
        reader = csv.reader(csv_file)  
        case_dic = {}  
        for line in reader:  
            if reader.line_num == 1:  
                continue  
            if line[0] == "testcase":
                name = str(line[1])
                internalid = str(line[4])
                summary = line[6]
                steps = line[7]
                expectedresults = line[8]
                case_dic[internalid] = (name,summary,steps,expectedresults)
        csv_file.close()
        print case_dic
        #用ElementTree方法打开xml文件，逐行解析XML文件，发现case为tag的行，就将name，sumary，steps，expectresult，这几项用字典的值替换。
        tree = ET.ElementTree()
        tree.parse('usb.xml')
        root = tree.getroot()
        root_suite_name = root.attrib['name']
        
        for node in tree.iter():
            if node.tag == "testsuite":
                print node.attrib['name']
                sub_suite_name = node.attrib['name']
                for child in node:
                    if child.tag == "node_order":
                        #print child.text
                        pass
                    if child.tag == "details":
                        pass
            if node.tag == "testcase":
                new_internalid = node.attrib['internalid']
                #将根目录和子目录的名字都写进了case名字中。如果不需要可以用下面那行注释掉的替换这一行
                node.attrib['name'] = root_suite_name+'_'+sub_suite_name+'_'+case_dic[new_internalid][0]
                #node.attrib['name'] = case_dic[new_internalid][0]
                print node.attrib['name']
                #解析tag为testcase的节点的子节点，并修改节点的值
                for child in node:
                    if child.tag == "node_order":
                        pass
                    if child.tag == "externalid":
                        pass
                    if child.tag == "summary":
                        child.text = case_dic[new_internalid][1]
                        child.text = str(child.text.replace('\n',"<p>"))
                    if child.tag == "steps":
                        child.text = str(case_dic[new_internalid][2])
                        child.text = str(child.text.replace('\n',"<p>"))
                    if child.tag == "expectedresults":
                        child.text = case_dic[new_internalid][3]
                        child.text = str(child.text.replace('\n',"<p>"))
        #将修改后的ElementTree对象写入xml文件中。
        tree.write('usb.xml',encoding='utf8')   

if __name__ == "__main__":
    test = XML_CSV()
    #test.read_xml_to_csv('usb2.csv','usb.xml')
    #test.read_csv_to_xml('usb2.csv','usb.xml')
    file_obj = open('testsuites.xml', 'rb')
    print file_obj
    #test.read_xml(file_obj)
