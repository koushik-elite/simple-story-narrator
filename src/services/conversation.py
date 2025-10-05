import textwrap
from typing import TYPE_CHECKING, List, Dict, Any, Optional
from models.story import Character, ConversationTurn, Scene
import logging

from prompts.characters import CharacterDialogueManager

logger = logging.getLogger("conversation")


class ConversationManager:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.conversation_history: List[Dict[str, str]] = []
        self.dialogueManager = CharacterDialogueManager()

    def generate_character_response(
        self,
        name: str,
        character: Character,
        narration: str,
        scene: Optional[Scene] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        current_conversation_vs_max: Optional[str] = None,
    ) -> ConversationTurn:
        """
        Generate a character’s response based on narration, their goals, backstory,
        and previous conversation history.
        """
        # Build conversation context
        # conversation_context = ""
        # if conversation_history:
        #     conversation_lines = [
        #         f"{entry['character']}: \"{entry['response']}\""
        #         for entry in conversation_history
        #     ]
        #     conversation_context = "\n".join(conversation_lines)

        character_message = self.dialogueManager.get_character_conversation_prompt(
            name,
            character,
            narration,
            scene,
            conversation_history,
            current_conversation_vs_max,
        )
        response = self.llm_client.execute_character_dialogue(character_message)
        # print(prompt)
        print("--------------------------------------------------------------------")
        print(response)
        return response

    def conduct_scene_conversation(
        self,
        characters: Dict[str, Character],
        narration: str,
        scene: Optional[Scene] = None,
        conversation_rounds: int = 2,
    ) -> List[ConversationTurn]:
        """
        Conduct a multi-round conversation among the given characters.
        """
        conversation = []
        conversation_history = []
        character_names = list(characters.keys())

        for round_num in range(conversation_rounds):
            logger.info(f"Starting conversation round {round_num + 1}")

            for character_name in character_names:
                print(characters[character_name])
                # If it's already a Character instance, use it directly
                character = characters[character_name] if isinstance(characters[character_name], Character) else Character(**characters[character_name])

                response: ConversationTurn = self.generate_character_response(
                    name=character_name,
                    character=character,
                    narration=narration,
                    scene=scene,
                    conversation_history=conversation_history,
                    current_conversation_vs_max=f"{round_num + 1}/{conversation_rounds}",
                )

                character_entry = {
                    "round": round_num + 1,
                    "character": character_name,
                    "response": response.dialogue,
                }

                conversation.append(character_entry)
                conversation_history.append(response)

        return conversation_history

    def reset_conversation_history(self):
        """Reset the conversation history."""
        self.conversation_history = []
