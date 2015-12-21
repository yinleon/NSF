from bs4 import BeautifulSoup
import os
import sys
from collections import OrderedDict
import time
import json

# for testing...
path = '2016'
# for automation...
paths = [str(x) for x in range(2010,2017)]


# Initiate globals
def main(path):
    outfiles= ["NSF_AWARDS_"+path+".json",
               "NSF_ABSTRACT_"+path+".json",
               "NSF_INSTITUTIONS_"+path+".json",
               "NSF_PI_"+path+".json",
               "NSF_DIVISION_"+path+".json"]
   
    d1_list = []
    d2_list = []
    d3_list = []
    d4_list = []
    d5_list = []

    def xml_parse(file):
        handler = open(file,'r',encoding='utf8').read()
        # get the xml file into soup
        soup = BeautifulSoup(handler,"lxml")
        soup.prettify()

        # sectional soups
        soup2= soup.find("institution")
        soup3 = soup.find("investigator")
        soup4 = soup.find("organization")

        # awards
        try:
            # some shared qualities
            award = soup.find("awardid").string
            university = soup2.find("name").string
            nsf_division = soup4.find("division").find("longname").string
            email = soup3.find("emailaddress").string
            
            d1_list.append(
                OrderedDict(
                    [('award_id',award),
                     ('award_title',soup.find("awardtitle").string),
                     ('award_effective_date',soup.find("awardeffectivedate").string),
                     ('award_expiration_date',soup.find("awardexpirationdate").string),
                     ('award_amount',soup.find("awardamount").string),
                     ('institution_name',university),
                     ('division',nsf_division),
                     ('email_address',email)]
                )
            )
        except:
            return
        # abstract
        try:
            d2_list.append(
                OrderedDict([
                    ('award_id',award),
                    ('abstract_narration',soup.find('abstractnarration').string.strip())]
                )
            )
        except:
            return

        # institution
        try:
            d3_list.append(
                OrderedDict(
                    [('institution_name',university),
                     ('city_name',soup2.find("cityname").string),
                     ('phone_number',soup2.find("phonenumber").string),
                     ('street_address',soup2.find("streetaddress").string),
                     ('country_name',soup2.find("countryname").string),
                     ('state_name',soup2.find("statename").string),
                     ('state_code',soup2.find("statecode").string)]
                )
            )
        except:
            return

        # PI
        try:
            d4_list.append(
                OrderedDict(
                    [('first_name',soup3.find("firstname").string),
                     ('last_name',soup3.find("lastname").string),
                     ('email_address',email),
                     ('institution_name',soup2.find("name").string)]
                )
            )
        except:
            return

        # Division
        try:
            d5_list.append(
                OrderedDict(
                    [('code',soup4.find("code").string),
                     ('directorate',soup4.find("directorate").find("longname").string),
                     ('division',nsf_division)]
                )
            )
        except:
            return

    def json_dump():
        dict_NSF = [d1_list, d2_list, d3_list, d4_list, d5_list]
        for i in range(len(dict_NSF)):
            # remove duplicates
            dict_NSF[i] = [j for n, j in enumerate(dict_NSF[i]) if j not in dict_NSF[i][n + 1:]]
            # dump the dictionary into a JSON
            with open(outfiles[i], 'w') as outfile:
                json.dump(dict_NSF[i], outfile, indent=4)

    # main script
    start = time.time()
    count = 0
    # iterate through the path directory
    for file in os.listdir('data/'+path):
        xml_parse(os.path.join('data/'+path,file))
        count += 1
    print("Scraped", count,"records in", round(time.time()-start, 2), "sec.")   
    json_dump()
    #TODO: create a SQL or noSQL dump!

# call for each year
main('2010')

'''
# iterate through each year
for path in paths:
    main(path)
'''
       