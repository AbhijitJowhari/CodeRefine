from graph_maker import GraphMaker, Ontology, GroqClient
from graph_maker import Document
from mixedbread_ai.client import MixedbreadAI
import datetime
import json
import subprocess
from openai import OpenAI
import os
from groq import Groq

from create_dynamic_database import *
from extract_query_paper import *
from extract_query_paras import *
from RRAG import *

################## ALL API CLIENTS AND MODEL INSTANCES GO HERE ##################
client_openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
mxbai = MixedbreadAI(api_key=os.environ.get("MXBAI_API_KEY"))
groq_client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)
GPT4o="gpt-4o"
embeddings_model = "mixedbread-ai/mxbai-embed-2d-large-v1"
# KG_builder_model = "mixtral-8x7b-32768"
# KG_builder_model ="llama3-8b-8192"
KG_builder_model = "llama3-70b-8192"
# KG_builder_model ="gemma-7b-it"

# RRAG_model = "mixtral-8x7b-32768"
# RRAG_model ="llama3-8b-8192"
RRAG_model = "llama3-70b-8192"
# RRAG_model="gemma-7b-it"

################### ALL THE PROMTS GO HERE ###############
PROMPT_1 = '''A text file named "query_paras.txt" which contains a python list of text_chunks
formed from the contents of a research paper is uploaded.
give me a list of text chunks out of the above text chunks which are important
for me to write the code implementation of the paper. Make sure the text chunks
are in a sequence which makes sense with respect to writing code.
Just classify each text_chunk in the above list as being useful for code
conversion or not useful. Keep all the text chunks which are useful for code
conversion in a single list and return that list. Do not output any explanation
just the python list.'''

PROMPT_2 = '''You are an expert at creating Knowledge Graphs. You will create a knowledge
graph for the text chunk provided to you. This knowledge graph will be put in a
generative machine learning model which will try to write python code which is
explained by the knowledge graph output by you. So make sure you catch the
entities and relationships from the text chunks which are ’code-oriented’."
"Consider the following ontology. \n"
f"{self._ontology} \n"
"Extract all the entities and relationships from the user-provided text as per
the given ontology. Do not use any previous knowledge about the context.
"Extract all the entities and relationships which are technically sound so that
the knowledge graph so formed can be used by a machine learning program to write
corresponding code."
"Remember there can be multiple direct (explicit) or implied relationships
between the same pair of nodes."
"Be consistent with the given ontology. Use ONLY the labels and relationships
mentioned in the ontology."
"Format your output as a json with the following schema. \n"
[\n
{\n
node_1: Required, an entity object with attributes: {"label": "as per the
ontology", "name": "Name of the entity"},\n
node_2: Required, an entity object with attributes: {"label": "as per the
ontology", "name": "Name of the entity"},\n
relationship: It is the description of the relationship between the 2 nodes 1
and 2. Make sure this description is related to one of the keywords given in the
’relationship’ attribute of Ontology.\n
},\n
]\n
"Do not add any other comment before or after the json. Respond ONLY with a well
formed json that can be directly read by a program."
"But NOTE that your output should be only of the above json format and not the
examples provided to you. These examples only serve the purpose to make you
understand how the input(text chunk) and the output are related to each other."
"Do not output any explanation, just a json structure of the output json format
given to you."'''

PROMPT_3 = ''''The contents of a research paper which describes a machine learning model
architecture is provided as "query_text.txt" file. And a JSON file is also
uploaded which represents the anthology of the methods needed to be realised.
JSON is retrieved for the scientific paper. The aim is to implement the model
architecture described in the paper. While you should utilize both the contents
of the research paper and JSON, note that the JSON consists of a "knowledge
Graph" which specifically contains refined information about aspects important
for writing the code implementation of the paper.'''

PROMPT_4 = '''Provide a list of required information needed at your end to improve the quality
of code output by you. Make sure your pointers are queries which can be sent to
a research literature database. Note that the research literature database is
formed using this research paper currently given to you and its reference
research paper. So the database effectively contains research papers which may
be related to the current problems you are facing. Outline those problems as
queries which will be used to look for similar problems in relevant research
papers.
Just give a python list of your queries.'''

PROMPT_5 = '''Given a search query, represent the query for searching relevant passages that
answer the query:'''


PROMPT_6 = '''Answer the query given asked by the user in very short and crisp manner and try
not to exceed 150 words. Also make sure your answers are very technical and
specific. The best matching document which provides context to help answer the
query is given here under:'''

PROMPT_7 = '''Below are the pairs of your query and their corresponding answer from relevant
literature. Now rewrite the python code to improve its quality.
f"{self.answers_to_queries}"
Above I have provided the answers to each of your query. Now improve the
structural quality of python code implementing the model architecture.'''

