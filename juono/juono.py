import random
import re
from bs4 import BeautifulSoup

# CHANGE THIS TO False IF YOU WANT ENGLISH
USE_FINNISH = True

# These actions are not to be used
excluded_actions = [
    "15b",
    "71a", # Don't wanna parse this for now
    "110", # Don't wanna parse this for now
    "136", # Don't wanna parse this for now
    "188", # Special case
    "210", # Don't wanna parse this for now
    "255", # Racist
    "259", # Don't wanna parse this for now
    "282b", # Racist
    "303", # Don't wanna parse this for now
    "305", # Racist
    "312", # Don't wanna parse this for now
    "323", # Racist
    "326", # Don't wanna parse this for now
    "331", # Racist
    "332", # Racist
    "336c", # Racist
    "364a", # Racist
    "364c", # Racist
    "423b", # Don't wanna parse this for now
    "425", # Racist
    "457", # Don't wanna parse this for now
    "527", # Racist
    "570", # Parsing fail
    "650", # Racist
    "651", # Don't wanna parse this for now
    "682", # Arguably passes
    "687", # Racist
    "718", # Racist
    "751", # Don't wanna parse this for now
    "842b", # Don't wanna parse this for now
    "851", # Don't wanna parse this for now
    "864", # Don't wanna parse this for now
    "901", # Racist
    "902", # Don't wanna parse this for now
    "959", # Racist
    "966", # Don't wanna parse this for now
    "973", # Racist
    "1015", # Confusing and possibly racist
    "1093", # Don't wanna parse this for now
    "1099", # Don't wanna parse this for now
    "1237b", # Don't wanna parse this for now
    "1289b", # Racist
    "1323c", # Don't wanna parse this for now
    "1342a", # Don't wanna parse this for now
    "1343", # Don't wanna parse this for now
    "1356", # Don't wanna parse this for now
    "1372", # Don't wanna parse this for now
    "1438b", # Don't wanna parse this for now
    "1440", # Don't wanna parse this for now
    "1458" # Racist
]

# These are the actions that can be selected as midpoints
# Change these freely, current values are just for testing purposes
# Some actions WILL BREAK this script though
midpoints = [
    "170",
    "261",
    "317"
]

# Some names for the actors, the list could be more extensive, see Plotto documentation
potterverse_mf = [
    ("A", "Harry"),
    ("A-2", "Ron"),
    ("A-3", "Draco"),
    ("B", "Ginny"),
    ("B-2", "Hermione"),
    ("B-3", "Dolores"),
    ("X", "The Philosopher's Stone")
]

# Gender-swapped version
potterverse_fm = [
    ("A", "Hermione"),
    ("A-2", "Harry"),
    ("A-3", "Lavender"),
    ("B", "Ron"),
    ("B-2", "Ginny"),
    ("B-3", "Draco"),
    ("X", "The Philosopher's Stone")
]

# These are the prototyped finnish midpoint actions, they exist in both plotto-mf and plotto-fm
finnish_midpoints = [
    "1465"
]

soup_data = random.choice([('data/plotto-mf.html', potterverse_mf), ('data/plotto-fm.html', potterverse_fm),])
soup = BeautifulSoup(open(soup_data[0], 'r').read(), 'html.parser')

class PlotAction:
    def __init__(self, id, mods):
        self.id = id
        self.mods = mods
        self.desc = self.parse_desc()
        self.apply_mods()
        #self.backstory = []
    
    def __str__(self):
        mods_string = ""

        for m in self.mods:
            mods_string = mods_string + " " + str(m) 

        return "\n" + "Event id " + self.id + ", applied modifiers:" + mods_string + "\n" + finalize_desc_output(self.desc, soup_data[1])
    
    def parse_desc(self):
        full_desc = recognize_subid(self.id, "desc")

        while full_desc.span:
            full_desc.span.decompose()

        return full_desc.text
    
    def apply_mods(self):
        for m in self.mods:
            self.desc = m.apply(self.desc)

