import math
from .rules import RulesEngine
from .question_bank import QuestionBank

TOPIC_ICONS = {
    "Gen AI":           "🤖",
    "Machine Learning": "📊",
    "Python":           "🐍",
    "NLP":              "💬",
    "Deep Learning":    "🧠",
    "System Design":    "🏗️",
    "Statistics":       "📐",
    "Behavioral":       "🤝",
}


class InterviewGenerator:
    def __init__(self):
        self.rules = RulesEngine()
        self.bank  = QuestionBank()

    def generate(self, name: str, company: str, role: str, experience: str) -> dict:
        rules = self.rules.get_rules(role, experience)

        topic_counts = self._distribute(rules["topics"], rules["weights"], rules["total_questions"])

        sections = []
        used = set()

        for topic, count in topic_counts.items():
            if count <= 0:
                continue

            if topic == "Behavioral":
                qs = self.bank.get(topic, "easy", count, exclude=used)
            else:
                qs = self.bank.get_mixed(topic, rules["difficulty_distribution"], count, exclude=used)

            used.update(q["id"] for q in qs)

            if qs:
                sections.append({
                    "topic": topic,
                    "icon":  TOPIC_ICONS.get(topic, "📌"),
                    "questions": qs,
                })

        all_qs = [q for sec in sections for q in sec["questions"]]
        for i, q in enumerate(all_qs, 1):
            q["number"] = i

        return {
            "candidate": {
                "name":       name,
                "company":    company,
                "role":       role,
                "experience": rules["experience_label"],
            },
            "meta": {
                "matched_role":     rules["matched_role"],
                "total":            len(all_qs),
                "topics_covered":   [s["topic"] for s in sections],
                "difficulty_dist":  rules["difficulty_distribution"],
            },
            "sections": sections,
        }

    @staticmethod
    def _distribute(topics: list, weights: dict, total: int) -> dict:
        counts = {}
        assigned = 0
        for i, topic in enumerate(topics):
            w = weights.get(topic, 1.0 / len(topics))
            if i == len(topics) - 1:
                counts[topic] = max(1, total - assigned)
            else:
                c = max(1, round(w * total))
                counts[topic] = c
                assigned += c

        # clamp if over-budget
        while sum(counts.values()) > total:
            biggest = max(counts, key=lambda t: counts[t])
            if counts[biggest] > 1:
                counts[biggest] -= 1

        return counts