## ALL THE REQUIRED DIRECTORIES GO HERE ####

ref_papers_xml_directory = './ref_papers_xml'
# Directory containing the XML files
query_paper_xml_directory = './query_paper_xml'
nodes_of_query_llama3 = 'nodes_of_query_llama3.json'
############ ONTOLOGY USED #################
ontology = Ontology(
    labels=[
        {"Research Paper" : "a research document document" },
        {"Machine Learning Task" : "The specific problem the model addresses"},
        {"Model Architecture" : '''The overall architecture of the ML model which includes 
        Layers, that is Different layers within the model (e.g., input, convolutional, recurrent, output).
        Activation Functions, that is Functions like ReLU, Sigmoid, etc.
        Hyperparameters, like Learning rate, number of epochs, batch size, etc.
        Optimizers, that is Algorithms to update the weight parameter (e.g., SGD, Adam).'''},
        {"Data_structures" : "The type of structure of the data (for example, arrays, Pandas DataFrames, Matrices, tensors etc.)"},
        {"Frameworks for Data Manipulation" : " different libraries for data manipulation like pytorch, tensorflow etc."},
        {"Dataset": "Data used for training and testing. This includes Data Preprocessing, which are techniques used to prepare data (normalization, augmentation)"},
        {"Evaluation Metric" : "Metrics used to assess performance (accuracy, F1 score, etc.)"},
        {"Results": "Outcomes of experiments, including statistical measures."},
        {"Experimental Setup" : '''Details about how experiments were structured. This includes but is not limited to
        Hardware: Specifications of the computing resources used.
        Software: Software and tools, versions used.'''},
        {"subtask" : "any task which is part of the whole process of achieveing the bigger goal"},
        {"method" : "the methodology used to achieve a subtask. This includes the logical sequence (which can be potentially converted to code) of steps, libraries and tools used"},
        {"tool" : "The standard or custom tools used in a method"}, 
        {"Miscellaneous": "Any important concept can not be categorised with any other given label"},
    ],
    relationships=[
        "Proposes : Links Research Paper to Model Architecture.",
        "Addresses : Connects Model Architecture to Machine Learning Task.",
        "Includes Layer : From Model Architecture to Layers.",
        "Uses Activation : From Layers to Activation Functions.",
        "Sets Hyperparameter : From Model Architecture to Hyperparameters.",
        "Utilizes Optimizer : From Model Architecture to Optimizers.",
        "Applies Preprocessing : From Dataset to Data Preprocessing methods.",
        "Uses : Links Model Architecture to Dataset.",
        "Evaluates With : Connects Model Architecture to Evaluation Metric.",
        "Reports Results : From Research Paper to Results.",
        "Conducted On : From Experimental Setup to Hardware and Software.", 
        "method for subtask : from method to subtask",
        "tool for method : from tool to method",
        "Misc : Miscellaneous relationship between any pair of Entities",
]
)

# run the grobid client to parse the input papers and its references
subprocess.run(["python3", "grobid_client_python.py"], check=True) 

text_chunks = extract_text_from_files(ref_papers_xml_directory) # get text_chunks from the references and the input paper 

# create the dynamic database
if('dynamic_database.npy' not in list(os.listdir("./"))):
    d_reps = []
    start = 0
    end = 100
    while(start <= len(text_chunks)):
        tmp = get_embeddings(text_chunks[start:end], embeddings_model,mxbai=mxbai)
        d_reps.extend(tmp)
        start+=100
        end+=100

    with open('dynamic_database.npy','wb') as file:
        np.save(file,np.array(d_reps))
        file.close
        print("created the dynamic database successfully !")

with open('DDB_text_chunks.txt','w') as file:
    file.write(str(text_chunks))

#Create the textual represtation of the input paper
# Namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

content_dict = get_content_dict(query_paper_xml_directory)
# Write the extracted headings and contents to the text file
with open('query_text.txt', 'w') as file:
    for heading, contents in content_dict.items():
        file.write(f"<{heading}>\n")
        file.write(" ".join(contents) + "\n\n")

# Create paragraphs from the input paper
content_list = get_content_list(query_paper_xml_directory)

with open('query_paras.txt','w') as file:
    file.write(str(content_list))

# Calling GPT-4o to extract code-oriented text chunks from the paper
query_paras = open('query_paras.txt','r').read()
code_oriented_text_chunks = client_openai.chat.completions.create(
  model=GPT4o,
  messages=[
    {"role": "system", "content": PROMPT_1},
    {"role": "user", "content": "query_paras.txt:\n"+query_paras}
  ]
)
query_strings_useful_for_code = eval(code_oriented_text_chunks.choices[0].message.content)

