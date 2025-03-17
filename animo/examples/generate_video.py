from animo import Animo
import os
import time
from pprint import pprint

# Get API key from environment variable (recommended)
api_key = os.getenv("ANIMO_API_KEY")

# Initialize the Animo client
client = Animo(api_key=api_key)

# Define the prompt for generating a video
prompt = "Create a simple animation of a circle transforming into a square and use voiceover"

print("🤖 Generating video from prompt...")

try:
    # Generate the video
    response = client.videos.generate(
        prompt=prompt,
        engine="anthropic",
        model="claude-3-7-sonnet-20250219"
    )
    
    # Print the initial response
    print("\n📋 Initial Response:")
    pprint(response)
    
    # Get the request ID
    request_id = response.get("requestId")
    
    if not request_id:
        print("\n❌ Error: No request ID in the response")
        exit(1)
    
    print(f"\n⏳ Processing request ID: {request_id}")
    print("Checking status every 5 seconds...")
    
    # Poll for status until complete
    while True:
        # Wait 5 seconds between status checks
        time.sleep(5)
        
        # Check the status
        status_response = client.videos.retrieve(request_id=request_id)
        status = status_response.get("status")
        
        print(f"Status: {status}")
        
        # If there's an error, exit
        if status_response.get("error"):
            print(f"\n❌ Error: {status_response.get('error')}")
            break
        
        # If complete, show the video URL
        if status == "COMPLETED":
            video_url = status_response.get("videoUrl")
            generated_code = status_response.get("generatedCode")
            
            print("\n✅ Success! Your video is ready.")
            print(f"Video URL: {video_url}")
            
            if generated_code:
                print("\n📝 Generated Manim Code:")
                print(generated_code)
            
            break
        
        # If failed, exit
        if status == "FAILED":
            print("\n❌ Generation failed")
            break

except Exception as e:
    print(f"\n❌ Error: {str(e)}") 