class ActionMod:
    def __init__(self, func, param_a, param_b):
        self.func = func
        self.param_a = param_a
        self.param_b = param_b
    
    def __str__(self):
        return self.func + "(" + self.param_a + ", " + self.param_b + ")"

    def apply(self, text):
        if self.func == "ch":
            return replace_actor(text, self.param_a, self.param_b)
        elif self.func == "tr":
            temp_text = replace_actor(text, self.param_a, "_")
            temp_text = replace_actor(temp_text, self.param_b, self.param_a)
            return replace_actor(temp_text, "_", self.param_b)
        elif self.func == "cut":
            if self.param_a == "":
                return re.match("(.*?)"+re.escape(self.param_b), text).group()[:-1].strip()
            else:
                return re.match("(.*?)"+re.escape(self.param_a)+"(.*?)"+re.escape(self.param_b)+"(.*)", text).group(2).strip()
        else:
            return "Unrecognized modifier function: " + self.func

class Story:
    def __init__(self, universe):
        self.universe = universe
        
        if USE_FINNISH:
            self.chosen_midpoint_action = PlotAction(random.choice(finnish_midpoints), [])
        else:
            self.chosen_midpoint_action = PlotAction(random.choice(midpoints), [])

        self.actions = [self.chosen_midpoint_action]
        self.action_prelinks = [self.parse_links(self.chosen_midpoint_action, "prelinks")]
        self.action_postlinks = [self.parse_links(self.chosen_midpoint_action, "postlinks")]
        self.lead_ins_generated = 0
        self.carry_ons_generated = 0
        #self.backstory = []
    
    def parse_links(self, action, link_type):
        links = []

        for s in recognize_subid(action.id, link_type).findAll("span", {"class": "clinkgroup"}):
            link_string = s.text

            if "," in link_string:
                parts = link_string.split(",")
                link_id = parts[0][:-1]

                links.append(parts[0])
                i = 1
                while i < len(parts):
                    links.append(link_id + parts[i].strip())
                    i += 1
            else:
                links.append(str(s.text))

        return links
    
    def parse_mods(self, mods):
        mod_strings = mods
        parsed_mods = []

        i = 0
        while i < len(mod_strings):
            curr = mod_strings[i]

            if re.match("\**-\*+", curr):
                curr = curr.split("-")
                parsed_mods.append(ActionMod("cut", curr[0], curr[1]))
                i += 1
                continue
            if curr == "ch":
                parsed_mods.append(ActionMod("ch", mod_strings[i+1], mod_strings[i+3]))
                i += 4
                continue
            if curr == "tr":
                parsed_mods.append(ActionMod("tr", mod_strings[i+1], mod_strings[i+3]))
                i += 4
                continue
            
            return "Error"
        
        return parsed_mods
    
    def generate_lead_in(self, accept_multi_part):
        earliest_prelinks = self.action_prelinks[0]
        possible_lead_ins = []

        for a in earliest_prelinks:
            if ";" not in a:
                a_id = a.split(" ")[0]
                a_mods = a.split(" ")[1:]

                if (a_id not in excluded_actions) and (not a_mods or self.parse_mods(a_mods) != "Error"):
                    possible_lead_ins.append(a)

            elif accept_multi_part and ";" in a:
                a_actions = a.split(";")

                for ax in a_actions:
                    ax_id = ax.split(" ")[0]
                    ax_mods = ax.split(" ")[1:]

                    if (ax_id not in excluded_actions) and (not ax_mods or self.parse_mods(ax_mods) != "Error"):
                        continue

                    possible_lead_ins.append(a)
        
        if possible_lead_ins:
            generated = random.choice(possible_lead_ins)

            if ";" in generated:
                gen_seq = generated.strip().split(";")

                for g in gen_seq:
                    self.addAction(g, True)

            else:
                self.addAction(generated, True)
        
        else:
            print("Empty lead-ins hit for action " + self.actions[0].id)
        
    def generate_carry_on(self, accept_multi_part):
        last_postlinks = self.action_postlinks[-1]
        possible_carry_ons = []

        for a in last_postlinks:
            if ";" not in a:
                a_id = a.split(" ")[0]
                a_mods = a.split(" ")[1:]

                if (a_id not in excluded_actions) and (not a_mods or self.parse_mods(a_mods) != "Error"):
                    possible_carry_ons.append(a)

            elif accept_multi_part and ";" in a:
                a_actions = a.split(";")

                for ax in a_actions:
                    ax_id = ax.split(" ")[0]
                    ax_mods = ax.split(" ")[1:]

                    if (ax_id not in excluded_actions) and (not ax_mods or self.parse_mods(ax_mods) != "Error"):
                        continue

                    possible_carry_ons.append(a)
        
        if possible_carry_ons:
            generated = random.choice(possible_carry_ons)
            
            if ";" in generated:
                gen_seq = generated.strip().split(";")

                for g in gen_seq:
                    self.addAction(g, False)

            else:
                self.addAction(generated, False)
        
        else:
            print("Empty carry-ons hit for action " + self.actions[-1].id)
    
    def addAction(self, action, before):
        action_strings = action.strip().split(" ")
        mod_strings = ""

        if len(action_strings) > 1:
            mod_strings = action_strings[1:]
        
        new = PlotAction(action_strings[0], self.parse_mods(mod_strings))

        if before:
            self.actions.insert(0, new)
            self.action_prelinks.insert(0, self.parse_links(new, "prelinks"))
            self.action_postlinks.insert(0, self.parse_links(new, "postlinks"))
            self.lead_ins_generated += 1
        else:
            self.actions.append(new)
            self.action_prelinks.append(self.parse_links(new, "prelinks"))
            self.action_postlinks.append(self.parse_links(new, "postlinks"))
            self.carry_ons_generated += 1

        excluded_actions.append(action_strings[0])
    
    def output(self):
        print()
        print("Story length: ", len(self.actions))
        print("Lead-ins generated: ", self.lead_ins_generated)
        print("Carry-ons generated: ", self.carry_ons_generated)
        print("Chosen midpoint action: ", self.chosen_midpoint_action)
        print("\n--------\n")
        
        for a in self.actions:
            print(a)
        print()
    
    def simple_output(self):
        for a in self.actions:
            print(finalize_desc_output(a.desc, soup_data[1]) + "\n")

