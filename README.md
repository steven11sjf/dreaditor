# Dreaditor

Dreaditor is a rewritten version of [dread-editor](https://github.com/randovania/dread-editor). It uses PyQt instead of imgui to allow image rendering. Only works on Windows for now. 

## Features

- [x] Implement a map-viewing widget that shows an accurate minimap of the game
- [x] View actors on this map
- [x] View all actors (including sounds and lights)
- [x] Map uses standard zoom-and-pan controls rather than min/max X/Y coords
- [x] Actor data shows actordef fields as well as actor data
- [ ] Render additional detail based on an actor's actordef
- [ ] Render additional detail based on an actor's components
- [ ] Render the collision cameras
- [ ] Render details in other files such as navmesh, static geo
- [ ] Ability to edit and save data to a "project" (a new folder which saves modified files, similar to a LayeredFS mod)

## Installation

```
py -m venv venv
venv\Scripts\activate
pip install -e .
py -m dreaditor
```
