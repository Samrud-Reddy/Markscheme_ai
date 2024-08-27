import chromadb
import vectordb
import ms_downloader

storage_path = "/home/DodoReddy/code/markscheme-ai/chromadb"

pdf = ms_downloader.pdf_manager()


db = {"comp_sci": vectordb.vectordb("./chromadb/", "Comp"),
    "eco": vectordb.vectordb("./chromadb/", "eco")
      }




def upload(paper, db):
    if not paper.exists():
        return
    text = pdf.get_text(paper)
    text = "\n\n".join(text)
    split = pdf.split_text(text)

    for i in split:
        db.add(paper.gen_id(), i, paper.gen_metadata())






def search_db(code, question):

    query = db[code].query(question, 10)
    
    metadata = query["metadatas"][0]
    document = query["documents"][0]
        
    return {"metadata": metadata,
            "document": document,
            }
