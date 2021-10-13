import requests
import json
import dataset
import os.path
from time import sleep

from requests.structures import CaseInsensitiveDict

# Number of Schools having Functional Toilet Facility by School Category and Management 
REPORT_ID = "3061"
MAP_ID = "64"
DB_PATH = "sqlite:///./data/functional_toilet_faciltiy_report_3601.sqlite"
RAW_FOLDER_PATH = "./raw/functional_toilet_faciltiy_report_3601/"
FILE_NAME_FORMAT = "{REPORT_ID}_{MAP_ID}_{LEVEL}_{STATE}_{DISTRICT}_{BLOCK}_{YEAR}.json"
YEARS = sorted(["2013-14","2014-15","2015-16","2016-17","2017-18","2018-19","2019-20"], reverse=True)
STATES = range(1, 38)

DB = dataset.connect(DB_PATH)

DB_REQUEST_INFO_TABLE = DB["request_info"]

def get_data(map_id, year, state):

    cookies = {
        'JSESSIONID': 'C0B970EABBA839E3C1861C74DF794DE9',
        'cookieWorked': 'yes',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain; charset=utf-8',
        'Origin': 'https://dashboard.udiseplus.gov.in',
        'Referer': 'https://dashboard.udiseplus.gov.in/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
    }

    data = '{"mapId":"'+map_id+'","dependencyValue":"{\\"year\\":\\"'+year+'\\",\\"state\\":\\"'+state+'\\",\\"dist\\":\\"none\\",\\"block\\":\\"none\\"}","isDependency":"Y","paramName":"civilian","paramValue":"","schemaName":"national","reportType":"T"}'
    print(data)
    response = requests.post('https://dashboard.udiseplus.gov.in/BackEnd-master/api/report/getTabularData', headers=headers, cookies=cookies, data=data)
    print(response)
    return response.json()

def write_data(data, file_name):
    f = open(file_name, "w") 
    f.write(json.dumps(data))
    f.close()


def format_state_code(s):
    s = s.zfill(2)
    return "" if s == "00" else s

def get_national_data():
    for year in YEARS:
        RAW_FILE_PATH = RAW_FOLDER_PATH + FILE_NAME_FORMAT.format(REPORT_ID=REPORT_ID, MAP_ID=MAP_ID, LEVEL="national", STATE="all", DISTRICT="NA", BLOCK="NA" ,YEAR=year)
        data = get_data(MAP_ID, year, state="national")
        write_data(data,RAW_FILE_PATH)
        db_data = {"map_id":MAP_ID, "report_id": REPORT_ID, "level":"national", "state":"national", "district":"NA", "block":"NA", "scraped":"yes", "parsed":"no", "file_path": RAW_FILE_PATH, "year": year}
        DB_REQUEST_INFO_TABLE.insert(db_data)
        input(" Continue ")

def get_state_data():
    for year in YEARS:
        for state in STATES:
            state_code = format_state_code(str(state))
            RAW_FILE_PATH = RAW_FOLDER_PATH + FILE_NAME_FORMAT.format(REPORT_ID=REPORT_ID, MAP_ID=MAP_ID, LEVEL="state", STATE=state_code, DISTRICT="NA", BLOCK="NA" ,YEAR=year)
            if DB_REQUEST_INFO_TABLE.find_one(file_path=RAW_FILE_PATH):
                print("EXISTS: {RAW_FILE_PATH}".format(RAW_FILE_PATH=RAW_FILE_PATH))
            else:
                DB.begin()
                data = get_data(MAP_ID, year, state=state_code)
                write_data(data,RAW_FILE_PATH)
                db_data = {"map_id":MAP_ID, "report_id": REPORT_ID, "level":"state", "state":state_code, "district":"NA", "block":"NA", "scraped":"yes", "parsed":"no", "file_path": RAW_FILE_PATH, "year": year}
                DB_REQUEST_INFO_TABLE.insert(db_data)
                DB.commit()
                #input(" Continue ")
                sleep(2)

def main():
    #NATIONAL LEVEL
    # get_national_data()

    #GET STATE LEVEL DATA, BY STATE
    get_state_data()

if __name__ == "__main__":
    main()
