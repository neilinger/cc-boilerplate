#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "elevenlabs",
#     "python-dotenv",
# ]
# ///

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    """
    ElevenLabs Turbo v2.5 TTS Script

    Uses ElevenLabs' Turbo v2.5 model for fast, high-quality text-to-speech.
    Accepts optional text prompt as command-line argument.

    Usage:
    - ./eleven_turbo_tts.py                    # Uses default text
    - ./eleven_turbo_tts.py "Your custom text" # Uses provided text

    Features:
    - Fast generation (optimized for real-time use)
    - High-quality voice synthesis
    - Stable production model
    - Cost-effective for high-volume usage
    """

    # Load environment variables
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ Error: ELEVENLABS_API_KEY not found in environment variables")
        print("Please add your ElevenLabs API key to .env file:")
        print("ELEVENLABS_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        import elevenlabs
        from elevenlabs import ElevenLabs

        # Initialize client
        client = ElevenLabs(api_key=api_key)

        print("🎙️  ElevenLabs Turbo v2.5 TTS")
        print("=" * 40)

        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # Join all arguments as text
        else:
            text = "The first move is what sets everything in motion."

        print(f"🎯 Text: {text}")
        print("🔊 Generating and playing...")

        try:
            # Generate and play audio directly
            audio = client.text_to_speech.convert(
                text=text,
                voice_id=os.getenv('ELEVENLABS_VOICE_ID') or "JBFqnCBsd6RMkjVDRZzb",  # Default to Adam's voice ID
                model_id="eleven_turbo_v2_5",
                output_format="mp3_44100_128"
            )

            elevenlabs.play(audio)
            print("✅ Playback complete!")

        except Exception as e:
            error_message = str(e).lower()

            # Handle specific error types gracefully
            if "quota_exceeded" in error_message or "credits" in error_message:
                # Gracefully handle credit exhaustion - don't print error in hook context
                if os.getenv('CLAUDE_HOOK_CONTEXT') == 'true':
                    # Silent failure in hook context to avoid blocking operations
                    sys.exit(0)
                else:
                    print(f"💳 ElevenLabs credits exhausted. TTS skipped.")
                    sys.exit(0)
            elif "unauthorized" in error_message or "invalid" in error_message:
                if os.getenv('CLAUDE_HOOK_CONTEXT') == 'true':
                    # Silent failure in hook context
                    sys.exit(0)
                else:
                    print(f"🔑 ElevenLabs API key issue. Check your configuration.")
                    sys.exit(1)
            else:
                # For other errors, fail silently in hook context, show error otherwise
                if os.getenv('CLAUDE_HOOK_CONTEXT') == 'true':
                    sys.exit(0)
                else:
                    print(f"❌ TTS Error: {e}")
                    sys.exit(1)


    except ImportError:
        print("❌ Error: elevenlabs package not installed")
        print("This script uses UV to auto-install dependencies.")
        print("Make sure UV is installed: https://docs.astral.sh/uv/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
