# DELETE_FILE_CONTENT

## Table of Contents

- [System Overview](#system-overview)
- [Provider Comparison](#provider-comparison)
- [Provider Configuration](#provider-configuration)
- [Fallback Logic](#fallback-logic)
- [Voice Customization](#voice-customization)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## System Overview

The CC-Boilerplate TTS system provides **intelligent audio feedback** with automatic provider selection and graceful fallback to ensure audio output is always available.

### Key Features

```
🔊 **Multi-Provider Support** - ElevenLabs, OpenAI, pyttsx3
⚡ **Intelligent Fallback** - Automatic provider switching  
🎯 **Quality Optimization** - Best available quality selection
🔒 **API Key Management** - Secure credential handling
🌍 **Multi-Language Support** - 29+ languages supported
📱 **Cross-Platform** - Works on macOS, Linux, Windows
```

### Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ElevenLabs    │    │     OpenAI      │    │    pyttsx3     │
│                 │    │                 │    │                 │
│ ✨ Premium      │    │ 🎯 High Quality │    │ 🏠 Local       │
│ 🌍 29 Languages │    │ 🎭 6 Voices     │    │ 💻 Offline     │
│ 🎭 Custom Voice │    │ ⚡ Fast API     │    │ 🔧 System TTS  │
│ 💰 Paid API    │    │ 💰 Paid API    │    │ 🆓 Free        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                TTS Provider Manager                             │
│                                                                 │
│  Selection Priority: ElevenLabs → OpenAI → pyttsx3            │
│  Fallback on Failure: API Error → Network Issue → Local       │
│  Quality Optimization: Best Available → Good → Basic          │
└─────────────────────────────────────────────────────────────────┘
```

## Provider Comparison

### ElevenLabs TTS

**Best For**: Production use, content creation, multilingual projects

| Feature | Rating | Details |
|---------|--------|---------|
| **Audio Quality** | ⭐⭐⭐⭐⭐ | Premium AI voices, natural speech |
| **Voice Options** | ⭐⭐⭐⭐⭐ | 100+ voices, custom voice cloning |
| **Language Support** | ⭐⭐⭐⭐⭐ | 29 languages with native accents |
| **Speed** | ⭐⭐⭐⭐ | 2-5 second API response time |
| **Cost** | ⭐⭐ | Paid service, usage-based pricing |
| **Reliability** | ⭐⭐⭐⭐ | High uptime, professional service |

**Pros**:
- Exceptional voice quality and naturalness
- Custom voice training capabilities
- Extensive language and accent support
- Professional-grade audio output
- Advanced voice controls (stability, similarity)

**Cons**:
- Requires paid API subscription
- Internet connection required
- Higher latency than local options
- Usage costs can accumulate

**Configuration**:
```bash
# .env configuration
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_NAME=Rachel          # Default voice
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
ELEVENLABS_STABILITY=0.5              # Voice stability (0-1)
ELEVENLABS_SIMILARITY_BOOST=0.75      # Voice similarity (0-1)
```

### OpenAI TTS

**Best For**: Development, testing, consistent quality needs

| Feature | Rating | Details |
|---------|--------|---------|
| **Audio Quality** | ⭐⭐⭐⭐ | High-quality AI voices |
| **Voice Options** | ⭐⭐⭐ | 6 distinct voices (alloy, echo, fable, onyx, nova, shimmer) |
| **Language Support** | ⭐⭐⭐⭐ | Multi-language with good accent support |
| **Speed** | ⭐⭐⭐⭐⭐ | 1-3 second API response time |
| **Cost** | ⭐⭐⭐ | Reasonable pricing, per-character billing |
| **Reliability** | ⭐⭐⭐⭐⭐ | Excellent uptime and service stability |

**Pros**:
- Excellent balance of quality and cost
- Fast API response times
- Reliable service with high uptime
- Good voice variety and quality
- Simple integration and configuration

**Cons**:
- Limited voice customization options
- Requires paid API subscription
- Internet connection required
- Fewer voices than ElevenLabs

**Configuration**:
```bash
# .env configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_TTS_VOICE=nova                 # alloy|echo|fable|onyx|nova|shimmer
OPENAI_TTS_MODEL=tts-1-hd             # tts-1 (standard) | tts-1-hd (high quality)
OPENAI_TTS_SPEED=1.0                  # Speech speed (0.25-4.0)
```

### pyttsx3 TTS

**Best For**: Offline use, development, cost-sensitive scenarios

| Feature | Rating | Details |
|---------|--------|---------|
| **Audio Quality** | ⭐⭐⭐ | System TTS quality varies by OS |
| **Voice Options** | ⭐⭐ | Limited to system-installed voices |
| **Language Support** | ⭐⭐⭐ | Depends on system voice packages |
| **Speed** | ⭐⭐⭐⭐⭐ | <1 second generation time |
| **Cost** | ⭐⭐⭐⭐⭐ | Completely free |
| **Reliability** | ⭐⭐⭐⭐⭐ | Always available offline |

**Pros**:
- Completely free and offline
- No API keys or internet required
- Instant audio generation
- Cross-platform compatibility
- No usage limits or costs

**Cons**:
- Lower audio quality than cloud providers
- Limited voice options
- System-dependent functionality
- Less natural-sounding speech
- Platform-specific voice availability

**Configuration**:
```bash
# .env configuration  
PYTTSX3_RATE=150                      # Words per minute (50-400)
PYTTSX3_VOLUME=0.8                    # Volume level (0.0-1.0)
PYTTSX3_VOICE_ID=default              # System voice ID
```

## Provider Configuration

### ElevenLabs Setup

#### 1. Account Creation
```bash
# Visit https://elevenlabs.io and create account
# Navigate to Profile → API Key
# Copy your API key
```

#### 2. API Key Configuration
```bash
# Add to .env file
ELEVENLABS_API_KEY=sk-your-api-key-here

# Test configuration
uv run .claude/hooks/utils/tts/elevenlabs_tts.py --text "ElevenLabs test" --debug
```

#### 3. Voice Selection
```bash
# List available voices
uv run .claude/hooks/utils/tts/elevenlabs_tts.py --list-voices

# Test specific voice
uv run .claude/hooks/utils/tts/elevenlabs_tts.py \
  --text "Testing voice quality" \
  --voice-name "Rachel"
```

#### 4. Advanced Configuration
```python
# Advanced ElevenLabs settings
elevenlabs_config = {
    "voice_name": "Rachel",           # Voice selection
    "model_id": "eleven_multilingual_v2",  # Model selection
    "stability": 0.5,                 # Voice consistency (0-1)
    "similarity_boost": 0.75,         # Voice similarity (0-1)  
    "style": 0.0,                     # Style exaggeration (0-1)
    "use_speaker_boost": True         # Speaker similarity boost
}
```

### OpenAI Setup

#### 1. Account Setup
```bash
# Visit https://platform.openai.com
# Create account and add payment method
# Navigate to API Keys section
# Create new API key
```

#### 2. API Key Configuration
```bash
# Add to .env file
OPENAI_API_KEY=sk-your-api-key-here

# Test configuration
uv run .claude/hooks/utils/tts/openai_tts.py --text "OpenAI test" --debug
```

#### 3. Voice and Model Selection
```bash
# Test different voices
voices=("alloy" "echo" "fable" "onyx" "nova" "shimmer")
for voice in "${voices[@]}"; do
  uv run .claude/hooks/utils/tts/openai_tts.py \
    --text "Testing $voice voice" \
    --voice "$voice"
done

# Test HD model
uv run .claude/hooks/utils/tts/openai_tts.py \
  --text "High definition audio test" \
  --model "tts-1-hd"
```

### pyttsx3 Setup

#### 1. System Dependencies

**macOS**:
```bash
# macOS includes built-in TTS - no additional setup needed
# Test system TTS
say "Testing macOS TTS"
```

**Ubuntu/Debian**:
```bash
# Install espeak
sudo apt-get update
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev

# Test espeak
espeak "Testing Ubuntu TTS"
```

**Windows**:
```bash
# Windows includes built-in TTS (SAPI)
# Test Windows TTS
powershell -c "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('Testing Windows TTS')"
```

#### 2. Voice Configuration
```bash
# List available voices
python -c "
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f'{i}: {voice.name} - {voice.id}')
"

# Test specific voice
uv run .claude/hooks/utils/tts/pyttsx3_tts.py \
  --text "Testing local voice" \
  --voice-id "0"
```

## Fallback Logic

### Provider Selection Algorithm

```python
def select_tts_provider():
    """
    Intelligent TTS provider selection with fallback.
    """
    # Priority 1: ElevenLabs (if API key available)
    if has_api_key('ELEVENLABS_API_KEY') and test_network_connection():
        try:
            provider = ElevenLabsProvider()
            if provider.test_connection():
                return provider
        except APIException:
            log_provider_failure('elevenlabs', 'API connection failed')
    
    # Priority 2: OpenAI (if API key available)
    if has_api_key('OPENAI_API_KEY') and test_network_connection():
        try:
            provider = OpenAIProvider()
            if provider.test_connection():
                return provider
        except APIException:
            log_provider_failure('openai', 'API connection failed')
    
    # Priority 3: pyttsx3 (always available fallback)
    try:
        provider = Pyttsx3Provider()
        if provider.test_system_tts():
            return provider
    except SystemException:
        log_provider_failure('pyttsx3', 'System TTS unavailable')
    
    # No providers available
    raise TTSUnavailableException("No TTS providers available")
```

### Fallback Scenarios

#### Network Connectivity Issues
```
ElevenLabs API Call → Network Error → Retry (3x) → Switch to OpenAI → Success
```

#### API Key Issues
```
ElevenLabs API Call → Invalid Key → Skip to OpenAI → API Success
```

#### Service Outages
```
ElevenLabs API Call → Service Unavailable → OpenAI API Call → Service Unavailable → pyttsx3 → Success
```

#### Complete Fallback
```
All Providers Failed → Silent Mode → Continue Without Audio
```

### Configuration Override

```bash
# Force specific provider (bypass fallback)
TTS_FORCE_PROVIDER=pyttsx3           # Force local TTS
TTS_FORCE_PROVIDER=openai            # Force OpenAI TTS
TTS_FORCE_PROVIDER=elevenlabs        # Force ElevenLabs TTS

# Disable fallback (fail if primary unavailable)
TTS_FALLBACK_ENABLED=false
```

## Voice Customization

### ElevenLabs Voice Customization

#### Voice Selection
```bash
# Popular ElevenLabs voices
ELEVENLABS_VOICE_NAME=Rachel          # Clear, professional female
ELEVENLABS_VOICE_NAME=Adam            # Clear, professional male  
ELEVENLABS_VOICE_NAME=Domi            # Warm, friendly female
ELEVENLABS_VOICE_NAME=Fin             # Friendly, energetic male
ELEVENLABS_VOICE_NAME=Josh            # Deep, authoritative male
ELEVENLABS_VOICE_NAME=Antoni          # Mature, wise male
```

#### Voice Parameters
```python
# Fine-tune voice characteristics
voice_settings = {
    "stability": 0.5,        # Higher = more consistent, Lower = more expressive
    "similarity_boost": 0.75, # Higher = closer to original voice
    "style": 0.0,           # Higher = more stylistic exaggeration  
    "use_speaker_boost": True # Enhanced speaker similarity
}
```

### OpenAI Voice Customization

#### Available Voices
```bash
# OpenAI TTS voices with characteristics
OPENAI_TTS_VOICE=alloy        # Neutral, balanced
OPENAI_TTS_VOICE=echo         # Male, clear
OPENAI_TTS_VOICE=fable        # British accent, articulate
OPENAI_TTS_VOICE=onyx         # Deep male voice
OPENAI_TTS_VOICE=nova         # Female, expressive
OPENAI_TTS_VOICE=shimmer      # Female, whispery
```

#### Speech Parameters
```bash
# Adjust speech characteristics
OPENAI_TTS_SPEED=0.8          # Slower speech (0.25-4.0)
OPENAI_TTS_SPEED=1.2          # Faster speech
OPENAI_TTS_MODEL=tts-1-hd     # High definition model
```

### pyttsx3 Voice Customization

#### System Voice Selection
```python
# List and select system voices
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Select voice by index
engine.setProperty('voice', voices[0].id)  # First voice
engine.setProperty('voice', voices[1].id)  # Second voice

# Adjust speech rate and volume
engine.setProperty('rate', 150)     # Words per minute (default ~200)
engine.setProperty('volume', 0.8)   # Volume level (0.0-1.0)
```

#### Platform-Specific Voices
```bash
# macOS voices
say -v "Alex" "Testing Alex voice"
say -v "Samantha" "Testing Samantha voice"
say -v "Victoria" "Testing Victoria voice"

# Windows voices (via PowerShell)
# List available voices and select different ones

# Linux espeak voices
espeak -v en+f3 "Female voice variant 3"
espeak -v en+m7 "Male voice variant 7"
```

## Performance Optimization

### Response Time Comparison

| Provider | Typical Latency | Network Required | Caching |
|----------|----------------|------------------|---------|
| ElevenLabs | 2-5 seconds | Yes | File cache available |
| OpenAI | 1-3 seconds | Yes | File cache available |
| pyttsx3 | <1 second | No | No caching needed |

### Caching Strategy

#### File-Based Caching
```bash
# Enable TTS file caching
TTS_CACHE_ENABLED=true
TTS_CACHE_DIR=~/.cache/cc-boilerplate/tts
TTS_CACHE_MAX_SIZE=100MB              # Maximum cache size
TTS_CACHE_TTL=86400                   # Time to live (24 hours)
```

#### Cache Management
```python
class TTSCache:
    """
    Intelligent TTS caching system.
    """
    def __init__(self, cache_dir, max_size_mb=100):
        self.cache_dir = Path(cache_dir)
        self.max_size = max_size_mb * 1024 * 1024
        
    def get_cached_audio(self, text, provider, voice):
        """Get cached audio file if available."""
        cache_key = self.generate_cache_key(text, provider, voice)
        cache_file = self.cache_dir / f"{cache_key}.mp3"
        
        if cache_file.exists() and self.is_cache_valid(cache_file):
            return str(cache_file)
        return None
    
    def cache_audio(self, text, provider, voice, audio_file):
        """Cache audio file for future use."""
        cache_key = self.generate_cache_key(text, provider, voice)
        cache_file = self.cache_dir / f"{cache_key}.mp3"
        
        shutil.copy2(audio_file, cache_file)
        self.cleanup_old_cache()
```

### Parallel Processing

```python
def parallel_tts_generation(messages, provider):
    """
    Generate multiple TTS files in parallel.
    """
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for message in messages:
            future = executor.submit(provider.synthesize, message)
            futures.append(future)
        
        results = []
        for future in as_completed(futures):
            try:
                result = future.result(timeout=30)
                results.append(result)
            except Exception as e:
                log_error(f"TTS generation failed: {e}")
                results.append(None)
        
        return results
```

## Troubleshooting

### Common Issues

#### Issue 1: "No TTS providers available"

**Symptoms**:
- Silent failures in notification system
- No audio output from any provider
- Error messages about TTS unavailability

**Diagnostic**:
```bash
# Test each provider individually
echo "Testing ElevenLabs..." && uv run .claude/hooks/utils/tts/elevenlabs_tts.py --text "test" --debug
echo "Testing OpenAI..." && uv run .claude/hooks/utils/tts/openai_tts.py --text "test" --debug
echo "Testing pyttsx3..." && uv run .claude/hooks/utils/tts/pyttsx3_tts.py --text "test" --debug

# Check API keys
echo "ElevenLabs key: ${ELEVENLABS_API_KEY:0:10}..."
echo "OpenAI key: ${OPENAI_API_KEY:0:10}..."

# Test network connectivity
curl -I https://api.elevenlabs.io/v1/user
curl -I https://api.openai.com/v1/models
```

**Solutions**:
1. **Configure at least one provider properly**:
   ```bash
   # Minimum working configuration (free)
   # No API keys needed - pyttsx3 should always work
   python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('test'); engine.runAndWait()"
   ```

2. **Check system TTS installation**:
   ```bash
   # macOS
   say "test"
   
   # Linux
   espeak "test"
   
   # Windows
   powershell -c "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('test')"
   ```

#### Issue 2: Poor Audio Quality

**Symptoms**:
- Robotic or unnatural speech
- Audio artifacts or distortion
- Inconsistent voice quality

**Solutions**:
1. **Upgrade to premium provider**:
   ```bash
   # Switch from pyttsx3 to paid API
   ELEVENLABS_API_KEY=your_key_here
   TTS_DEFAULT_PROVIDER=elevenlabs
   ```

2. **Adjust voice parameters**:
   ```bash
   # ElevenLabs optimization
   ELEVENLABS_STABILITY=0.7          # Increase stability
   ELEVENLABS_SIMILARITY_BOOST=0.8   # Increase similarity
   
   # OpenAI optimization
   OPENAI_TTS_MODEL=tts-1-hd         # Use HD model
   OPENAI_TTS_SPEED=0.9              # Slightly slower for clarity
   ```

#### Issue 3: Slow TTS Performance

**Symptoms**:
- Long delays before audio playback
- Timeouts in TTS generation
- Poor user experience due to latency

**Diagnostic**:
```bash
# Measure TTS performance
time uv run .claude/hooks/utils/tts/elevenlabs_tts.py --text "performance test"
time uv run .claude/hooks/utils/tts/openai_tts.py --text "performance test"
time uv run .claude/hooks/utils/tts/pyttsx3_tts.py --text "performance test"
```

**Solutions**:
1. **Enable caching**:
   ```bash
   TTS_CACHE_ENABLED=true
   TTS_CACHE_DIR=~/.cache/cc-boilerplate/tts
   ```

2. **Use faster provider for development**:
   ```bash
   # Development: Use pyttsx3 for speed
   TTS_DEFAULT_PROVIDER=pyttsx3
   
   # Production: Use ElevenLabs for quality
   TTS_DEFAULT_PROVIDER=elevenlabs
   ```

3. **Optimize network settings**:
   ```bash
   # Increase timeout for slow connections
   TTS_TIMEOUT=60
   
   # Use lower quality model for speed
   OPENAI_TTS_MODEL=tts-1            # Standard quality (faster)
   ```

### Debug Mode

```bash
# Enable comprehensive TTS debugging
export TTS_DEBUG=true
export TTS_VERBOSE=true

# Test with debug output
uv run .claude/hooks/notification.py --debug << 'EOF'
{"message": "Debug test notification"}
EOF
```

### Log Analysis

```bash
# View TTS-related logs
grep "tts\|TTS\|audio" logs/hooks.log | tail -20

# Monitor TTS performance
grep "execution_time.*tts" logs/performance.log

# Check for TTS errors
grep "ERROR.*tts\|TTS.*error" logs/error.log
```

## Advanced Usage

### Custom TTS Integration

#### Adding New TTS Provider

```python
class CustomTTSProvider:
    """
    Template for custom TTS provider integration.
    """
    def __init__(self, config):
        self.config = config
        self.client = self.initialize_client()
    
    def synthesize_speech(self, text, voice=None, **kwargs):
        """
        Convert text to speech using custom provider.
        """
        try:
            # Provider-specific API call
            audio_data = self.client.synthesize(
                text=text,
                voice=voice or self.config.default_voice,
                **kwargs
            )
            
            # Save audio file
            audio_file = self.save_audio_file(audio_data)
            return audio_file
            
        except Exception as e:
            raise TTSError(f"Custom TTS failed: {e}")
    
    def is_available(self):
        """Check if provider is available and configured."""
        return bool(self.config.api_key) and self.test_connection()
```

### Batch TTS Processing

```python
def batch_tts_processing(messages, provider='auto'):
    """
    Process multiple TTS messages efficiently.
    """
    # Group messages by provider for optimization
    batches = group_messages_by_provider(messages, provider)
    
    results = []
    for provider_name, batch_messages in batches.items():
        provider_instance = get_tts_provider(provider_name)
        
        # Process batch with provider-specific optimization
        if provider_instance.supports_batch():
            batch_results = provider_instance.batch_synthesize(batch_messages)
        else:
            # Sequential processing for providers without batch support
            batch_results = []
            for message in batch_messages:
                result = provider_instance.synthesize(message)
                batch_results.append(result)
        
        results.extend(batch_results)
    
    return results
```

### TTS Monitoring and Analytics

```python
class TTSAnalytics:
    """
    TTS usage analytics and monitoring.
    """
    def __init__(self):
        self.metrics = {
            'total_requests': 0,
            'provider_usage': defaultdict(int),
            'average_latency': defaultdict(list),
            'error_rates': defaultdict(int)
        }
    
    def log_tts_request(self, provider, text_length, latency, success):
        """Log TTS request metrics."""
        self.metrics['total_requests'] += 1
        self.metrics['provider_usage'][provider] += 1
        self.metrics['average_latency'][provider].append(latency)
        
        if not success:
            self.metrics['error_rates'][provider] += 1
    
    def generate_report(self):
        """Generate TTS usage report."""
        report = {
            'total_requests': self.metrics['total_requests'],
            'provider_distribution': dict(self.metrics['provider_usage']),
            'average_latencies': {
                provider: sum(latencies) / len(latencies)
                for provider, latencies in self.metrics['average_latency'].items()
            },
            'error_rates': {
                provider: errors / self.metrics['provider_usage'][provider]
                for provider, errors in self.metrics['error_rates'].items()
            }
        }
        return report
```

The CC-Boilerplate TTS system provides a robust, flexible foundation for audio feedback that adapts to your needs, budget, and technical requirements while ensuring audio output is always available through intelligent fallback mechanisms.