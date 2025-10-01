from ast import List
import textwrap
from typing import Dict, Optional
from models.agents import Character, Scene


class CharacterDialogueManager:
    def __init__(self):
        pass

    def get_character_conversation_prompt(
        self,
        character: Character,
        narration: str,
        scene: Optional[Scene] = None,
        conversation_context: Optional[Scene] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        current_conversation_vs_max: Optional[str] = None,
    ) -> str:
        
        character_prompt = f"""
        You are roleplaying as {character.name}.

        Character Details:
        - Goal: {character.goal}
        - Backstory: {character.backstory}
        - Traits: {character.traits}
        - Emotional State: {character.emotional_state}

        Current Scene Narration (from narrator/director):
        {narration}

        Previous Conversation in this Scene:
        {conversation_context if conversation_context else 'Nothing yet, you are the first to speak.'}

        Instructions:
        - Respond as {character.name} would, considering their personality, goal, and backstory.
        - React naturally to the narrator's description of the scene.
        - If there is previous conversation, respond appropriately.
        - Keep responses 2 sentences, in character.
        - Do not narrate actions, only speak as {character.name}.
        - Be aware of pacing: this scene allows {scene.max_conversations} total turns.
        - Current Conversation turn: {current_conversation_vs_max}

        {character.name}'s Response:
        """
        return character_prompt