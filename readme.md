Use the python scripts in the root directory of this repository.

Example usage of python script:
```
C:\Users\<USERNAME>\Desktop\Python Scripts\splitter.py mill_\*.liggghts 3
```
The above example will split all occurrences of files with the pattern mill_\*.liggghts into three separate particle files.

1. Run a LIGGGHTS simulation and navigate to the post directory

2. Run splitter.py if different particles are desired in blender

3. Run rename_dump.py (only supports files generated from splitter.py currently)
    * If not splitting, change line three from ('1_', '2_', '3_') to ('mesh_')

4. Verify that a file named 'dump_test' has been created.
    * The particle files must be separated by one value and zero-padded
            * e.g. 1_0000.liggghts, 1_0001.liggghts

5. Navigate to 'dump_test' and run liggghts_to_vtk.py for each particle type
    * e.g. python "C:\Users\wchen\Desktop\Python Scripts\liggghts_to_vtk.py" 1_\*.liggghts
    * liggghts_to_vtk.py has not been tested since the last update, please report any bugs

6. Open Blender load the simulation files:
    1. (Mouse in 3D area) Shift+A > Mesh > DualSPHysics Object
        1. Navigate to the 'dump_test' folder and load from there
        2. Repeat for every particle type
        <img align="middle" src="https://github.com/mwmuni/LIGGGHTS-Post-Processing-Utilities/blob/master/images/Blender_1.png">
    2. Load the STL files
        * I recommend avoiding animated STL files for the time being

7. Change the render type to Cycles (Blender Render > Cycles Render)

8. Press Num 0, then press Shift+F. Move the camera using WASD + Mouse, right click to accept new position

9. Delete the global light and create a plane, placing it behind the camera

10. Create new shapes for particles (I use UV Sphere for particles, and Metaballs for water)
    1. Drag the newly created object to the desired VTK object, making the new object a child of the VTK object
    2. Select the VTK object and, in the object settings, change the duplication option to 'vertices'

11. Add meshes to all visible objects (not mandatory for visibility)
    1. Test different settings for walls and particles.
        * Diffuse for walls and non-transparent particles
        * Transparent for walls you want to see through
        * Glass with a very slightly blue colour for water
    2. Add a Emitter type mesh to the plane you placed behind the camera, this will be your light

12. Adjust the Scene settings for rendering
    1. In Render, change the Device from CPU to GPU
    2. In Sampling, change the preset to 'Preview' and check 'Square Samples' 
    3. In Light Paths, change the preset to Limited Global Illumination
        * Turn back on Reflective and Refractive Caustics
    4. In Performance, change the tile size to (X: 960, Y: 540)
        * If rendering at 100% use (X: 1920, Y: 1080)
        * DO NOT use progressive refine, this will slow down render time
    5. In Dimensions, change the end frame to the number of files you want to render
        * you can change the start frame to skip ahead as well

13. Render the animation and wait until it finishes

14. Navigate to the output directory (default is C:/tmp/) and run to_vid.py after moving 'openh264-1.6.0-win64msvc.dll' to the output directory
    * Select the lossless method

15. Compress the output video for emailing
