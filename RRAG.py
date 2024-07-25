import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from create_dynamic_database import get_embeddings

def Retrospective_RAG(embeddings_model,mxbai, RRAG_client, text_chunks, queries, d_reps,QA_model,instruction_tuning_prompt,RRAG_instruction):
    model_name = embeddings_model
    queries = queries
    q_reps = get_embeddings(queries, model_name,mxbai=mxbai,prompt=instruction_tuning_prompt)

    # Print the best document for each query
    with open("answers_to_queries.txt",'w') as file:
        for i, query_embeddings in enumerate(q_reps):
            # Compute cosine similarity
            similarities = cosine_similarity(query_embeddings.reshape(1,len(query_embeddings)), d_reps)
            retrieved_doc_id = np.argmax(similarities)
            best_doc = text_chunks[retrieved_doc_id]
            response = RRAG_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": RRAG_instruction+best_doc,
                    },
                    {"role":"user",
                    "content": queries[i]
                    }
                ],
                model=QA_model,
            )
            file.write("Query :" + queries[i] + "\n")
            file.write("Answer :\n")
            file.write(response.choices[0].message.content)
            file.write("\n\n\n ----------------")
