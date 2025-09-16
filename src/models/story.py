from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Character(BaseModel):
    goal: str
    backstory: str

class Scene(BaseModel):
    scene_no: int
    context: str
    description: Optional[str] = None

class StoryInput(BaseModel):
    context: str
    characters: Dict[str, Character]
    scenes: List[Scene]