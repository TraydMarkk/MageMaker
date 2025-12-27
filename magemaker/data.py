"""
Mage: The Ascension 20th Anniversary Edition Character Data
Contains all game data for attributes, abilities, backgrounds, spheres, merits, flaws, etc.
"""

# ============================================================================
# ATTRIBUTES
# ============================================================================

ATTRIBUTES = {
    "Physical": ["Strength", "Dexterity", "Stamina"],
    "Social": ["Charisma", "Manipulation", "Appearance"],
    "Mental": ["Perception", "Intelligence", "Wits"]
}

# ============================================================================
# ABILITIES
# ============================================================================

PRIMARY_ABILITIES = {
    "Talents": [
        "Alertness", "Art", "Athletics", "Awareness", "Brawl",
        "Empathy", "Expression", "Intimidation", "Leadership",
        "Streetwise", "Subterfuge"
    ],
    "Skills": [
        "Crafts", "Drive", "Etiquette", "Firearms", "Martial Arts",
        "Meditation", "Melee", "Research", "Stealth", "Survival",
        "Technology"
    ],
    "Knowledges": [
        "Academics", "Computer", "Cosmology", "Enigmas", "Esoterica",
        "Investigation", "Law", "Medicine", "Occult", "Politics", "Science"
    ]
}

SECONDARY_ABILITIES = {
    "Talents": [
        "Animal Kinship", "Blatancy", "Carousing", "Do", "Flying",
        "High Ritual", "Lucid Dreaming", "Seduction"
    ],
    "Skills": [
        "Acrobatics", "Archery", "Biotech", "Energy Weapons",
        "Hypertech", "Jetpack", "Riding", "Torture"
    ],
    "Knowledges": [
        "Area Knowledge", "Belief Systems", "Cultural Savvy",
        "Cryptography", "Demolitions", "Finance", "Lore",
        "Media", "Pharmacopeia"
    ]
}

# ============================================================================
# SPHERES
# ============================================================================

SPHERES = [
    "Correspondence", "Entropy", "Forces", "Life", "Matter",
    "Mind", "Prime", "Spirit", "Time"
]

# Technocratic alternate names for spheres
TECHNOCRATIC_SPHERE_NAMES = {
    "Correspondence": "Data",
    "Prime": "Primal Utility", 
    "Spirit": "Dimensional Science"
}

# ============================================================================
# BACKGROUNDS
# ============================================================================

BACKGROUNDS = {
    "standard": [
        ("Allies", "Friends who'll help you out"),
        ("Alternate Identity", "An established alias"),
        ("Arcane", "Mysterious ability to remain unrecognized"),
        ("Avatar", "Embodiment of the Awakened Self"),
        ("Backup", "Agents you can call upon in emergencies"),
        ("Blessing", "Strange powers gave you an uncanny gift"),
        ("Certification", "Special permits for special things"),
        ("Chantry", "Mystic stronghold"),
        ("Contacts", "Information sources and social networks"),
        ("Cult", "Group of dedicated believers"),
        ("Demesne", "Personal inner dream-space"),
        ("Destiny", "Inspiring sense of great purpose"),
        ("Dream", "Ability to tap into Abilities you don't normally possess"),
        ("Fame", "Notoriety in the Sleeper world"),
        ("Familiar", "Non-human helper with special abilities"),
        ("Influence", "Social clout in the mortal world"),
        ("Legend", "A potent archetype connected to you"),
        ("Library", "Access to special information"),
        ("Mentor", "Awakened elder with a bond to you"),
        ("Node", "A place of power in your possession"),
        ("Past Lives", "Helpful memories from prior incarnations"),
        ("Patron", "Influential benefactor with helpful resources"),
        ("Rank", "A title of importance among the Masses"),
        ("Resources", "Financial credit, cash flow, and property"),
        ("Retainers", "Skilled followers"),
        ("Spies", "Information networks"),
        ("Status", "Favored position among your peers"),
        ("Wonder", "A Talisman, Fetish, or Device")
    ],
    "double_cost": [
        ("Enhancement", "Cybernetic or biotech improvements"),
        ("Sanctum", "Special place to work your arts"),
        ("Totem", "A powerful spirit ally (Shamanic only)")
    ],
    "technocracy_only": [
        ("Requisitions", "Access to Technocratic hardware"),
        ("Secret Weapons", "Guinea-pig status with Technocratic inventors")
    ]
}

# ============================================================================
# AFFILIATIONS / FACTIONS
# ============================================================================

