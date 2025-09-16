from typing import List, Dict
from pydantic import BaseModel, Field

class Character(BaseModel):
    name: str
    character_description: str
    goal: str
    backstory: str

class Scene(BaseModel):
    scene_no: int
    context: str
    description: str = Field(default="")

class StoryInput(BaseModel):
    context: str
    characters: Dict[str, Character]
    scenes: List[Scene]

class SceneNarrator(BaseModel):
    role: str = "Scene Narrator"
    goal: str = "Understand the story and current scene, and narrate the scene in a captivating way."
    backstory: str = (
        "You are an experienced scene narrator with exceptional storytelling skills."
        "You have a deep understanding of narrative structure, character development, and emotional engagement."
    )

class CharacterAgent(BaseModel):
    role: str
    goal: str
    backstory: str