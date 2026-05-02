"""Demo: Structured output — LLM -> Pydantic model."""

import json
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from mock_llm import MockChatModel


class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    rating: int = Field(description="Rating out of 10")
    summary: str = Field(description="Brief summary")


def main():
    print("=== Structured Output Demo ===")

    llm = MockChatModel()

    # In production, you'd use: structured_llm = llm.with_structured_output(MovieReview)
    # With mock, we simulate by parsing the JSON response
    response = llm.invoke([HumanMessage(content="Review the movie Inception")])

    try:
        data = json.loads(response.content)
        review = MovieReview(**data)
    except (json.JSONDecodeError, Exception):
        # Fallback for demo
        review = MovieReview(
            title="Inception",
            rating=9,
            summary="A mind-bending thriller about dream infiltration.",
        )

    print(f"MovieReview(title='{review.title}', rating={review.rating}, summary='{review.summary}')")
    print()


if __name__ == "__main__":
    main()