AFFILIATIONS = {
    "Traditions": {
        "Akashayana": {
            "alt_name": "Akashic Brotherhood",
            "description": "Masters of mind, body, and spirit through the Arts of personal discipline",
            "affinity_spheres": ["Mind", "Life"]
        },
        "Celestial Chorus": {
            "alt_name": None,
            "description": "Sacred singers who give a human Voice to the Divine Song",
            "affinity_spheres": ["Prime", "Forces", "Spirit"]
        },
        "Cult of Ecstasy": {
            "alt_name": "Sahajiya",
            "description": "Visionary seers who transcend limitations through sacred experience",
            "affinity_spheres": ["Time", "Life", "Mind"]
        },
        "Dreamspeakers": {
            "alt_name": "Kha'vadi",
            "description": "Preservers and protectors of both the Spirit Ways and the Earthly cultures",
            "affinity_spheres": ["Spirit", "Forces", "Life", "Matter"]
        },
        "Euthanatoi": {
            "alt_name": "Chakravanti",
            "description": "Disciples of mortality who purge corruption and bring merciful release",
            "affinity_spheres": ["Entropy", "Life", "Spirit"]
        },
        "Order of Hermes": {
            "alt_name": None,
            "description": "Rigorous masters of High Magick and the Elemental Arts",
            "affinity_spheres": ["Forces"]
        },
        "Society of Ether": {
            "alt_name": "Sons of Ether",
            "description": "Graceful saviors of scientific potential",
            "affinity_spheres": ["Matter", "Forces", "Prime"]
        },
        "Verbena": {
            "alt_name": None,
            "description": "Primal devotees of rough Nature and mystic blood",
            "affinity_spheres": ["Life", "Forces"]
        },
        "Virtual Adepts": {
            "alt_name": None,
            "description": "Reality-hackers devoted to rebooting their world",
            "affinity_spheres": ["Correspondence", "Forces"]
        }
    },
    "Technocratic Union": {
        "Iteration X": {
            "alt_name": None,
            "description": "Perfectors of the human machine",
            "affinity_spheres": ["Forces", "Matter", "Time"]
        },
        "New World Order": {
            "alt_name": None,
            "description": "Custodians of social order and global stability",
            "affinity_spheres": ["Mind", "Correspondence"]
        },
        "Progenitors": {
            "alt_name": None,
            "description": "Innovators dedicated to the potential of organic life",
            "affinity_spheres": ["Life", "Prime"]
        },
        "Syndicate": {
            "alt_name": None,
            "description": "Masters of finance, status, and the power of wealth",
            "affinity_spheres": ["Entropy", "Mind", "Prime"]
        },
        "Void Engineers": {
            "alt_name": None,
            "description": "Explorers and protectors of extradimensional space",
            "affinity_spheres": ["Spirit", "Correspondence", "Forces"]
        }
    },
    "Disparates": {
        "Ahl-i-Batin": {
            "alt_name": None,
            "description": "Seers of Unity through Divine connection and subtle influence",
            "affinity_spheres": ["Correspondence", "Mind"],
            "forbidden_spheres": ["Entropy"]
        },
        "Bata'a": {
            "alt_name": None,
            "description": "Inheritors of voodoo, dedicated to restoring a broken world",
            "affinity_spheres": ["Life", "Spirit"]
        },
        "Children of Knowledge": {
            "alt_name": None,
            "description": "Crowned Ones devoted to alchemical perfection",
            "affinity_spheres": ["Forces", "Matter", "Prime", "Entropy"]
        },
        "Hollow Ones": {
            "alt_name": None,
            "description": "Dark romantics laughing in the face of ruin",
            "affinity_spheres": SPHERES.copy()  # Any
        },
        "Kopa Loei": {
            "alt_name": None,
            "description": "Defenders of Nature, the Old Gods, and their culture",
            "affinity_spheres": SPHERES.copy()  # Any
        },
        "Ngoma": {
            "alt_name": None,
            "description": "African High Magi, sworn to restore what's been taken",
            "affinity_spheres": ["Life", "Mind", "Prime", "Spirit"]
        },
        "Orphans": {
            "alt_name": None,
            "description": "Self-Awakened mages surviving in the shadows",
            "affinity_spheres": SPHERES.copy()  # Any
        },
        "Sisters of Hippolyta": {
            "alt_name": None,
            "description": "Guardians of the Sacred Feminine",
            "affinity_spheres": ["Life", "Mind"]
        },
        "Taftâni": {
            "alt_name": None,
            "description": "Middle Eastern mystics shaping the gifts of Allah",
            "affinity_spheres": ["Forces", "Matter", "Prime", "Spirit"]
        },
        "Templar Knights": {
            "alt_name": None,
            "description": "Bastions of chivalry in a corrupt age",
            "affinity_spheres": ["Forces", "Life", "Mind", "Prime"]
        },
        "Wu Lung": {
            "alt_name": None,
            "description": "Preservers of heavenly wisdom, order, and nobility",
            "affinity_spheres": ["Spirit", "Forces", "Matter", "Life"]
        }
    }
}

