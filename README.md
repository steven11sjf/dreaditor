# Dreaditor

Dreaditor is a rewritten version of [dread-editor](https://github.com/randovania/dread-editor). It uses PyQt instead of imgui to allow image rendering. Only works on Windows for now. 

## Features

- [x] Implement a map-viewing widget that shows an accurate minimap of the game
- [x] View actors on this map
- [x] View all actors (including sounds and lights)
- [x] Map uses standard zoom-and-pan controls rather than min/max X/Y coords
- [x] Actor data shows actordef fields as well as actor data
- [x] Render additional detail based on an actor's actordef
- [x] Render additional detail based on an actor's components
- [ ] Render the collision cameras
- [ ] Render details in other files such as navmesh, static geo
- [ ] Ability to edit and save data to a "project" (a new folder which saves modified files, similar to a LayeredFS mod)

## Installation

Pip:
```
py -m venv venv
venv\Scripts\activate
pip install dreaditor
py -m dreaditor
```

From source: 
```
py -m venv venv
venv\Scripts\activate
pip install -e .
py -m dreaditor
```

## Usage

![Main Dreaditor Window](docs/images/MainWindow.png)

First, open `File -> Select RomFS` in the menu bar and select an extracted copy of your Metroid Dread RomFS. This should be a directory containing folders such as `gui`, `packs`, `sounds`, `system` and `textures`, as well as a `config.ini` file. This path will be saved in a config file and only needs to be updated if the RomFS is moved to another directory. 

Next, you can select a scenario from the `Select Scenario` menu. For larger scenarios such as Artaria, Cataris and Dairon, this may take several seconds. It is finished when the `BRFLD` item on the right is checked and populated with layer data. 

There are three main sections of the screen: the Actor List dock on the left, the Area Map in the middle, and the Actor Data dock on the right. These can all be used to visualize and inspect actors. Each actor can track if it is visible and if it is selected. The effects of this will be explained in the following sections as we dive into the different panels. 

### Actor List

The Actor List dock is a tree of all actors in the scenario. The BRFLD is the root item, and contains items for each layer - entities, sounds and lights. Each of these has a number of sublayers, each of which contains one or more actors. Adjusting the checkboxes will change the visibility of actors in the Area Map. These checkboxes are tri-state so you can easily see which layers and sublayers are hidden, fully displayed, or partially displayed. 

Double-clicking on an actor will toggle its selection state, which is separate from checkboxes. Selected items are highlighted in red on the Area Map and displayed in the Actor Data dock. 

### Area Map

The Area Map displays a visual representation of the scenario. The gray map is generated from data stored in the game's internal minimap file (BMMAP) and shows the static collision (floors, walls, ceilings, platforms). 

Each visible actor is rendered as a colored dots - green dots are entity actors, purple dots are sound actors, and yellow dots are light actors. Double-clicking on an actor will toggle its selection, highlighting it red and displaying its data in the Actor Data dock. When multiple actors are layered on one another, double-clicking will select all actors below the cursor. If you want to unselect actor(s), right click to unselect regardless of the current selection state. 

Some actors have custom painters to render additional detail. For example, doors are rendered as gray rectangles, and objects with collision will render all collsion layers in red rectangles or polygons. 

### Actor Data

The Actor Data dock shows detailed information on actors. Each selected actor is a top-level item, and contains the level/instance data stored in the BRFLD, the actordef or BMSAD data, and collision or BMSCD data if the actor supports it. 

Actors can be unselected from this pane by double-clicking on their top-level item. 