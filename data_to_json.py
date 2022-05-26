import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
import json


#############################################BSA-DETAILS################################

directory_B = "BSA_files"

lst_B = []
files = Path(directory_B).glob('*')
for file in files:
    xml_data = open(file, 'r').read()
    main_root = ET.XML(xml_data)
    
    for i in range(0, len(main_root)):
        root = main_root[i]
        
        t = root.find(".//MonthlyDetails")
        xml_str = ET.tostring(t, encoding='utf-8')
        df= pd.read_xml(xml_str)
        name = main_root[i][1][0].attrib["name"]
        total_cred_amt = df['totalCredit'].sum()
        total_debt_amt = df['totalDebit'].sum()
        no_creds = df['credits'].sum()
        no_debts = df['debits'].sum()
        max_cred = df['totalCredit'].max()
        max_debt = df['totalDebit'].max()
        
        try:
            t_emi = root.find(".//EmiEcsLoanXns")
            xml_str_emi = ET.tostring(t_emi, encoding='utf-8')
            df_emi= pd.read_xml(xml_str_emi)
            no_emi_txns = len(df_emi)
            total_emi_amt = df_emi['amount'].sum()
        except:
            no_emi_txns = ""
            total_emi_amt = ""
            
        t_date = root.find(".//EODBalances")
        xml_str_date = ET.tostring(t_date, encoding='utf-8')
        df_date = pd.read_xml(xml_str_date)
        start_date = df_date['date'].iloc[0]
        end_date = df_date['date'].iloc[len(df_date)-1]
        
        res = [name, total_cred_amt, total_debt_amt, no_creds, no_debts, max_cred, max_debt, no_emi_txns, total_emi_amt, start_date, end_date]
        lst_B.append(res)
        
df_B = pd.DataFrame(lst_B, columns=['name','totalCredit','total Debit', 'noOfCredit', 'noOfDebit', 'maxCreditAmt', 'maxDebitAmt', 'totalEmiTxns', 'totalEmiAmt', 'statementStartDate', 'statementEndDate'])


############################################ITR-DETAILS################################

directory_I = "ITR_files"

lst_I = []
files = Path(directory_I).glob('*')
for file in files:
    f = open(file)
    data = json.load(f)
    data = data['itrDetails']
    
    res = pd.json_normalize(data, "ITR")
    name = res.loc[0, 'personalInfo.surNameOrOrgName']
    ay = res.loc[0, 'ay']
    grossIncome = res.loc[0, 'grossTotalIncome']
    netIncome = res.loc[0, 'totalIncome']
    
    try:
        DeductionsUnderVI = res.loc[0, 'deductionsUnderScheduleVIA']
    except:
        DeductionsUnderVI = ""
        
    totalTax = res.loc[0, 'totalTaxesPaid']
    tds = res.loc[0, 'TDS']
    tcs = res.loc[0, 'TCS']
    refund = res.loc[0, 'amountPayableOrRefund']
    
    res_data = [name, ay, grossIncome, netIncome, DeductionsUnderVI, totalTax, tds, tcs, refund]
    lst_I.append(res_data)
    
df_I = pd.DataFrame(lst_I, columns=['Name','ay','grossTotalIncome', 'totalIncome', 'DeductionsUnderVI(PF)', 'totalTaxesPaid', 'TDS', 'TCS', 'amountPayableOrRefund'])


#####################################SS-DETAILS####################################

directory_S = "SS_files"

lst_S = []
files = Path(directory_S).glob('*')
for file in files:
    xml_data = open(file, 'r').read()
    root = ET.XML(xml_data)
    
    df = pd.read_xml(xml_data, xpath=".//data")
    
    employee_name = df.loc[0, 'employee_name']
    employer_name = df.loc[0, 'employer_name']
    netSalary = df.loc[0, 'NetIncome']
    salaryMonth = df.loc[0, 'earnings']
    basicSalary = df.loc[0, 'basic']
    deductions = df.loc[0, 'deductions']
    pf = df.loc[0, 'pfno']
    
    res = [employee_name, employer_name, netSalary, salaryMonth, basicSalary, deductions, pf]
    lst_S.append(res)
    
df_S = pd.DataFrame(lst_S, columns=['employee_name', 'employer_name', 'netSalary', 'salaryMonth', 'basicSalary', 'deductions', 'pf'])


#############################Loading data to excel######################################

with pd.ExcelWriter("final_result.xlsx") as writer:
    df_B.to_excel(writer, sheet_name="BankAnalysis", index=None)  
    df_I.to_excel(writer, sheet_name="ITR_Analysis", index=None)
    df_S.to_excel(writer, sheet_name="SS_Analysis", index=None)


############################Loading data to Json file################################

excel_data_df_B = pd.read_excel('final_result.xlsx', sheet_name='BankAnalysis')
excel_data_df_I = pd.read_excel('final_result.xlsx', sheet_name='ITR_Analysis')
excel_data_df_S = pd.read_excel('final_result.xlsx', sheet_name='SS_Analysis')

json_str_B = excel_data_df_B.to_json(orient='records')
json_str_I = excel_data_df_I.to_json(orient='records')
json_str_S = excel_data_df_S.to_json(orient='records')

json_dict_B = json.loads(json_str_B)
json_dict_I = json.loads(json_str_I)
json_dict_S = json.loads(json_str_S)

datas = {"BankAnalysis":json_dict_B,
        "ITR_Analysis":json_dict_I,
         "SS_Analysis":json_dict_S}
with open('final_result.json', 'w') as json_file:
    json.dump(datas, json_file, indent = 5)