# ============================================================================
# ESSENCES
# ============================================================================

ESSENCES = {
    "Dynamic": "Passionate force for progress and change",
    "Static": "Grounded agent of secure stability",
    "Primordial": "Elusive figure of primal mystery",
    "Questing": "Wandering dreamer of new horizons"
}

# ============================================================================
# ARCHETYPES (Nature & Demeanor)
# ============================================================================

ARCHETYPES = {
    "Activist": "You fix a broken world",
    "Benefactor": "You've got the power to help, and so you do",
    "Contrary": "You invert order to reveal greater truths",
    "Crusader": "You're a front-line fighter for a better tomorrow",
    "Hacker": "You upgrade things by taking them apart",
    "Idealist": "A greater Truth awaits us, and you know what it is",
    "Innovator": "Your imagination drives progress forward",
    "Kid": "Innocent and playful, you inspire others to take care of you",
    "Loner": "You need no one else",
    "Machine": "Weakness is for lesser beings",
    "Mad Scientist": "True science knows no bounds!",
    "Martyr": "It's your pleasure to serve",
    "Monster": "You're the unapologetic shadow in the mirror of your world",
    "Prophet": "Speaking truth to power is your life's work",
    "Rogue": "Rebellion is your gospel and your fame",
    "Sensualist": "Sensation is your drug of choice",
    "Survivor": "No matter what happens, you endure",
    "Traditionalist": "As far as you're concerned, the old ways are best",
    "Trickster": "You make the world your toy",
    "Visionary": "You see beyond the obvious and chase a greater vision"
}

# ============================================================================
# MERITS AND FLAWS
# ============================================================================

