from pydantic import BaseModel
from typing import Optional, List, Dict

class VoiceAnalysisResult(BaseModel):
    text: Optional[str]
    emotion: Dict[str, float]  # {arousal, valence, dominance}
    voice_features: Dict[str, List[List[float]]]
    
class VoiceResponse(BaseModel):
    text_response: str
    emotion_adapted: bool
    voice_analysis: VoiceAnalysisResult