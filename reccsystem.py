import sqlite3
import random

DB_PATH = "stalls.db"

# to read stalls from db
def get_all_stalls():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stalls")
    rows = cursor.fetchall()
    conn.close()

    stalls = []
    for row in rows:
        stalls.append({
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "price_range": row["price_range"],
            "vibe": row["vibe"].split(","),        # to give spacing in between words for neatness .split
            "dietary": row["dietary"].split(","),  
            "description": row["description"]
        })
        return stalls


    
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


    # score counter
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


 # recommendation generator

    preferences = {}
    for q in QUESTIONS:
        qid = q["id"]
        if qid in answers:
            selected = answers[qid]
            tags = q["options"].get(selected, {}).get("tags", {})
            preferences.update(tags)

            scored = [(stall, stall_score(stall, preferences)) for stall in stalls]

            if not scored:
                return random.choice(stalls), "random", preferences

            max_score = max(s for _, s in scored)

            if max_score == 0:
                result = random.choice(stalls)
                mode = "random"
            else:
                top_stalls = [stall for stall, s in scored if s == max_score]
                result = random.choice(top_stalls)
                mode = "matched"

                return result, mode, preferences


# ─recommendaiton reason generator
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