MERITS = {
    "Physical": {
        "Acute Senses (Single)": {"cost": 1, "description": "One physical sense is unusually sharp (-2 difficulty to Perception rolls with that sense)"},
        "Acute Senses (All)": {"cost": 3, "description": "All five physical senses are unusually sharp (-2 difficulty to Perception rolls)"},
        "Alcohol/Drug Tolerance (Natural)": {"cost": 1, "description": "Stamina roll to shake off natural intoxicants"},
        "Alcohol/Drug Tolerance (All)": {"cost": 2, "description": "Stamina roll to shake off any intoxicants"},
        "Ambidextrous": {"cost": 1, "description": "No penalty for using off-hand"},
        "Cast-Iron Stomach": {"cost": 1, "description": "Can eat anything without gagging"},
        "Catlike Balance": {"cost": 1, "description": "-2 difficulty on balance-related rolls"},
        "Hyperflexible": {"cost": 1, "description": "-2 difficulty on flexibility rolls"},
        "Light Sleeper": {"cost": 1, "description": "Four hours of sleep works fine; wake up ready for action"},
        "Noble Blood": {"cost": 1, "description": "Physical features link you to a powerful family"},
        "Enchanting Feature": {"cost": 2, "description": "-2 difficulty when deploying a standout physical feature socially"},
        "Physically Impressive": {"cost": 2, "description": "+2 dice to intimidation rolls"},
        "Poison Resistance": {"cost": 2, "description": "+2 dice to Stamina rolls resisting toxins"},
        "Poker Face": {"cost": 2, "description": "-2 difficulty to intimidation/subterfuge; +2 difficulty for others to read you"},
        "Daredevil": {"cost": 3, "description": "+3 dice to non-combat acts of physical recklessness"},
        "Hypersensitivity": {"cost": 3, "description": "-2 difficulty to identify sensory details"},
        "Nightsight": {"cost": 3, "description": "Can see in near-total darkness"},
        "Huge Size": {"cost": 4, "description": "Over 7 feet tall; one extra Bruised health level"},
        "Insensate to Pain": {"cost": 5, "description": "Wound penalties do not affect you"},
        "Too Tough to Die": {"cost": 5, "description": "Can soak lethal damage"}
    },
    "Mental": {
        "Artistically Gifted": {"cost": 1, "description": "-2 difficulty to Art rolls"},
        "Common Sense": {"cost": 1, "description": "Storyteller warns you before doing something stupid"},
        "Computer Aptitude": {"cost": 1, "description": "-2 difficulty to computer rolls"},
        "Concentration": {"cost": 1, "description": "Eliminates modifiers from distractions"},
        "Expert Driver": {"cost": 1, "description": "-2 difficulty to driving rolls"},
        "Language": {"cost": 1, "description": "Understand an additional language"},
        "Lightning Calculator": {"cost": 1, "description": "-2 difficulty to math/calculation rolls"},
        "Mechanical Aptitude": {"cost": 1, "description": "-2 difficulty to mechanical technology rolls"},
        "Time Sense": {"cost": 1, "description": "Intuitive sense of time"},
        "Code of Honor": {"cost": 2, "description": "+2 dice to Willpower when acting according to your code"},
        "Eidetic Memory": {"cost": 2, "description": "Photographic memory"},
        "Inner Strength": {"cost": 2, "description": "-2 difficulty to Willpower rolls against overwhelming odds"},
        "Natural Linguist": {"cost": 2, "description": "Each Language Merit gives 2 languages; +3 dice to communication rolls"},
        "Hyperfocus": {"cost": 3, "description": "Add dice for extended focus on mundane tasks"},
        "Iron Will": {"cost": 3, "description": "+3 dice for Willpower rolls resisting mental influence"},
        "Jack-of-All-Trades": {"cost": 3, "description": "No penalty for untrained Skills; reduced penalty for untrained Knowledges"},
        "Scientific Mystic": {"cost": 3, "description": "Can employ mystic instruments as a technomancer"},
        "Techgnosi": {"cost": 3, "description": "Can employ tech instruments as a mystic"},
        "Berserker": {"cost": 4, "description": "Berserk rage grants combat bonuses but lose control"},
        "Judge's Wisdom": {"cost": 4, "description": "Mastered emotions through self-discipline"},
        "Self-Confident": {"cost": 5, "description": "When Willpower is spent, any success counts"}
    },
    "Social": {
        "Loyalty": {"cost": 1, "description": "Your loyalty inspires others"},
        "Family Support": {"cost": 1, "description": "Your family backs you up"},
        "Natural Leader": {"cost": 1, "description": "-2 difficulty to Leadership rolls"},
        "Pitiable": {"cost": 1, "description": "People want to help you"},
        "Dark Triad": {"cost": 3, "description": "+3 dice to Seduction, Manipulation, Leadership, Subterfuge, and Charisma rolls"},
        "Ties": {"cost": 3, "description": "Connections in a specific social group"},
        "True Love": {"cost": 4, "description": "Willpower restored when pursuing your true love"}
    },
    "Supernatural": {
        "Stormwarden (Personal)": {"cost": 3, "description": "Pass through the Gauntlet without Avatar Storm effects"},
        "Stormwarden (Extended)": {"cost": 5, "description": "Take others through Gauntlet without Avatar Storm effects"},
        "Umbral Affinity": {"cost": 4, "description": "Reduced ill effects from Otherworld travel"},
        "Green Thumb": {"cost": 1, "description": "Plants thrive in your presence"},
        "Burning Aura": {"cost": 2, "description": "Your aura blazes with power"},
        "Medium": {"cost": 2, "description": "Can perceive and communicate with ghosts"},
        "Spirit Sight": {"cost": 4, "description": "Can see spirits without using magick"},
        "Avatar Companion": {"cost": 5, "description": "Your Avatar manifests to aid you"},
        "True Faith": {"cost": 7, "description": "Strong belief grants miraculous powers"}
    }
}

