from repositories.memory import MemoryStore


def get_store() -> MemoryStore:
    return MemoryStore()
