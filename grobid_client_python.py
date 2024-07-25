from grobid_client.grobid_client import GrobidClient

client = GrobidClient(config_path="./config.json")
# client.process("processFulltextDocument", input_path="./ref_papers", output="./ref_papers_xml", consolidate_citations=True, tei_coordinates=True, force=True)
client.process("processFulltextDocument", input_path="./query_paper", output="./query_paper_xml", consolidate_citations=True, tei_coordinates=True, force=True)

print("All PDFs parsed successfully !")
