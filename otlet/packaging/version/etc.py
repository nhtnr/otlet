from . import LegacyVersion

class TopVersion(LegacyVersion):
    def __init__(self) -> None:
        super().__init__("0")
    
    @property
    def epoch(self) -> int:
        return 100
    
class BottomVersion(LegacyVersion):
    def __init__(self) -> None:
        super().__init__("0")
    
    @property
    def epoch(self) -> int:
        return -2