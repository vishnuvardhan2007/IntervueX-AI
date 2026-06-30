from difflib import SequenceMatcher

ROLE_MAP = {
    "gen ai engineer": {
        "topics": ["Gen AI", "Python", "Machine Learning", "System Design", "Behavioral"],
        "weights": {"Gen AI": 0.40, "Python": 0.20, "Machine Learning": 0.20, "System Design": 0.10, "Behavioral": 0.10},
    },
    "generative ai engineer": {
        "topics": ["Gen AI", "Python", "Machine Learning", "System Design", "Behavioral"],
        "weights": {"Gen AI": 0.40, "Python": 0.20, "Machine Learning": 0.20, "System Design": 0.10, "Behavioral": 0.10},
    },
    "ai engineer": {
        "topics": ["Gen AI", "Machine Learning", "Python", "System Design", "Behavioral"],
        "weights": {"Gen AI": 0.30, "Machine Learning": 0.25, "Python": 0.25, "System Design": 0.10, "Behavioral": 0.10},
    },
    "llm engineer": {
        "topics": ["Gen AI", "NLP", "Python", "Machine Learning", "Behavioral"],
        "weights": {"Gen AI": 0.45, "NLP": 0.20, "Python": 0.15, "Machine Learning": 0.10, "Behavioral": 0.10},
    },
    "ml engineer": {
        "topics": ["Machine Learning", "Python", "Deep Learning", "System Design", "Behavioral"],
        "weights": {"Machine Learning": 0.35, "Python": 0.25, "Deep Learning": 0.20, "System Design": 0.10, "Behavioral": 0.10},
    },
    "machine learning engineer": {
        "topics": ["Machine Learning", "Python", "Deep Learning", "System Design", "Behavioral"],
        "weights": {"Machine Learning": 0.35, "Python": 0.25, "Deep Learning": 0.20, "System Design": 0.10, "Behavioral": 0.10},
    },
    "data scientist": {
        "topics": ["Machine Learning", "Python", "Statistics", "NLP", "Behavioral"],
        "weights": {"Machine Learning": 0.35, "Python": 0.25, "Statistics": 0.20, "NLP": 0.10, "Behavioral": 0.10},
    },
    "nlp engineer": {
        "topics": ["NLP", "Machine Learning", "Python", "Gen AI", "Behavioral"],
        "weights": {"NLP": 0.35, "Machine Learning": 0.20, "Python": 0.20, "Gen AI": 0.15, "Behavioral": 0.10},
    },
    "research intern": {
        "topics": ["Gen AI", "Machine Learning", "Deep Learning", "Python", "Behavioral"],
        "weights": {"Gen AI": 0.30, "Machine Learning": 0.25, "Deep Learning": 0.20, "Python": 0.15, "Behavioral": 0.10},
    },
    "ai research intern": {
        "topics": ["Gen AI", "Machine Learning", "Deep Learning", "Python", "Behavioral"],
        "weights": {"Gen AI": 0.30, "Machine Learning": 0.25, "Deep Learning": 0.20, "Python": 0.15, "Behavioral": 0.10},
    },
    "ml research intern": {
        "topics": ["Machine Learning", "Deep Learning", "Python", "Statistics", "Behavioral"],
        "weights": {"Machine Learning": 0.35, "Deep Learning": 0.25, "Python": 0.20, "Statistics": 0.10, "Behavioral": 0.10},
    },
    "software engineer": {
        "topics": ["Python", "System Design", "Machine Learning", "Behavioral"],
        "weights": {"Python": 0.40, "System Design": 0.30, "Machine Learning": 0.20, "Behavioral": 0.10},
    },
    "deep learning engineer": {
        "topics": ["Deep Learning", "Machine Learning", "Python", "System Design", "Behavioral"],
        "weights": {"Deep Learning": 0.35, "Machine Learning": 0.25, "Python": 0.20, "System Design": 0.10, "Behavioral": 0.10},
    },
    "computer vision engineer": {
        "topics": ["Deep Learning", "Machine Learning", "Python", "Gen AI", "Behavioral"],
        "weights": {"Deep Learning": 0.40, "Machine Learning": 0.25, "Python": 0.20, "Gen AI": 0.05, "Behavioral": 0.10},
    },
    "mlops engineer": {
        "topics": ["System Design", "Machine Learning", "Python", "Deep Learning", "Behavioral"],
        "weights": {"System Design": 0.35, "Machine Learning": 0.25, "Python": 0.25, "Deep Learning": 0.05, "Behavioral": 0.10},
    },
    "data engineer": {
        "topics": ["Python", "System Design", "Statistics", "Machine Learning", "Behavioral"],
        "weights": {"Python": 0.35, "System Design": 0.30, "Statistics": 0.15, "Machine Learning": 0.10, "Behavioral": 0.10},
    },
    "default": {
        "topics": ["Gen AI", "Python", "Machine Learning", "Behavioral"],
        "weights": {"Gen AI": 0.35, "Python": 0.25, "Machine Learning": 0.30, "Behavioral": 0.10},
    },
}

DIFFICULTY_BY_EXPERIENCE = {
    "fresher":  {"easy": 0.50, "medium": 0.40, "hard": 0.10},
    "0-1":      {"easy": 0.35, "medium": 0.45, "hard": 0.20},
    "1-3":      {"easy": 0.20, "medium": 0.50, "hard": 0.30},
    "3-5":      {"easy": 0.10, "medium": 0.40, "hard": 0.50},
    "5+":       {"easy": 0.00, "medium": 0.30, "hard": 0.70},
}

QUESTION_COUNT_BY_EXPERIENCE = {
    "fresher": 8,
    "0-1":     10,
    "1-3":     10,
    "3-5":     12,
    "5+":      12,
}

EXPERIENCE_LABELS = {
    "fresher": "Fresher / No Experience",
    "0-1":     "0–1 Year",
    "1-3":     "1–3 Years",
    "3-5":     "3–5 Years",
    "5+":      "5+ Years",
}


class RulesEngine:
    def get_rules(self, role: str, experience: str) -> dict:
        matched = self._normalize_role(role)
        config = ROLE_MAP[matched]
        return {
            "topics":                config["topics"],
            "weights":               config["weights"],
            "difficulty_distribution": DIFFICULTY_BY_EXPERIENCE.get(experience, DIFFICULTY_BY_EXPERIENCE["fresher"]),
            "total_questions":       QUESTION_COUNT_BY_EXPERIENCE.get(experience, 10),
            "matched_role":          matched,
            "experience_label":      EXPERIENCE_LABELS.get(experience, experience),
        }

    def _normalize_role(self, role: str) -> str:
        role_lower = role.lower().strip()

        if role_lower in ROLE_MAP:
            return role_lower

        for known in ROLE_MAP:
            if known == "default":
                continue
            if known in role_lower or role_lower in known:
                return known

        best, best_ratio = "default", 0.0
        for known in ROLE_MAP:
            if known == "default":
                continue
            ratio = SequenceMatcher(None, role_lower, known).ratio()
            if ratio > best_ratio and ratio > 0.55:
                best_ratio, best = ratio, known

        return best
