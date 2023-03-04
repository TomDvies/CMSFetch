import argparse
from fetch_dpmms import fetch_dpmms
from fetch_dampt import fetch_dampt
import os, requests, shutil
from fetch_papers import fetch_papers


parser = argparse.ArgumentParser(description='Fetch cambridge maths example sheets.')
parser.add_argument('outdir', metavar='outdir', type=str, nargs=1,
                    help='directory to store sheets in')
args = parser.parse_args()

print("Indexing dpmms...")
sheets = fetch_dpmms()
print("Indexing dampt...")
sheets += fetch_dampt()
print("Indexing past papers...")
papers = fetch_papers()

for sheet in sheets:
    print(f"Fetching {args.outdir[0]}/sheets/{sheet[1]}/{sheet[1]}-{sheet[2]}.pdf")
    if not os.path.exists(f'{args.outdir[0]}/sheets/{sheet[1]}/'):
        os.makedirs(f'{args.outdir[0]}/sheets/{sheet[1]}/')
    filepath = f"{args.outdir[0]}/sheets/{sheet[1]}/{sheet[1]}-{sheet[2]}.pdf"

    with requests.get(sheet[0], stream=True) as r:
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

for paper in papers:
    outpath = f"{args.outdir[0]}/pastpapers/{paper[1]}/{paper[2]}"
    if paper[3] != "All questions":
        name = f"{paper[1]}-{paper[2]}-paper-{paper[3]}.pdf"
        print(f"Fetching {name}")
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        filepath = outpath+"/"+name
        with requests.get(paper[0], stream=True) as r:
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    else:
        name = f"{paper[1]}-{paper[2]}-all-questions.pdf"
        print(f"Fetching {outpath}/{name}")
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        filepath = outpath+"/"+name
        with requests.get(paper[0], stream=True) as r:
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
