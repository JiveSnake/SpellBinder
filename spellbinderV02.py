#-------------------------------------------------------------------------------
# Name:        SpellBinder
# Purpose:     A search and display program for tabletop RPG spells
#
# Author:      Sean Landis
#
# Created:     11/01/2015
# Copyright:   (c) Sean 2015
# Licence:     None
#-------------------------------------------------------------------------------
#!/usr/bin/env python

try:
    #Python 3
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk
except:
    #Python 2.7
    import Tkinter as tk
    import ttk
    import tkMessageBox

from lxml import etree as ET
import tkHyperlinkManager

large_font = ("Verdana", 12)
small_font = ("Verdana", 8)

spell_book = ET.parse("spelldatabase.xml")
class_spell_lists = ET.parse("class_spell_lists.xml")


class SpellBinder(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default=".ico")
        self.wm_title("SpellBinder v0.2")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (MainPage, FuturePages):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class SpellData:
    def __init__ (self, data_list):
        (self.spellid, self.edition, self.name, self.level, self.school, self.ritual,
        self.casting_time, self.range, self.components, self.cost, self.duration, self.expandable) = data_list

class DisplaySpell:
    def __init__(self, display_list):
        (self.display_name, self.display_spelltype, self.display_casting_time,
        self.display_range, self.display_components, self.display_duration, self.display_description) = display_list

    def display_all(self):
        return "{name}\n{spelltype}\nCasting Time: {casting_time}\nRange: {range}\nComponents: {components}\nDuration: {duration}\n{description}".format(name=self.display_name,
            spelltype=self.display_spelltype, casting_time=self.display_casting_time,
            range=self.display_range, components=self.display_components, duration=self.display_duration, description=self.display_description)

def spell_data_generator(spell_node):
    spell_data_list = [spell_node.findtext("name")]
    for elem in spell_node.iter():
        spell_data_list.append(elem.text)
    spell_data = SpellData(spell_data_list)
    return spell_data

def display_spell_generator(spell_node):
    display_list = [spell_node.findtext("name")]
    for elem in spell_node.iter("display"):
        display_list.append(elem.text)
    display_spell = DisplaySpell(display_list)
    return display_spell

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.search_string = tk.StringVar()

        self.title_label = ttk.Label(self, text="SpellBinder", font=large_font)
        self.title_label.pack(pady=10,padx=10)

        self.entry_box = ttk.Entry(self, textvariable=self.search_string)
        self.entry_box.bind('<Return>', lambda e: self.update_display_window(self.search_string))
        self.entry_box.pack()

        self.search_button = ttk.Button(self, text="Search", command=lambda: self.update_display_window(self.search_string))
        self.search_button.bind('<Return>', lambda e: self.update_display_window(self.search_string))
        self.search_button.pack()

        self.spell_display_window = tk.Text(state="disable", font=small_font, wrap="word")
        self.spell_display_window.pack()

        self.hyperlink = tkHyperlinkManager.HyperlinkManager(self.spell_display_window)

    def update_display_window(self,search_string):
        self.search_name = search_string.get()
        if self.search_name.strip() == "":
            self.clear_and_display("Please Enter a Spell's Name")
        else:
            self.spell_nodes = self.find_by_name(self.search_name)
            if self.spell_nodes == []:
                self.clear_and_display("No Spell Found")
            elif len(self.spell_nodes) == 1:
                self.display_single_spell(self.spell_nodes[0])
            else:
                self.display_spell_links(self.spell_nodes)

    def display_single_spell(self, spell_node):
        self.display_spell = display_spell_generator(spell_node).display_all()
        self.clear_and_display(self.display_spell)

    def display_spell_links(self, spell_nodes):
        self.spell_display_window["state"] = "normal"
        self.spell_display_window.delete(1.0, "end")
        for spell_node in spell_nodes:
            self.insert_link(spell_node)
        self.spell_display_window["state"] = "disable"

    def insert_link(self, spell_node):
        self.spell_display_window.insert("insert", spell_node.findtext("name"), self.hyperlink.add(lambda: self.display_single_spell(spell_node)))
        self.spell_display_window.insert("insert", "\n")

    def find_by_name(self, search_name):
        search_name_lower = search_name.replace(" ", "").lower()
        spell_nodes = []
        for elem in spell_book.iter("name"):
            if search_name_lower in elem.text.replace(" ", "").lower():
                spell_nodes.append(elem.getparent())
        return spell_nodes

    def clear_and_display(self, display_text):
        self.spell_display_window["state"] = "normal"
        self.spell_display_window.delete(1.0, "end")
        self.spell_display_window.insert(1.0, display_text)
        self.spell_display_window["state"] = "disable"

#This Class is a template to make additional frames if needed
class FuturePages(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="HAYOO!", font=large_font)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Visit Page 1", command=lambda: controller)
        button1.pack()


def main():
    app = SpellBinder()
    app.mainloop()

if __name__ == '__main__':
    main()
