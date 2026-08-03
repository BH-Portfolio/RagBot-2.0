from logger import logger

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running the chain for input: {user_input}")
        result = chain.invoke({"input": user_input})
        response = result["answer"]

        sources = [
            doc.metadata.get("source", "")
            for doc in result.get("source_documents", [])
        ]

        logger.debug(f"Chain response: {response}")
        return {"response": response, "sources": sources}

    except Exception as e:
        logger.exception("Error in query chain")
        raise e
    