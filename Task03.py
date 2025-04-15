import re
from difflib import SequenceMatcher

# Common words list (expandable)
COMMON_WORDS = ["password", "123456", "qwerty", "letmein", "admin", "welcome", "the", "and", "have", "that", "for", "you", "with", "say", "this", "they", "but", "his", "from", "not", "she", "as", "what", "their", "can", "who", "get", "would", "her", "all", "make", "about", "know", "will", "one", "time", "there", "year", "think", "when", "which", "them", "some", "people", "take", "out", "into", "just", "see", "him", "your", "come", "could", "now", "than", "like", "other", "how", "then", "its", "our", "two", "more", "these", "want", "way", "look", "first", "also", "new", "because", "day", "use", "man", "find", "here", "thing", "give", "many", "well", "only", "those", "tell", "very", "even", "back", "any", "good", "woman", "through", "life", "child", "work", "down", "may", "after", "should", "call", "world", "over", "school", "still", "try", "last", "ask", "need", "too", "feel", "three", "state", "never", "become", "between", "high", "really", "something", "most", "another", "much", "family", "own", "leave", "put", "old", "while", "mean", "keep", "student", "why", "let", "great", "same", "big", "group", "begin", "seem", "country", "help", "talk", "where", "turn", "problem", "every", "start", "hand", "might", "American", "show", "part", "against", "place", "such", "again", "few", "case", "week", "company", "system", "each", "right", "program", "hear", "question", "during", "play", "government", "run", "small", "number", "off", "always", "move", "night", "live", "Mr", "point", "believe", "hold", "today", "bring", "happen", "next", "without", "before", "large", "million", "must", "home", "under", "water", "room", "write", "mother", "area", "national", "money", "story", "young", "fact", "month", "different", "lot", "study", "book", "eye", "job", "word", "though", "business", "issue", "side", "kind", "four", "head", "far", "black", "long", "both", "little", "house", "yes", "since", "provide", "service", "around", "friend", "important", "father", "sit", "away", "until", "power", "hour", "game", "often", "yet", "line", "political", "end", "among", "ever", "stand", "bad", "lose", "however", "member", "pay", "law", "meet", "car", "city", "almost", "include", "continue", "set", "later", "community", "name", "five", "once", "white", "least", "president", "learn", "real", "change", "team", "minute", "best", "several", "idea", "kid", "body", "information", "nothing", "ago", "lead", "social", "understand", "whether", "watch", "together", "follow", "parent", "stop", "face", "anything", "create", "public", "already", "speak", "others", "read", "level", "allow", "add", "office", "spend", "door", "health", "person", "art", "sure", "war", "history", "party", "within", "grow", "result", "open", "morning", "walk", "reason", "low", "win", "research", "girl", "guy", "early", "food", "moment", "himself", "air", "teacher", "force", "offer", "enough", "education", "across", "although", "remember", "foot", "second", "boy", "maybe", "toward", "able", "age", "policy", "everything", "love", "process", "music", "including", "consider", "appear", "actually", "buy", "probably", "human", "wait", "serve", "market", "die", "send", "expect", "sense", "build", "stay", "fall", "oh", "nation", "plan", "cut", "college", "interest", "death", "course", "someone", "experience", "behind", "reach", "local", "kill", "six", "remain", "effect", "yeah", "suggest", "class", "control", "raise", "care", "perhaps", "late", "hard", "field", "else", "pass", "former", "sell", "major", "sometimes", "require", "along", "development", "themselves", "report", "role", "better", "economic", "effort", "decide", "rate", "strong", "possible", "heart", "drug", "leader", "light", "voice", "wife", "whole", "police", "mind", "finally", "pull", "return", "free", "military", "price", "less", "according", "decision", "explain", "son", "hope", "develop", "view", "relationship", "carry", "town", "road", "drive", "arm", "TRUE", "federal", "break", "difference", "thank", "receive", "value", "international", "building", "action", "full", "model", "join", "season", "society", "tax", "director", "position", "player", "agree", "especially", "record", "pick", "wear", "paper", "special", "space", "ground", "form", "support", "event", "official", "whose", "matter", "everyone", "center", "couple", "site", "project", "hit", "base", "activity", "star", "table", "court", "produce", "eat", "teach", "oil", "half", "situation", "easy", "cost", "industry", "figure", "street", "image", "itself", "phone", "either", "data", "cover", "quite", "picture", "clear", "practice", "piece", "land", "recent", "describe", "product", "doctor", "wall", "patient", "worker", "news", "test", "movie", "certain", "north", "personal", "simply", "third", "technology", "catch", "step", "baby", "computer", "type", "attention", "draw", "film", "Republican", "tree", "source", "red", "nearly", "organization", "choose", "cause", "hair", "century", "evidence", "window", "difficult", "listen", "soon", "culture", "billion", "chance", "brother", "energy", "period", "summer", "realize", "hundred", "available", "plant", "likely", "opportunity", "term", "short", "letter", "condition", "choice", "single", "rule", "daughter", "administration", "south", "husband", "Congress", "floor", "campaign", "material", "population", "economy", "medical", "hospital", "church", "close", "thousand", "risk", "current", "fire", "future", "wrong", "involve", "defense", "anyone", "increase", "security", "bank", "myself", "certainly", "west", "sport", "board", "seek", "per", "subject", "officer", "private", "rest", "behavior", "deal", "performance", "fight", "throw", "top", "quickly", "past", "goal", "bed", "order", "author", "fill", "represent", "focus", "foreign", "drop", "blood", "upon", "agency", "push", "nature", "color", "recently", "store", "reduce", "sound", "note", "fine", "near", "movement", "page", "enter", "share", "common", "poor", "natural", "race", "concern", "series", "significant", "similar", "hot", "language", "usually", "response", "dead", "rise", "animal", "factor", "decade", "article", "shoot", "east", "save", "seven", "artist", "scene", "stock", "career", "despite", "central", "eight"]

