import json
import os
import random


class QuestionBank:
    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "questions.json")
        with open(path, "r", encoding="utf-8") as f:
            self.questions = json.load(f)["questions"]

    def get(self, topic: str, difficulty: str, count: int, exclude: set = None) -> list:
        exclude = exclude or set()
        pool = [
            q for q in self.questions
            if q["topic"] == topic and q["difficulty"] == difficulty and q["id"] not in exclude
        ]
        random.shuffle(pool)
        return pool[:count]

    def get_mixed(self, topic: str, dist: dict, count: int, exclude: set = None) -> list:
        exclude = exclude or set()
        result = []

        raw_counts = {d: round(w * count) for d, w in dist.items()}
        total = sum(raw_counts.values())
        diff = count - total
        if diff != 0:
            raw_counts["medium"] = raw_counts.get("medium", 0) + diff

        for difficulty, needed in raw_counts.items():
            if needed <= 0:
                continue
            qs = self.get(topic, difficulty, needed, exclude=exclude | {q["id"] for q in result})
            result.extend(qs)

        return result
