import random
import time
from voice import speak
import re

class HumanAI:
    def __init__(self):
        self.personality_traits = {
            'friendly': True,
            'casual': True,
            'sometimes_forgets': True,
            'makes_typos': False,
            'thinks_before_speaking': True,
            'uses_fillers': True,
            'varies_response_time': True
        }
        
        self.fillers = [
            "um", "uh", "well", "you know", "like", "actually", 
            "let me see", "hmm", "oh", "right", "basically"
        ]
        
        self.conversation_starters = [
            "Alright, let me help you with that.",
            "Okay, I see what you need.",
            "Got it! Let me work on that for you.",
            "Sure thing! Let me handle that.",
            "No problem, I'm on it."
        ]
        
        self.thinking_phrases = [
            "Let me think about that for a moment...",
            "Hmm, give me a second to process that.",
            "Okay, let me figure this out...",
            "Alright, let me check on that...",
            "Just a moment while I look into that..."
        ]
        
        self.success_responses = [
            "There we go!",
            "Perfect! That's done.",
            "All set!",
            "Great! That worked out.",
            "Excellent! Task completed."
        ]
        
        self.error_responses = [
            "Oops, something went wrong there.",
            "Hmm, that didn't work as expected.",
            "Sorry, hit a little snag there.",
            "Well, that didn't go as planned.",
            "Looks like we have a small issue here."
        ]
    
    def human_speak(self, text, add_personality=True):
        """Speak with human-like characteristics"""
        if not add_personality:
            speak(text)
            return
        
        # Add thinking delay
        if self.personality_traits['thinks_before_speaking']:
            thinking_time = random.uniform(0.5, 2.0)
            time.sleep(thinking_time)
        
        # Add filler words occasionally
        if self.personality_traits['uses_fillers'] and random.random() < 0.3:
            filler = random.choice(self.fillers)
            text = f"{filler}, {text}"
        
        # Vary response time
        if self.personality_traits['varies_response_time']:
            time.sleep(random.uniform(0.2, 0.8))
        
        speak(text)
    
    def get_conversation_starter(self):
        """Get a natural conversation starter"""
        return random.choice(self.conversation_starters)
    
    def get_thinking_phrase(self):
        """Get a natural thinking phrase"""
        return random.choice(self.thinking_phrases)
    
    def get_success_response(self):
        """Get a natural success response"""
        return random.choice(self.success_responses)
    
    def get_error_response(self):
        """Get a natural error response"""
        return random.choice(self.error_responses)
    
    def humanize_command_response(self, command, response):
        """Make command responses more human-like"""
        # Remove robotic phrases
        response = re.sub(r'Opening (\w+)', r'Let me open \1 for you', response)
        response = re.sub(r'Closing (\w+)', r'I\'ll close \1 now', response)
        response = re.sub(r'Searching for (\w+)', r'Let me search for \1', response)
        response = re.sub(r'(\w+) not found', r'I couldn\'t find \1', response)
        response = re.sub(r'(\w+) completed', r'Finished with \1', response)
        
        # Add human touches
        if random.random() < 0.4:
            response = response + " There we go!"
        elif random.random() < 0.3:
            response = "Okay, " + response.lower()
        
        return response
    
    def simulate_typing_sound(self, duration=1.0):
        """Simulate the sound of typing (visual feedback in console)"""
        print(".", end="", flush=True)
        time.sleep(duration / 10)
        print(".", end="", flush=True)
        time.sleep(duration / 10)
        print(".", end="", flush=True)
        time.sleep(duration / 10)
        print(" Done!")
        print()
    
    def acknowledge_command(self, command):
        """Give natural acknowledgment of received command"""
        acknowledgments = [
            "Got it!",
            "Okay, I'm on that.",
            "Sure thing!",
            "Alright, let me do that.",
            "No problem!",
            "I can help with that.",
            "Coming right up!",
            "Let me take care of that."
        ]
        
        acknowledgment = random.choice(acknowledgments)
        
        # Sometimes add a thinking phrase for complex commands
        complex_commands = ['find', 'search', 'chat', 'remember']
        if any(cmd in command.lower() for cmd in complex_commands):
            if random.random() < 0.5:
                acknowledgment += f" {self.get_thinking_phrase()}"
        
        self.human_speak(acknowledgment)
    
    def natural_delay(self, min_seconds=0.5, max_seconds=2.0):
        """Add natural human-like delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

# Global human AI instance
human_ai = HumanAI()
