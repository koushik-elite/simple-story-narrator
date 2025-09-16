"""
story narrator

this script take yaml input file contain story contex, characters and scenes process them 
through the story narrator and conversation system, and outputs the 
results in a structured yaml format.
"""
import sys
import yaml
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Import our story components
from models.story import StoryInput
from services.llm_client import LLMClient
from services.narrator import Narrator
from services.conversation import ConversationManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("story_processor")

class StoryProcessor:
    def __init__(self):
        self.llm_client = LLMClient()
        self.narrator = Narrator(self.llm_client)
        self.conversation_manager = ConversationManager(self.llm_client)

    def load_story_config(self, yaml_file: str) -> Dict[str, Any]:
        """Load story configuration from YAML file."""
        try:
            with open(yaml_file, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
            logger.info(f"Loaded story configuration from {yaml_file}")
            return config
        except FileNotFoundError:
            logger.error(f"Input file {yaml_file} not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            sys.exit(1)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate the story configuration."""
        required_keys = ["context", "characters", "scenes"]

        # Check required keys
        for key in required_keys:
            if key not in config:
                logger.error(f"Missing required key: {key}")
                return False

        # Validate characters
        if not isinstance(config["characters"], dict):
            logger.error("Characters must be a dictionary")
            return False

        # Validate scenes
        if not isinstance(config["scenes"], list):
            logger.error("Scenes must be a list")
            return False

        # Validate character structure
        for char_name, char_data in config["characters"].items():
            if not isinstance(char_data, dict) or "goal" not in char_data or "backstory" not in char_data:
                logger.error(f"Character {char_name} missing goal or backstory")
                return False

        # Validate scene structure
        for i, scene in enumerate(config["scenes"]):
            if not isinstance(scene, dict) or "scene_no" not in scene or "context" not in scene:
                logger.error(f"Scene {i} missing 'scene_no' or 'context'")
                return False

        logger.info("Configuration validation passed")
        return True

    def save_output(self, data: Dict[str, Any], output_file: str):
        """Save the processed story to YAML file."""
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                yaml.dump(
                    data,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                    indent=2,
                )
            logger.info(f"Output saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving output file: {e}")
            sys.exit(1)

    def run(self, input_file: str = "story_input.yaml", output_file: str = "output.yaml"):
        """Main processing function."""
        logger.info("Starting Story Narrator YAML Processor")

        # Load configuration
        config = self.load_story_config(input_file)

        # Validate configuration
        if not self.validate_config(config):
            sys.exit(1)

        # Use output file from config if specified
        if "config" in config and "output_file" in config["config"]:
            output_file = config["config"]["output_file"]

        # Process the story
        output_data = self.process_story(config)

        # Save results
        self.save_output(output_data, output_file)

        # Final log summary
        logger.info("Story processing completed successfully!")
        logger.info(f"Generated narrations for {len(output_data['scenes'])} scenes")
        logger.info(f"Created conversations between {len(config['characters'])} characters")
        logger.info(f"Results saved to: {output_file}")

    def process_story(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process the story and generate narration and conversations."""

        # Create StoryInput object
        story_input = StoryInput(
            context=config["context"],
            characters=config["characters"],
            scenes=config["scenes"]
        )

        # Get configuration options
        story_config = config.get("config", {})
        conversation_rounds = story_config.get("conversation_rounds", 2)

        # Prepare output structure
        output_data: Dict[str, Any] = {
            "story_info": {
                "context": config["context"],
                "generated_at": datetime.now().isoformat(),
                "total_scenes": len(config["scenes"]),
                "characters": list(config["characters"].keys()),
            },
            "scenes": []
        }

        logger.info(f"Processing {len(story_input.scenes)} scenes...")

        for scene in story_input.scenes:
            logger.info(f"Processing scene {scene.scene_no}")

            # Generate narration
            narration = self.narrator.narrate_scene(story_input.context, scene)

            # Generate conversation
            conversation = self.conversation_manager.conduct_scene(
                characters=story_input.characters,
                narration=narration,
                scene_context=scene.context,
                conversation_rounds=conversation_rounds,
            )

            # Structure the scene output
            scene_output = {
                "scene_no": scene.scene_no,
                "context": scene.context,
                "narration": {
                    "narrator": narration
                },
                "conversations": []
            }

            # Group conversations by round
            current_round = 1
            round_conversations = []

            for entry in conversation:
                if entry["round"] != current_round:
                    if round_conversations:
                        scene_output["conversations"].append({
                            "round": current_round,
                            "exchanges": round_conversations
                        })
                    current_round = entry["round"]
                    round_conversations = []

                round_conversations.append({
                    "character": entry["character"],
                    "text": entry["response"]
                })

            # Add the last round
            if round_conversations:
                scene_output["conversations"].append({
                    "round": current_round,
                    "exchanges": round_conversations
                })

            # Append this scene to output
            output_data["scenes"].append(scene_output)

            # Reset conversation history for next scene
            self.conversation_manager.reset_conversation_history()

        logger.info("Story processing completed")
        return output_data

def main():
    """Command line entry point."""
    # Parse command line arguments
    input_file = sys.argv[1] if len(sys.argv) > 1 else "story_input.yaml"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.yaml"

    # Create and run processor
    processor = StoryProcessor()
    processor.run(input_file, output_file)


if __name__ == "__main__":
    main()