import requests
from client.client_types.document import Document


def visit_page(url: str) -> Document:
    try:
        req = requests.get(url)
        raw = req.text
    except Exception as error:
        raw = f"<label>Error! Did not reach server.</label><label>{error}</label>"

    return Document(raw).parse()
