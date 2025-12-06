"""
Character model for Mage: The Ascension 20th Anniversary Edition
"""

import json
import os
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from .data import (
    ATTRIBUTES, PRIMARY_ABILITIES, SECONDARY_ABILITIES, SPHERES,
    BACKGROUNDS, AFFILIATIONS, CREATION_RULES, FREEBIE_COSTS, EXPERIENCE_COSTS
)


@dataclass
class Character:
    """Represents a Mage character."""
    
    # Identity
    name: str = "New Character"
    player: str = ""
    chronicle: str = ""
    concept: str = ""
    
    # Affiliation
    faction: str = ""  # Traditions, Technocratic Union, Disparates
    group: str = ""    # Specific tradition/convention/craft
    essence: str = ""
    nature: str = ""
    demeanor: str = ""
    
    # Attributes (dict of attribute name -> rating)
    attributes: dict = field(default_factory=lambda: {
        attr: 1 for category in ATTRIBUTES.values() for attr in category
    })
    
    # Priority assignments for creation mode
    attribute_priorities: dict = field(default_factory=lambda: {
        "Physical": None, "Social": None, "Mental": None
    })
    ability_priorities: dict = field(default_factory=lambda: {
        "Talents": None, "Skills": None, "Knowledges": None
    })
    
    # Abilities (dict of ability name -> rating)
    abilities: dict = field(default_factory=dict)
    
    # Specialties (dict of trait name -> list of specialties)
    specialties: dict = field(default_factory=dict)
    
    # Spheres (dict of sphere name -> rating)
    spheres: dict = field(default_factory=lambda: {sphere: 0 for sphere in SPHERES})
    affinity_sphere: str = ""
    
    # Backgrounds (dict of background name -> rating)
    backgrounds: dict = field(default_factory=dict)
    
    # Core traits
    arete: int = 1
    willpower: int = 5
    willpower_current: int = 5
    quintessence: int = 0
    paradox: int = 0
    
    # Health
    health_levels: dict = field(default_factory=lambda: {
        "Bruised": False, "Hurt": False, "Injured": False,
        "Wounded": False, "Mauled": False, "Crippled": False,
        "Incapacitated": False
    })
    
    # Merits and Flaws (dict of name -> cost/bonus)
    merits: dict = field(default_factory=dict)
    flaws: dict = field(default_factory=dict)
    
    # Experience
    experience_total: int = 0
    experience_spent: int = 0
    experience_log: list = field(default_factory=list)
    
    # Character creation tracking
    creation_mode: str = "creation"  # creation, freebie, xp
    freebie_points_spent: int = 0
    
    # Track baseline values from previous modes (cannot be reduced below these)
    creation_baselines: dict = field(default_factory=dict)  # trait_name -> value
    freebie_baselines: dict = field(default_factory=dict)   # trait_name -> value
    
    # Metadata
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_date: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""
    
    # Focus elements
    paradigm: str = ""
    practice: str = ""
    instruments: list = field(default_factory=list)
    
    # Avatar description
    avatar_description: str = ""
    
    def __post_init__(self):
        """Initialize abilities to empty if not set."""
        if not self.abilities:
            self.abilities = {}
    
    @property
    def avatar_rating(self) -> int:
        """Get Avatar rating from backgrounds."""
        return self.backgrounds.get("Avatar", 0)
    
    @property
    def experience_available(self) -> int:
        """Get available experience points."""
        return self.experience_total - self.experience_spent
    
    @property
    def freebie_points_total(self) -> int:
        """Get total freebie points including flaws (flaws add points)."""
        base = CREATION_RULES["freebie_points"]
        flaw_bonus = min(sum(self.flaws.values()), CREATION_RULES["max_flaw_points"])
        return base + flaw_bonus
    
    @property
    def merit_costs(self) -> int:
        """Get total cost of merits (merits cost freebie points)."""
        return sum(self.merits.values())
    
    @property
    def freebie_points_available(self) -> int:
        """Get remaining freebie points (merits subtract from available)."""
        return self.freebie_points_total - self.freebie_points_spent - self.merit_costs
    
    def get_max_sphere_rating(self) -> int:
        """Get max allowed sphere rating (cannot exceed affinity sphere)."""
        if not self.affinity_sphere:
            return 0  # Must have affinity sphere set first
        return self.spheres.get(self.affinity_sphere, 0)
    
    def can_increase_sphere(self, sphere_name: str, to_rating: int) -> bool:
        """Check if a sphere can be increased to the given rating."""
        # Affinity sphere can always be increased (up to Arete limit)
        if sphere_name == self.affinity_sphere:
            return to_rating <= self.arete
        
        # Other spheres cannot exceed affinity sphere rating
        affinity_rating = self.spheres.get(self.affinity_sphere, 0)
        return to_rating <= affinity_rating and to_rating <= self.arete
    
    def get_attribute_category(self, attr_name: str) -> Optional[str]:
        """Get the category for an attribute."""
        for category, attrs in ATTRIBUTES.items():
            if attr_name in attrs:
                return category
        return None
    
    def get_ability_category(self, ability_name: str) -> Optional[str]:
        """Get the category for an ability."""
        for category, abilities in PRIMARY_ABILITIES.items():
            if ability_name in abilities:
                return category
        for category, abilities in SECONDARY_ABILITIES.items():
            if ability_name in abilities:
                return category
        return None
    
    def get_affinity_sphere_options(self) -> list:
        """Get available affinity sphere options based on group."""
        if not self.faction or not self.group:
            return SPHERES.copy()
        
        faction_data = AFFILIATIONS.get(self.faction, {})
        group_data = faction_data.get(self.group, {})
        
        return group_data.get("affinity_spheres", SPHERES.copy())
    
    def get_forbidden_spheres(self) -> list:
        """Get spheres forbidden to this character's group."""
        if not self.faction or not self.group:
            return []
        
        faction_data = AFFILIATIONS.get(self.faction, {})
        group_data = faction_data.get(self.group, {})
        
        return group_data.get("forbidden_spheres", [])
    
    def calculate_creation_dots_spent(self) -> dict:
        """Calculate dots spent in creation mode for each category."""
        result = {
            "attributes": {"Physical": 0, "Social": 0, "Mental": 0},
            "abilities": {"Talents": 0, "Skills": 0, "Knowledges": 0},
            "backgrounds": 0,
            "spheres": 0
        }
        
        # Count attribute dots (minus base 1)
        for category, attrs in ATTRIBUTES.items():
            for attr in attrs:
                result["attributes"][category] += max(0, self.attributes.get(attr, 1) - 1)
        
        # Count ability dots
        for ability, rating in self.abilities.items():
            category = self.get_ability_category(ability)
            if category:
                result["abilities"][category] += rating
        
        # Count background dots
        for bg, rating in self.backgrounds.items():
            # Check if double cost
            double_cost_bgs = [b[0] for b in BACKGROUNDS["double_cost"]]
            if bg in double_cost_bgs:
                result["backgrounds"] += rating * 2
            else:
                result["backgrounds"] += rating
        
        # Count sphere dots
        for sphere, rating in self.spheres.items():
            result["spheres"] += rating
        
        return result
    
    def get_creation_dots_remaining(self) -> dict:
        """Get remaining dots to spend in creation mode."""
        spent = self.calculate_creation_dots_spent()
        rules = CREATION_RULES
        
        # Determine attribute allowances based on priorities
        attr_allowances = {"Physical": 0, "Social": 0, "Mental": 0}
        priority_values = {"primary": rules["attributes"]["primary"],
                         "secondary": rules["attributes"]["secondary"],
                         "tertiary": rules["attributes"]["tertiary"]}
        
        for category, priority in self.attribute_priorities.items():
            if priority:
                attr_allowances[category] = priority_values.get(priority, 0)
        
        # Determine ability allowances based on priorities
        ability_allowances = {"Talents": 0, "Skills": 0, "Knowledges": 0}
        priority_values_abilities = {"primary": rules["abilities"]["primary"],
                                    "secondary": rules["abilities"]["secondary"],
                                    "tertiary": rules["abilities"]["tertiary"]}
        
        for category, priority in self.ability_priorities.items():
            if priority:
                ability_allowances[category] = priority_values_abilities.get(priority, 0)
        
        return {
            "attributes": {
                cat: attr_allowances[cat] - spent["attributes"][cat]
                for cat in ATTRIBUTES.keys()
            },
            "abilities": {
                cat: ability_allowances[cat] - spent["abilities"][cat]
                for cat in PRIMARY_ABILITIES.keys()
            },
            "backgrounds": rules["backgrounds"] - spent["backgrounds"],
            "spheres": rules["spheres"] - spent["spheres"]
        }
    
    def get_minimum_value(self, trait_type: str, trait_name: str) -> int:
        """Get minimum allowed value for a trait (from previous modes)."""
        key = f"{trait_type}:{trait_name}"
        # Check freebie baseline first (highest), then creation baseline
        if key in self.freebie_baselines:
            return self.freebie_baselines[key]
        if key in self.creation_baselines:
            return self.creation_baselines[key]
        # Default minimums
        if trait_type == "attribute":
            return 1  # All attributes start at 1
        return 0
    
    def can_advance_mode(self) -> tuple[bool, list[str]]:
        """Check if character can advance to next mode. Returns (can_advance, warnings)."""
        warnings = []
        
        if self.creation_mode == "creation":
            remaining = self.get_creation_dots_remaining()
            
            # Check attributes
            for cat, dots in remaining["attributes"].items():
                if dots > 0:
                    warnings.append(f"{cat} Attributes: {dots} dots remaining")
            
            # Check abilities
            for cat, dots in remaining["abilities"].items():
                if dots > 0:
                    warnings.append(f"{cat}: {dots} dots remaining")
            
            # Check backgrounds
            if remaining["backgrounds"] > 0:
                warnings.append(f"Backgrounds: {remaining['backgrounds']} dots remaining")
            
            # Check spheres
            if remaining["spheres"] > 0:
                warnings.append(f"Spheres: {remaining['spheres']} dots remaining")
            
            # Check affinity sphere
            if not self.affinity_sphere:
                warnings.append("No Affinity Sphere selected")
            
            return len(warnings) == 0, warnings
        
        elif self.creation_mode == "freebie":
            if self.freebie_points_available > 0:
                warnings.append(f"Freebie Points: {self.freebie_points_available} remaining")
            
            return len(warnings) == 0, warnings
        
        # XP mode - can't advance further
        return False, ["Already in XP mode"]
    
    def calculate_freebie_cost(self, trait_type: str, trait_name: str, 
                              old_value: int, new_value: int) -> int:
        """Calculate freebie point cost for changing a trait."""
        if new_value <= old_value:
            return 0  # No cost for decreases (though they may not be allowed)
        
        costs = FREEBIE_COSTS
        total_cost = 0
        
        # Calculate cost for each dot increase
        for rating in range(old_value, new_value):
            if trait_type == "attribute":
                total_cost += costs["attribute"]
            elif trait_type == "ability":
                total_cost += costs["ability"]
            elif trait_type == "background":
                # Check if double cost
                double_cost_bgs = [b[0] for b in BACKGROUNDS["double_cost"]]
                if trait_name in double_cost_bgs:
                    total_cost += costs["background"] * 2
                else:
                    total_cost += costs["background"]
            elif trait_type == "sphere":
                total_cost += costs["sphere"]
            elif trait_type == "arete":
                total_cost += costs["arete"]
            elif trait_type == "willpower":
                total_cost += costs["willpower"]
            elif trait_type == "quintessence":
                # Quintessence is 1 point per 4 dots
                if (rating + 1) % 4 == 0:
                    total_cost += 1
        
        return total_cost
    
    def calculate_xp_cost(self, trait_type: str, trait_name: str,
                         old_value: int, new_value: int) -> int:
        """Calculate XP cost for changing a trait."""
        if new_value <= old_value:
            return 0  # No cost for decreases (though they may not be allowed)
        
        costs = EXPERIENCE_COSTS
        total_cost = 0
        
        # Calculate cost for each dot increase
        for rating in range(old_value, new_value):
            if trait_type == "attribute":
                total_cost += (rating + 1) * costs["attribute"]
            elif trait_type == "ability":
                if rating == 0:
                    total_cost += costs["new_ability"]
                else:
                    total_cost += (rating + 1) * costs["ability"]
            elif trait_type == "sphere":
                if rating == 0:
                    total_cost += costs["new_sphere"]
                elif trait_name == self.affinity_sphere:
                    total_cost += (rating + 1) * costs["affinity_sphere"]
                else:
                    total_cost += (rating + 1) * costs["other_sphere"]
            elif trait_type == "arete":
                total_cost += (rating + 1) * costs["arete"]
            elif trait_type == "background":
                total_cost += (rating + 1) * costs["background"]
            elif trait_type == "willpower":
                total_cost += (rating + 1) * costs["willpower"]
        
        return total_cost
    
    def snapshot_baseline(self):
        """Snapshot current values as baseline for current mode."""
        # Snapshot all current trait values
        baselines = {}
        
        # Attributes
        for attr, value in self.attributes.items():
            baselines[f"attribute:{attr}"] = value
        
        # Abilities
        for ability, value in self.abilities.items():
            baselines[f"ability:{ability}"] = value
        
        # Backgrounds
        for bg, value in self.backgrounds.items():
            baselines[f"background:{bg}"] = value
        
        # Spheres
        for sphere, value in self.spheres.items():
            baselines[f"sphere:{sphere}"] = value
        
        # Core traits
        baselines["arete"] = self.arete
        baselines["willpower"] = self.willpower
        baselines["quintessence"] = self.quintessence
        
        # Store in appropriate baseline dict
        if self.creation_mode == "creation":
            self.creation_baselines = baselines.copy()
        elif self.creation_mode == "freebie":
            self.freebie_baselines = baselines.copy()
    
    def calculate_xp_cost_for_increase(self, trait_type: str, trait_name: str, 
                                       current_rating: int) -> int:
        """Calculate XP cost to increase a trait by 1."""
        costs = EXPERIENCE_COSTS
        
        if trait_type == "attribute":
            return current_rating * costs["attribute"]
        elif trait_type == "ability":
            if current_rating == 0:
                return costs["new_ability"]
            return current_rating * costs["ability"]
        elif trait_type == "sphere":
            if current_rating == 0:
                return costs["new_sphere"]
            if trait_name == self.affinity_sphere:
                return current_rating * costs["affinity_sphere"]
            return current_rating * costs["other_sphere"]
        elif trait_type == "arete":
            return current_rating * costs["arete"]
        elif trait_type == "background":
            return current_rating * costs["background"]
        elif trait_type == "willpower":
            return current_rating * costs["willpower"]
        
        return 0
    
    def to_dict(self) -> dict:
        """Convert character to dictionary for serialization."""
        return {
            "name": self.name,
            "player": self.player,
            "chronicle": self.chronicle,
            "concept": self.concept,
            "faction": self.faction,
            "group": self.group,
            "essence": self.essence,
            "nature": self.nature,
            "demeanor": self.demeanor,
            "attributes": self.attributes,
            "attribute_priorities": self.attribute_priorities,
            "ability_priorities": self.ability_priorities,
            "abilities": self.abilities,
            "specialties": self.specialties,
            "spheres": self.spheres,
            "affinity_sphere": self.affinity_sphere,
            "backgrounds": self.backgrounds,
            "arete": self.arete,
            "willpower": self.willpower,
            "willpower_current": self.willpower_current,
            "quintessence": self.quintessence,
            "paradox": self.paradox,
            "health_levels": self.health_levels,
            "merits": self.merits,
            "flaws": self.flaws,
            "experience_total": self.experience_total,
            "experience_spent": self.experience_spent,
            "experience_log": self.experience_log,
            "creation_mode": self.creation_mode,
            "freebie_points_spent": self.freebie_points_spent,
            "creation_baselines": self.creation_baselines,
            "freebie_baselines": self.freebie_baselines,
            "created_date": self.created_date,
            "modified_date": self.modified_date,
            "notes": self.notes,
            "paradigm": self.paradigm,
            "practice": self.practice,
            "instruments": self.instruments,
            "avatar_description": self.avatar_description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Character':
        """Create character from dictionary."""
        char = cls()
        for key, value in data.items():
            if hasattr(char, key):
                setattr(char, key, value)
        return char
    
    def save_to_markdown(self, filepath: str):
        """Save character to markdown file."""
        self.modified_date = datetime.now().isoformat()
        
        md_content = self._generate_markdown()
        
        # Append JSON data as a hidden block
        json_data = json.dumps(self.to_dict(), indent=2)
        md_content += f"\n\n<!-- CHARACTER_DATA\n{json_data}\nEND_CHARACTER_DATA -->\n"
        
        with open(filepath, 'w') as f:
            f.write(md_content)
    
    def _generate_markdown(self) -> str:
        """Generate readable markdown representation."""
        lines = []
        lines.append(f"# {self.name}")
        lines.append("")
        
        # Identity
        lines.append("## Identity")
        lines.append(f"- **Player:** {self.player}")
        lines.append(f"- **Chronicle:** {self.chronicle}")
        lines.append(f"- **Concept:** {self.concept}")
        lines.append(f"- **Faction:** {self.faction}")
        lines.append(f"- **Group:** {self.group}")
        lines.append(f"- **Essence:** {self.essence}")
        lines.append(f"- **Nature:** {self.nature}")
        lines.append(f"- **Demeanor:** {self.demeanor}")
        lines.append("")
        
        # Attributes
        lines.append("## Attributes")
        for category, attrs in ATTRIBUTES.items():
            lines.append(f"### {category}")
            for attr in attrs:
                rating = self.attributes.get(attr, 1)
                dots = "●" * rating + "○" * (5 - rating)
                lines.append(f"- **{attr}:** {dots}")
            lines.append("")
        
        # Abilities
        lines.append("## Abilities")
        for category in ["Talents", "Skills", "Knowledges"]:
            lines.append(f"### {category}")
            abilities_in_cat = [a for a in self.abilities.keys() 
                              if self.get_ability_category(a) == category]
            for ability in sorted(abilities_in_cat):
                rating = self.abilities[ability]
                if rating > 0:
                    dots = "●" * rating + "○" * (5 - rating)
                    spec = ""
                    if ability in self.specialties:
                        spec = f" ({', '.join(self.specialties[ability])})"
                    lines.append(f"- **{ability}:** {dots}{spec}")
            lines.append("")
        
        # Spheres
        lines.append("## Spheres")
        lines.append(f"**Affinity Sphere:** {self.affinity_sphere}")
        lines.append("")
        for sphere in SPHERES:
            rating = self.spheres.get(sphere, 0)
            if rating > 0:
                dots = "●" * rating + "○" * (5 - rating)
                affinity = " (Affinity)" if sphere == self.affinity_sphere else ""
                lines.append(f"- **{sphere}:** {dots}{affinity}")
        lines.append("")
        
        # Backgrounds
        lines.append("## Backgrounds")
        for bg, rating in sorted(self.backgrounds.items()):
            if rating > 0:
                dots = "●" * rating + "○" * (5 - rating)
                lines.append(f"- **{bg}:** {dots}")
        lines.append("")
        
        # Core Traits
        lines.append("## Core Traits")
        arete_dots = "●" * self.arete + "○" * (10 - self.arete)
        lines.append(f"- **Arete:** {arete_dots}")
        will_dots = "●" * self.willpower + "○" * (10 - self.willpower)
        lines.append(f"- **Willpower:** {will_dots} (Current: {self.willpower_current})")
        lines.append(f"- **Quintessence:** {self.quintessence}")
        lines.append(f"- **Paradox:** {self.paradox}")
        lines.append("")
        
        # Merits and Flaws
        if self.merits or self.flaws:
            lines.append("## Merits and Flaws")
            if self.merits:
                lines.append("### Merits")
                for merit, cost in sorted(self.merits.items()):
                    lines.append(f"- {merit} ({cost} pts)")
            if self.flaws:
                lines.append("### Flaws")
                for flaw, bonus in sorted(self.flaws.items()):
                    lines.append(f"- {flaw} ({bonus} pts)")
            lines.append("")
        
        # Focus
        lines.append("## Focus")
        lines.append(f"- **Paradigm:** {self.paradigm}")
        lines.append(f"- **Practice:** {self.practice}")
        lines.append(f"- **Instruments:** {', '.join(self.instruments) if self.instruments else 'None'}")
        lines.append("")
        
        # Avatar
        if self.avatar_description:
            lines.append("## Avatar")
            lines.append(self.avatar_description)
            lines.append("")
        
        # Experience
        lines.append("## Experience")
        lines.append(f"- **Total:** {self.experience_total}")
        lines.append(f"- **Spent:** {self.experience_spent}")
        lines.append(f"- **Available:** {self.experience_available}")
        lines.append("")
        
        # Notes
        if self.notes:
            lines.append("## Notes")
            lines.append(self.notes)
            lines.append("")
        
        return "\n".join(lines)
    
    @classmethod
    def load_from_markdown(cls, filepath: str) -> 'Character':
        """Load character from markdown file."""
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Extract JSON data from hidden block
        import re
        match = re.search(r'<!-- CHARACTER_DATA\n(.*?)\nEND_CHARACTER_DATA -->', 
                         content, re.DOTALL)
        
        if match:
            json_data = json.loads(match.group(1))
            return cls.from_dict(json_data)
        
        # Fallback: create new character with just the name from title
        char = cls()
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            char.name = title_match.group(1)
        return char
    
    def export_to_text(self, filepath: str):
        """Export character to plain text file."""
        lines = []
        lines.append("=" * 60)
        lines.append(f"  {self.name.upper()}")
        lines.append("  Mage: The Ascension 20th Anniversary Edition")
        lines.append("=" * 60)
        lines.append("")
        
        # Identity
        lines.append("-" * 30 + " IDENTITY " + "-" * 30)
        lines.append(f"Player: {self.player:<30} Chronicle: {self.chronicle}")
        lines.append(f"Concept: {self.concept:<28} Essence: {self.essence}")
        lines.append(f"Faction: {self.faction:<28} Group: {self.group}")
        lines.append(f"Nature: {self.nature:<29} Demeanor: {self.demeanor}")
        lines.append("")
        
        # Attributes
        lines.append("-" * 28 + " ATTRIBUTES " + "-" * 28)
        
        # Format attributes in columns
        phys = ATTRIBUTES["Physical"]
        soc = ATTRIBUTES["Social"]
        ment = ATTRIBUTES["Mental"]
        
        lines.append(f"{'PHYSICAL':<22} {'SOCIAL':<22} {'MENTAL':<22}")
        for i in range(3):
            p_attr = phys[i]
            s_attr = soc[i]
            m_attr = ment[i]
            p_dots = "●" * self.attributes.get(p_attr, 1) + "○" * (5 - self.attributes.get(p_attr, 1))
            s_dots = "●" * self.attributes.get(s_attr, 1) + "○" * (5 - self.attributes.get(s_attr, 1))
            m_dots = "●" * self.attributes.get(m_attr, 1) + "○" * (5 - self.attributes.get(m_attr, 1))
            lines.append(f"{p_attr:<12} {p_dots}  {s_attr:<12} {s_dots}  {m_attr:<12} {m_dots}")
        lines.append("")
        
        # Abilities
        lines.append("-" * 28 + " ABILITIES " + "-" * 29)
        lines.append(f"{'TALENTS':<22} {'SKILLS':<22} {'KNOWLEDGES':<22}")
        
        talents = [a for a in self.abilities if self.get_ability_category(a) == "Talents"]
        skills = [a for a in self.abilities if self.get_ability_category(a) == "Skills"]
        knowledges = [a for a in self.abilities if self.get_ability_category(a) == "Knowledges"]
        
        max_len = max(len(talents), len(skills), len(knowledges), 1)
        for i in range(max_len):
            t = talents[i] if i < len(talents) else ""
            s = skills[i] if i < len(skills) else ""
            k = knowledges[i] if i < len(knowledges) else ""
            
            t_dots = "●" * self.abilities.get(t, 0) + "○" * (5 - self.abilities.get(t, 0)) if t else "     "
            s_dots = "●" * self.abilities.get(s, 0) + "○" * (5 - self.abilities.get(s, 0)) if s else "     "
            k_dots = "●" * self.abilities.get(k, 0) + "○" * (5 - self.abilities.get(k, 0)) if k else "     "
            
            lines.append(f"{t:<12} {t_dots}  {s:<12} {s_dots}  {k:<12} {k_dots}")
        lines.append("")
        
        # Spheres
        lines.append("-" * 29 + " SPHERES " + "-" * 30)
        lines.append(f"Affinity: {self.affinity_sphere}")
        sphere_strs = []
        for sphere in SPHERES:
            rating = self.spheres.get(sphere, 0)
            dots = "●" * rating + "○" * (5 - rating)
            sphere_strs.append(f"{sphere:<15} {dots}")
        
        # Print in 3 columns
        for i in range(0, len(sphere_strs), 3):
            row = sphere_strs[i:i+3]
            lines.append("  ".join(row))
        lines.append("")
        
        # Backgrounds
        lines.append("-" * 27 + " BACKGROUNDS " + "-" * 28)
        bg_strs = []
        for bg, rating in sorted(self.backgrounds.items()):
            if rating > 0:
                dots = "●" * rating + "○" * (5 - rating)
                bg_strs.append(f"{bg:<15} {dots}")
        
        for i in range(0, len(bg_strs), 3):
            row = bg_strs[i:i+3]
            lines.append("  ".join(row))
        lines.append("")
        
        # Core Traits
        lines.append("-" * 27 + " CORE TRAITS " + "-" * 28)
        arete_dots = "●" * self.arete + "○" * (10 - self.arete)
        will_dots = "●" * self.willpower + "○" * (10 - self.willpower)
        lines.append(f"Arete:       {arete_dots}")
        lines.append(f"Willpower:   {will_dots}  (Current: {self.willpower_current})")
        lines.append(f"Quintessence: {self.quintessence:<5} Paradox: {self.paradox}")
        lines.append("")
        
        # Health
        lines.append("-" * 30 + " HEALTH " + "-" * 30)
        health_labels = ["Bruised -0", "Hurt -1", "Injured -1", "Wounded -2", 
                        "Mauled -2", "Crippled -5", "Incapacitated"]
        for label in health_labels:
            key = label.split()[0]
            marked = "[X]" if self.health_levels.get(key, False) else "[ ]"
            lines.append(f"  {marked} {label}")
        lines.append("")
        
        # Merits and Flaws
        if self.merits or self.flaws:
            lines.append("-" * 26 + " MERITS & FLAWS " + "-" * 26)
            if self.merits:
                lines.append("MERITS:")
                for merit, cost in sorted(self.merits.items()):
                    lines.append(f"  {merit} ({cost} pts)")
            if self.flaws:
                lines.append("FLAWS:")
                for flaw, bonus in sorted(self.flaws.items()):
                    lines.append(f"  {flaw} ({bonus} pts)")
            lines.append("")
        
        # Focus
        lines.append("-" * 30 + " FOCUS " + "-" * 31)
        lines.append(f"Paradigm:    {self.paradigm}")
        lines.append(f"Practice:    {self.practice}")
        lines.append(f"Instruments: {', '.join(self.instruments) if self.instruments else 'None'}")
        lines.append("")
        
        # Experience
        lines.append("-" * 28 + " EXPERIENCE " + "-" * 28)
        lines.append(f"Total: {self.experience_total}  Spent: {self.experience_spent}  Available: {self.experience_available}")
        lines.append("")
        
        # Notes
        if self.notes:
            lines.append("-" * 30 + " NOTES " + "-" * 31)
            lines.append(self.notes)
            lines.append("")
        
        lines.append("=" * 68)
        lines.append(f"Created: {self.created_date}  Modified: {self.modified_date}")
        lines.append("=" * 68)
        
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))

