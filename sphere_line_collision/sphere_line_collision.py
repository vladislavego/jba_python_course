""" The program find if sphere and line have colission points and print it in console.

    To run program enter 'program_name.py source_file_name.txt' in console.
    
    sourse_file must have folowing format: 

    {sphere: {center: [0, 0, 0], radius: 10.67}, line: {[1, 0.5, 15], [43, -14.6, 0.04]}} 

    pay atention the placement of spaces inside objects.
"""
    
    

class Point:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'\n{self.x}, {self.y}, {self.z}\n'
        
        
class Line:

    def __init__(self, point1:Point, point2:Point):
        self.point1 = point1
        self.point2 = point2
        self.dv = self.__get_direct_vector()
        
    def __get_direct_vector(self) -> Point:

        return Point(self.point2.x - self.point1.x, self.point2.y - self.point1.y, self.point2.z - self.point1.z)
        
        
class Sphere:

    def __init__(self, center:Point, radius:float):
        self.center = center
        self.radius = radius

def get_quadratic_equation_coefficients(line:Line, sphere:Sphere) -> list:
    
    dv = line.dv
    pt = line.point1

    c = sphere.center
    r = sphere.radius
    
    a = dv.x ** 2 + dv.y ** 2 + dv.z ** 2 
    b = 2 * ((pt.x - c.x) * dv.x + (pt.y - c.y) * dv.y + (pt.z - c.z) * dv.z)
    c = (pt.x - c.x) ** 2 + (pt.y - c.y) ** 2 + (pt.z - c.z) ** 2 - r ** 2
    
    return [a, b, c]

def find_collision_point(line:Line, t:float) -> Point:

        pt = line.point1
        dv = line.dv

        x = pt.x + t * dv.x
        y = pt.y + t * dv.y
        z = pt.z + t * dv.z

        return Point(x, y, z)

def solve_quadratic_equation(a, b, c) -> list:

    desc = b ** 2 - 4 * a * c
    
    if desc < 0:
        return []
    
    if desc == 0:
        x = -b / (2 * a)
        return [x] 
    
    x1 = (-b - desc ** 0.5) / (2 * a)
    x2 = (-b + desc ** 0.5) / (2 * a)
    
    return [x1, x2]
    
def convert_source_to_dict(source_string:str) -> dict:
    """ Function convert str object like

        '{sphere: {center: [0, 0, 0], radius: 10.67}, line: {[1, 0.5, 15], [43, -14.6, 0.04]}}'

        to dict object like

        {'sphere': {'center': [0.0, 0.0, 0.0], 'radius': 10.67}, 'line': {'point1': [1.0, 0.5, 15.0], 'point2': [43.0, -14.6, 0.04]}}
    """
    source = source_string.split('}')
    for sep in ('{', ':', '[', ']', ',', ' '):
        source = ''.join(source).split(sep)
    
    objects = []
    for el, cnt in (('radius', 2), ('center', 4), ('line', 7)):
        i = source.index(el)
        objects.append([float(x) for x in source[i + 1 : i + cnt]])
        
    radius, center, line = objects
    point1, point2 = line[:3], line[3:]
    
    return {'sphere': {'center': center, 'radius': radius[0]}, 'line': {'point1': point1, 'point2': point2}}
   
def create_line(source:str):
    """ Function gets str object in the folowing format: 
        
        {'point1': [1.0, 0.5, 15.0], 'point2': [43.0, -14.6, 0.04]}
        
        retrun Point object.
    """
    
    point1 = Point(*source.get('point1'))
    point2 = Point(*source.get('point2'))

    return Line(point1, point2)
        
def create_sphere(source:str):
    """ Function gets str object in the folowing format: 
        
        {'center': [0.0, 0.0, 0.0], 'radius': 10.67}
        
        retrun Sphere object.
    """
    
    center = Point(*(source.get('center')))
    radius = source.get('radius')
    
    return Sphere(center, radius)

def find_sphere_line_collision(line:Line, sphere:Sphere):

    a, b, c = get_quadratic_equation_coefficients(line, sphere)

    ans = solve_quadratic_equation(a, b, c)

    if len(ans) == 1:
        t = ans[0]

        point = find_collision_point(line, t)
        return f'{point.__str__()}'

    if len(ans) == 2:
        t1, t2 = ans
        
        point_one = find_collision_point(line, t1)
        point_two = find_collision_point(line, t2)
        
        return f'{point_one.__str__()}{point_two.__str__()}'

    return 'No collision detected'
   
def main():
    
    file_name = sys.argv[1]
    
    try:
        f = open(file_name, 'r')
        f.close()
    except:
        print("Couldn't open the file")
    else:
        with open(file_name, 'r') as source_file:
            count = 0
            for line in source_file:
                count += 1
                line = line.strip().replace('\n','')
                if not line:
                    continue
                
                try:
                    source = convert_source_to_dict(line)
                except:
                    print(f'String {count}: invalid data format')
                    print("""
Data about the sphere and line should have folowing format:

                    {sphere: {center: [0, 0, 0], radius: 10.67}, line: {[1, 0.5, 15], [43, -14.6, 0.04]}}
                        
Objects and keys can be placed in a free sequence. Observe the placement of whitespace characters inside objects
""")

                else:
                
                    line_source = source.get('line')
                    line = create_line(line_source)
                    
                    sphere_source = source.get('sphere')
                    sphere = create_sphere(sphere_source)

                    print(find_sphere_line_collision(line, sphere))

            if count == 0:
                print("File is empty")

if __name__ == '__main__':

    import sys

    if len(sys.argv) != 2:
        print("""
Pass the name of the file with the sphere and line data as a command-line argument, for example: main.py main.txt
        
Data about the sphere and line should have folowing format:

                    {sphere: {center: [0, 0, 0], radius: 10.67}, line: {[1, 0.5, 15], [43, -14.6, 0.04]}}
                        
Objects and keys can be placed in a free sequence. Observe the placement of whitespace characters inside objects.
""")
    else:
        main()
    

    