FLAWS = {
    "Physical": {
        "Addiction (Minor)": {"bonus": 1, "description": "Addicted to something trivial"},
        "Child (Near Adult)": {"bonus": 1, "description": "Near the verge of adulthood"},
        "Impediment (Minor)": {"bonus": 1, "description": "Minor physical condition"},
        "Sterile": {"bonus": 1, "description": "Cannot sire/conceive children"},
        "Aging (2 dots)": {"bonus": 2, "description": "Lost 1 Physical Attribute dot to age"},
        "Child (Pre-Adolescent)": {"bonus": 2, "description": "Pre-adolescent young person"},
        "Easily Intoxicated": {"bonus": 2, "description": "+3 difficulty to resist intoxication"},
        "Impediment (Moderate)": {"bonus": 2, "description": "Moderate physical condition (+1 difficulty)"},
        "Repulsive Feature": {"bonus": 2, "description": "+2 difficulty to social rolls involving this feature"},
        "Profiled Appearance": {"bonus": 2, "description": "Your appearance attracts negative attention"},
        "Addiction (Severe)": {"bonus": 3, "description": "Addicted to something dangerous/illegal"},
        "Child (Young)": {"bonus": 3, "description": "Young child"},
        "Degeneration (Cannot Self-Heal)": {"bonus": 3, "description": "Cannot heal without magick/medicine"},
        "Impediment (Significant)": {"bonus": 3, "description": "Significant physical condition (+1 difficulty)"},
        "Monstrous": {"bonus": 3, "description": "Frightening appearance (Appearance 0)"},
        "Permanent Wound": {"bonus": 3, "description": "Always at Wounded health level"},
        "Short": {"bonus": 3, "description": "Shorter than 5 feet tall"},
        "Aging (4 dots)": {"bonus": 4, "description": "Lost 2 Physical Attribute dots to age"},
        "Impediment (Major)": {"bonus": 4, "description": "Major physical condition (+2 difficulty)"},
        "Horrific": {"bonus": 5, "description": "Nightmarishly hideous (+3 difficulty to social rolls)"},
        "Impediment (Profound)": {"bonus": 5, "description": "Profound physical condition (+2 difficulty)"},
        "Mayfly Curse (5 yr)": {"bonus": 5, "description": "Age 1 year per 2 months"},
        "Aging (6 dots)": {"bonus": 6, "description": "Lost 3 Physical Attribute dots to age"},
        "Degeneration (Constant)": {"bonus": 6, "description": "Lose 1 health level every 2 weeks"},
        "Impediment (Severe)": {"bonus": 6, "description": "Severe condition (+2-3 difficulty)"},
        "Degeneration (Aggravated)": {"bonus": 9, "description": "Constant damage that's aggravated"},
        "Mayfly Curse (10 yr)": {"bonus": 10, "description": "Age 1 year per week"}
    },
    "Mental": {
        "Compulsion": {"bonus": 1, "description": "Compelled to perform a specific behavior"},
        "Hero Worship": {"bonus": 1, "description": "Idolize someone to an unhealthy degree"},
        "Nightmares": {"bonus": 1, "description": "Plagued by disturbing dreams"},
        "Phobia (Minor)": {"bonus": 1, "description": "Fear of something that can be avoided"},
        "Absent-Minded": {"bonus": 2, "description": "Forget things and lose track of time"},
        "Chronic Depression": {"bonus": 2, "description": "Suffer from persistent depression"},
        "Intolerance": {"bonus": 2, "description": "Strong prejudice against something"},
        "Phobia (Major)": {"bonus": 2, "description": "Fear of something common"},
        "PTSD (Moderate)": {"bonus": 2, "description": "Triggered memories of trauma"},
        "Deranged (Moderate)": {"bonus": 3, "description": "Suffer from a mental illness"},
        "Mental Lock": {"bonus": 3, "description": "Fixate on tasks to an unhealthy degree"},
        "Phobia (Severe)": {"bonus": 3, "description": "Debilitating fear"},
        "PTSD (Severe)": {"bonus": 3, "description": "Severe triggered memories"},
        "Stress Atavism": {"bonus": 4, "description": "Berserk in stressful situations (liability)"},
        "Deranged (Severe)": {"bonus": 5, "description": "Severe mental illness"},
        "PTSD (Extreme)": {"bonus": 5, "description": "Extreme triggered memories"}
    },
    "Social": {
        "Blacklisted": {"bonus": 1, "description": "Barred from certain groups"},
        "Compulsive Speech": {"bonus": 1, "description": "Cannot keep secrets"},
        "Dark Secret": {"bonus": 1, "description": "A secret that would ruin you"},
        "Construct": {"bonus": 2, "description": "Perceived as manufactured being"},
        "Cultural Other": {"bonus": 2, "description": "Your culture marks you as an outsider"},
        "Debts": {"bonus": 2, "description": "Owe significant debts"},
        "Enemy (Minor)": {"bonus": 1, "description": "Someone wants to harm you"},
        "Enemy (Moderate)": {"bonus": 2, "description": "A dangerous person wants to harm you"},
        "Enemy (Major)": {"bonus": 3, "description": "A powerful person wants to harm you"},
        "Enemy (Severe)": {"bonus": 4, "description": "A very powerful person wants to destroy you"},
        "Enemy (Extreme)": {"bonus": 5, "description": "An extremely powerful enemy seeks your destruction"},
        "Infamy": {"bonus": 2, "description": "Bad reputation"},
        "Mistaken Identity": {"bonus": 2, "description": "Confused with someone else"},
        "Notoriety": {"bonus": 3, "description": "Known for something shameful"},
        "Ward": {"bonus": 3, "description": "Responsible for protecting someone"},
        "Hunted": {"bonus": 4, "description": "Being actively pursued"},
        "Probationary Member": {"bonus": 4, "description": "Not fully trusted by your organization"}
    },
    "Supernatural": {
        "Echoes (Minor)": {"bonus": 1, "description": "Slight supernatural manifestations"},
        "Cursed (Minor)": {"bonus": 1, "description": "Minor quirks of fate"},
        "Anachronism": {"bonus": 2, "description": "Out of place in time"},
        "Apprentice": {"bonus": 2, "description": "Responsible for training a student"},
        "Cursed (Annoying)": {"bonus": 2, "description": "Small but annoying problems"},
        "Echoes (Mild)": {"bonus": 2, "description": "Mild supernatural effects"},
        "Gremlin": {"bonus": 2, "description": "Technology malfunctions around you"},
        "Cursed (Chronic)": {"bonus": 3, "description": "Chronic misfortune"},
        "Echoes (Noticeable)": {"bonus": 3, "description": "Noticeable supernatural manifestations"},
        "Throwback": {"bonus": 3, "description": "Ancestral features mark you as different"},
        "Cursed (Major)": {"bonus": 4, "description": "Major problems arise"},
        "Echoes (Pronounced)": {"bonus": 4, "description": "Pronounced supernatural aura"},
        "Uncanny": {"bonus": 4, "description": "Supernatural creatures react to you"},
        "Cursed (Pervasive)": {"bonus": 5, "description": "Pervasive bad luck"},
        "Echoes (Severe)": {"bonus": 5, "description": "Severe supernatural manifestations"},
        "Permanent Paradox": {"bonus": 5, "description": "Carry permanent Paradox points"},
        "Jinx": {"bonus": 7, "description": "Magick often goes wrong for you"},
        "Branded": {"bonus": 4, "description": "Marked by a supernatural power"},
        "Taint of Corruption": {"bonus": 7, "description": "Touched by dark forces"}
    }
}