def finalize_desc_output(desc, verse):
    ret = re.sub("\*+", ".", desc)

    for p in verse:
        ret = replace_actor(ret, p[0], p[1])
    
    return ret

def recognize_subid(action_id, div_class):
    if action_id[-1].isnumeric():
        return soup.find(id=str(action_id)).find("div", {"class": div_class})
        
    else:
        subid = action_id[-1]
        ret = ""
        all_classes = soup.find(id=str(action_id[:-1])).findAll("div", {"class": div_class})

        if subid == 'a':
            return all_classes[0]
        elif subid == 'b':
            return all_classes[1]
        elif subid == 'c':
            return all_classes[2]
        elif subid == 'd':
            return all_classes[3]
        elif subid == 'e':
            return all_classes[4]
        elif subid == 'f':
            return all_classes[5]
        elif subid == 'g':
            return all_classes[6]
        else:
            return all_classes[7]

def replace_actor(text, a, b):
    words = text.split(" ")
    ret = []

    for w in words:
        if w == a or re.match(a+"[.,'’;:]+", w):
            ret.append(w.replace(a, b))
        else:
            ret.append(w)

    return " ".join(ret)

# ---- STORY GENERATION STEPS BELOW ----

s = Story([])
s.generate_lead_in(True)
s.generate_carry_on(True)
s.generate_lead_in(False)
s.generate_carry_on(False)

#s.output() # More verbose output, better for testing
s.simple_output() # Just the descriptions