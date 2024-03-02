# Dreaditor

Dreaditor is a rewritten version of [dread-editor](https://github.com/randovania/dread-editor). It uses PyQt instead of imgui to allow image rendering. Only works on Windows for now. 

## Features

[ ] Implement a map-viewing widget that shows collision cameras and actors over images of the map
[ ] Map uses standard zoom-and-pan controls rather than min/max X/Y coords
[ ] Actor data shows actordef fields as well as actor data
[ ] Separate toolbox tabs to show data in other files (EMMI transitions and enemy paths in navmesh, static scenario models, etc)
[ ] Ability to edit and save data to a "project" (a new folder which saves modified files, similar to a LayeredFS mod)

## Installation

```
py -m venv venv
venv\Scripts\activate
pip install -e .
py -m dreaditor
```
