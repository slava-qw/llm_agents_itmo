# # Requires SCIPHI_API_KEY in the environment
# from agent_search import SciPhi
#
# client = SciPhi(api_key=)
#
# # Specify instructions for the task
# instruction = "Your task is to perform retrieval augmented generation (RAG) over the given query and search results. Return your answer in a json format that includes a summary of the search results and a list of related queries."
# query = "What is Fermat's Last Theorem?"
#
# # construct search context
# search_response = client.search(query=query, search_provider='agent-search')
# search_context = "\n\n".join(
#       f"{idx + 1}. Title: {item['title']}\nURL: {item['url']}\nText: {item['text']}"
#       for idx, item in enumerate(search_response)
# ).encode('utf-8')
#
# # Prefix to enforce a JSON response
# json_response_prefix = '{"summary":'
#
# # Prepare a prompt
# formatted_prompt = f"### Instruction:{instruction}\n\nQuery:\n{query}\n\nSearch Results:\n${search_context}\n\nQuery:\n{query}\n### Response:\n{json_response_prefix}",
#
# # Generate a completion with Sensei-7B-V1
# completion = json_response_prefix + client.completion(formatted_prompt, llm_model_name="SciPhi/Sensei-7B-V1")
#
# print(completion)
# # {
# #   "summary":  "\nFermat's Last Theorem is a mathematical proposition first prop ... ",
# #   "other_queries": ["The role of elliptic curves in the proof of Fermat's Last Theorem", ...]
# # }