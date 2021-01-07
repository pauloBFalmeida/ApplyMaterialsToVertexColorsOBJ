import argparse
from sklearn.cluster import KMeans

class Vertex():
    def __init__(self, x, y, z, r, g, b):
        self.x = x
        self.y = y
        self.z = z
        self.r = int(float(r) * 255)
        self.g = int(float(g) * 255)
        self.b = int(float(b) * 255)
    def to_str(self):
        return 'v '+self.x+' '+self.y+' '+self.z+'\n'

class Material():
    def __init__(self, value, id):
        self.value = value
        self.id = str(id)
        self.faces = []
    def addFaces(self, faces):
        self.faces += faces
    def faces_to_str(self):
        t = "usemtl "+self.id+'\n'
        for f in self.faces:
            t += 'f '+str(f[0])+' '+str(f[1])+' '+str(f[2])+'\n'
        return t
    def material_to_str(self):
        rgb = [str(v / 255) for v in self.value]
        return 'newmtl '+self.id+'\n' \
                'Ka 0.2 0.2 0.2 \n' \
                'Kd ' +rgb[0]+' '+rgb[1]+' '+rgb[2]+'\n' \
                'illum 1'+'\n'

# ==============


def main(args):
    fileName = args.fileName
    n_materials = args.n_materials if args.n_materials else 50
    fileNameOut = args.output_fileName if args.output_fileName else fileName[:-4] +'_2'

    vertices    = [None]
    faces       = []
    materials   = []

    # read
    print('reading file')
    with open(fileName, 'r') as file:
        for line in file.read().split('\n'):
            if len(line) > 1:
                line = line.split(' ')
                if line[0] == 'v':
                    vertices.append( Vertex(line[1], line[2], line[3], line[4], line[5], line[6]) )
                elif line[0] == 'f':
                    faces.append( list(map(int, [line[1], line[2], line[3]])) )

    #
    print('creating rgb for the faces')
    rgbToFaces = {}
    rgbs = []
    # get the average rgb from the face vertices
    for face in faces:
        vs = [vertices[v_i] for v_i in face]
        r = sum([v.r for v in vs]) // len(vs)
        g = sum([v.g for v in vs]) // len(vs)
        b = sum([v.b for v in vs]) // len(vs)
        # create a key for that rgb
        key = r*10000 + g*100 + b
        # add the face to the rgbToFace dict
        if key not in rgbToFaces:
            rgbToFaces[key] = []
            rgbs.append( [r,g,b] )
        rgbToFaces[key].append(face)

    # start kmeans
    print('starting KMeans')

    kmeans = KMeans(n_clusters=n_materials)
    kmeans.fit(rgbs)

    for i in range(len(kmeans.cluster_centers_)):
        # get the rgb from the center
        rgbValue = [int(k) for k in kmeans.cluster_centers_[i]]
        materials.append( Material(rgbValue, i) ) 

    print('ajusting faces to materials')
    for i in range(len(rgbs)):
        # get the material index (kmeans center) of the rgb from the face
        # and add that face to material
        material_i = kmeans.labels_[i]
        r,g,b = rgbs[i]
        key = r*10000 + g*100 + b
        materials[material_i].addFaces( rgbToFaces[key] )

    # write
    print('writing output file')

    outputFile      = fileNameOut + '.obj'
    outputFileMtl   = fileNameOut + '.mtl'

    with open(outputFile, 'w') as file:
        file.write('mtllib '+outputFileMtl+'\n')
        print('writing vertices')
        for v in vertices[1:]:
            file.write(v.to_str())
        print('writing faces')
        for m in materials:
            file.write(m.faces_to_str())
    print('writing mtl file')
    with open(outputFileMtl, 'w') as file:
        for m in materials:
            file.write(m.material_to_str())

    #
    print('done')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fileName", help="name of the .obj file (with the extension .obj)")
    parser.add_argument("-n", "--n_materials", help="max number of materials (default 50)", type=int)
    parser.add_argument('-out', "--output_fileName", help="name of the output file (without the extension)")
    args = parser.parse_args()
    main(args)
