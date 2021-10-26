import tabula
import pandas as pd
# !pip install tabula-py

#programe extracts the tabels from the PDF files.
# Need some Preprocessing to convert to RawCSV
#Have Done for KA and HR for reference

#declare the path of your file
file_path = r"../INPUT/2021-10-26/KA.pdf"
#Convert your file
# reads all the tables in the PDF
df = tabula.read_pdf(file_path,pages='all')
#Save the file 
df[6].to_csv('test_KA.csv')

#declare the path of your file
file_path = r"../INPUT/2021-10-26/HR.pdf"
#Convert your file
# reads all the tables in the PDF
df = tabula.read_pdf(file_path,pages='2')
#Save the file 
df[0].to_csv('test_HR.csv')

