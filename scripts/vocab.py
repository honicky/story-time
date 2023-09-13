import random

words = [
    "Mommy", "Daddy", "baby", "yes", "no", "dog", "cat", "ball", "car", "juice",
    "milk", "cup", "spoon", "bottle", "bed", "shoe", "sock", "hat", "book", "bird",
    "fish", "tree", "flower", "sun", "moon", "star", "water", "bath", "food", "eat",
    "drink", "chair", "table", "door", "house", "toy", "bear", "blanket", "bunny", "bus",
    "apple", "banana", "cookie", "cheese", "ice", "cream", "chocolate", "bread", "candy", "fruit",
    "vegetable", "meat", "egg", "butter", "jam", "peanut", "salt", "sugar", "tea", "coffee",
    "cereal", "rice", "pasta", "soup", "pizza", "sandwich", "salad", "potato", "tomato", "onion",
    "carrot", "bean", "pea", "corn", "pepper", "chicken", "beef", "pork", "lamb", "turkey",
    "duck", "rabbit", "deer", "cow", "sheep", "goat", "horse", "donkey", "pig", "elephant",
    "lion", "tiger", "bear", "giraffe", "zebra", "monkey", "gorilla", "kangaroo", "whale", "shark",
    "dolphin", "octopus", "jellyfish", "turtle", "snake", "lizard", "frog", "toad", "alligator", "crocodile",
    "spider", "ant", "bee", "butterfly", "moth", "fly", "mosquito", "worm", "snail", "slug",
    # Continuing the list with more common words
    "airplane", "train", "bike", "truck", "boat", "helicopter", "scooter", "motorcycle", "wheel", "road",
    "sky", "cloud", "rain", "snow", "wind", "storm", "thunder", "lightning", "fog", "mist",
    "river", "lake", "ocean", "sea", "mountain", "hill", "valley", "desert", "forest", "jungle",
    "island", "beach", "cave", "cliff", "waterfall", "bridge", "tunnel", "tower", "castle", "church",
    "temple", "mosque", "synagogue", "school", "office", "hospital", "store", "restaurant", "hotel", "bank",
    "library", "museum", "zoo", "park", "garden", "farm", "ranch", "factory", "gas", "station",
    "airport", "bus", "station", "train", "station", "port", "harbor", "market", "mall", "theater",
    "cinema", "stadium", "arena", "club", "bar", "cafe", "bakery", "butcher", "pharmacy", "salon",
    "gym", "pool", "spa", "playground", "amusement", "park", "casino", "prison", "cemetery", "graveyard",
    "home", "police", "station", "fire", "station", "post", "office", "church", "mosque",

    # Expanding the list further with more diverse words
    "brother", "sister", "aunt", "uncle", "cousin", "grandma", "grandpa", "friend", "boy", "girl",
    "man", "woman", "teacher", "doctor", "nurse", "policeman", "fireman", "postman", "farmer", "cook",
    "driver", "pilot", "sailor", "soldier", "guard", "thief", "king", "queen", "prince", "princess",
    "robot", "alien", "monster", "dragon", "unicorn", "mermaid", "pirate", "ninja", "cowboy",
    "clown", "magician", "acrobat", "astronaut", "diver", "detective", "spy", "hero", "villain", "victim",
    "hostage", "refugee", "immigrant", "citizen", "native", "resident", "tourist", "visitor", "guest", "stranger",
    "neighbor",
    # More words to get closer to 1000
    "chair", "sofa", "table", "desk", "bed", "mirror", "lamp", "clock", "phone", "computer",
    "television", "radio", "camera", "refrigerator", "oven", "microwave", "toaster", "sink", "bathtub", "toilet",
    "shower", "faucet", "door", "window", "floor", "ceiling", "roof", "wall", "fence", "gate",
    "garden", "lawn", "yard", "balcony", "porch", "patio", "driveway", "garage", "basement", "attic",
    "living", "room", "dining", "room", "kitchen", "bathroom", "bedroom", "office", "study", "library",
    "closet", "pantry", "laundry", "room", "workshop", "shed", "barn", "stable", "pen", "coop",
]

def three_random_words():
    return random.sample(words, 3)