#Building Knowledge graph
class KnowledgeGraphBuilder:
    def __init__(self, ontology, model, output_file):
        self.ontology = ontology
        self.model = model
        self.output_file = output_file

    def generate_summary(self, text):
        SYS_PROMPT = (
            "Succinctly summarise the text provided by the user. "
            "Respond only with the summary and no other comments"
        )
        try:
            summary = self.llm.generate(user_message=text, system_message=SYS_PROMPT)
        except Exception as e:
            print(f"Error generating summary: {e}")
            summary = ""
        finally:
            return summary

    def create_graph(self, query_strings):
        self.llm = GroqClient(model=self.model, temperature=0.1, top_p=0.5)
        query_docs = []
        for query in query_strings:
            current_time = str(datetime.datetime.now())
            doc = Document(text=query, metadata={"summary": self.generate_summary(query), 'generated_at': current_time})
            query_docs.append(doc)
        graph_maker = GraphMaker(ontology=self.ontology, llm_client=self.llm, verbose=False)
        graph = graph_maker.from_documents(query_docs)
        nodes_list = [str(edge.model_dump()) for edge in graph]
        
        return nodes_list

    def save_graph_to_file(self, graph_data):
        with open(self.output_file, 'w') as json_file:
            json.dump(graph_data, json_file, indent=4)
        print(f"Data has been written to {self.output_file} with proper formatting.")

    def build_and_store_graph(self, query_strings):
        graph_data = self.create_graph(query_strings)
        self.save_graph_to_file(graph_data)
        print(graph_data)

# Create the KnowledgeGraphBuilder object
kg_builder = KnowledgeGraphBuilder(ontology, KG_builder_model, output_file=nodes_of_query_llama3)
# create and store the knowledge graph
kg_builder.build_and_store_graph(query_strings_useful_for_code)


# Calling GPT-4o to write code implementation of the paper using the 
# textual representation of the paper and the previously built knowledge graph
 
query_text = open('query_text.txt','r').read()

with open("nodes_of_query_llama3.json", 'r') as file:
    knowledge_graph = str(json.load(file))

INTERMEDIATE_CODE = client_openai.chat.completions.create(
  model=GPT4o,
  messages=[
    {"role": "system", "content": "you are a helpful assistant." + PROMPT_3},
    {"role": "user", "content": "query_paras.txt:\n"+query_text+"\n,Knowledge graph in json format :\n"+knowledge_graph}
  ]
)

INTERMEDIATE_CODE = INTERMEDIATE_CODE.choices[0].message.content

with open('INTERMEDIATE_CODE.txt','r') as file:
    file.write(INTERMEDIATE_CODE)

# Initiate the Retrospective RAG (RRAG)

queries = client_openai.chat.completions.create(
  model=GPT4o,
  messages=[
    {"role": "system", "content": "you are a helpful assistant." + PROMPT_3},
    {"role": "user", "content": "query_text.txt:\n"+query_text+"\n,Knowledge graph in json format :\n"+knowledge_graph},
    {"role": "assistant", "content": INTERMEDIATE_CODE},
    {"role": "user", "content": PROMPT_4}
  ]
)

list_queries = eval(queries.choices[0].message.content)

#queriying the dynamic database 
with open('DDB_text_chunks.txt','r') as file:
    DDB_text_chunks = file.read()
with open("dynamic_database.npy",'rb') as file:
    dynamic_database = file.read()

# calling RRAG to write the answers to query in the file 'answer_to_query.txt'

Retrospective_RAG(embeddings_model=embeddings_model,
                  mxbai=mxbai, 
                  RRAG_client = groq_client,
                  text_chunks=DDB_text_chunks, 
                  queries=list_queries, 
                  d_reps=dynamic_database,
                  QA_model=RRAG_model,
                  instruction_tuning_prompt=PROMPT_5,
                  RRAG_instruction=PROMPT_6)


# prompt GPT-40 to write enhanced python code for the given queries

with open('answers_to_queries.txt','r') as file:
    answers_to_queries = file.read()

FINAL_CODE = client_openai.chat.completions.create(
  model=GPT4o,
  messages=[
    {"role": "system", "content": "you are a helpful assistant." + PROMPT_3},
    {"role": "user", "content": "query_text.txt:\n"+query_text+"\n,Knowledge graph in json format :\n"+ knowledge_graph},
    {"role": "assistant", "content": INTERMEDIATE_CODE},
    {"role": "user", "content": PROMPT_4},
    {"role": "assistant", "content": str(queries)},
    {"role":"user", "content": PROMPT_7.format(answers_to_queries=answers_to_queries)}
  ]
)

FINAL_CODE = FINAL_CODE.choices[0].message.content

with open('FINAL_CODE.txt','w') as file:
    file.write(FINAL_CODE)


