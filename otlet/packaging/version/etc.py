from . import Version

class TopVersion(Version):
    def __init__(self) -> None:
        super().__init__("100!0")
    
class BottomVersion(Version):
    def __init__(self) -> None:
        super().__init__("0")
    
    @property
    def epoch(self) -> int:
        return -2