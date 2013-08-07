import pprint
import csv

address = "https://spreadsheets.google.com/feeds/list/0ArNEXxu0b66PdHpNS3o1bnVDOVNPRHFKcnoxNEd5cXc/od6/public/basic?alt=csv"

pp = pprint.PrettyPrinter(indent=4)

def get_keywords_xml(_address):
    feeds = data = csv.reader(open(_address))
    return feeds

def get_keywords_from_spreadsheet():
    pass

xml = get_keywords_xml(address)
pp.pprint(xml)