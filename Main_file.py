# -*- coding: utf-8 -*-
"""
Created on Wed May  4 21:39:22 2022

@author: metri
"""

import os
import BSA
import ITR
import SS
import xml.etree.cElementTree as ET

from xml.dom import minidom
import json

from jsonpath_ng import parse


root = minidom.Document()
  
xml = root.createElement('PersonalDataReport') 
root.appendChild(xml)

#############################################BSA-DETAILS################################
# assign directory
directory = "BSA_files"

for filename in os.listdir(directory): # iterate over files in that directory
    f = os.path.join(directory, filename)
    
    personalInfo = root.createElement('PersonalInfo')
    personalInfo.setAttribute('txnId', filename[:17])

    personalInfo.setAttribute('documentType', 'BSA-XML')
    xml.appendChild(personalInfo)
    xml_str = root.toprettyxml(indent ="\t")
    
    if os.path.isfile(f):
        tree = ET.parse(f)
        
    path = BSA.path
    
    
    #CHILD-1
    child1 = root.createElement(BSA.name[15:])
    personalInfo.appendChild(child1)
    xml_str = root.toprettyxml(indent ="\t")

    name = root.createTextNode(tree.find(path).attrib["name"])
    child1.appendChild(name)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-2
    child2 = root.createElement(BSA.pan[15:])
    personalInfo.appendChild(child2)
    xml_str = root.toprettyxml(indent ="\t")

    pan = root.createTextNode(tree.find(path).attrib["pan"])
    child2.appendChild(pan)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-3
    child3 = root.createElement(BSA.email[15:])
    personalInfo.appendChild(child3)
    xml_str = root.toprettyxml(indent ="\t")

    email = root.createTextNode(tree.find(path).attrib["email"])
    child3.appendChild(email)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-4
    child4 = root.createElement(BSA.address[15:])
    personalInfo.appendChild(child4)
    xml_str = root.toprettyxml(indent ="\t")

    address = root.createTextNode(tree.find(path).attrib["address"])
    child4.appendChild(address)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-5
    child5 = root.createElement(BSA.mobile[15:])
    personalInfo.appendChild(child5)
    xml_str = root.toprettyxml(indent ="\t")

    mobile = root.createTextNode(tree.find(path).attrib["mobile"])
    child5.appendChild(mobile)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-6
    child6 = root.createElement(BSA.landline[15:])
    personalInfo.appendChild(child6)
    xml_str = root.toprettyxml(indent ="\t")

    landline = root.createTextNode(tree.find(path).attrib["landline"])
    child6.appendChild(landline)
    xml_str = root.toprettyxml(indent ="\t")
    

############################################ITR-DETAILS#############################

directory = "ITR_files"


for filename in os.listdir(directory): # iterate over files in that directory
    f = os.path.join(directory, filename)
    
    personalInfo = root.createElement('PersonalInfo')
    personalInfo.setAttribute('txnId', filename[:21])
    
    personalInfo.setAttribute('documentType', 'ITR-JSON')
    xml.appendChild(personalInfo)
    xml_str = root.toprettyxml(indent ="\t")
    
    if os.path.isfile(f):
        with open(f, 'r') as json_file:
            json_data = json.load(json_file)
        
    jsonpath_expression_1 = parse(ITR.path_sur)
    jsonpath_expression_2 = parse(ITR.path_firn)
    jsonpath_expression_3 = parse(ITR.path_add)
    jsonpath_expression_4 = parse(ITR.path_dob)
    jsonpath_expression_5 = parse(ITR.path_pan)
    
    
    for match in jsonpath_expression_1.find(json_data):
        surNameOrOrgName = match.value

    for xox in jsonpath_expression_2.find(json_data):
        firstname = xox.value

    for a in jsonpath_expression_3.find(json_data):
        address = a.value
        
    for b in jsonpath_expression_4.find(json_data):
        DOB = b.value
        
    for c in jsonpath_expression_5.find(json_data):
        PAN = c.value

    #CHILD-1
    I_child1 = root.createElement(ITR.name[15:])
    personalInfo.appendChild(I_child1)
    xml_str = root.toprettyxml(indent ="\t")

    SURN = root.createTextNode(surNameOrOrgName)
    I_child1.appendChild(SURN)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-2
    I_child2 = root.createElement(ITR.fir_name[15:])
    personalInfo.appendChild(I_child2)
    xml_str = root.toprettyxml(indent ="\t")

    firstName = root.createTextNode(firstname)
    I_child2.appendChild(firstName)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-3
    I_child3 = root.createElement(ITR.address[15:])
    personalInfo.appendChild(I_child3)
    xml_str = root.toprettyxml(indent ="\t")

    address_I = root.createTextNode(address)
    I_child3.appendChild(address_I)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-4
    I_child4 = root.createElement(ITR.dob[15:])
    personalInfo.appendChild(I_child4)
    xml_str = root.toprettyxml(indent ="\t")

    DOB = root.createTextNode(DOB)
    I_child4.appendChild(DOB)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-5
    I_child5 = root.createElement(ITR.pan[15:])
    personalInfo.appendChild(I_child5)
    xml_str = root.toprettyxml(indent ="\t")

    pan_I = root.createTextNode(PAN)
    I_child5.appendChild(pan_I)
    xml_str = root.toprettyxml(indent ="\t")
      
    
#####################################SS-DETAILS####################################
    
    
directory = "SS_files"

for filename in os.listdir(directory): # iterate over files in that directory
    f = os.path.join(directory, filename)
    
    personalInfo = root.createElement('PersonalInfo')
    personalInfo.setAttribute('txnId', filename[:17])
    
    personalInfo.setAttribute('documentType', 'SS-XML')
    xml.appendChild(personalInfo)
    xml_str = root.toprettyxml(indent ="\t")
    
    if os.path.isfile(f):
        S_tree = ET.parse(f)
    
    myroot = S_tree.getroot()
    emp_name = str(myroot.find(SS.path_empn).text)
    pan_S = str(myroot.find(SS.path_pan).text)
    
    #CHILD-1
    E_child1 = root.createElement(SS.name[15:])
    personalInfo.appendChild(E_child1)
    xml_str = root.toprettyxml(indent ="\t")

    employee_name = root.createTextNode(emp_name)
    E_child1.appendChild(employee_name)
    xml_str = root.toprettyxml(indent ="\t")

    #CHILD-2
    E_child2 = root.createElement(SS.pan[15:])
    personalInfo.appendChild(E_child2)
    xml_str = root.toprettyxml(indent ="\t")

    pan_S = root.createTextNode(pan_S)
    E_child2.appendChild(pan_S)
    xml_str = root.toprettyxml(indent ="\t")
   
    
save_path_file = "personal_detail_main.xml"
  
with open(save_path_file, "w") as x:
    x.write(xml_str)