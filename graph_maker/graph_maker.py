from .types import Ontology, LLMClient, Edge, Document
from .llm_clients.groq_client import GroqClient
from pydantic import ValidationError
import json
import re
from .logger import GraphLogger
from typing import List, Union
import time

green_logger = GraphLogger(name="GRAPH MAKER LOG", color="green_bright").getLogger()
json_parse_logger = GraphLogger(name="GRAPH MAKER ERROR", color="magenta").getLogger()
verbose_logger = GraphLogger(name="GRAPH MAKER VERBOSE", color="blue").getLogger()

default_ontology = Ontology(
    labels=[
        {"Person": "Person name without any adjectives"},
        "Place",
        "Object",
        "Document",
        "Concept",
        "Organisation",
        "Event",
        "Action",
    ],
    relationships=["Relationship between Any two labeled entities"],
)
default_nearest_5 = '''[
    {
        "Hacking with LLMs. : To the best of our knowledge, there is currently no darknet-offered LLM-aided penetration testing tool. But, as the other areas have shown, this is just a question of time.": [
            {
                "node_1": {
                    "label": "Research Paper",
                    "name": "Hacking with LLMs"
                },
                "node_2": {
                    "label": "Tool",
                    "name": "LLM-aided penetration testing tool"
                },
                "relationship": "Proposes the future development of an LLM-aided penetration testing tool, which is currently not available on the darknet."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "LLM-aided penetration testing tool"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Darknet"
                },
                "relationship": "Anticipates that LLM-aided penetration testing tools will eventually be offered on the darknet."
            },
            {
                "node_1": {
                    "label": "Miscellaneous",
                    "name": "Darknet"
                },
                "node_2": {
                    "label": "Tool",
                    "name": "LLM-aided penetration testing tool"
                },
                "relationship": "Speculates that LLM-aided penetration testing tools will become available on the darknet in the future."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "LLM-aided penetration testing tool"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Time"
                },
                "relationship": "Indicates that the emergence of LLM-aided penetration testing tools is only a matter of time."
            }
        ]
    },
    {
        "Baselines : As prior works use different setups and do not use LLMs, they are hard to compare directly. Instead, we use the following three LLM-based baselines.": [
            {
                "node_1": {
                    "label": "Miscellaneous",
                    "name": "Prior Works"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Different Setups"
                },
                "relationship": "Describes the challenge of comparing prior works due to their use of different experimental setups and the absence of LLMs."
            },
            {
                "node_1": {
                    "label": "Miscellaneous",
                    "name": "Prior Works"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "LLMs"
                },
                "relationship": "Explains that prior works did not use LLMs, making direct comparisons difficult."
            },
            {
                "node_1": {
                    "label": "Miscellaneous",
                    "name": "Baselines"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Three LLM-based Baselines"
                },
                "relationship": "Introduces three LLM-based baselines to address the comparison challenge presented by prior works."
            }
        ]
    },
    {
        "Comparing LLMs to Human Pen-Testers : As our research concerns the offensive use of LLMs, ethical considerations are warranted. LLMs are already in use by darknet operators (Section 2.2) so we cannot contain their threat anymore. Blue Teams can only benefit from understanding the capabilities and limitations of LLMs in the context of penetration testing. Our work provides insights (Section 6.4) that can be leveraged to differentiate attack patterns LLMs from human operators.": [
            {
                "node_1": {
                    "label": "Miscellaneous",
                    "name": "LLMs"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Human Pen-Testers"
                },
                "relationship": "Compares LLMs to human penetration testers, focusing on their offensive capabilities and ethical implications."
            },
            {
                "node_1": {
                    "label": "Miscellaneous",
                    "name": "LLMs"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Darknet Operators"
                },
                "relationship": "Mentions that LLMs are currently used by darknet operators, which amplifies their threat potential."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "LLMs"
                },
                "node_2": {
                    "label": "Machine Learning Task",
                    "name": "Offensive Use in Penetration Testing"
                },
                "relationship": "Examines how LLMs can be applied to offensive tasks within the field of penetration testing."
            },
            {
                "node_1": {
                    "label": "Research Paper",
                    "name": "Comparing LLMs to Human Pen-Testers"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Ethical Considerations"
                },
                "relationship": "Discusses the ethical considerations associated with the offensive use of LLMs."
            },
            {
                "node_1": {
                    "label": "Miscellaneous",
                    "name": "Blue Teams"
                },
                "node_2": {
                    "label": "Tool",
                    "name": "LLMs"
                },
                "relationship": "Suggests that Blue Teams (defensive security teams) can benefit from understanding LLM capabilities and limitations in penetration testing."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "LLMs"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Penetration Testing"
                },
                "relationship": "Focuses on the role of LLMs in penetration testing."
            },
            {
                "node_1": {
                    "label": "Research Paper",
                    "name": "Comparing LLMs to Human Pen-Testers"
                },
                "node_2": {
                    "label": "Tool",
                    "name": "LLMs"
                },
                "relationship": "Explores how LLMs compare to human penetration testers in various attack scenarios."
            },
            {
                "node_1": {
                    "label": "Research Paper",
                    "name": "Comparing LLMs to Human Pen-Testers"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Insights"
                },
                "relationship": "Provides insights into differentiating between attack patterns of LLMs and human operators."
            },
            {
                "node_1": {
                    "label": "Miscellaneous",
                    "name": "Section 6.4"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Insights"
                },
                "relationship": "References Section 6.4 for insights on differentiating LLMs from human operators in attack patterns."
            }
        ]
    },
    {
        "Double Quantization : We use NF4 for W and FP8 for c2. We use a blocksize of 64 for W for higher quantization precision and a blocksize of 256 for c2 to conserve memory.": [
            {
                "node_1": {
                    "label": "Tool",
                    "name": "NF4 for W"
                },
                "node_2": {
                    "label": "Tool",
                    "name": "FP8 for c2"
                },
                "relationship": "Describes the use of NF4 for W and FP8 for c2 as quantization techniques for different variables."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "NF4 for W"
                },
                "node_2": {
                    "label": "Method",
                    "name": "Double Quantization"
                },
                "relationship": "Indicates that NF4 for W is utilized within the method of Double Quantization."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "FP8 for c2"
                },
                "node_2": {
                    "label": "Method",
                    "name": "Double Quantization"
                },
                "relationship": "Specifies that FP8 for c2 is applied within the method of Double Quantization."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "NF4 for W"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Higher Quantization Precision"
                },
                "relationship": "Highlights that NF4 for W is chosen for its ability to provide higher quantization precision."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "FP8 for c2"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Conserve Memory"
                },
                "relationship": "Notes that FP8 for c2 is selected to conserve memory during the quantization process."
            }
        ]
    },
    {
        "Hacking with LLMs. : pentestGPT uses HackTheBox cloud-based virtual machines for their evaluation. To allow for greater control, our benchmark is based upon locally generated and operated virtual machines. By narrowing the scope to Linux privilege-escalation vulnerabilities, we are able to more deeply analyze the differences between the different LLMs hoping that future research can base their model selection upon firmer foundations. Our benchmark environment is released as open source on github.": [
            {
                "node_1": {
                    "label": "Tool",
                    "name": "pentestGPT"
                },
                "node_2": {
                    "label": "Tool",
                    "name": "HackTheBox Cloud-based Virtual Machines"
                },
                "relationship": "Uses HackTheBox cloud-based virtual machines to evaluate pentestGPT."
            },
            {
                "node_1": {
                    "label": "Tool",
                    "name": "pentestGPT"
                },
                "node_2": {
                    "label": "Tool",
                    "name": "Locally Generated and Operated Virtual Machines"
                },
                "relationship": "Also utilizes locally generated and operated virtual machines for more controlled evaluations of pentestGPT."
            },
            {
                "node_1": {
                    "label": "Dataset",
                    "name": "Linux Privilege-escalation Vulnerabilities"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Differences between Different LLMs"
                },
                "relationship": "Focuses on Linux privilege-escalation vulnerabilities to analyze differences among various LLMs."
            },
            {
                "node_1": {
                    "label": "Dataset",
                    "name": "Linux Privilege-escalation Vulnerabilities"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Future Research"
                },
                "relationship": "Aims to provide a foundation for future research in model selection based on the analysis of Linux privilege-escalation vulnerabilities."
            },
            {
                "node_1": {
                    "label": "Experimental Setup",
                    "name": "Benchmark Environment"
                },
                "node_2": {
                    "label": "Miscellaneous",
                    "name": "Open Source on GitHub"
                },
                "relationship": "Releases the benchmark environment as open source on GitHub to facilitate broader research and replication."
            }
        ]
    }
]'''


