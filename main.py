import zipfile
import shutil
import json
import os
import requests
# from pprint import pprint

# dimensions for outputted qr.png
QR_SIZE = 200
PASS = 'passes/a.pkpass'

# extraction directory for apple wallet pass (.pkpass)
if os.path.isdir('extracted'):
    shutil.rmtree('extracted')

# make sure you're passing the right filetype
if not PASS.lower().endswith('.pkpass'):
    print ("File type must be of type 'pkpass'. You provided '%s'." % PASS.split('.')[-1])
    exit()

# extract the apple wallet pass; I think it's just a zip
zip_ref = zipfile.ZipFile(PASS, 'r')
zip_ref.extractall('./extracted')
zip_ref.close()

# pass.json has all the ticket details we want to parse
with open('./extracted/pass.json') as data_file:
    data = json.load(data_file)

# some example parsing (not sure how the format differs across events)
date_time = data["relevantDate"].split("T")
date = date_time[0]
time = date_time[1]

event_info = "Event info: performer: %s, venue: %s, date: %s, time: %s" % (data["eventTicket"]["secondaryFields"][0]["value"], data["eventTicket"]["secondaryFields"][0]["label"], date, time)
seat_info = "Seat info: section %s, row %s, seat %s" % (data["eventTicket"]["auxiliaryFields"][0]["value"], data["eventTicket"]["auxiliaryFields"][1]["value"], data["eventTicket"]["auxiliaryFields"][2]["value"])
# might be additional seat_info
if len(data["eventTicket"]["auxiliaryFields"]) > 3:
    seat_info += ", additional info: " + data["eventTicket"]["auxiliaryFields"][3]["value"]
# note: PKBarcodeFormatQR = "PassKit" (Apple) format https://developer.apple.com/library/content/documentation/UserExperience/Reference/PassKit_Bundle/Chapters/LowerLevel.html
barcode_info = "Barcode info: message: %s, encoding: %s, format: %s" % (data["barcode"]["message"], data["barcode"]["messageEncoding"], data["barcode"]["format"])

# google has an API to generate QR codes (this generates the exact QR code shown in wallet)
# https://developers.google.com/chart/infographics/docs/qr_codes
qr_url = "https://chart.googleapis.com/chart?cht=qr&chld=M&chl=" + data["barcode"]["message"] + "&choe=" + data["barcode"]["messageEncoding"] + "&chs=" + str(QR_SIZE) + "x" + str(QR_SIZE)
r = requests.get(qr_url)
if (r.status_code == requests.codes.ok):
    image_name = PASS.split('/')[-1].split('.')[0] + ".png"
    qr_img = open(image_name, "w")
    qr_img.write(r.content)
    qr_img.close()

# can delete the extracted folder now
if os.path.isdir('extracted'):
    shutil.rmtree('extracted')

print(event_info)
print(seat_info)
print(barcode_info)
# pprint(data)
