from typing import TYPE_CHECKING, List, Dict, Any, Optional
from models.story import Character, Scene
import logging

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
        scene: Optional[Scene] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        current_conversation_vs_max: Optional[str] = None,
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

        prompt = f"""
        You are roleplaying as {character_name}.

        Character Details:
        - Goal: {character.goal}
        - Backstory: {character.backstory}
        - Traits: {character.traits}
        - Current Emotional State: {character.emotional_state}

        Scene Details:
        - Location: {scene.location}
        - Atmosphere: {scene.atmosphere}
        - Conflict: {scene.conflict}
        - Possible Outcomes: {scene.possible_outcomes}
        - Max Conversations Allowed: {scene.max_conversations}
        - Current Conversation Count: {current_conversation_vs_max}

        Current Scene Narration:
        {narration}

        Previous conversation so far:
        {conversation_context if conversation_context else "Nothing yet."}

        Instructions:
        - Respond as {character_name} would, considering their goal, backstory, traits, and emotional state.
        - React to the current scene narration and the conversation so far.
        - Stay consistent with the scene's conflict and atmosphere.
        - If approaching the max conversation limit, start steering the dialogue toward one of the possible outcomes.
        - Keep your response natural and in character.
        - Limit your response to 2 sentences.
        - Do not narrate actions, only speak as {character_name}.
        - Always response in plain text.

        {character_name}'s response:
        """
        response = self.llm_client.call_llm(prompt)
        # print(prompt)
        # print("--------------------------------------------------------------------")
        # print(response)
        return response.strip().strip('"')
    
    def conduct_scene_conversation(
        self,
        characters: Dict[str, "Character"],
        narration: str,
        scene: Optional[Scene] = None,
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
                    scene=scene,
                    conversation_history=conversation,
                    current_conversation_vs_max=f"{round_num + 1}/{conversation_rounds}"
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
