from __future__ import annotations

from uuid import uuid4
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence


@dataclass
class TrackingId:
    ax: int
    bx: int

    @staticmethod
    def New() -> TrackingId:
        ex = uuid4().bytes
        ax, bx = (
            int.from_bytes(ex[i : i + 8], signed=True)
            for i in range(0, len(ex), 8)
        )
        return TrackingId(ax, bx)


@dataclass
class Tag:
    name: str


@dataclass
class Entry:
    tid: TrackingId
    title: str
    content: str
    tags: Sequence[Tag]
    username: str

    @staticmethod
    def New_WithRawTags(
        title: str, content: str, raw_tags: str, username: str
    ) -> Entry:
        tid = TrackingId.New()
        tag_names = (tag.strip() for tag in raw_tags.split(","))
        tags = tuple(Tag(name=name) for name in tag_names)

        return Entry(tid, title, content, tags, username)


class EntryRepository(ABC):

    @abstractmethod
    async def Store(self, entry: Entry) -> None: ...
