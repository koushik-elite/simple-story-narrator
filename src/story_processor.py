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

from models.story import StoryInput
from services.llm_client import LLMClient