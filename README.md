# misc
Just random stuff, scripts, and utils.

decorators.py
-------------
Some decorator functions. Some of those are pretty useful stuff, e.g. for
memoization, or trace output, or type-checking, or making any function a var-
args function, or for re-trying some function until it works.

automata/
---------
Different generic automata (elementary automata, cellular automata, etc.),
fractal generators, and other stuff. Fun to play around with, but really just 
that.

algorithms/
-----------
Some common algorithms; some really useful, like disjoint-sets, and others that 
can also be found in the standard library. Mostly from some e-learning courses.

stuff/
------
More random stuff. Nothing in this directory is any useful, but curious or
interesting to program and to experiment with.

Planner/
--------
A simple Python AI planner, again nothing serious, just for playing around with.
Can solve some simple problems, but I never got around to implement any more
elaborate planning algorithms.

Space3D/
----------
Generic pseudo "3D engine" in Java, with simple camera control for various
small particle simulations, 3D fractals, and similar. Scenes can be viewed
with a camera that can be rotated freely around the scene, looking inwards.

* Particle/Gravity/Universe-Simulator. Rather simple, can (more or less
realistically) simulate a number of particles being pulled towards each
other by "gravity". 
* Fractal Mountain generator. Starting with a regular Pyramid, recursively
split the sides into smaller and smaller triangles, until the results
looks very natural and mountain-like.
