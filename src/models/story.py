from typing import Dict, List, Optional, Union
from pydantic import BaseModel

class Character(BaseModel):
    goal: str
    backstory: str
    traits: Optional[Dict[str, float]] = None  # e.g., {"bravery": 0.7, "patience": 0.4}
    emotional_state: Optional[str] = None      # current emotion (e.g., "focused", "calm")
    abilities: Optional[Dict[str, str]] = None # e.g., {"magic": "moonlight spells"}
    relationships: Optional[Dict[str, str]] = None # ties to other characters

class Scene(BaseModel):
    scene_no: int
    location: Optional[str] = None
    atmosphere: Optional[str] = None
    context: str
    conflict: Optional[str] = None
    possible_outcomes: Optional[List[str]] = None
    narrator_prompt: Optional[str] = None
    themes: Optional[List[str]] = None
    max_conversations: Optional[int] = None
    description: Optional[str] = None  # extra narrative details

class Config(BaseModel):
    conversation_rounds: int
    output_file: str
    randomness: Optional[float] = None
    branching_factor: Optional[int] = None
    memory_tracking: Optional[bool] = None
    narrative_style: Optional[str] = None

class StoryInput(BaseModel):
    context: str
    characters: Dict[str, Character]
    scenes: List[Scene]
    config: Optional[Config] = None
