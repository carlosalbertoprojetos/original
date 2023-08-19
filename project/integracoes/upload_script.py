# https://www.youtube.com/watch?v=xOSfXi98x1o
# https://www.geeksforgeeks.org/upload-files-in-python/

import cgi, os, sys
from django.shortcuts import render

form = cgi.FieldStorage()
fileitem = form['ArquivoXML'].value
print(fileitem)


my_xml = []
if fileitem.ArquivoXML:
    fn = os.path.basename(fileitem.ArquivoXML)
    open(fn, 'r', encoding='utf-8').write(fileitem.file.read())
    with open(fn, 'r', encoding='utf-8') as file:
        my_xml = file.read()



my_dict = xmltodict.parse(my_xml)

print(my_dict)





import xmltodict



# Open the file and read the contents
# with open('C:\\PROJETOS\\TRABALHOS\\INTIP\ERP\\erp\\project\\integracoes\\arq.xml', 'r', encoding='utf-8') as file:
# with open('C:\\xml\\32230101754239000896550010005912221000247546.xml', 'r', encoding='utf-8') as file:
#     my_xml = file.read()

# # Use xmltodict to parse and convert the 
# # XML document
# my_dict = xmltodict.parse(my_xml)

# print(my_dict)


# https://www.stechies.com/upload-files-python/

# import os
# fi = form['filename']
# if fi.filename:
# 	# This code will strip the leading absolute path from your file-name
# 	fil = os.path.basename(fi.filename)
# 	# open for reading & writing the file into the server
# 	open(fn, 'wb').write(fi.file.read())



# https://www.youtube.com/watch?v=pPSZpCVRbvQ
# def af(request):
#     if request.method == 'POST':
#         file = request.files['ArquivoXML']
#         return print(file)



import xmltodict

def get(request):
    template_name = 'notafiscal/uploadxml.html'
    form = (request.POST or None, request.FILE)

    if request.method == 'POST':
        with open(form, 'r', encoding='utf-8') as file:
            my_xml = file.read()
            my_dict = xmltodict.parse(my_xml)
            print(my_dict)

    context = {
        'form': form
    }
    return render(request, template_name, context)