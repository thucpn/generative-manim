from animo import Animo
import os
from pprint import pprint

# Get API key from environment variable (recommended)
# You can also hardcode it, but it's not recommended for security reasons
api_key = os.getenv("ANIMO_API_KEY")

# Initialize the Animo client
client = Animo(api_key=api_key)

# Define the Manim scene code
# This will create a scene that writes "Arte de programar" with an animation
code = """
from manim import *

class GenScene(Scene):
    def construct(self):
        text = Text("Arte de programar", font_size=72, color=WHITE)
        self.play(Write(text))
"""

print("🎬 Creating video...")

try:
    # Create the video
    # You can customize:
    # - file_class: The name of your scene class
    # - aspect_ratio: "16:9" (default), "1:1", or "9:16"
    # - stream: Set to True if you want to receive progress updates
    response = client.videos.create(
        code=code,
        file_class="GenScene",
        aspect_ratio="16:9",
        stream=False
    )
    
    # Print the full response for debugging
    print("\n📋 API Response:")
    pprint(response)
    
    # Get the video URL
    video_url = response.get("video_url")
    
    if video_url:
        print(f"\n✅ Success! Your video is ready at:\n{video_url}")
    else:
        print("\n❌ Error: No video URL in the response")

except Exception as e:
    print(f"\n❌ Error: {str(e)}") 