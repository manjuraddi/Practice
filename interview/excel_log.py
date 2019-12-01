import urllib.request
import pandas as pd
import pdb

def get_data():
    emp_data = ""
    with urllib.request.urlopen("http://dummy.restapiexample.com/api/v1/employees") as url:
        emp_data = url.read()
    return emp_data

def write_excel(emp_data):
    df = pd.DataFrame(eval(emp_data))
    df.to_excel(r'/home/mraddi/ml_env/excel_data.xlsx')

if __name__ == "__main__":
    emp_data = get_data()
    write_excel(emp_data)
