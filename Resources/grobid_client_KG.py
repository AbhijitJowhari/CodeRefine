from grobid_client.grobid_client import GrobidClient

client = GrobidClient(config_path="./config.json")
client.process("processFulltextDocument", input_path="./papers", output="./papers_xml", consolidate_citations=True, tei_coordinates=True, force=True)