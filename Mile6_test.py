##Import Needed Libraries
import streamlit as st
import urllib
from zipfile import ZipFile
from os import mkdir
from urllib.request import urlretrieve
from io import BytesIO
from urllib.request import urlopen
import time
import os
import pandas as pd
import numpy as np
import bs4 as bs
import urllib.request as url
import requests
from pathlib import Path

##############################################
## Identify local path to store zipped files
LocalPath = ""
outputDir = ""

#--------------------------------------------
def check_if_submit(submitted,File1):
    if submitted == True:
        # initialize list of lists
        # create DF
        outDF = pd.DataFrame(columns=['custID', 'fraudster'])
        custID = []
        fraudster = []
        for filename in File1:
            m = filename.split('.')
            custID.append(m[0])
            fraudster.append(0)
        outDF['custID'] = custID
        outDF['custID'] = outDF['custID'].str.strip()
        outDF['fraudster'] = fraudster
        # print(outDF)

        ##13 Read and format data in liveCustomerList file
        liveCustomerListName = "./liveCustomerList.csv"
        liveCustomerListPath = outputDir + liveCustomerListName
        liveCustomerListDF = pd.read_csv(liveCustomerListPath)
        liveCustomerListDF['firstName'] = liveCustomerListDF['firstName'].str.lower()
        liveCustomerListDF['lastName'] = liveCustomerListDF['lastName'].str.lower()
        liveCustomerListDF['firstName'] = liveCustomerListDF['firstName'].str.strip()
        liveCustomerListDF['lastName'] = liveCustomerListDF['lastName'].str.strip()

        ##14 Read and format data in liveFraudList file
        liveFraudListName = "./liveFraudList.csv"
        liveFraudListPath = outputDir + liveFraudListName
        liveFraudListDF = pd.read_csv(liveFraudListPath)
        liveFraudListDF['firstName'] = liveFraudListDF['firstName'].str.lower()
        liveFraudListDF['lastName'] = liveFraudListDF['lastName'].str.lower()
        liveFraudListDF['firstName'] = liveFraudListDF['firstName'].str.strip()
        liveFraudListDF['lastName'] = liveFraudListDF['lastName'].str.strip()

        ##15 Create Fraud List DF from liveCustomerList and liveFraudList
        fraudsterDF = pd.merge(left=liveFraudListDF, right=liveCustomerListDF, how="left", on=["firstName", "lastName"])
        fraudsterDF['custID'] = fraudsterDF['custID'].astype(str)

        ##16 toggle 0 to 1 for fraudster detection
        outDF['fraudster'] = np.where(outDF['custID'].isin(fraudsterDF['custID']), 1, 0)
        return outDF

def convert_df(outDF):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    if submitted == True:
        #st.write("inside convert function")
        #st.write(outDF)
        #OutPut_Path = os.path.abspath(resp1)
        #if os.path.exists(OutPut_file):
        #    os.remove(OutPut_Path)
        df1 = outDF.to_csv(index = False).encode('utf-8')
        return df1

def get_url_file_name(text):
    #thepage = urllib.request.urlopen(text).read()
    filename = str(text).split("/")[-1].split("?")[0]
    print("before filename")
    print(filename)
    OutPut_file = filename.replace(".zip", ".csv")
    print("before outfilename")
    print(OutPut_file)
    return OutPut_file
#----------------------------------------------------------------
st.set_page_config(layout="wide")
#with col1:
st.title('Welcome to Milestone 6')

st.header("Step1: Provide Milestone 2 Input file")
text = st.text_input('Enter URL of test Data')   # text= Apple


submitted = st.button('submit') # submitted a boolean value = True
#-------------------------------------------
if len(text) > 1 and submitted == True:
    st.write('the link:')
    resp = requests.get(text)
    re = st.write(text)
    IPFileFolder = "./dropbox_"+datetime.now()
    IPFilePath = LocalPath + IPFileFolder
    #resp1 = get_url_file_name(text)


    # zipurl = 'https://www.dropbox.com/s/m59grf09cpe1y1u/sampleFraudTestInput.zip?dl=1'
    #with urlopen(resp) as zipresp:
    with ZipFile(BytesIO(resp.content)) as zfile:
         zfile.extractall(IPFilePath)



    ##12 extract customer Ids from the images in url location
    File1 = os.listdir(IPFilePath)
    #st.write(File1)
#--------------------------------------------------------------------------

    st.header("Step2: Download Fraudster detection results")
    st.write("When result is ready to download, you will get an alert")
#----------------------------------------------------------------------------
#--------------------------------------------------------------------

    df2 = check_if_submit(submitted,File1)   # df dataframe is returned
    #st.dataframe(df1)
    #st.write("Inside if true")
    #resp1 = get_url_file_name(text)
    csv = convert_df(df2)

    downloaded = st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=str(text).split("/")[-1].split("?")[0].replace(".zip", ".csv"),
        mime='text/csv',
    )
elif submitted == False:
    st.write("Submit with a new URL or Close the window")

#--------------------------------------------------------------------
if __name__ == '"__main__"':
     main()



