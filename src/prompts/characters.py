import textwrap
from typing import Dict, List, Optional
from models.story import Character, Scene
from models.story import ConversationTurn


class CharacterDialogueManager:
    def __init__(self):
        pass

    def to_rich_format(self, turn: ConversationTurn) -> str:
        parts = []

        # Character name with body language
        character_line = f"**{turn.character}**"
        if turn.body_language:
            character_line += f" ({turn.body_language})"
        character_line += ":"
        parts.append(character_line)

        # Dialogue
        parts.append(f'"{turn.dialogue}"')

        # Inner thoughts (optional, in italics)
        if turn.inner_thoughts:
            parts.append(f"\n*[Inner thought: {turn.inner_thoughts}]*")

        return " ".join(parts)

    def get_character_conversation_prompt(
        self,
        name: str,
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
        """
        message.append(
            {"role": "system", "content": textwrap.dedent(system_propmt).strip()}
        )

        for entry in conversation_history or []:
            message.append(
                {"role": "assistant", "content": self.to_rich_format(entry)}
            )

        print(character)
        
        character_prompt = f"""
        You are roleplaying as {name}.

        Character Details:
        - Goal: {character.goal}
        - Backstory: {character.backstory}
        - Traits: {character.traits}
        - Emotional State: {character.emotional_state}

        {name}'s Response:
        """

        message.append(
            {
                "role": "user",
                "content": textwrap.dedent(character_prompt).strip(),
            }
        )

        return message