# ============================================================================
# CHARACTER CREATION RULES
# ============================================================================

CREATION_RULES = {
    "attributes": {
        "primary": 7,
        "secondary": 5,
        "tertiary": 3,
        "base": 1  # All attributes start at 1
    },
    "abilities": {
        "primary": 13,
        "secondary": 9,
        "tertiary": 5,
        "max_at_creation": 3
    },
    "backgrounds": 7,
    "spheres": 6,
    "arete": {
        "starting": 1,
        "max_at_creation": 3
    },
    "willpower": {
        "starting": 5,
        "max": 10
    },
    "quintessence": {
        "starting": 0,  # Equals Avatar rating
        "max": 10
    },
    "paradox": {
        "starting": 0,
        "max": 10
    },
    "freebie_points": 15,
    "max_flaw_points": 7
}

FREEBIE_COSTS = {
    "attribute": 5,
    "ability": 2,
    "background": 1,
    "sphere": 7,
    "arete": 4,
    "willpower": 1,
    "quintessence": 0.25,  # 1 point per 4 dots
    "merit": 1,  # Merits cost their listed value
    "specialty": 1
}

EXPERIENCE_COSTS = {
    "new_ability": 3,
    "new_sphere": 10,
    "affinity_sphere": 7,  # current rating x 7
    "other_sphere": 8,     # current rating x 8
    "arete": 8,            # current rating x 8
    "attribute": 4,        # current rating x 4
    "ability": 2,          # current rating x 2
    "background": 3,       # current rating x 3
    "willpower": 1,        # current rating x 1
    "specialty": 3
}

# ============================================================================
# SAMPLE CONCEPTS
# ============================================================================

CONCEPTS = [
    "Activist", "Artist", "Athlete", "Caretaker", "Criminal",
    "Executive", "Guardian", "Intellectual", "Kid", "Laborer",
    "Mystic", "Night-Owl", "Rebel", "Technician", "Warrior"
]




