import os
from typing import Tuple, Optional
import numpy as np
import librosa
from pydub import AudioSegment
from speech_recognition import Recognizer, AudioFile, UnknownValueError, RequestError
from app.core.config import settings
from app.db.models.user import User
from app.schemas.voice import VoiceAnalysisResult  

class VoiceProcessor:
    def __init__(self):
        self.recognizer = Recognizer()
        self.sample_rate = 16000  # Standard for speech recognition
        
    async def process_audio(
        self, 
        user: User,
        audio_bytes: bytes,
        content_type: str = "wav"
    ) -> Tuple[Optional[str], VoiceAnalysisResult]:
        """
        Processes voice input and returns:
        - Transcribed text
        - Emotional analysis
        """
        try:
            # 1. Save temporary audio file
            temp_path = f"temp_audio_{user.id}.{content_type}"
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)
            
            # 2. Convert to proper format if needed
            if content_type != "wav":
                audio = AudioSegment.from_file(temp_path, format=content_type)
                audio.export("converted.wav", format="wav")
                temp_path = "converted.wav"
            
            # 3. Speech-to-Text
            text = await self._transcribe_audio(temp_path)
            
            # 4. Emotional analysis
            emotion = await self._analyze_emotion(temp_path)
            
            return text, VoiceAnalysisResult(
                text=text,
                emotion=emotion,
                voice_features=await self._extract_features(temp_path)
            )
            
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists("converted.wav"):
                os.remove("converted.wav")
    
    async def _transcribe_audio(self, file_path: str) -> Optional[str]:
        """Convert speech to text using Google Web Speech API"""
        try:
            with AudioFile(file_path) as source:
                audio_data = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio_data)
        except UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except RequestError as e:
            print(f"Could not request results from Google: {e}")
            return None
    
    async def _analyze_emotion(self, file_path: str) -> dict:
        """Analyze voice emotion using librosa"""
        y, sr = librosa.load(file_path, sr=self.sample_rate)
        
        # Extract features
        pitch = await self._extract_pitch(y, sr)
        tempo = await self._extract_tempo(y)
        energy = np.mean(librosa.feature.rms(y=y))
        
        # Classify emotion (simplified - replace with your ML model)
        return {
            "arousal": float(np.clip(energy * 2, 0, 1)),  # Energy level 0-1
            "valence": float(np.clip(pitch / 500, 0, 1)),  # Positivity 0-1
            "dominance": float(np.clip(tempo / 200, 0, 1))  # Control 0-1
        }
    
    async def _extract_features(self, file_path: str) -> dict:
        """Extract advanced voice features"""
        y, sr = librosa.load(file_path, sr=self.sample_rate)
        return {
            "mfcc": librosa.feature.mfcc(y=y, sr=sr).tolist(),
            "spectral_centroid": librosa.feature.spectral_centroid(y=y, sr=sr).tolist(),
            "zero_crossing_rate": librosa.feature.zero_crossing_rate(y).tolist()
        }
    
    async def _extract_pitch(self, y: np.ndarray, sr: int) -> float:
        """Extract dominant pitch in Hz"""
        pitches, _ = librosa.piptrack(y=y, sr=sr)
        return np.mean(pitches[pitches > 0])
    
    async def _extract_tempo(self, y: np.ndarray) -> float:
        """Extract tempo in BPM"""
        return float(librosa.beat.tempo(y=y)[0])

voice_processor = VoiceProcessor()