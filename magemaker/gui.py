"""
MageMaker GTK4/Adwaita GUI
Main application window with three-panel layout
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Pango

import os
from pathlib import Path
from .character import Character
from .data import (
    ATTRIBUTES, PRIMARY_ABILITIES, SECONDARY_ABILITIES, SPHERES,
    BACKGROUNDS, AFFILIATIONS, ESSENCES, ARCHETYPES, MERITS, FLAWS,
    CREATION_RULES, FREEBIE_COSTS, EXPERIENCE_COSTS, CONCEPTS
)


class DotRating(Gtk.Box):
    """Widget for displaying/editing dot ratings (1-5 or 1-10)."""
    
    def __init__(self, max_dots: int = 5, current: int = 0, min_dots: int = 0,
                 on_change=None, editable: bool = True):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        
        self.max_dots = max_dots
        self.min_dots = min_dots
        self.current = current
        self.on_change = on_change
        self.editable = editable
        self.buttons = []
        
        for i in range(max_dots):
            btn = Gtk.Button()
            btn.set_has_frame(False)
            btn.add_css_class("dot-button")
            btn.set_size_request(20, 20)
            btn.connect("clicked", self._on_dot_clicked, i + 1)
            if not editable:
                btn.set_sensitive(False)
            self.buttons.append(btn)
            self.append(btn)
        
        self._update_display()
    
    def _on_dot_clicked(self, button, dot_num):
        if not self.editable:
            return
        
        # Clicking the current dot reduces by 1, otherwise set to that dot
        if dot_num == self.current:
            new_val = max(self.min_dots, dot_num - 1)
        else:
            new_val = max(self.min_dots, dot_num)
        
        self.set_value(new_val)
    
    def _update_display(self):
        for i, btn in enumerate(self.buttons):
            if i < self.current:
                btn.set_label("●")
                btn.add_css_class("dot-filled")
                btn.remove_css_class("dot-empty")
            else:
                btn.set_label("○")
                btn.add_css_class("dot-empty")
                btn.remove_css_class("dot-filled")
    
    def set_value(self, value: int):
        old_value = self.current
        self.current = max(self.min_dots, min(value, self.max_dots))
        self._update_display()
        if self.on_change and old_value != self.current:
            self.on_change(self.current)
    
    def get_value(self) -> int:
        return self.current
    
    def set_editable(self, editable: bool):
        self.editable = editable
        for btn in self.buttons:
            btn.set_sensitive(editable)


class TraitRow(Gtk.Box):
    """Row widget for a single trait with label and dot rating."""
    
    def __init__(self, name: str, max_dots: int = 5, current: int = 0,
                 min_dots: int = 0, on_change=None, editable: bool = True,
                 show_specialty: bool = False):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.set_hexpand(True)
        
        self.name = name
        self.on_change = on_change
        
        # Label
        label = Gtk.Label(label=name)
        label.set_xalign(0)
        label.set_hexpand(True)
        label.set_width_chars(15)
        self.append(label)
        
        # Specialty entry (optional)
        self.specialty_entry = None
        if show_specialty:
            self.specialty_entry = Gtk.Entry()
            self.specialty_entry.set_placeholder_text("Specialty")
            self.specialty_entry.set_width_chars(12)
            self.append(self.specialty_entry)
        
        # Dot rating
        self.dots = DotRating(max_dots, current, min_dots, 
                             self._on_dots_changed, editable)
        self.append(self.dots)
    
    def _on_dots_changed(self, value):
        if self.on_change:
            self.on_change(self.name, value)
    
    def set_value(self, value: int):
        self.dots.set_value(value)
    
    def get_value(self) -> int:
        return self.dots.get_value()


class CharacterEditor(Gtk.Box):
    """Main character editing panel."""
    
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.app = app
        self.character = None
        self.trait_widgets = {}
        self._updating = False
        
        # Create scrolled content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        # Main content box
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content.set_margin_start(16)
        content.set_margin_end(16)
        content.set_margin_top(16)
        content.set_margin_bottom(16)
        
        # Build sections
        content.append(self._create_identity_section())
        content.append(Gtk.Separator())
        content.append(self._create_attributes_section())
        content.append(Gtk.Separator())
        content.append(self._create_abilities_section())
        content.append(Gtk.Separator())
        content.append(self._create_spheres_section())
        content.append(Gtk.Separator())
        content.append(self._create_backgrounds_section())
        content.append(Gtk.Separator())
        content.append(self._create_core_traits_section())
        content.append(Gtk.Separator())
        content.append(self._create_merits_flaws_section())
        content.append(Gtk.Separator())
        content.append(self._create_focus_section())
        content.append(Gtk.Separator())
        content.append(self._create_notes_section())
        
        scrolled.set_child(content)
        self.append(scrolled)
    
    def _create_section_header(self, title: str) -> Gtk.Label:
        label = Gtk.Label(label=title)
        label.add_css_class("title-2")
        label.set_xalign(0)
        label.set_margin_top(8)
        label.set_margin_bottom(4)
        return label
    
    def _create_identity_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Identity"))
        
        # Name row
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        name_label = Gtk.Label(label="Name:")
        name_label.set_width_chars(12)
        name_label.set_xalign(0)
        self.name_entry = Gtk.Entry()
        self.name_entry.set_hexpand(True)
        self.name_entry.connect("changed", self._on_identity_changed, "name")
        name_box.append(name_label)
        name_box.append(self.name_entry)
        section.append(name_box)
        
        # Player and Chronicle
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        
        player_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        player_label = Gtk.Label(label="Player:")
        player_label.set_width_chars(12)
        player_label.set_xalign(0)
        self.player_entry = Gtk.Entry()
        self.player_entry.set_hexpand(True)
        self.player_entry.connect("changed", self._on_identity_changed, "player")
        player_box.append(player_label)
        player_box.append(self.player_entry)
        player_box.set_hexpand(True)
        row1.append(player_box)
        
        chron_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        chron_label = Gtk.Label(label="Chronicle:")
        chron_label.set_width_chars(12)
        chron_label.set_xalign(0)
        self.chronicle_entry = Gtk.Entry()
        self.chronicle_entry.set_hexpand(True)
        self.chronicle_entry.connect("changed", self._on_identity_changed, "chronicle")
        chron_box.append(chron_label)
        chron_box.append(self.chronicle_entry)
        chron_box.set_hexpand(True)
        row1.append(chron_box)
        
        section.append(row1)
        
        # Concept
        concept_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        concept_label = Gtk.Label(label="Concept:")
        concept_label.set_width_chars(12)
        concept_label.set_xalign(0)
        self.concept_combo = Gtk.ComboBoxText()
        self.concept_combo.set_entry_text_column(0)
        self.concept_combo.append_text("")
        for concept in CONCEPTS:
            self.concept_combo.append_text(concept)
        self.concept_combo.set_hexpand(True)
        self.concept_combo.connect("changed", self._on_identity_changed, "concept")
        concept_box.append(concept_label)
        concept_box.append(self.concept_combo)
        section.append(concept_box)
        
        # Faction and Group
        faction_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        
        faction_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        faction_label = Gtk.Label(label="Faction:")
        faction_label.set_width_chars(12)
        faction_label.set_xalign(0)
        self.faction_combo = Gtk.ComboBoxText()
        self.faction_combo.append_text("")
        for faction in AFFILIATIONS.keys():
            self.faction_combo.append_text(faction)
        self.faction_combo.set_hexpand(True)
        self.faction_combo.connect("changed", self._on_faction_changed)
        faction_box.append(faction_label)
        faction_box.append(self.faction_combo)
        faction_box.set_hexpand(True)
        faction_row.append(faction_box)
        
        group_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        group_label = Gtk.Label(label="Group:")
        group_label.set_width_chars(12)
        group_label.set_xalign(0)
        self.group_combo = Gtk.ComboBoxText()
        self.group_combo.set_hexpand(True)
        self.group_combo.connect("changed", self._on_group_changed)
        group_box.append(group_label)
        group_box.append(self.group_combo)
        group_box.set_hexpand(True)
        faction_row.append(group_box)
        
        section.append(faction_row)
        
        # Essence
        essence_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        essence_label = Gtk.Label(label="Essence:")
        essence_label.set_width_chars(12)
        essence_label.set_xalign(0)
        self.essence_combo = Gtk.ComboBoxText()
        self.essence_combo.append_text("")
        for essence in ESSENCES.keys():
            self.essence_combo.append_text(essence)
        self.essence_combo.set_hexpand(True)
        self.essence_combo.connect("changed", self._on_identity_changed, "essence")
        essence_row.append(essence_label)
        essence_row.append(self.essence_combo)
        section.append(essence_row)
        
        # Nature and Demeanor
        arch_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        
        nature_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        nature_label = Gtk.Label(label="Nature:")
        nature_label.set_width_chars(12)
        nature_label.set_xalign(0)
        self.nature_combo = Gtk.ComboBoxText()
        self.nature_combo.append_text("")
        for archetype in ARCHETYPES.keys():
            self.nature_combo.append_text(archetype)
        self.nature_combo.set_hexpand(True)
        self.nature_combo.connect("changed", self._on_identity_changed, "nature")
        nature_box.append(nature_label)
        nature_box.append(self.nature_combo)
        nature_box.set_hexpand(True)
        arch_row.append(nature_box)
        
        demeanor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        demeanor_label = Gtk.Label(label="Demeanor:")
        demeanor_label.set_width_chars(12)
        demeanor_label.set_xalign(0)
        self.demeanor_combo = Gtk.ComboBoxText()
        self.demeanor_combo.append_text("")
        for archetype in ARCHETYPES.keys():
            self.demeanor_combo.append_text(archetype)
        self.demeanor_combo.set_hexpand(True)
        self.demeanor_combo.connect("changed", self._on_identity_changed, "demeanor")
        demeanor_box.append(demeanor_label)
        demeanor_box.append(self.demeanor_combo)
        demeanor_box.set_hexpand(True)
        arch_row.append(demeanor_box)
        
        section.append(arch_row)
        
        return section
    
    def _create_attributes_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Attributes"))
        
        # Priority selection
        priority_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        priority_label = Gtk.Label(label="Priorities:")
        priority_label.set_margin_end(8)
        priority_box.append(priority_label)
        
        self.attr_priority_combos = {}
        priorities = ["", "primary", "secondary", "tertiary"]
        
        for category in ["Physical", "Social", "Mental"]:
            cat_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            cat_label = Gtk.Label(label=f"{category}:")
            combo = Gtk.ComboBoxText()
            for p in priorities:
                combo.append_text(p.capitalize() if p else "—")
            combo.set_active(0)
            combo.connect("changed", self._on_attr_priority_changed, category)
            self.attr_priority_combos[category] = combo
            cat_box.append(cat_label)
            cat_box.append(combo)
            priority_box.append(cat_box)
        
        section.append(priority_box)
        
        # Attribute rows in columns
        attr_grid = Gtk.Grid()
        attr_grid.set_column_spacing(32)
        attr_grid.set_row_spacing(4)
        
        col = 0
        for category, attrs in ATTRIBUTES.items():
            header = Gtk.Label(label=category.upper())
            header.add_css_class("heading")
            header.set_margin_bottom(4)
            attr_grid.attach(header, col, 0, 1, 1)
            
            for row, attr in enumerate(attrs, 1):
                trait_row = TraitRow(attr, 5, 1, 1, self._on_attribute_changed)
                self.trait_widgets[f"attr_{attr}"] = trait_row
                attr_grid.attach(trait_row, col, row, 1, 1)
            
            col += 1
        
        section.append(attr_grid)
        return section
    
    def _create_abilities_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Abilities"))
        
        # Priority selection
        priority_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        priority_label = Gtk.Label(label="Priorities:")
        priority_label.set_margin_end(8)
        priority_box.append(priority_label)
        
        self.ability_priority_combos = {}
        priorities = ["", "primary", "secondary", "tertiary"]
        
        for category in ["Talents", "Skills", "Knowledges"]:
            cat_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            cat_label = Gtk.Label(label=f"{category}:")
            combo = Gtk.ComboBoxText()
            for p in priorities:
                combo.append_text(p.capitalize() if p else "—")
            combo.set_active(0)
            combo.connect("changed", self._on_ability_priority_changed, category)
            self.ability_priority_combos[category] = combo
            cat_box.append(cat_label)
            cat_box.append(combo)
            priority_box.append(cat_box)
        
        section.append(priority_box)
        
        # Create notebook for Primary/Secondary abilities
        notebook = Gtk.Notebook()
        
        # Primary abilities tab
        primary_box = self._create_abilities_grid(PRIMARY_ABILITIES, "primary")
        notebook.append_page(primary_box, Gtk.Label(label="Primary Abilities"))
        
        # Secondary abilities tab
        secondary_box = self._create_abilities_grid(SECONDARY_ABILITIES, "secondary")
        notebook.append_page(secondary_box, Gtk.Label(label="Secondary Abilities"))
        
        section.append(notebook)
        return section
    
    def _create_abilities_grid(self, abilities_dict: dict, prefix: str) -> Gtk.Box:
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        container.set_margin_top(8)
        container.set_margin_bottom(8)
        
        grid = Gtk.Grid()
        grid.set_column_spacing(32)
        grid.set_row_spacing(4)
        
        col = 0
        for category, abilities in abilities_dict.items():
            header = Gtk.Label(label=category.upper())
            header.add_css_class("heading")
            header.set_margin_bottom(4)
            grid.attach(header, col, 0, 1, 1)
            
            for row, ability in enumerate(abilities, 1):
                trait_row = TraitRow(ability, 5, 0, 0, self._on_ability_changed, 
                                    show_specialty=True)
                self.trait_widgets[f"ability_{ability}"] = trait_row
                grid.attach(trait_row, col, row, 1, 1)
            
            col += 1
        
        container.append(grid)
        return container
    
    def _create_spheres_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Spheres"))
        
        # Affinity sphere selection
        affinity_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        affinity_label = Gtk.Label(label="Affinity Sphere:")
        affinity_label.set_width_chars(15)
        affinity_label.set_xalign(0)
        self.affinity_combo = Gtk.ComboBoxText()
        self.affinity_combo.append_text("")
        for sphere in SPHERES:
            self.affinity_combo.append_text(sphere)
        self.affinity_combo.connect("changed", self._on_affinity_changed)
        affinity_box.append(affinity_label)
        affinity_box.append(self.affinity_combo)
        section.append(affinity_box)
        
        # Sphere grid (3x3)
        sphere_grid = Gtk.Grid()
        sphere_grid.set_column_spacing(32)
        sphere_grid.set_row_spacing(4)
        
        for i, sphere in enumerate(SPHERES):
            row = i // 3
            col = i % 3
            trait_row = TraitRow(sphere, 5, 0, 0, self._on_sphere_changed)
            self.trait_widgets[f"sphere_{sphere}"] = trait_row
            sphere_grid.attach(trait_row, col, row, 1, 1)
        
        section.append(sphere_grid)
        return section
    
    def _create_backgrounds_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Backgrounds"))
        
        # Create expandable rows for each background category
        # Standard backgrounds
        std_expander = Gtk.Expander(label="Standard Backgrounds")
        std_expander.set_expanded(True)
        std_box = Gtk.FlowBox()
        std_box.set_selection_mode(Gtk.SelectionMode.NONE)
        std_box.set_max_children_per_line(3)
        std_box.set_column_spacing(16)
        std_box.set_row_spacing(4)
        
        for bg_name, bg_desc in BACKGROUNDS["standard"]:
            trait_row = TraitRow(bg_name, 5, 0, 0, self._on_background_changed)
            trait_row.set_tooltip_text(bg_desc)
            self.trait_widgets[f"bg_{bg_name}"] = trait_row
            std_box.append(trait_row)
        
        std_expander.set_child(std_box)
        section.append(std_expander)
        
        # Double cost backgrounds
        double_expander = Gtk.Expander(label="Double Cost Backgrounds")
        double_box = Gtk.FlowBox()
        double_box.set_selection_mode(Gtk.SelectionMode.NONE)
        double_box.set_max_children_per_line(3)
        double_box.set_column_spacing(16)
        double_box.set_row_spacing(4)
        
        for bg_name, bg_desc in BACKGROUNDS["double_cost"]:
            trait_row = TraitRow(bg_name, 5, 0, 0, self._on_background_changed)
            trait_row.set_tooltip_text(f"{bg_desc} (Costs double)")
            self.trait_widgets[f"bg_{bg_name}"] = trait_row
            double_box.append(trait_row)
        
        double_expander.set_child(double_box)
        section.append(double_expander)
        
        # Technocracy only
        tech_expander = Gtk.Expander(label="Technocracy Only")
        tech_box = Gtk.FlowBox()
        tech_box.set_selection_mode(Gtk.SelectionMode.NONE)
        tech_box.set_max_children_per_line(3)
        tech_box.set_column_spacing(16)
        tech_box.set_row_spacing(4)
        
        for bg_name, bg_desc in BACKGROUNDS["technocracy_only"]:
            trait_row = TraitRow(bg_name, 5, 0, 0, self._on_background_changed)
            trait_row.set_tooltip_text(f"{bg_desc} (Technocracy only)")
            self.trait_widgets[f"bg_{bg_name}"] = trait_row
            tech_box.append(trait_row)
        
        tech_expander.set_child(tech_box)
        section.append(tech_expander)
        
        return section
    
    def _create_core_traits_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Core Traits"))
        
        # Arete
        arete_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        arete_label = Gtk.Label(label="Arete:")
        arete_label.set_width_chars(15)
        arete_label.set_xalign(0)
        self.arete_dots = DotRating(10, 1, 1, self._on_arete_changed)
        arete_row.append(arete_label)
        arete_row.append(self.arete_dots)
        section.append(arete_row)
        
        # Willpower
        will_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        will_label = Gtk.Label(label="Willpower:")
        will_label.set_width_chars(15)
        will_label.set_xalign(0)
        self.willpower_dots = DotRating(10, 5, 1, self._on_willpower_changed)
        will_row.append(will_label)
        will_row.append(self.willpower_dots)
        section.append(will_row)
        
        # Quintessence and Paradox
        qp_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=32)
        
        quint_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        quint_label = Gtk.Label(label="Quintessence:")
        quint_label.set_width_chars(15)
        quint_label.set_xalign(0)
        self.quintessence_spin = Gtk.SpinButton.new_with_range(0, 20, 1)
        self.quintessence_spin.connect("value-changed", self._on_quintessence_changed)
        quint_box.append(quint_label)
        quint_box.append(self.quintessence_spin)
        qp_row.append(quint_box)
        
        paradox_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        paradox_label = Gtk.Label(label="Paradox:")
        paradox_label.set_width_chars(15)
        paradox_label.set_xalign(0)
        self.paradox_spin = Gtk.SpinButton.new_with_range(0, 20, 1)
        self.paradox_spin.connect("value-changed", self._on_paradox_changed)
        paradox_box.append(paradox_label)
        paradox_box.append(self.paradox_spin)
        qp_row.append(paradox_box)
        
        section.append(qp_row)
        
        return section
    
    def _create_merits_flaws_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Merits & Flaws"))
        
        notebook = Gtk.Notebook()
        
        # Merits tab
        merits_scroll = Gtk.ScrolledWindow()
        merits_scroll.set_min_content_height(200)
        merits_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        merits_box.set_margin_start(8)
        merits_box.set_margin_end(8)
        merits_box.set_margin_top(8)
        
        self.merit_checks = {}
        for category, merits in MERITS.items():
            cat_label = Gtk.Label(label=category)
            cat_label.add_css_class("heading")
            cat_label.set_xalign(0)
            merits_box.append(cat_label)
            
            for merit_name, merit_data in merits.items():
                check_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                check = Gtk.CheckButton(label=f"{merit_name} ({merit_data['cost']} pts)")
                check.set_tooltip_text(merit_data['description'])
                check.connect("toggled", self._on_merit_toggled, merit_name, merit_data['cost'])
                self.merit_checks[merit_name] = check
                check_row.append(check)
                merits_box.append(check_row)
        
        merits_scroll.set_child(merits_box)
        notebook.append_page(merits_scroll, Gtk.Label(label="Merits"))
        
        # Flaws tab
        flaws_scroll = Gtk.ScrolledWindow()
        flaws_scroll.set_min_content_height(200)
        flaws_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        flaws_box.set_margin_start(8)
        flaws_box.set_margin_end(8)
        flaws_box.set_margin_top(8)
        
        self.flaw_checks = {}
        for category, flaws in FLAWS.items():
            cat_label = Gtk.Label(label=category)
            cat_label.add_css_class("heading")
            cat_label.set_xalign(0)
            flaws_box.append(cat_label)
            
            for flaw_name, flaw_data in flaws.items():
                check_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                check = Gtk.CheckButton(label=f"{flaw_name} ({flaw_data['bonus']} pts)")
                check.set_tooltip_text(flaw_data['description'])
                check.connect("toggled", self._on_flaw_toggled, flaw_name, flaw_data['bonus'])
                self.flaw_checks[flaw_name] = check
                check_row.append(check)
                flaws_box.append(check_row)
        
        flaws_scroll.set_child(flaws_box)
        notebook.append_page(flaws_scroll, Gtk.Label(label="Flaws"))
        
        section.append(notebook)
        return section
    
    def _create_focus_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Focus"))
        
        # Paradigm
        para_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        para_label = Gtk.Label(label="Paradigm:")
        para_label.set_width_chars(12)
        para_label.set_xalign(0)
        self.paradigm_entry = Gtk.Entry()
        self.paradigm_entry.set_hexpand(True)
        self.paradigm_entry.connect("changed", self._on_focus_changed, "paradigm")
        para_box.append(para_label)
        para_box.append(self.paradigm_entry)
        section.append(para_box)
        
        # Practice
        prac_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        prac_label = Gtk.Label(label="Practice:")
        prac_label.set_width_chars(12)
        prac_label.set_xalign(0)
        self.practice_entry = Gtk.Entry()
        self.practice_entry.set_hexpand(True)
        self.practice_entry.connect("changed", self._on_focus_changed, "practice")
        prac_box.append(prac_label)
        prac_box.append(self.practice_entry)
        section.append(prac_box)
        
        # Instruments
        inst_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        inst_label = Gtk.Label(label="Instruments:")
        inst_label.set_width_chars(12)
        inst_label.set_xalign(0)
        self.instruments_entry = Gtk.Entry()
        self.instruments_entry.set_hexpand(True)
        self.instruments_entry.set_placeholder_text("Comma-separated list")
        self.instruments_entry.connect("changed", self._on_focus_changed, "instruments")
        inst_box.append(inst_label)
        inst_box.append(self.instruments_entry)
        section.append(inst_box)
        
        # Avatar description
        avatar_label = Gtk.Label(label="Avatar Description:")
        avatar_label.set_xalign(0)
        section.append(avatar_label)
        
        self.avatar_text = Gtk.TextView()
        self.avatar_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.avatar_text.get_buffer().connect("changed", self._on_avatar_changed)
        
        avatar_frame = Gtk.Frame()
        avatar_frame.set_child(self.avatar_text)
        avatar_frame.set_size_request(-1, 80)
        section.append(avatar_frame)
        
        return section
    
    def _create_notes_section(self) -> Gtk.Box:
        section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        section.append(self._create_section_header("Notes"))
        
        self.notes_text = Gtk.TextView()
        self.notes_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.notes_text.get_buffer().connect("changed", self._on_notes_changed)
        
        notes_frame = Gtk.Frame()
        notes_frame.set_child(self.notes_text)
        notes_frame.set_size_request(-1, 120)
        section.append(notes_frame)
        
        return section
    
    # Event handlers
    def _on_identity_changed(self, widget, field):
        if self._updating or not self.character:
            return
        
        if field == "name":
            self.character.name = widget.get_text()
        elif field == "player":
            self.character.player = widget.get_text()
        elif field == "chronicle":
            self.character.chronicle = widget.get_text()
        elif field == "concept":
            self.character.concept = widget.get_active_text() or ""
        elif field == "essence":
            self.character.essence = widget.get_active_text() or ""
        elif field == "nature":
            self.character.nature = widget.get_active_text() or ""
        elif field == "demeanor":
            self.character.demeanor = widget.get_active_text() or ""
        
        self.app.update_tracker()
    
    def _on_faction_changed(self, widget):
        if self._updating or not self.character:
            return
        
        faction = widget.get_active_text() or ""
        self.character.faction = faction
        
        # Update group combo
        self.group_combo.remove_all()
        self.group_combo.append_text("")
        
        if faction and faction in AFFILIATIONS:
            for group in AFFILIATIONS[faction].keys():
                self.group_combo.append_text(group)
        
        self.character.group = ""
        self.app.update_tracker()
    
    def _on_group_changed(self, widget):
        if self._updating or not self.character:
            return
        
        self.character.group = widget.get_active_text() or ""
        
        # Update affinity sphere options
        self._update_affinity_options()
        self.app.update_tracker()
    
    def _update_affinity_options(self):
        if not self.character:
            return
        
        available = self.character.get_affinity_sphere_options()
        current = self.affinity_combo.get_active_text()
        
        self._updating = True
        self.affinity_combo.remove_all()
        self.affinity_combo.append_text("")
        
        for sphere in SPHERES:
            if sphere in available:
                self.affinity_combo.append_text(sphere)
        
        # Restore selection if still valid
        if current in available:
            model = self.affinity_combo.get_model()
            for i, row in enumerate(model):
                if row[0] == current:
                    self.affinity_combo.set_active(i)
                    break
        
        self._updating = False
    
    def _on_attr_priority_changed(self, widget, category):
        if self._updating or not self.character:
            return
        
        text = widget.get_active_text()
        priority = text.lower() if text and text != "—" else None
        self.character.attribute_priorities[category] = priority
        self._update_attr_priority_options()
        self.app.update_tracker()
    
    def _on_ability_priority_changed(self, widget, category):
        if self._updating or not self.character:
            return
        
        text = widget.get_active_text()
        priority = text.lower() if text and text != "—" else None
        self.character.ability_priorities[category] = priority
        self._update_ability_priority_options()
        self.app.update_tracker()
    
    def _update_attr_priority_options(self):
        """Update attribute priority combos to hide already-selected priorities."""
        if self._updating or not self.character:
            return
        
        self._updating = True
        
        # Get currently selected priorities
        selected = {}
        for cat, combo in self.attr_priority_combos.items():
            text = combo.get_active_text()
            if text and text != "—":
                selected[cat] = text.lower()
        
        # Used priorities (excluding current category)
        for cat, combo in self.attr_priority_combos.items():
            current_selection = selected.get(cat)
            used_by_others = [p for c, p in selected.items() if c != cat]
            
            # Rebuild combo options
            combo.remove_all()
            combo.append_text("—")
            
            for priority in ["primary", "secondary", "tertiary"]:
                # Only show if not used by another category
                if priority not in used_by_others:
                    combo.append_text(priority.capitalize())
            
            # Restore selection
            if current_selection:
                model = combo.get_model()
                for i, row in enumerate(model):
                    if row[0] and row[0].lower() == current_selection:
                        combo.set_active(i)
                        break
            else:
                combo.set_active(0)
        
        self._updating = False
    
    def _update_ability_priority_options(self):
        """Update ability priority combos to hide already-selected priorities."""
        if self._updating or not self.character:
            return
        
        self._updating = True
        
        # Get currently selected priorities
        selected = {}
        for cat, combo in self.ability_priority_combos.items():
            text = combo.get_active_text()
            if text and text != "—":
                selected[cat] = text.lower()
        
        # Used priorities (excluding current category)
        for cat, combo in self.ability_priority_combos.items():
            current_selection = selected.get(cat)
            used_by_others = [p for c, p in selected.items() if c != cat]
            
            # Rebuild combo options
            combo.remove_all()
            combo.append_text("—")
            
            for priority in ["primary", "secondary", "tertiary"]:
                # Only show if not used by another category
                if priority not in used_by_others:
                    combo.append_text(priority.capitalize())
            
            # Restore selection
            if current_selection:
                model = combo.get_model()
                for i, row in enumerate(model):
                    if row[0] and row[0].lower() == current_selection:
                        combo.set_active(i)
                        break
            else:
                combo.set_active(0)
        
        self._updating = False
    
    def _change_trait(self, trait_type: str, trait_name: str, new_value: int, 
                     current_value: int = None) -> bool:
        """Handle trait changes with cost calculation and restrictions.
        Returns True if change was successful, False if blocked."""
        if self._updating or not self.character:
            return False
        
        char = self.character
        
        # Get current value if not provided
        if current_value is None:
            if trait_type == "attribute":
                current_value = char.attributes.get(trait_name, 1)
            elif trait_type == "ability":
                current_value = char.abilities.get(trait_name, 0)
            elif trait_type == "sphere":
                current_value = char.spheres.get(trait_name, 0)
            elif trait_type == "background":
                current_value = char.backgrounds.get(trait_name, 0)
            elif trait_type == "arete":
                current_value = char.arete
            elif trait_type == "willpower":
                current_value = char.willpower
            elif trait_type == "quintessence":
                current_value = char.quintessence
            else:
                return False
        
        # Check minimum value (cannot go below baseline from previous modes)
        min_value = char.get_minimum_value(trait_type, trait_name)
        if new_value < min_value:
            # Revert to minimum
            widget = self.trait_widgets.get(f"{trait_type}_{trait_name}")
            if widget:
                self._updating = True
                widget.set_value(min_value)
                self._updating = False
            
            dialog = Adw.MessageDialog(
                transient_for=self.app.win,
                heading="Cannot Reduce Trait",
                body=f"Cannot reduce {trait_name} below {min_value} (set in previous mode)."
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            return False
        
        # Handle costs based on mode
        if char.creation_mode == "freebie" and not self.app.tracker.storyteller_override:
            # Calculate freebie cost
            cost = char.calculate_freebie_cost(trait_type, trait_name, current_value, new_value)
            if cost > 0:
                if cost > char.freebie_points_available:
                    dialog = Adw.MessageDialog(
                        transient_for=self.app.win,
                        heading="Insufficient Freebie Points",
                        body=f"Need {cost} freebie points, but only {char.freebie_points_available} available."
                    )
                    dialog.add_response("ok", "OK")
                    dialog.present()
                    # Revert
                    widget = self.trait_widgets.get(f"{trait_type}_{trait_name}")
                    if widget:
                        self._updating = True
                        widget.set_value(current_value)
                        self._updating = False
                    return False
                
                char.freebie_points_spent += cost
        
        elif char.creation_mode == "xp" and not self.app.tracker.storyteller_override:
            # Calculate XP cost
            cost = char.calculate_xp_cost(trait_type, trait_name, current_value, new_value)
            if cost > 0:
                if cost > char.experience_available:
                    dialog = Adw.MessageDialog(
                        transient_for=self.app.win,
                        heading="Insufficient Experience Points",
                        body=f"Need {cost} XP, but only {char.experience_available} available."
                    )
                    dialog.add_response("ok", "OK")
                    dialog.present()
                    # Revert
                    widget = self.trait_widgets.get(f"{trait_type}_{trait_name}")
                    if widget:
                        self._updating = True
                        widget.set_value(current_value)
                        self._updating = False
                    return False
                
                char.experience_spent += cost
        
        # Apply the change
        if trait_type == "attribute":
            char.attributes[trait_name] = new_value
        elif trait_type == "ability":
            if new_value > 0:
                char.abilities[trait_name] = new_value
            elif trait_name in char.abilities:
                del char.abilities[trait_name]
        elif trait_type == "sphere":
            char.spheres[trait_name] = new_value
        elif trait_type == "background":
            if new_value > 0:
                char.backgrounds[trait_name] = new_value
            elif trait_name in char.backgrounds:
                del char.backgrounds[trait_name]
        elif trait_type == "arete":
            char.arete = new_value
        elif trait_type == "willpower":
            char.willpower = new_value
            char.willpower_current = min(char.willpower_current, new_value)
        elif trait_type == "quintessence":
            char.quintessence = new_value
        
        self.app.update_tracker()
        return True
    
    def _on_attribute_changed(self, name, value):
        self._change_trait("attribute", name, value)
    
    def _on_ability_changed(self, name, value):
        self._change_trait("ability", name, value)
    
    def _on_sphere_changed(self, name, value):
        if self._updating or not self.character:
            return
        
        # Validate: non-affinity spheres cannot exceed affinity sphere rating
        if name != self.character.affinity_sphere and self.character.affinity_sphere:
            affinity_rating = self.character.spheres.get(self.character.affinity_sphere, 0)
            if value > affinity_rating:
                # Revert to max allowed
                value = affinity_rating
                widget = self.trait_widgets.get(f"sphere_{name}")
                if widget:
                    self._updating = True
                    widget.set_value(value)
                    self._updating = False
        
        self._change_trait("sphere", name, value)
    
    def _on_affinity_changed(self, widget):
        if self._updating or not self.character:
            return
        
        new_affinity = widget.get_active_text() or ""
        old_affinity = self.character.affinity_sphere
        self.character.affinity_sphere = new_affinity
        
        # When affinity changes, cap all other spheres to new affinity rating
        if new_affinity:
            new_affinity_rating = self.character.spheres.get(new_affinity, 0)
            self._updating = True
            for sphere in SPHERES:
                if sphere != new_affinity:
                    current = self.character.spheres.get(sphere, 0)
                    if current > new_affinity_rating:
                        self.character.spheres[sphere] = new_affinity_rating
                        sphere_widget = self.trait_widgets.get(f"sphere_{sphere}")
                        if sphere_widget:
                            sphere_widget.set_value(new_affinity_rating)
            self._updating = False
        
        self.app.update_tracker()
    
    def _on_background_changed(self, name, value):
        self._change_trait("background", name, value)
    
    def _on_arete_changed(self, value):
        self._change_trait("arete", "Arete", value)
    
    def _on_willpower_changed(self, value):
        self._change_trait("willpower", "Willpower", value)
    
    def _on_quintessence_changed(self, widget):
        value = int(widget.get_value())
        self._change_trait("quintessence", "Quintessence", value)
    
    def _on_paradox_changed(self, widget):
        if self._updating or not self.character:
            return
        self.character.paradox = int(widget.get_value())
        self.app.update_tracker()
    
    def _on_merit_toggled(self, widget, name, cost):
        if self._updating or not self.character:
            return
        if widget.get_active():
            self.character.merits[name] = cost
        elif name in self.character.merits:
            del self.character.merits[name]
        self.app.update_tracker()
    
    def _on_flaw_toggled(self, widget, name, bonus):
        if self._updating or not self.character:
            return
        if widget.get_active():
            self.character.flaws[name] = bonus
        elif name in self.character.flaws:
            del self.character.flaws[name]
        self.app.update_tracker()
    
    def _on_focus_changed(self, widget, field):
        if self._updating or not self.character:
            return
        
        if field == "paradigm":
            self.character.paradigm = widget.get_text()
        elif field == "practice":
            self.character.practice = widget.get_text()
        elif field == "instruments":
            text = widget.get_text()
            self.character.instruments = [i.strip() for i in text.split(",") if i.strip()]
    
    def _on_avatar_changed(self, buffer):
        if self._updating or not self.character:
            return
        start, end = buffer.get_bounds()
        self.character.avatar_description = buffer.get_text(start, end, False)
    
    def _on_notes_changed(self, buffer):
        if self._updating or not self.character:
            return
        start, end = buffer.get_bounds()
        self.character.notes = buffer.get_text(start, end, False)
    
    def load_character(self, character: Character):
        """Load a character into the editor."""
        self._updating = True
        self.character = character
        
        # Identity
        self.name_entry.set_text(character.name)
        self.player_entry.set_text(character.player)
        self.chronicle_entry.set_text(character.chronicle)
        
        # Set combo boxes
        self._set_combo_text(self.concept_combo, character.concept)
        self._set_combo_text(self.faction_combo, character.faction)
        
        # Update group options
        self.group_combo.remove_all()
        self.group_combo.append_text("")
        if character.faction in AFFILIATIONS:
            for group in AFFILIATIONS[character.faction].keys():
                self.group_combo.append_text(group)
        self._set_combo_text(self.group_combo, character.group)
        
        self._set_combo_text(self.essence_combo, character.essence)
        self._set_combo_text(self.nature_combo, character.nature)
        self._set_combo_text(self.demeanor_combo, character.demeanor)
        
        # Priorities
        priority_map = {"primary": 1, "secondary": 2, "tertiary": 3}
        for cat, priority in character.attribute_priorities.items():
            combo = self.attr_priority_combos.get(cat)
            if combo:
                combo.set_active(priority_map.get(priority, 0))
        
        for cat, priority in character.ability_priorities.items():
            combo = self.ability_priority_combos.get(cat)
            if combo:
                combo.set_active(priority_map.get(priority, 0))
        
        # Attributes
        for attr, value in character.attributes.items():
            widget = self.trait_widgets.get(f"attr_{attr}")
            if widget:
                widget.set_value(value)
        
        # Abilities
        for key, widget in self.trait_widgets.items():
            if key.startswith("ability_"):
                ability = key[8:]
                widget.set_value(character.abilities.get(ability, 0))
        
        # Spheres
        self._update_affinity_options()
        self._set_combo_text(self.affinity_combo, character.affinity_sphere)
        
        for sphere, value in character.spheres.items():
            widget = self.trait_widgets.get(f"sphere_{sphere}")
            if widget:
                widget.set_value(value)
        
        # Backgrounds
        for key, widget in self.trait_widgets.items():
            if key.startswith("bg_"):
                bg = key[3:]
                widget.set_value(character.backgrounds.get(bg, 0))
        
        # Core traits
        self.arete_dots.set_value(character.arete)
        self.willpower_dots.set_value(character.willpower)
        self.quintessence_spin.set_value(character.quintessence)
        self.paradox_spin.set_value(character.paradox)
        
        # Merits and Flaws
        for name, check in self.merit_checks.items():
            check.set_active(name in character.merits)
        
        for name, check in self.flaw_checks.items():
            check.set_active(name in character.flaws)
        
        # Focus
        self.paradigm_entry.set_text(character.paradigm)
        self.practice_entry.set_text(character.practice)
        self.instruments_entry.set_text(", ".join(character.instruments))
        self.avatar_text.get_buffer().set_text(character.avatar_description)
        
        # Notes
        self.notes_text.get_buffer().set_text(character.notes)
        
        self._updating = False
    
    def _set_combo_text(self, combo, text):
        """Set combo box to show specific text."""
        model = combo.get_model()
        if model is None:
            return
        for i, row in enumerate(model):
            if row[0] == text:
                combo.set_active(i)
                return
        combo.set_active(0)


class ProgressTracker(Gtk.Box):
    """Right sidebar showing progress through character creation."""
    
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.app = app
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        
        # Mode header
        self.mode_label = Gtk.Label(label="Creation Mode")
        self.mode_label.add_css_class("title-3")
        self.append(self.mode_label)
        
        # Mode switch button
        self.mode_button = Gtk.Button(label="Advance to Freebie Mode")
        self.mode_button.connect("clicked", self._on_mode_advance)
        self.append(self.mode_button)
        
        self.append(Gtk.Separator())
        
        # Progress content (will be updated based on mode)
        self.progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.append(self.progress_box)
        
        # XP tracker (shown in XP mode)
        self.xp_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.xp_label = Gtk.Label()
        self.xp_label.set_xalign(0)
        self.xp_box.append(self.xp_label)
        
        # XP entry
        xp_entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        xp_entry_label = Gtk.Label(label="Add XP:")
        self.xp_entry = Gtk.SpinButton.new_with_range(0, 1000, 1)
        xp_add_btn = Gtk.Button(label="Add")
        xp_add_btn.connect("clicked", self._on_add_xp)
        xp_entry_box.append(xp_entry_label)
        xp_entry_box.append(self.xp_entry)
        xp_entry_box.append(xp_add_btn)
        self.xp_box.append(xp_entry_box)
        
        # Storyteller Override toggle
        self.xp_box.append(Gtk.Separator())
        
        override_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        override_header = Gtk.Label(label="Storyteller Override")
        override_header.add_css_class("heading")
        override_header.set_xalign(0)
        override_box.append(override_header)
        
        override_desc = Gtk.Label(label="Enable to change stats directly\nwithout spending XP (for ST-\ndictated changes, curses, etc.)")
        override_desc.set_xalign(0)
        override_desc.add_css_class("dim-label")
        override_box.append(override_desc)
        
        self.override_switch = Gtk.Switch()
        self.override_switch.set_halign(Gtk.Align.START)
        self.override_switch.connect("state-set", self._on_override_toggled)
        
        switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        switch_label = Gtk.Label(label="Force Edit Mode:")
        switch_box.append(switch_label)
        switch_box.append(self.override_switch)
        override_box.append(switch_box)
        
        self.xp_box.append(override_box)
        
        self.xp_box.set_visible(False)
        self.append(self.xp_box)
        
        # Track override state
        self.storyteller_override = False
    
    def _on_mode_advance(self, button):
        if not self.app.current_character:
            return
        
        char = self.app.current_character
        
        # Check if mode can be advanced
        can_advance, warnings = char.can_advance_mode()
        
        if not can_advance:
            # Show warning dialog
            dialog = Adw.MessageDialog(
                transient_for=self.app.win,
                heading="Cannot Advance Mode",
                body="Please resolve all issues before advancing:\n\n" + "\n".join(f"• {w}" for w in warnings)
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            return
        
        # Snapshot baseline before advancing
        char.snapshot_baseline()
        
        if char.creation_mode == "creation":
            char.creation_mode = "freebie"
            self.mode_button.set_label("Advance to XP Mode")
        elif char.creation_mode == "freebie":
            char.creation_mode = "xp"
            self.mode_button.set_label("(In XP Mode)")
            self.mode_button.set_sensitive(False)
        
        self.update()
    
    def _on_add_xp(self, button):
        if not self.app.current_character:
            return
        
        amount = int(self.xp_entry.get_value())
        if amount > 0:
            self.app.current_character.experience_total += amount
            self.xp_entry.set_value(0)
            self.update()
    
    def _on_override_toggled(self, switch, state):
        self.storyteller_override = state
        # Update visual indicator
        if state:
            self.mode_label.set_label("XP Mode (OVERRIDE)")
            self.mode_label.add_css_class("warning")
        else:
            self.mode_label.set_label("Experience Mode")
            self.mode_label.remove_css_class("warning")
        return False  # Allow the switch to change state
    
    def is_override_active(self) -> bool:
        """Check if storyteller override is active."""
        if not self.app.current_character:
            return False
        return (self.app.current_character.creation_mode == "xp" and 
                self.storyteller_override)
    
    def update(self):
        """Update the tracker display."""
        # Clear progress box
        while child := self.progress_box.get_first_child():
            self.progress_box.remove(child)
        
        if not self.app.current_character:
            return
        
        char = self.app.current_character
        
        # Update mode label (with override indicator for XP mode)
        mode_names = {"creation": "Creation Mode", "freebie": "Freebie Point Mode", "xp": "Experience Mode"}
        
        # Remove any existing warning class
        self.mode_label.remove_css_class("warning")
        
        if char.creation_mode == "xp" and self.storyteller_override:
            self.mode_label.set_label("XP Mode (OVERRIDE)")
            self.mode_label.add_css_class("warning")
        else:
            self.mode_label.set_label(mode_names.get(char.creation_mode, "Unknown"))
        
        if char.creation_mode == "creation":
            self._show_creation_progress(char)
            self.mode_button.set_label("Advance to Freebie Mode")
            self.mode_button.set_sensitive(True)
            self.xp_box.set_visible(False)
            # Reset override when not in XP mode
            self.storyteller_override = False
            self.override_switch.set_active(False)
            
        elif char.creation_mode == "freebie":
            self._show_freebie_progress(char)
            self.mode_button.set_label("Advance to XP Mode")
            self.mode_button.set_sensitive(True)
            self.xp_box.set_visible(False)
            # Reset override when not in XP mode
            self.storyteller_override = False
            self.override_switch.set_active(False)
            
        elif char.creation_mode == "xp":
            self._show_xp_progress(char)
            self.mode_button.set_label("(In XP Mode)")
            self.mode_button.set_sensitive(False)
            self.xp_box.set_visible(True)
    
    def _show_creation_progress(self, char: Character):
        """Show creation mode progress."""
        remaining = char.get_creation_dots_remaining()
        
        # Attributes
        header = Gtk.Label(label="Attributes")
        header.add_css_class("heading")
        header.set_xalign(0)
        self.progress_box.append(header)
        
        for category in ["Physical", "Social", "Mental"]:
            priority = char.attribute_priorities.get(category)
            priority_str = f" ({priority})" if priority else ""
            dots = remaining["attributes"][category]
            color = "success" if dots == 0 else ("warning" if dots > 0 else "error")
            
            label = Gtk.Label(label=f"  {category}{priority_str}: {dots}")
            label.set_xalign(0)
            label.add_css_class(color)
            self.progress_box.append(label)
        
        self.progress_box.append(Gtk.Separator())
        
        # Abilities
        header = Gtk.Label(label="Abilities")
        header.add_css_class("heading")
        header.set_xalign(0)
        self.progress_box.append(header)
        
        for category in ["Talents", "Skills", "Knowledges"]:
            priority = char.ability_priorities.get(category)
            priority_str = f" ({priority})" if priority else ""
            dots = remaining["abilities"][category]
            color = "success" if dots == 0 else ("warning" if dots > 0 else "error")
            
            label = Gtk.Label(label=f"  {category}{priority_str}: {dots}")
            label.set_xalign(0)
            label.add_css_class(color)
            self.progress_box.append(label)
        
        self.progress_box.append(Gtk.Separator())
        
        # Backgrounds
        bg_dots = remaining["backgrounds"]
        bg_color = "success" if bg_dots == 0 else ("warning" if bg_dots > 0 else "error")
        bg_label = Gtk.Label(label=f"Backgrounds: {bg_dots}")
        bg_label.set_xalign(0)
        bg_label.add_css_class(bg_color)
        self.progress_box.append(bg_label)
        
        # Spheres
        sphere_dots = remaining["spheres"]
        sphere_color = "success" if sphere_dots == 0 else ("warning" if sphere_dots > 0 else "error")
        sphere_label = Gtk.Label(label=f"Spheres: {sphere_dots}")
        sphere_label.set_xalign(0)
        sphere_label.add_css_class(sphere_color)
        self.progress_box.append(sphere_label)
        
        # Affinity sphere check
        if not char.affinity_sphere:
            affinity_label = Gtk.Label(label="⚠ No Affinity Sphere")
            affinity_label.set_xalign(0)
            affinity_label.add_css_class("warning")
            self.progress_box.append(affinity_label)
        
        # Show warnings if mode can't be advanced
        can_advance, warnings = char.can_advance_mode()
        if not can_advance and warnings:
            self.progress_box.append(Gtk.Separator())
            warning_header = Gtk.Label(label="⚠ Cannot Advance Mode")
            warning_header.add_css_class("heading")
            warning_header.add_css_class("error")
            warning_header.set_xalign(0)
            self.progress_box.append(warning_header)
            
            for warning in warnings:
                warn_label = Gtk.Label(label=f"  • {warning}")
                warn_label.set_xalign(0)
                warn_label.add_css_class("error")
                self.progress_box.append(warn_label)
    
    def _show_freebie_progress(self, char: Character):
        """Show freebie point mode progress."""
        available = char.freebie_points_available
        total = char.freebie_points_total
        
        # Color based on remaining points
        avail_color = "success" if available >= 0 else "error"
        header = Gtk.Label(label=f"Freebie Points: {available}/{total}")
        header.add_css_class("heading")
        header.add_css_class(avail_color)
        header.set_xalign(0)
        self.progress_box.append(header)
        
        # Breakdown
        base_label = Gtk.Label(label=f"  Base: {CREATION_RULES['freebie_points']}")
        base_label.set_xalign(0)
        self.progress_box.append(base_label)
        
        flaw_bonus = min(sum(char.flaws.values()), CREATION_RULES["max_flaw_points"])
        flaw_label = Gtk.Label(label=f"  Flaws (bonus): +{flaw_bonus}")
        flaw_label.set_xalign(0)
        flaw_label.add_css_class("success")
        self.progress_box.append(flaw_label)
        
        merit_cost = char.merit_costs
        merit_label = Gtk.Label(label=f"  Merits (cost): -{merit_cost}")
        merit_label.set_xalign(0)
        if merit_cost > 0:
            merit_label.add_css_class("warning")
        self.progress_box.append(merit_label)
        
        spent_label = Gtk.Label(label=f"  Other spent: -{char.freebie_points_spent}")
        spent_label.set_xalign(0)
        self.progress_box.append(spent_label)
        
        self.progress_box.append(Gtk.Separator())
        
        # Cost reference
        ref_header = Gtk.Label(label="Freebie Costs:")
        ref_header.add_css_class("heading")
        ref_header.set_xalign(0)
        self.progress_box.append(ref_header)
        
        costs = [
            ("Attribute", FREEBIE_COSTS["attribute"]),
            ("Ability", FREEBIE_COSTS["ability"]),
            ("Background", FREEBIE_COSTS["background"]),
            ("Sphere", FREEBIE_COSTS["sphere"]),
            ("Arete", FREEBIE_COSTS["arete"]),
            ("Willpower", FREEBIE_COSTS["willpower"]),
        ]
        
        for name, cost in costs:
            label = Gtk.Label(label=f"  {name}: {cost}/dot")
            label.set_xalign(0)
            self.progress_box.append(label)
        
        # Show warnings if mode can't be advanced
        can_advance, warnings = char.can_advance_mode()
        if not can_advance and warnings:
            self.progress_box.append(Gtk.Separator())
            warning_header = Gtk.Label(label="⚠ Cannot Advance Mode")
            warning_header.add_css_class("heading")
            warning_header.add_css_class("error")
            warning_header.set_xalign(0)
            self.progress_box.append(warning_header)
            
            for warning in warnings:
                warn_label = Gtk.Label(label=f"  • {warning}")
                warn_label.set_xalign(0)
                warn_label.add_css_class("error")
                self.progress_box.append(warn_label)
    
    def _show_xp_progress(self, char: Character):
        """Show XP mode progress."""
        self.xp_label.set_label(
            f"Total XP: {char.experience_total}\n"
            f"Spent: {char.experience_spent}\n"
            f"Available: {char.experience_available}"
        )
        
        # Override mode indicator
        if self.storyteller_override:
            override_label = Gtk.Label(label="⚠ OVERRIDE MODE ACTIVE")
            override_label.add_css_class("warning")
            override_label.set_xalign(0)
            self.progress_box.append(override_label)
            
            override_info = Gtk.Label(label="Changes do not cost XP")
            override_info.set_xalign(0)
            self.progress_box.append(override_info)
            
            self.progress_box.append(Gtk.Separator())
        
        # XP cost reference
        header = Gtk.Label(label="XP Costs:")
        header.add_css_class("heading")
        header.set_xalign(0)
        self.progress_box.append(header)
        
        costs = [
            ("New Ability", str(EXPERIENCE_COSTS["new_ability"])),
            ("New Sphere", str(EXPERIENCE_COSTS["new_sphere"])),
            ("Affinity Sphere", f"current × {EXPERIENCE_COSTS['affinity_sphere']}"),
            ("Other Sphere", f"current × {EXPERIENCE_COSTS['other_sphere']}"),
            ("Arete", f"current × {EXPERIENCE_COSTS['arete']}"),
            ("Attribute", f"current × {EXPERIENCE_COSTS['attribute']}"),
            ("Ability", f"current × {EXPERIENCE_COSTS['ability']}"),
            ("Background", f"current × {EXPERIENCE_COSTS['background']}"),
            ("Willpower", f"current × {EXPERIENCE_COSTS['willpower']}"),
        ]
        
        for name, cost in costs:
            label = Gtk.Label(label=f"  {name}: {cost}")
            label.set_xalign(0)
            self.progress_box.append(label)


class CharacterList(Gtk.Box):
    """Left sidebar showing saved characters."""
    
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.app = app
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        
        # Header
        header = Gtk.Label(label="Characters")
        header.add_css_class("title-3")
        self.append(header)
        
        # New character button
        new_btn = Gtk.Button(label="New Character")
        new_btn.connect("clicked", self._on_new_character)
        self.append(new_btn)
        
        self.append(Gtk.Separator())
        
        # Character list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-selected", self._on_character_selected)
        scrolled.set_child(self.listbox)
        
        self.append(scrolled)
        
        # Refresh button
        refresh_btn = Gtk.Button(label="Refresh")
        refresh_btn.connect("clicked", lambda b: self.refresh_list())
        self.append(refresh_btn)
    
    def _on_new_character(self, button):
        self.app.new_character()
    
    def _on_character_selected(self, listbox, row):
        if row is None:
            return
        
        filepath = row.filepath
        self.app.load_character(filepath)
    
    def refresh_list(self):
        """Refresh the character list from the save directory."""
        # Clear existing
        while child := self.listbox.get_first_child():
            self.listbox.remove(child)
        
        save_dir = self.app.save_directory
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            return
        
        for filename in sorted(os.listdir(save_dir)):
            if filename.endswith(".md"):
                filepath = os.path.join(save_dir, filename)
                
                # Try to get character name
                try:
                    char = Character.load_from_markdown(filepath)
                    name = char.name
                except:
                    name = filename[:-3]
                
                row = Gtk.ListBoxRow()
                row.filepath = filepath
                
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                box.set_margin_start(4)
                box.set_margin_end(4)
                box.set_margin_top(4)
                box.set_margin_bottom(4)
                
                label = Gtk.Label(label=name)
                label.set_xalign(0)
                label.set_hexpand(True)
                box.append(label)
                
                row.set_child(box)
                self.listbox.append(row)


class MageMakerApp(Adw.Application):
    """Main application class."""
    
    def __init__(self):
        super().__init__(application_id="org.magemaker.MageMaker",
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        self.current_character = None
        self.current_filepath = None
        
        # Save directory - relative to current working directory
        cwd = os.getcwd()
        self.save_directory = os.path.join(cwd, "characters")
        os.makedirs(self.save_directory, exist_ok=True)
        
        self.connect("activate", self.on_activate)
    
    def on_activate(self, app):
        # Create main window
        self.win = Adw.ApplicationWindow(application=app)
        self.win.set_title("MageMaker - Mage: The Ascension 20th Anniversary Edition")
        self.win.set_default_size(1400, 900)
        
        # Apply CSS
        self._apply_css()
        
        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Header bar
        header = Adw.HeaderBar()
        
        # Save button
        save_btn = Gtk.Button(label="Save")
        save_btn.connect("clicked", self._on_save)
        header.pack_start(save_btn)
        
        # Export button
        export_btn = Gtk.Button(label="Export TXT")
        export_btn.connect("clicked", self._on_export)
        header.pack_end(export_btn)
        
        main_box.append(header)
        
        # Three-panel layout
        paned_outer = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned_outer.set_vexpand(True)
        
        # Left sidebar - Character list
        self.char_list = CharacterList(self)
        self.char_list.set_size_request(200, -1)
        
        left_frame = Gtk.Frame()
        left_frame.set_child(self.char_list)
        paned_outer.set_start_child(left_frame)
        paned_outer.set_shrink_start_child(False)
        
        # Inner paned for center and right
        paned_inner = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        
        # Center - Character editor
        self.editor = CharacterEditor(self)
        
        center_frame = Gtk.Frame()
        center_frame.set_child(self.editor)
        center_frame.set_hexpand(True)
        paned_inner.set_start_child(center_frame)
        paned_inner.set_shrink_start_child(False)
        
        # Right sidebar - Progress tracker
        self.tracker = ProgressTracker(self)
        self.tracker.set_size_request(250, -1)
        
        right_frame = Gtk.Frame()
        right_frame.set_child(self.tracker)
        paned_inner.set_end_child(right_frame)
        paned_inner.set_shrink_end_child(False)
        
        paned_outer.set_end_child(paned_inner)
        paned_outer.set_shrink_end_child(False)
        
        main_box.append(paned_outer)
        
        self.win.set_content(main_box)
        
        # Refresh character list
        self.char_list.refresh_list()
        
        # Create new character by default
        self.new_character()
        
        self.win.present()
    
    def _apply_css(self):
        """Apply custom CSS styling."""
        css = b"""
        .title-2 {
            font-size: 16pt;
            font-weight: bold;
        }
        .title-3 {
            font-size: 14pt;
            font-weight: bold;
        }
        .heading {
            font-weight: bold;
            margin-top: 8px;
        }
        .dot-button {
            min-width: 20px;
            min-height: 20px;
            padding: 0;
        }
        .dot-filled {
            color: @accent_color;
        }
        .dot-empty {
            color: alpha(@window_fg_color, 0.3);
        }
        .success {
            color: #2ec27e;
        }
        .warning {
            color: #e5a50a;
        }
        .error {
            color: #c01c28;
        }
        """
        
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            self.win.get_display(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def new_character(self):
        """Create a new character."""
        self.current_character = Character()
        self.current_filepath = None
        self.editor.load_character(self.current_character)
        self.update_tracker()
    
    def load_character(self, filepath: str):
        """Load a character from file."""
        try:
            self.current_character = Character.load_from_markdown(filepath)
            self.current_filepath = filepath
            self.editor.load_character(self.current_character)
            self.update_tracker()
        except Exception as e:
            dialog = Adw.MessageDialog(
                transient_for=self.win,
                heading="Error Loading Character",
                body=str(e)
            )
            dialog.add_response("ok", "OK")
            dialog.present()
    
    def _on_save(self, button):
        """Save current character."""
        if not self.current_character:
            return
        
        if not self.current_filepath:
            # Generate filename from character name
            safe_name = "".join(c for c in self.current_character.name if c.isalnum() or c in " -_").strip()
            if not safe_name:
                safe_name = "New Character"
            self.current_filepath = os.path.join(self.save_directory, f"{safe_name}.md")
        
        try:
            self.current_character.save_to_markdown(self.current_filepath)
            self.char_list.refresh_list()
            
            # Show toast
            toast = Adw.Toast(title="Character saved!")
            # Note: We'd need an AdwToastOverlay for this, simplified for now
        except Exception as e:
            dialog = Adw.MessageDialog(
                transient_for=self.win,
                heading="Error Saving Character",
                body=str(e)
            )
            dialog.add_response("ok", "OK")
            dialog.present()
    
    def _on_export(self, button):
        """Export character to TXT."""
        if not self.current_character:
            return
        
        dialog = Gtk.FileDialog()
        dialog.set_initial_name(f"{self.current_character.name}.txt")
        
        def on_save_response(dialog, result):
            try:
                file = dialog.save_finish(result)
                if file:
                    filepath = file.get_path()
                    self.current_character.export_to_text(filepath)
            except GLib.Error:
                pass  # User cancelled
        
        dialog.save(self.win, None, on_save_response)
    
    def update_tracker(self):
        """Update the progress tracker."""
        self.tracker.update()


def main():
    """Entry point for the application."""
    app = MageMakerApp()
    app.run(None)


if __name__ == "__main__":
    main()

