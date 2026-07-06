from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Cloud Lab Portfolio")


class Challenge(BaseModel):
    id: int
    title: str
    category: str
    difficulty: str
    description: str


CHALLENGES = [
    Challenge(
        id=1,
        title="Create a Namespace for the Lab",
        category="kubernetes",
        difficulty="beginner",
        description="Deploy a workload into its own namespace with proper labels.",
    ),
    Challenge(
        id=2,
        title="Expose the Service Correctly",
        category="kubernetes",
        difficulty="intermediate",
        description="Use a Service to expose the app and verify connectivity.",
    ),
    Challenge(
        id=3,
        title="Provision a Secure Network",
        category="terraform",
        difficulty="intermediate",
        description="Create a VPC and subnet layout with secure defaults.",
    ),
    Challenge(
        id=4,
        title="Design for High Availability",
        category="aws",
        difficulty="advanced",
        description="Plan for resilience with multi-AZ and redundant components.",
    ),
]


@app.get("/")
def home():
    return {
        "message": "Cloud Lab Portfolio",
        "focus": ["kubernetes", "terraform", "aws-saa"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/challenges", response_model=list[Challenge])
def get_challenges():
    return CHALLENGES
