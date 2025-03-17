from animo import Animo
import os
import time
import sys

# Get API key from environment variable
api_key = "Test123"
if not api_key:
    print("Error: ANIMO_API_KEY environment variable not set")
    sys.exit(1)

# Initialize client
client = Animo(api_key=api_key)

# Get prompt from command line or use default
prompt = sys.argv[1] if len(sys.argv) > 1 else "Create a blue square"

print(f"🚀 Generating video for: '{prompt}'")

# Start generation
try:
    generation = client.videos.generate(prompt=prompt)
    request_id = generation.get("requestId")
    
    if not request_id:
        print("❌ No request ID received")
        sys.exit(1)
        
    print(f"✅ Generation started with ID: {request_id}")
    
    # Poll for status with a simple progress indicator
    print("⏳ Waiting for completion", end="")
    dots = 0
    
    while True:
        status_data = client.videos.retrieve(request_id=request_id)
        print(status_data)
        status = status_data.get("status")
        
        # Update progress indicator
        sys.stdout.write(".")
        sys.stdout.flush()
        dots = (dots + 1) % 3
        
        # Check for completion or error
        if status == "SUCCEEDED":
            video_url = status_data.get("videoUrl")
            print(f"\n\n🎬 Video ready! URL: {video_url}")
            
            # Print processing time if available
            if processing_time := status_data.get("processingTime"):
                print(f"⏱️  Processing time: {processing_time} seconds")
                
            break
            
        elif status == "FAILED":
            error = status_data.get("error") or "Unknown error"
            print(f"\n\n❌ Generation failed: {error}")
            break
            
        # Wait before next check
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\n\n🛑 Process interrupted by user")
    sys.exit(0)
    
except Exception as e:
    print(f"\n\n❌ Error: {str(e)}")
    sys.exit(1) 