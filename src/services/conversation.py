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

        try:
            response = self.llm_client.call_llm(prompt)
            return response.strip().strip('"')
        except Exception as e:
            logger.error(f"Error generating response for {character_name}: {e}")
            return f"[Error: could not generate response for {character_name}]"

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
        conversation_results: List[Dict[str, str]] = []

        for _ in range(conversation_rounds):
            for char_name, char in characters.items():
                response = self.generate_character_response(
                    character_name=char_name,
                    character=char,
                    narration=narration,
                    scene_context=scene_context,
                    conversation_history=conversation_results,
                )
                turn = {"character": char_name, "response": response}
                conversation_results.append(turn)
                self.conversation_history.append(turn)

        return conversation_results
