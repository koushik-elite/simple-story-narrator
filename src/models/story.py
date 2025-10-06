from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field

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
    # narrator_prompt: Optional[str] = None
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
    initial_conversation: Optional[List[Dict[str, Union[str, int]]]] = None

class StoryOutput(BaseModel):
    dialogues: Dict[str, List[str]]  # character name to list of dialogues
    scene_summaries: Dict[int, str]  # scene number to summary
    narrative_progression: List[str]  # overall story progression
    emotional_arcs: Dict[str, List[str]]  # character name to emotional arc descriptions
    unresolved_conflicts: Optional[List[str]] = None
    next_steps: Optional[List[str]] = None

class ConversationTurn(BaseModel):
    character: str = Field(description="character's name")
    dialogue: str = Field(description="character's spoken dialogue")
    emotion: str = Field(description="character's emotional tone. e.g. 'sad', 'angry'")
    tone: str = Field(description="character's tone e.g. 'sarcastic', 'serious'")
    body_language: str = Field(description="character's body language e.g. 'stepping forward with measured grace', 'armor gleaming softly', 'posture commanding yet approachable'")
    inner_thoughts: str = Field(description="character's internal thoughts or motivations. e.g. 'I must protect them at all costs', 'This is my moment to shine'")

class SceneConversation(BaseModel):
    scene_no: int
    turns: List[ConversationTurn]
    summary: Optional[str] = None  # brief summary of the conversation
    revelations: Optional[List[str]] = None  # key secrets or info revealed
    unresolved_tensions: Optional[List[str]] = None  # ongoing conflicts
    directors_rewarks: Optional[int] = -1 # 0-10 scale of how well the conversation met goals