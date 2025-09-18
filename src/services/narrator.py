from typing import TYPE_CHECKING
import logging
import textwrap

if TYPE_CHECKING:
    from models.story import Scene  # Forward reference for type checking

# Configure logger
logger = logging.getLogger("narrator")


class Narrator:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def narrate_scene(self, context: str, scene: 'Scene', previous_narration: str = None, previous_conversation: str = None) -> str:
        """Generate narration for a given scene."""

        narrator_prompt = f"""
            You are a skilled narrator tasked with bringing scenes to life in an engaging and immersive manner, you are the director of th show.

            Objective:
            - Given the story context, the current scene, and past developments, narrate the scene in a captivating way.
            - Ensure narration flows naturally from prior events and conversations.

            Story Context:
            {context}

            ------------------------------------------------------------------
            Current Scene:
            {scene.context}

            Scene Details:
            - Location: {scene.location}
            - Atmosphere: {scene.atmosphere}
            - Conflict: {scene.conflict}
            - Possible Outcomes: {scene.possible_outcomes}

            Previous Narration (if any):
            {previous_narration if previous_narration else "Nothing as far"}

            Previous Conversation (if any):
            {previous_conversation if previous_conversation else "Nothing as far"}

            Narrator's Response:
            """
        
        prompt = textwrap.dedent(narrator_prompt).strip()
        response = self.llm_client.call_llm(prompt)
        print("--------------------------------------------------------------------")
        print(response)
        return response

