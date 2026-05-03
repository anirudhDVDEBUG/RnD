"""Game engine: world state, grid, entities, and tick loop."""

from __future__ import annotations
import random
from dataclasses import dataclass, field


@dataclass
class Entity:
    id: str
    name: str
    x: int = 0
    y: int = 0
    kind: str = "object"  # "npc", "object", "item"
    properties: dict = field(default_factory=dict)


class World:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.entities: dict[str, Entity] = {}
        self.tick_count: int = 0
        self.running: bool = True
        self.log: list[str] = []

    def add_entity(self, entity: Entity) -> None:
        self.entities[entity.id] = entity

    def get_state(self) -> dict:
        """Return a serialisable snapshot of the world."""
        return {
            "tick": self.tick_count,
            "size": f"{self.width}x{self.height}",
            "entities": {
                eid: {
                    "name": e.name,
                    "pos": (e.x, e.y),
                    "kind": e.kind,
                    "properties": e.properties,
                }
                for eid, e in self.entities.items()
            },
        }

    def move_entity(self, entity_id: str, x: int, y: int) -> str:
        e = self.entities.get(entity_id)
        if not e:
            return f"Entity {entity_id} not found."
        x = max(0, min(self.width - 1, x))
        y = max(0, min(self.height - 1, y))
        old = (e.x, e.y)
        e.x, e.y = x, y
        msg = f"{e.name} moved from {old} to ({x}, {y})"
        self.log.append(msg)
        return msg

    def tick(self) -> None:
        self.tick_count += 1


def build_demo_world() -> World:
    """Create a small demo world with objects and items."""
    world = World(width=12, height=12)
    world.add_entity(Entity("well", "Town Well", 6, 6, "object", {"type": "landmark"}))
    world.add_entity(Entity("anvil", "Blacksmith Anvil", 2, 3, "object", {"type": "workstation"}))
    world.add_entity(Entity("chest", "Treasure Chest", 10, 9, "object", {"type": "container", "locked": True}))
    world.add_entity(Entity("herb_1", "Moonpetal Herb", 8, 2, "item", {"rarity": "rare"}))
    world.add_entity(Entity("sword_1", "Iron Sword", 3, 3, "item", {"damage": 10}))
    return world
