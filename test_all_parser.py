from src.preprocessing.document_parser import DocumentParser


parser = DocumentParser()


documents = parser.parse_all_documents()


print("\n========== SAMPLE OUTPUT ==========")


for doc in documents[:3]:

    print("----------------------")
    print("File:", doc.manual_name)
    print("Type:", doc.source_type)
    print("Title:", doc.title)
    print(doc.text[:200])