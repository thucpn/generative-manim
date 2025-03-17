# Animo API Examples

This directory contains example scripts demonstrating how to use the Animo API for creating animations with Manim.

## Setup

Before running any examples, make sure to:

1. Install the Animo package:
   ```
   pip install animo
   ```

2. Set your API key as an environment variable:
   ```
   export ANIMO_API_KEY="your_api_key_here"
   ```

## Available Examples

### 1. Basic Manim Code Rendering

**File:** `sample.py`

This example demonstrates how to render a video from Manim code using the Animo API. It creates a simple animation that writes "Arte de programar" on the screen.

```
python sample.py
```

### 2. AI-Generated Video with Polling

**File:** `generate_video.py`

This example shows how to generate a video from a text prompt using AI. It includes detailed status polling and displays the generated Manim code.

```
python generate_video.py
```

### 3. Quick Video Generation Test

**File:** `quick_generate.py`

A streamlined script for testing the video generation API with minimal output. You can provide your own prompt as a command-line argument:

```
python quick_generate.py "Create an animation of a bouncing ball with physics"
```

Or run without arguments to use the default prompt:

```
python quick_generate.py
```

## API Response Structure

The video generation API returns responses with the following structure:

- Initial generation response:
  ```json
  {
    "message": "Your request has been submitted and is being processed.",
    "requestId": "210b186f-c50a-4f40-bd4c-bb73c154afec",
    "status": "PENDING"
  }
  ```

- Status check response:
  ```json
  {
    "createdAt": "2025-03-16T15:34:29.006000+00:00",
    "error": null,
    "generatedCode": "from manim import *\n\nclass GenScene(Scene):\n    def construct(self):\n        # Animation code here",
    "processingTime": 45.2,
    "requestId": "210b186f-c50a-4f40-bd4c-bb73c154afec",
    "status": "COMPLETED",
    "updatedAt": "2025-03-16T15:35:14.132000+00:00",
    "videoUrl": "https://storage.animo.video/videos/210b186f-c50a-4f40-bd4c-bb73c154afec.mp4"
  }
  ``` 