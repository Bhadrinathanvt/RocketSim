# File path
file_path = '../obj models/Rocket.obj'

# Open the file and read its lines
with open(file_path, "r") as file:
    lines = file.readlines()

# Filter lines that do not start with 'f'
filtered_lines_f = [line for line in lines if line.startswith("f")]
filtered_lines_v = [line for line in lines if line.startswith("v ")]
filtered_lines = filtered_lines_v + filtered_lines_f
# Write the filtered lines back to the file
with open(file_path, "w") as file:
    file.writelines(filtered_lines)

processed_faces = []
for elements in filtered_lines_f:
    fac_ = elements.split()
    face1 = 'f ' + fac_[1].split('/')[0] + ' ' + fac_[2].split('/')[0] + ' ' + fac_[4].split('/')[0]
    face2 = 'f ' + fac_[2].split('/')[0] + ' ' + fac_[3].split('/')[0] + ' ' + fac_[4].split('/')[0]

    processed_faces.append(face1)
    processed_faces.append(face2)

filtered_lines = filtered_lines_v + processed_faces
# Write to the .obj file
with open(file_path, "w") as obj_file:
    obj_file.writelines(filtered_lines)

