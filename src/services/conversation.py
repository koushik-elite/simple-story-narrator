from typing import TYPE_CHECKING, List, Dict, Any, Optional
import logging

if TYPE_CHECKING:
    from models.story import Scene, Character

logger = logging.getLogger("conversation")


class ConversationManager:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.conversation_history: List[Dict[str, str]] = []

    def generate_character_response(
        self,
        character_name: str,
        character: "Character",
        narration: str,
        scene_context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Generate a character’s response based on narration, their goals, backstory,
        and previous conversation history.
        """
        # Build conversation context
        conversation_context = ""
        if conversation_history:
            conversation_lines = [
                f"{entry['character']}: \"{entry['response']}\""
                for entry in conversation_history
            ]
            conversation_context = "\n".join(conversation_lines)

        # Create the prompt for character response
        scene_context_line = f"Scene Context: {scene_context}" if scene_context else ""
        conversation_line = f"Previous conversation:\n{conversation_context}" if conversation_context else ""

        prompt = f"""
        You are roleplaying as {character_name}.

        Character Details:
        - Goal: {character.goal}
        - Backstory: {character.backstory}

        Current Scene Narration:
        {narration}

        {scene_context_line}

        {conversation_line}

        Instructions:
        - Respond as {character_name} would, considering their personality, goal, and backstory.
        - React to the current scene narration.
        - If there's previous conversation, respond appropriately to what others have said.
        - Keep your response natural and in character.
        - Limit your response to 2–3 sentences.
        - Do not narrate actions, only speak as the character would speak.

        {character_name}'s response:
        """
        response = self.llm_client.call_llm(prompt)
        return response.strip().strip('"')
    
    def conduct_scene_conversation(
        self,
        characters: Dict[str, "Character"],
        narration: str,
        scene_context: Optional[str] = None,
        conversation_rounds: int = 2,
    ) -> List[Dict[str, str]]:
        """
        Conduct a multi-round conversation among the given characters.
        """
        conversation = []
        character_names = list(characters.keys())

        for round_num in range(conversation_rounds):
            logger.info(f"Starting conversation round {round_num + 1}")

            for character_name in character_names:
                character = characters[character_name]

                response = self.generate_character_response(
                    character_name=character_name,
                    character=character,
                    narration=narration,
                    scene_context=scene_context,
                    conversation_history=conversation,
                )

                character_entry = {
                    "round": round_num + 1,
                    "character": character_name,
                    "response": response
                }
                conversation.append(character_entry)
        return conversation

    def reset_conversation_history(self):
        """Reset the conversation history."""
        self.conversation_history = []
