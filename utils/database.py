import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class InterviewDatabase:
    """Simple JSON-based database for storing interview data"""
    
    def __init__(self, data_dir: str = "data/interviews"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_interview(self, interview_data: Dict) -> str:
        """Save interview data and return the interview ID"""
        interview_id = interview_data.get('interview_id')
        filepath = self.data_dir / f"{interview_id}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(interview_data, f, indent=4, ensure_ascii=False)
        
        return interview_id
    
    def get_interview(self, interview_id: str) -> Optional[Dict]:
        """Retrieve interview data by ID"""
        filepath = self.data_dir / f"{interview_id}.json"
        
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_all_interviews(self) -> List[Dict]:
        """Get all interview records"""
        interviews = []
        
        for filepath in self.data_dir.glob("*.json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                interviews.append(json.load(f))
        
        # Sort by timestamp (newest first)
        interviews.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return interviews
    
    def delete_interview(self, interview_id: str) -> bool:
        """Delete an interview record"""
        filepath = self.data_dir / f"{interview_id}.json"
        
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    
    def get_interview_count(self) -> int:
        """Get total number of interviews"""
        return len(list(self.data_dir.glob("*.json")))
