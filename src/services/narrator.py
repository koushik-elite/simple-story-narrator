from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from models.story import Scene  # Forward reference for type checking

# Configure logging
logger = logging.getLogger("narrator")


class Narrator:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def narrate_scene(self, context: str, scene: "Scene") -> str:
        prompt = f"""
        Objective:
        - Given the story context and the current scene, narrate the scene in a captivating way.

        Story Context:
        {context}
        ------------------------------------------------------------------
        Current Scene:
        {scene.context}
        """
        response = self.llm_client.call_llm(prompt)
        return response
