from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI

llm = ChatMistralAI(model="mistral-small-2506")
embedding_model = MistralAIEmbeddings(model="mistral-embed")