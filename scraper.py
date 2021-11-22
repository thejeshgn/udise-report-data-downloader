import requests
import json
import dataset
import os.path
from os import path
from time import sleep

from requests.structures import CaseInsensitiveDict

# REPORT_ID = "3061"
# MAP_ID = "64"
# REPORT_NAME = "functional_toilet_facility_report_3061"

# REPORT_ID = "1003"
# MAP_ID = "81"
# REPORT_NAME = "number_of_schools_report_1003"

# REPORT_ID = "3031"
# MAP_ID = "54"
# REPORT_NAME = "schools_having_library_report_3031"


REPORT_ID = "3109"
MAP_ID = "80"
REPORT_NAME = "schools_having_computer_available_report_3109"

# REPORT_ID = "3106"
# MAP_ID = "79"
# REPORT_NAME = "schools_having_internet_facility_report_3106"

# REPORT_ID = "4017"
# MAP_ID = "117"
# REPORT_NAME = "student_dropout_rate_report_4017"

# REPORT_ID = "4014"
# MAP_ID = "113"
# REPORT_NAME = "student_promotion_repetition_dropout_report_4014"

RAW_FOLDER_PATH = "./raw/{REPORT_NAME}/".format(REPORT_NAME=REPORT_NAME)
DISTRICTS_JSON_DATA_FILE_PATH = "./raw/UDISE_Districts.json"
FILE_NAME_FORMAT = "{REPORT_ID}_{MAP_ID}_{LEVEL}_{STATE}_{DISTRICT}_{BLOCK}_{YEAR}.json"
YEARS = sorted(["2013-14","2014-15","2015-16","2016-17","2017-18","2018-19","2019-20"], reverse=True)
STATES = range(1, 38)

#DB_PATH = "sqlite:///./temp/{REPORT_NAME}.sqlite".format(REPORT_NAME=REPORT_NAME)
#DB = dataset.connect(DB_PATH)
#DB_REQUEST_INFO_TABLE = DB["request_info"]

def get_data(map_id, year, state, district="NA", block="NA"):

    cookies = {
        'JSESSIONID': 'FA731291610103E4793EFCA98238C102',
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
    if district == "NA":
        district = "none"
    data = '{"mapId":"'+map_id+'","dependencyValue":"{\\"year\\":\\"'+year+'\\",\\"state\\":\\"'+state+'\\",\\"dist\\":\\"'+district+'\\",\\"block\\":\\"none\\"}","isDependency":"Y","paramName":"civilian","paramValue":"","schemaName":"national","reportType":"T"}'
    print(data)
    response = requests.post('https://dashboard.udiseplus.gov.in/BackEnd-master/api/report/getTabularData', headers=headers, cookies=cookies, data=data)
    print(response)
    return response.json()

def write_data(data, file_name):
    f = open(file_name, "w") 
    f.write(json.dumps(data))
    f.close()

def pause(msg="Continue"):
    sleep(2)
    #input(msg)


def format_state_code(s):
    s = s.zfill(2)
    return "" if s == "00" else s

def get_national_data():
    for year in YEARS:
        RAW_FILE_PATH = RAW_FOLDER_PATH + FILE_NAME_FORMAT.format(REPORT_ID=REPORT_ID, MAP_ID=MAP_ID, LEVEL="national", STATE="all", DISTRICT="NA", BLOCK="NA" ,YEAR=year)
        if path.exists(RAW_FILE_PATH):        
            print("EXISTS")
        else:
            data = get_data(MAP_ID, year, state="national")
            write_data(data,RAW_FILE_PATH)
            db_data = {"map_id":MAP_ID, "report_id": REPORT_ID, "level":"national", "state":"national", "district":"NA", "block":"NA", "scraped":"yes", "parsed":"no", "file_path": RAW_FILE_PATH, "year": year}
            pause()

def get_state_data():
    print("----------------- STATES")    
    for year in YEARS:
        for state in STATES:
            state_code = format_state_code(str(state))
            RAW_FILE_PATH = RAW_FOLDER_PATH + FILE_NAME_FORMAT.format(REPORT_ID=REPORT_ID, MAP_ID=MAP_ID, LEVEL="state", STATE=state_code, DISTRICT="NA", BLOCK="NA" ,YEAR=year)

            if path.exists(RAW_FILE_PATH):
                print("EXISTS: {RAW_FILE_PATH}".format(RAW_FILE_PATH=RAW_FILE_PATH))
            else:
                data = get_data(MAP_ID, year, state=state_code)
                write_data(data,RAW_FILE_PATH)
                db_data = {"map_id":MAP_ID, "report_id": REPORT_ID, "level":"state", "state":state_code, "district":"NA", "block":"NA", "scraped":"yes", "parsed":"no", "file_path": RAW_FILE_PATH, "year": year}
                pause()

def get_district_data():
    print("----------------- DISTICTS")
    districts_json_data_file = open(DISTRICTS_JSON_DATA_FILE_PATH, "r")
    districts_json_data = json.loads(districts_json_data_file.read())
    districts = sorted(districts_json_data["rowValue"],  key=lambda x: x["udise_state_code"])
    districts_json_data_file.close()
    for year in YEARS:
        for district in districts:
            state_code = district["udise_state_code"]
            district_code = district["udise_district_code"] 
            district_name = district["district_name"] 
            RAW_FILE_PATH = RAW_FOLDER_PATH + FILE_NAME_FORMAT.format(REPORT_ID=REPORT_ID, MAP_ID=MAP_ID, LEVEL="district", STATE=state_code, DISTRICT=district_code, BLOCK="NA" ,YEAR=year)
            print(RAW_FILE_PATH)
            #input("wait")
            if path.exists(RAW_FILE_PATH):
                print("EXISTS: {RAW_FILE_PATH}".format(RAW_FILE_PATH=RAW_FILE_PATH))
            else:
                data = get_data(MAP_ID, year, state=state_code, district=district_code)
                write_data(data,RAW_FILE_PATH)
                db_data = {"map_id":MAP_ID, "report_id": REPORT_ID, "level":"district", "state":state_code, "district":district_code, "block":"NA", "scraped":"yes", "parsed":"no", "file_path": RAW_FILE_PATH, "year": year, "level_name": district_name}
                pause()

def main():
    print("----------------- RUNNING ---------------------")
    print("----------------- REPORT_ID={}".format(REPORT_ID))
    print("----------------- MAP_ID={}".format(MAP_ID))
    print("----------------- REPORT_NAME={}".format(REPORT_NAME))

    #NATIONAL LEVEL
    # get_national_data()

    #GET STATE LEVEL DATA, BY STATE
    get_state_data()

    # # GET DISTRICT LEVEL DATA, BY DISTRICT
    #get_district_data()

if __name__ == "__main__":
    main()