class GraphMaker:
    _ontology: Ontology
    _Nearest_5 : str
    _llm_client: LLMClient
    _model: str
    _verbose: bool

    def __init__(
        self,
        ontology: Ontology = default_ontology,
        nearest_5 : str = default_nearest_5,
        llm_client: LLMClient = GroqClient(
            model="mixtral-8x7b-32768", temperature=0.2, top_p=1
        ),
        verbose: bool = False,
    ):
        self._ontology = ontology
        self._llm_client = llm_client
        self._verbose = verbose
        self._Nearest_5 = nearest_5
        if self._verbose:
            verbose_logger.setLevel("INFO")
        else:
            verbose_logger.setLevel("DEBUG")

    def user_message(self, text: str) -> str:
        return f"input text: ```\n{text}\n```"

    def system_message(self) -> str:
        return (
            "You are an expert at creating Knowledge Graphs. You will create a knowledge graph for each of the text_chunk element in the list. This knowledge graph will be put in a generative machine learning model which will try to write python code which is explained by the knowledge graph output by you. So make sure you catch the entities and relationships from the text chunks which are 'code-oriented' ."
            "Consider the following ontology. \n"
            f"{self._ontology} \n"
            "Extract all the entities and relationships from the user-provided text as per the given ontology. Do not use any previous knowledge about the context."
            "Extract all the entities and relationships which are technically sound so that the knowledge graph so formed can be used by a machine learning program to write corresponding code "
            "Remember there can be multiple direct (explicit) or implied relationships between the same pair of nodes. "
            "Be consistent with the given ontology. Use ONLY the labels and relationships mentioned in the ontology. "
            "Consder the below example. Construct the relationship as a complete 'description' not just a keyword. \n"
            f"{self._Nearest_5}"
            "The above example has the structure : \n"
	    " [ {text_chunk} : {The corresponding Knowledge graph structure of the text chunk}]"
	    "understand the coherence between the text chunk and its corresponding knowledge graph structure."
            "Format your output as a json with the following schema. \n"
            "[\n"
            "   {\n"
            '       node_1: Required, an entity object with attributes: {"label": "as per the ontology", "name": "Name of the entity"},\n'
            '       node_2: Required, an entity object with attributes: {"label": "as per the ontology", "name": "Name of the entity"},\n'
            "       relationship: It is the description of the relationship between the 2 nodes 1 and 2. Make sure this description pertains to one of the keywords given in the 'relationship' attribute of Ontology.\n"
            "   },\n"
            "]\n"
            "Do not add any other comment before or after the json. Respond ONLY with a well formed json that can be directly read by a program."
	    "But NOTE that your output should be only of the above json format and not the examples provided to you. These examples only serve the purpose to make you understand how the input(text chunk) and the output are related to each other"
	    "Do not output any exaplantion, just a json structure of the output json format given to you."
        )

    def generate(self, text: str) -> str:
        # verbose_logger.info(f"SYSTEM_PROMPT: {self.system_message()}")
        response = self._llm_client.generate(
            user_message=self.user_message(text),
            system_message=self.system_message(),
        )
        return response

    def parse_json(self, text: str):
        green_logger.info(f"Trying JSON Parsing: \n{text}")
        try:
            parsed_json = json.loads(text)
            green_logger.info(f"JSON Parsing Successful!")
            return parsed_json
        except json.JSONDecodeError as e:
            json_parse_logger.info(f"JSON Parsing failed with error: { e.msg}")
            verbose_logger.info(f"FAULTY JSON: {text}")
            return None

    def manually_parse_json(self, text: str):
        green_logger.info(f"Trying Manual Parsing: \n{text}")
        pattern = r"\}\s*,\s*\{"
        stripped_text = text.strip("\n[{]} ")
        # Split the json string into string of objects
        splits = re.split(pattern, stripped_text, flags=re.MULTILINE | re.DOTALL)
        # reconstruct object strings
        obj_string_list = list(map(lambda x: "{" + x + "}", splits))
        edge_list = []
        for string in obj_string_list:
            try:
                edge = json.loads(string)
                edge_list.append(edge)
            except json.JSONDecodeError as e:
                json_parse_logger.info(f"Failed to Parse the Edge: {string}\n{e.msg}")
                verbose_logger.info(f"FAULTY EDGE: {string}")
                continue
        green_logger.info(f"Manually exracted {len(edge_list)} Edges")
        return edge_list

    def json_to_edge(self, edge_dict):
        try:
            edge = Edge(**edge_dict)
        except ValidationError as e:
            json_parse_logger.info(
                f"Failed to parse the Edge: \n{e.errors(include_url=False, include_input=False)}"
            )
            verbose_logger.info(f"FAULTY EDGE: {edge_dict}")
            edge = None
        finally:
            return edge

    def from_text(self, text):
        response = self.generate(text)
        verbose_logger.info(f"LLM Response:\n{response}")

        json_data = self.parse_json(response)
        if not json_data:
            json_data = self.manually_parse_json(response)

        edges = [self.json_to_edge(edg) for edg in json_data]
        edges = list(filter(None, edges))
        return edges

    def from_document(
        self, doc: Document, order: Union[int, None] = None
    ) -> List[Edge]:
        verbose_logger.info(f"Using Ontology:\n{self._ontology}")
        graph = self.from_text(doc.text)
        for edge in graph:
            edge.metadata = doc.metadata
            edge.order = order
        return graph

    def from_documents(
        self,
        docs: Document,
        order_attribute: Union[int, None] = None,
        delay_s_between=0,
    ) -> List[Edge]:
        graph: List[Edge] = []
        for index, doc in enumerate(docs):
            ## order defines the chronology or the order in which the documents should in interpretted.
            order = getattr(doc, order_attribute) if order_attribute else index
            green_logger.info(f"Document: {index+1}")
            subgraph = self.from_document(doc, order)
            graph = [*graph, *subgraph]
            time.sleep(delay_s_between)
        return graph
