import argparse
from fetch_dpmms import fetch_dpmms
from fetch_dampt import fetch_dampt
import os, requests, shutil

def fetch_sheet(sheetarr) -> str:
   if not os.path.exists('pdfs'):
      os.makedirs('pdfs')
   filepath = f"pdfs/{id}.pdf"

   if not os.path.exists(filepath):
      print(f"couldn't find {sheetarr[1]}, sheet number {sheetarr[2]}, fetching to {filepath}")
      with requests.get(sheetarr[0], stream=True) as r:
         with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

   return filepath


parser = argparse.ArgumentParser(description='Fetch cambridge maths example sheets.')
parser.add_argument('outdir', metavar='outdir', type=str, nargs=1,
                    help='directory to store sheets in')
args = parser.parse_args()

print("Indexing dpmms...")
sheets = fetch_dpmms()
print("Indexing dampt...")
sheets += fetch_dampt()

for sheet in sheets:
    print(f"Fetching {args.outdir[0]}/{sheet[1]}/{sheet[1]}-{sheet[2]}.pdf")
    if not os.path.exists(f'{args.outdir[0]}/{sheet[1]}/'):
        os.makedirs(f'{args.outdir[0]}/{sheet[1]}/')
    filepath = f"{args.outdir[0]}/{sheet[1]}/{sheet[1]}-{sheet[2]}.pdf"

    with requests.get(sheet[0], stream=True) as r:
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

