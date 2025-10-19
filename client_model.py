from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from datetime import datetime
import json


def _dt_to_iso(value):
    if value is None:
        return None
    try:
        # Some gophish objects may already be strings
        if isinstance(value, str):
            return value
        return value.isoformat()
    except Exception:
        return str(value)


@dataclass
class EmailTarget:
    email: str
    count: int = 0


@dataclass
class CampaignInfo:
    id: str
    title: str
    status: str
    sent: int
    opened: int
    clicked: int
    launch_date: Any = None
    send_by_date: Any = None

    def to_dict(self):
        d = asdict(self)
        d["launch_date"] = _dt_to_iso(self.launch_date)
        d["send_by_date"] = _dt_to_iso(self.send_by_date)
        return d


@dataclass
class ClientSummary:
    client: str
    emails: List[EmailTarget] = field(default_factory=list)
    campaigns: List[CampaignInfo] = field(default_factory=list)
    global_stats: Dict[str, int] = field(default_factory=dict)

    def to_dict(self):
        return {
            "client": self.client,
            "emails": [asdict(e) for e in self.emails],
            "campaigns": [c.to_dict() for c in self.campaigns],
            "global_stats": self.global_stats,
        }

    def to_json(self, path=None):
        payload = self.to_dict()
        if path:
            with open(path, 'w') as f:
                json.dump(payload, f, indent=2)
        return json.dumps(payload, indent=2)
