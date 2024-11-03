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
- [x] Render the collision cameras
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

Next, you can select a scenario from the `Select Scenario` menu. For larger scenarios such as Artaria, Cataris and Dairon, this may take several seconds. It is finished when the `BRFLD` item on the right is checked and populated with layer data. If you added a 2.1.0 copy of the RomFS, you can also access the bossrush scenarios. 

There are three main sections of the screen: the Actor List dock on the left, the Area Map in the middle, and the Actor Data dock on the right. These can all be used to visualize and inspect actors. Each actor can track if it is checked (visible) and if it is selected. The effects of this will be explained in the following sections as we dive into the different panels. 

### Actor List

The Actor List dock is a tree of all actors in the scenario. The BRFLD is the root item, and contains items for each layer - entities, sounds and lights. Each of these has a number of sublayers, each of which contains one or more actors. Adjusting the checkboxes will change the visibility of actors in the Area Map. These checkboxes are tri-state so you can easily see which layers and sublayers are hidden, fully displayed, or partially displayed. 

Double-clicking on an actor will toggle its selection state, which is separate from checkboxes. Selected items are highlighted in red on the Area Map and displayed in the Actor Data dock. 

### Subarea List

The Subarea List dock is a tree of all subarea setups in the scenario, based on the BRSA. The root node contains an item for each subarea setup (i.e. Default, PostXRelease), and each of these contain a list of collision cameras included. When expanded, the collision camera will be rendered in the Scene View and it contains the subarea's Item IDs, which correspond to actor groups, scene blocks, and soundtracks (only Actor Groups is currently implemented). 

The actors in these check boxes are synchronized with the Actor List, so if you check or uncheck a subarea setup or collision camera, these changes will be reflected in both the Subarea List and the Actor List. 

### Area Map

The Area Map displays a visual representation of the scenario. The gray map is generated from data stored in the game's internal minimap file (BMMAP) and shows the static collision (floors, walls, ceilings, platforms). 

Each visible actor is rendered as a colored dots - green dots are entity actors, cyan dots are sound actors, and yellow dots are light actors. Double-clicking on an actor will toggle its selection, highlighting it red and displaying its data in the Actor Data dock. When multiple actors are layered on one another, double-clicking will select all actors below the cursor. If you want to unselect actor(s), right click to unselect regardless of the current selection state. 

Some actors have custom rendering for additional detail. For example, doors render as gray rectangles, breakable tiles are color-coded similar to in-game, and actors with LogicShape or LogicPath components have those rendered. 

### Actor Data

The Actor Data dock shows detailed information on actors. Each selected actor is a top-level item, and contains the level/instance data stored in the BRFLD, the actordef or BMSAD data, and collision or BMSCD data if it is attached to the actor. 

Actors can be unselected from this pane by double-clicking on their top-level item. 

### Painting options

The painting options menubar item can be used to customize how some actors are drawn in the Area Map. For most of these, checking the box will render all instances of the specified item that are visible (i.e. checked in the Actor List). Unchecking the box will only render items that are visible *and* selected in the Actor Data dock. 

#### Static Geometry

This will disable the gray "minimap" geometry in the background. Disabling this helps smooth out performance in some heavy scenarios such as Artaria, as Qt doesn't paint triangle buffers efficiently. 

#### Collision Cameras

This will paint all collision cameras in the scenario. When off, only collision cameras expanded in the Subareas List are rendered. 

#### Doors

This will paint all doors in the scenario that are checked. When off, doors are only painted when the actor is selected. 

#### Collision

This will paint collision for actors such as breakable blobs, grapple boxes, and weight-activated platforms. This can be from a `bmscd` file referenced in the `CCollisionComponent` of an actordef, or from `CreateCollider` functions attached to the `CCollisionComponent`. When off, collision is only painted when the actor is selected. 

#### Breakable Tiles

This will paint all tiles and tilegroups. When disabled, tiles are only painted when the actor is selected. 

#### Logic Shapes

This will paint all actors with a `CLogicShapeComponent` in the color of their actor type (entity/light/sound). These are typically used for triggers, enemy Areas of Interest, music, and other things. When disabled, logic shapes are only painted when the actor is selected. 

#### Logic Paths

This will paint all actors with a `CLogicPathComponent` in white. These are typically used for enemy patrol paths, magnetic ziplines and wide block movement paths. When disabled, logic paths are only painted when the actor is selected. 

#### World Graph

This will paint the `CWorldGraph` attached to the `LE_WorldGraph` of each scenario with an E.M.M.I. This contains a series of connected nodes which seems to be related to EMMI traversal patterns. When disabled, it is only painted if the `LE_WorldGraph` node is selected. 