def check_criteria(password):
    criteria_scores = {}
    
    # Scoring each criterion strictly
    criteria_scores["length"] = 5 if len(password) >= 12 else (len(password) / 12 * 5)
    criteria_scores["uppercase"] = 5 if sum(1 for char in password if char.isupper()) >= 2 else 0
    criteria_scores["lowercase"] = 5 if sum(1 for char in password if char.islower()) >= 2 else 0
    criteria_scores["digit"] = 5 if sum(1 for char in password if char.isdigit()) >= 3 else 0
    criteria_scores["special_char"] = 5 if sum(1 for char in password if re.search(r"[!@#$%^&*(),.?\":{}|<>]", char)) >= 3 else 0
    criteria_scores["words"] = evaluate_word_similarity(password)

    return criteria_scores

def evaluate_word_similarity(password):
    # Check for whole, partial, or similar words
    max_score = 5
    penalty = 0

    for word in COMMON_WORDS:
        match_ratio = SequenceMatcher(None, word, password).ratio()
        if match_ratio == 1:  # Full match
            penalty = max(penalty, 5)  # Reduce to 0 stars
        elif 0.7 <= match_ratio < 1:  # Near match
            penalty = max(penalty, 4)
        elif 0.3 <= match_ratio < 0.7:  # Partial match
            penalty = max(penalty, 2.5)
        elif len(word) >= 3 and word in password:  # Small word
            penalty = max(penalty, 1.5)
    
    # Calculate final score for "words" criterion
    return max(max_score - penalty, 0)

def evaluate_criteria(criteria_scores):
    feedback = {}
    for criterion, score in criteria_scores.items():
        if score <= 2:
            feedback[criterion] = "Critical: Needs improvement."
        elif 2 < score < 5:
            feedback[criterion] = "Warning: Can be improved."
        else:
            feedback[criterion] = "Pass: Meets requirements."
    
    return feedback

def overall_strength(avg_score):
    if avg_score < 1:
        return "Do Not Use"
    elif 1 <= avg_score < 2:
        return "Weak"
    elif 2 <= avg_score < 3.5:
        return "Moderate"
    elif 3.5 <= avg_score < 4.5:
        return "Strong"
    else:
        return "Secure"

# Input and processing
password = input("Enter a password to check: ")
criteria_scores = check_criteria(password)
feedback = evaluate_criteria(criteria_scores)
average_score = sum(criteria_scores.values()) / len(criteria_scores)
overall_feedback = overall_strength(average_score)

# Output
print("\nPassword Strength Analysis:")
for criterion, score in criteria_scores.items():
    print(f"{criterion.capitalize()} Score: {score:.1f} - {feedback[criterion]}")
print(f"\nAverage Score: {average_score:.1f}")
print(f"Overall Strength: {overall_feedback}")