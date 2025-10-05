from ast import List
import textwrap
from typing import Dict, Optional
from models.agents import Character, Scene
from models.story import ConversationTurn


class CharacterDialogueManager:
    def __init__(self):
        pass

    def get_character_conversation_prompt(
        self,
        character: Character,
        narration: str,
        scene: Optional[Scene] = None,
        conversation_history: Optional[List[ConversationTurn]] = None,
        current_conversation_vs_max: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        
        message = []
        
        system_propmt = f"""
        You are an AI language model designed to roleplay as fictional characters in a story.
        Your task is to generate dialogue for a specific character based on their personality, goals, backstory,
        and the current scene narration provided by the narrator/director.

        Current Scene Narration (from narrator/director):
        {narration}

        Instructions:
        - You should respond in a way that is consistent with the character's traits and emotional state.
        - React naturally to the narrator's description of the scene.
        - If there is previous conversation, respond appropriately.
        - Keep responses concise, ideally 2 sentences, and avoid narrating actions unless specified.
        - Be aware of pacing: this scene allows {scene.max_conversations} total turns.
        - Current Conversation turn: {current_conversation_vs_max}
        """
        message.push({"role": "system", "content": textwrap.dedent(system_propmt).strip()})

        for entry in conversation_history or []:
            message.append({"role": entry.character, "content": entry.dialogue})

        character_prompt = f"""
        You are roleplaying as {character.name}.

        Character Details:
        - Goal: {character.goal}
        - Backstory: {character.backstory}
        - Traits: {character.traits}
        - Emotional State: {character.emotional_state}

        {character.name}'s Response:
        """

        message.append({"role": character.name, "content": textwrap.dedent(character_prompt).strip()})

        return message