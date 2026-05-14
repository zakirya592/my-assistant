#!/usr/bin/env python3
"""
Test script to verify edge_tts voices are loaded correctly
"""
import asyncio
import edge_tts

async def test_voices():
    print("Fetching available voices from edge_tts...")
    voices = await edge_tts.list_voices()
    print(f"Total voices available: {len(voices)}")
    print("\nFirst 5 voices:")
    for i, voice in enumerate(voices[:5]):
        short_name = voice.get("ShortName", "Unknown")
        gender = voice.get("Gender", "Unknown")
        locale = voice.get("Locale", "Unknown")
        print(f"  {i+1}. {short_name} ({gender}) - {locale}")
    
    print("\nEnglish US voices:")
    us_voices = [v for v in voices if v.get("Locale", "").startswith("en-US")]
    for voice in us_voices[:5]:
        short_name = voice.get("ShortName", "Unknown")
        gender = voice.get("Gender", "Unknown")
        print(f"  - {short_name} ({gender})")

if __name__ == "__main__":
    asyncio.run(test_voices())
