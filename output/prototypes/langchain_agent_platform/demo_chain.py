"""Demo: LCEL Chain — prompt | llm | output_parser"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from mock_llm import MockChatModel


def main():
    print("=== LCEL Chain Demo ===")

    llm = MockChatModel()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant specialized in {topic}."),
        ("human", "{question}"),
    ])

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({
        "topic": "Python",
        "question": "What are decorators?",
    })

    print(f"Q: What are Python decorators?")
    print(f"A: {result}")
    print()


if __name__ == "__main__":
    main()
