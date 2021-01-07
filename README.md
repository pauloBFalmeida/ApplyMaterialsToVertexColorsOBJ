# ApplyMaterialsToVertexColorsOBJ
 simple python code to create and apply materials to faces from an .obj with colors in the vertex data

# Origin
Made to be used with the .obj from: <br>
3D Face Reconstruction from a Single Image <br>
https://cvl-demos.cs.nott.ac.uk/vrn/ <br>
https://github.com/AaronJackson/vrn

# Run
python3 color.py filename -n n_materials -out output_filename <br>

exemples: <br>
python3 color.py myface.obj -n 40 -out myfacecolored <br>
or <br>
python3 color.py myface.obj

# Tips
Smaller n_materials work faster but get a worse quallity. <br>
Larger n_materials take much longer and are very cpu intensive, and can spend a lot of memory when importing into 3D softwares. <br>
Recommend in the range of 30 and 80
