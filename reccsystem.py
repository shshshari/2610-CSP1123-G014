import random

# ── DATASET ────────────────────────────────────────────────────────────────────
STALLS = [
    {
        "id": 1,
        "name": "Stall 1",
        "category": "local",
        "price_range": "cheap",
        "vibe": ["chill", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 2,
        "name": "Stall 2",
        "category": "noodles",
        "price_range": "cheap",
        "vibe": ["quick", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 3,
        "name": "Stall 3",
        "category": "mamak",
        "price_range": "cheap",
        "vibe": ["chaotic", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 4,
        "name": "Stall 4",
        "category": "arab",
        "price_range": "cheap",
        "vibe": ["smokey", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 5,
        "name": "Stall 5",
        "category": "local",
        "price_range": "cheap",
        "vibe": ["chill", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 6,
        "name": "Stall 6",
        "category": "chinese",
        "price_range": "cheap",
        "vibe": ["spicy", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 7,
        "name": "Stall 7",
        "category": "local",
        "price_range": "cheap",
        "vibe": ["explosive", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 8,
        "name": "Stall 8",
        "category": "mamak",
        "price_range": "cheap",
        "vibe": ["diversity", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 9,
        "name": "Stall 9",
        "category": "korean",
        "price_range": "expensive",
        "vibe": ["quirky", "filling"],
        "dietary": ["halal"],
        "description": "description."
    },
    {
        "id": 10,
        "name": "Stall 10",
        "category": "cafe",
        "price_range": "cheap",
        "vibe": ["calm", "happy"],
        "dietary": ["halal"],
        "description": "description."
    },
]

# ── QUESTIONS ──────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": "hunger",
        "question": "How hungry are you right now?",
        "emoji": "🤤",
        "options": {
            "a": {"label": "Starving", "tags": {"vibe": "filling"}},
            "b": {"label": "Not much", "tags": {"vibe": "light"}},
        }
    },
    {
        "id": "mood",
        "question": "What's your vibe today?",
        "emoji": "🤩",
        "options": {
            "a": {"label": "Feeling a little bit dangerous today", "tags": {"vibe": "explosive"}},
            "b": {"label": "I feel so different today", "tags": {"vibe": "quirky"}},
            "c": {"label": "I feel colorful today", "tags": {"vibe": "diversity"}},
            "d": {"label": "I feel so calm today", "tags": {"vibe": "chill"}},
        }
    },
    {
        "id": "budget",
        "question": "What does your budget look like?",
        "emoji": "💸",
        "options": {
            "a": {"label": "Broke student 💔 (under RM10)", "tags": {"price_range": "cheap"}},
            "b": {"label": "Moderate (RM10+)", "tags": {"price_range": "moderate"}},
            "c": {"label": "Treating myself today! (RM15+)", "tags": {"price_range": "expensive"}},
        }
    },
    {
        "id": "dietary",
        "question": "Any dietary preference?",
        "emoji": "👀",
        "options": {
            "a": {"label": "Halal", "tags": {"dietary": "halal"}},
            "b": {"label": "Vegetarian", "tags": {"dietary": "vegetarian"}},
            "c": {"label": "No preference", "tags": {}},
        }
    },
    {
        "id": "category",
        "question": "Feeling any particular cuisine?",
        "emoji": "🍔",
        "options": {
            "a": {"label": "Local / Malay", "tags": {"category": "local"}},
            "b": {"label": "Western", "tags": {"category": "western"}},
            "c": {"label": "Mamak", "tags": {"category": "mamak"}},
            "d": {"label": "Arab", "tags": {"category": "arab"}},
            "e": {"label": "Japanese", "tags": {"category": "japanese"}},
            "f": {"label": "Korean", "tags": {"category": "korean"}},
            "g": {"label": "Chinese", "tags": {"category": "chinese"}},
            "h": {"label": "Anything", "tags": {}},
        }
    },
]

# ── SCORING ENGINE ─────────────────────────────────────────────────────────────
def stall_score(stall, preferences):
    score = 0
    for key, value in preferences.items():
        stall_value = stall.get(key)

        if isinstance(value, list):
            if isinstance(stall_value, list):
                if any(v in stall_value for v in value):
                    score += 1
                else:
                    if stall_value in value:
                        score += 1
                    else:
                        if isinstance(stall_value, list):
                            if value in stall_value:
                                score += 1
                            else:
                                if stall_value == value:
                                    score += 1

                                    return score


# ── RECOMMENDATION ─────────────────────────────────────────────────────────────
def get_recommendation(answers):
    preferences = {}
    for q in QUESTIONS:
        qid = q["id"]
        if qid in answers:
            selected = answers[qid]
            tags = q["options"].get(selected, {}).get("tags", {})
            preferences.update(tags)

            scored = [(stall, stall_score(stall, preferences)) for stall in STALLS]

            if not scored:
                return random.choice(STALLS), "random"

            max_score = max(s for _, s in scored)

            if max_score == 0:
                result = random.choice(STALLS)
                mode = "random"
            else:
                top_stalls = [stall for stall, s in scored if s == max_score]
                result = random.choice(top_stalls)
                mode = "matched"

                return result, mode


# ── REASON GENERATOR ───────────────────────────────────────────────────────────
def generate_reason(stall, preferences):
    reasons = []

    if preferences.get("price_range") == "cheap":
        reasons.append("fits your budget")
    elif preferences.get("price_range") == "expensive":
        reasons.append("because you deserve a treat today")

        if preferences.get("vibe") == "filling":
            reasons.append("will keep you full")
        elif preferences.get("vibe") == "quick":
            reasons.append("is quick to grab")
        elif preferences.get("vibe") == "explosive":
            reasons.append("matches your dangerous mood 🌶️")
        elif preferences.get("vibe") == "quirky":
            reasons.append("matches your unique taste")

            if preferences.get("dietary") == "halal":
                reasons.append("is halal-certified")

                if not reasons:
                    reasons.append("felt right for you today 🎲")

                    return "We picked this because it " + ", and ".join(reasons) + "!"


 # ── TEST RUN ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== MMU Smart Food Recommender — Quiz ===\n")

    user_answers = {}

    for q in QUESTIONS:
        print(f"{q['emoji']}  {q['question']}")
        for key, opt in q["options"].items():
            print(f"   {key}) {opt['label']}")
            choice = input("   Your answer: ").strip().lower()
            user_answers[q["id"]] = choice
            print()

            stall, mode = get_recommendation(user_answers)

            preferences = {}
            for q in QUESTIONS:
                qid = q["id"]
                if qid in user_answers:
                    selected = user_answers[qid]
                    tags = q["options"].get(selected, {}).get("tags", {})
                    preferences.update(tags)

                    print("=" * 45)
                    print(f"🍴  We recommend: {stall['name']}")
                    print(f"📍  {stall['description']}")
                    print(f"💬  {generate_reason(stall, preferences)}")
                    if mode == "random":
                        print("🎲  (Random pick — no strong preference detected)")
                        print("=" * 45)