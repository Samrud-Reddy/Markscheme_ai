import requests
import os


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

    def create_url(self):
        table = {"9618": "computer-science-(9618)"}
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
        


class pdf_downloader:
    def __init__(self) -> None:
        pass


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





