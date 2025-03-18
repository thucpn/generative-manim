from animo import Animo
import os
import time
import sys
import platform
import subprocess
import json

# Get API key from environment variable
api_key = "Test123"
if not api_key:
    print("Error: ANIMO_API_KEY environment variable not set")
    sys.exit(1)

# Initialize client
client = Animo(api_key=api_key)

# Get prompt from command line or use default
prompt = sys.argv[1] if len(sys.argv) > 1 else "Create a heart shape, and explain the basic definition of love with voiceover"

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
    print("⏳ Waiting for completion")
    last_status = None
    
    while True:
        status_data = client.videos.retrieve(request_id=request_id)
        status = status_data.get("status")
        
        # Print full response data for debugging
        print("\n📊 Full response data:")
        print(json.dumps(status_data, indent=2))
        print()
        
        # Only print status update when it changes
        if status != last_status:
            timestamp = status_data.get("updatedAt", "")
            timestamp_str = f" (updated: {timestamp})" if timestamp else ""
            
            if status == "PENDING":
                print(f"⏳ Request pending{timestamp_str}")
            elif status == "PROCESSING":
                print(f"🔄 Processing video{timestamp_str}")
            elif status == "RENDERED":
                print(f"🎞️ Video rendered, finalizing{timestamp_str}")
                if generated_code := status_data.get("generatedCode"):
                    print(f"📝 Generated code available")
            elif status == "SUCCEEDED":
                video_url = status_data.get("videoUrl")
                print(f"✅ Video generation complete!{timestamp_str}")
                print(f"🎬 Video URL: {video_url}")
                
                # Print processing time if available
                if processing_time := status_data.get("processingTime"):
                    print(f"⏱️  Processing time: {processing_time} seconds")
                
                # Use macOS "say" command if available
                if platform.system() == "Darwin":  # Darwin is the system name for macOS
                    try:
                        subprocess.run(["say", "Your video is ready"], check=False)
                    except Exception as e:
                        # Silently fail if the say command doesn't work
                        pass
                    
                break
                
            elif status == "FAILED":
                error = status_data.get("error") or "Unknown error"
                print(f"❌ Generation failed: {error}{timestamp_str}")
                break
            
            last_status = status
            
        # Wait before next check
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\n🛑 Process interrupted by user")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    sys.exit(1) 