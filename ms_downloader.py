import PyPDF2
import requests
import os
import re


def gen_paper_type(is_ms):
    if is_ms:
        return "ms"
    else:
        return "qp"


class paper:
    def __init__(self, code, year, season, paper_no, is_ms):
        self.code = str(code)
        self.year = str(year)
        self.season = str(season)
        self.paper_no = str(paper_no)
        self.is_ms = is_ms

        self.url = self.create_url()
        self.path = self.path_gen()
        self.id = None

    def create_url(self):
        table = {"9618": "computer-science-(9618)",
                 "9708":"economics-(9708)"}
        base_url = "https://papers.gceguide.cc/a-levels"
        
        code = str(self.code)
        year = str(self.year)
        season = str(self.season)
        paper_no = str(self.paper_no)
        


        url = f"{base_url}/{table[code]}/{year}/{code}_{season}{year[-2:]}_{gen_paper_type(self.is_ms)}_{paper_no}.pdf"

        return url

    def path_gen(self):

        path = f"./mark_schemes/{self.code}/{self.year}/{self.season}{self.paper_no}_{gen_paper_type(self.is_ms)}.pdf"

        return path


    def __str__(self) -> str:
        return self.url


    def exists(self):
        return os.path.exists(self.path)


    def gen_metadata(self):
        return {"subject_code": self.code,
                "year": self.year,
                "season": self.season,
                "paper_no": self.paper_no,
                "is_ms": self.is_ms,
                "url" : self.url,
                "path": self.path
                }

    def gen_id(self):
        if self.id:
            self.id += 1
        else:
            self.id = 0
        return self.url+"_"+str(self.id)


class pdf_manager:
    def download(self, paper):
        response = requests.get(paper.url, stream=True)

        if response.status_code == 200:
            directory = os.path.dirname(paper.path)
            if not os.path.exists(directory):
                os.makedirs(directory)


            filepath = paper.path
            with open(filepath, 'wb') as pdf_object:
                pdf_object.write(response.content)
                return True
        else:
            print(f'Uh oh! Could not download {paper},')
            print(f'HTTP response status code: {response.status_code}')
            return False


    def get_text(self, paper):
        path = paper.path

        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Extract text from each page
            text = []
            for (page_no, page) in enumerate(reader.pages[1:]):
                page_text = page.extract_text()
                lines = page_text.split("\n")

                if lines[0].strip() == str(page_no + 2):
                    lines.pop(0)

                if "BLANK PAGE" in page_text:
                    continue

                page_text = [line for line in lines if "© UCLES 20" not in line]
                page_text = "\n".join(page_text)



                text.append(page_text)

        pages = text
        text = "\n".join(text)
            

        return pages

    def split_text(self, text):
        question_split = r"(\[[0-9]{1,2}\])"
        # sub_part_split = r"\n\s+(?=\([a-h]\))"
        # sub_sub_part_split = r"\n\s+(?=\([ivx]+\))"


        #Splits the papers based on marks
        parts = re.split(question_split, text)
        result = []

        if parts[-1] == "":
            parts.pop(-1)

        #adds marks back after removing it
        for i in range(0, len(parts), 2):
            result.append(parts[i] + parts[i+1] if i + 1 < len(parts) else parts[i])



        return result






