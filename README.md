# manim_fractals

This project is the sceond part of a bigger project. The first part can be found here : https://github.com/Elektriman/fractal_curves
The first part is not necessary to test the script as I added some data manually to the project.

This script displays the construction of fractal curves by the process of adding new points for each vertices of a given line of n points and n-1 vertices.
The data is recovered from csv files and it is played using the manim library. (https://docs.manim.community/en/stable/)

DO NOT ATTEMPT to animate the dragon_curve or the sierpinski triangle up to the 19 (for the dragon curve) or the 12 (for the sierpinski triangle) iterations because they have +100 000 points and manim can't handle Line objects with so many points in a reasonable amount of time. From experience, stop at 12 for the dragon and 8 for the triangle, it should give you good enought results.

feel free to make a pull request if you feel like improving my code to make it able to handle more points. I'm planning already to use the VGroup mobject to improve the performances.
