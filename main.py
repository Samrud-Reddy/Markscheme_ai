import chromadb
import vectordb
import ms_downloader

storage_path = "/home/DodoReddy/code/markscheme-ai/chromadb"

pdf = ms_downloader.pdf_downloader()

paper = ms_downloader.paper(9618, 2021, "s", 42, True)
print(paper.create_url())
print(pdf.download(paper))



