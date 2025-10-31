"""
Script to create sample Hindi audio files for testing
"""

from gtts import gTTS
import os


def create_sample_audio():
    """Create sample Hindi audio files"""
    
    # Create sample_audio directory if it doesn't exist
    if not os.path.exists('sample_audio'):
        os.makedirs('sample_audio')
    
    # Define test samples
    test_samples = [
        {
            'filename': 'sample_audio/hindi_test.wav',
            'text': 'नमस्ते, आप कैसे हैं? मेरा नाम राहुल है।',
            'description': 'Basic greeting with name'
        },
        {
            'filename': 'sample_audio/hindi_greeting.wav',
            'text': 'नमस्ते, आपका स्वागत है।',
            'description': 'Simple greeting'
        },
        {
            'filename': 'sample_audio/hindi_weather.wav',
            'text': 'आज मौसम कैसा है?',
            'description': 'Weather question'
        },
        {
            'filename': 'sample_audio/hindi_capabilities.wav',
            'text': 'आप क्या कर सकते हैं?',
            'description': 'Capabilities question'
        },
        {
            'filename': 'sample_audio/hindi_thanks.wav',
            'text': 'धन्यवाद, आपका बहुत धन्यवाद।',
            'description': 'Thank you'
        }
    ]
    
    print("🔊 Creating sample Hindi audio files...\n")
    
    for sample in test_samples:
        try:
            print(f"Creating: {sample['filename']}")
            print(f"Text: {sample['text']}")
            
            # Generate TTS
            tts = gTTS(text=sample['text'], lang='hi', slow=False)
            tts.save(sample['filename'])
            
            print(f"✅ Created: {sample['filename']}\n")
            
        except Exception as e:
            print(f"❌ Error creating {sample['filename']}: {e}\n")
    
    print("🎉 Sample audio files created successfully!")
    print("\nYou can now test the STT functionality with these files.")


if __name__ == "__main__":
    create_sample_audio()

