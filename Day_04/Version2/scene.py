from manim import *
import math
# manim -pql --resolution 1920,1080 scene.py Day4

class Day4(Scene):
    def construct(self):
        X = [-1,1, -1,1, -1,1, 0,0]
        Y = [-1,1, 1,-1, 0,0, -1,1]
        n, m = 10, 10

        
        s = [['M', 'M', 'M', 'S', 'X', 'X', 'M', 'A', 'S', 'M'], 
             ['M', 'S', 'A', 'M', 'X', 'M', 'S', 'M', 'S', 'A'], 
             ['A', 'M', 'X', 'S', 'X', 'M', 'A', 'A', 'M', 'M'], 
             ['M', 'S', 'A', 'M', 'A', 'S', 'M', 'S', 'M', 'X'], 
             ['X', 'M', 'A', 'S', 'A', 'M', 'X', 'A', 'M', 'M'], 
             ['X', 'X', 'A', 'M', 'M', 'X', 'X', 'A', 'M', 'A'], 
             ['S', 'M', 'S', 'M', 'S', 'A', 'S', 'X', 'S', 'S'], 
             ['S', 'A', 'X', 'A', 'M', 'A', 'S', 'A', 'A', 'A'], 
             ['M', 'A', 'M', 'M', 'M', 'X', 'M', 'M', 'M', 'M'], 
             ['M', 'X', 'M', 'X', 'A', 'X', 'M', 'A', 'S', 'X']]
        for i in range(len(s)):
            for j in range(len(s[0])):
                if s[i][j] == '.':
                    s[i][j] = ' '
        x,y = 6,4
        m = len(s[0])

        cnt, counter_tracker = 0, 0
        counter = Variable(cnt,Text("Count"), num_decimal_places=0)
        counter.label.scale(0.5)
        counter.value.next_to(counter.label.get_center(),RIGHT*3.3)

        counter.move_to(UP*3.5)
        counter_tracker = counter.tracker

        grid = VGroup()
        for row in s:
            w = VGroup(*[Square(side_length=0.65, color=WHITE, fill_color=ORANGE, fill_opacity=0.05).add(Text(str(c),font_size=20)) for c in row])
            w.arrange(RIGHT, buff=0.0).center()
            grid.add(w)

        grid.arrange(DOWN, aligned_edge=LEFT, buff=0.0)
        vis = [[0 for j in range(m)] for i in range(n)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j].submobjects[0].text=='X':
                    grid[i][j].submobjects[0].color = RED
                elif grid[i][j].submobjects[0].text=='M':
                    grid[i][j].submobjects[0].color = BLUE
                elif grid[i][j].submobjects[0].text=='A':
                    grid[i][j].submobjects[0].color = GREEN
                elif grid[i][j].submobjects[0].text=='S':
                    grid[i][j].submobjects[0].color = YELLOW

        self.play(Write(grid))
        self.wait()
        self.play(Write(counter))
        self.wait()
        
        for i in range(n):
            for j in range(m):
                for di in range(8):
                    ok = 1
                    for k,c in enumerate("XMAS"):
                        ni = i+X[di]*k
                        nj = j+Y[di]*k
                        if ni<0 or ni>=n or nj<0 or nj>=m or s[ni][nj]!=c:
                            ok=0
                            break
                    if ok:
                        i2 = i+X[di]*3
                        j2 = j+Y[di]*3
                        of = 0.21
                        x5, y5, z5 = grid[i][j].get_center()
                        x6, y6, z6 = grid[i2][j2].get_center()
                        ok = 1
                        if di<2:
                            x1, y1, z1 = grid[i][j].get_corner(DL)+[of,of,0]
                            x2, y2, z2 = grid[i2][j2].get_corner(DL)+[of,of,0]
                            x3, y3, z3 = grid[i][j].get_corner(UR)+[-of,-of,0]
                            x4, y4, z4 = grid[i2][j2].get_corner(UR)+[-of,-of,0]
                            if di == 0:
                                ok = -1
                                
                            ang = PI/3-0.265
                            radd = math.dist([x1,y1],[x5,y5])
                            arc1 = Arc(radius = radd, start_angle = ang, angle = PI*ok, arc_center=[x5, y5, z5])
                            arc2 = Arc(radius = radd, start_angle = ang, angle = -PI*ok, arc_center=[x6, y6, z6])
                        elif di<4:
                            x1, y1, z1 = grid[i][j].get_corner(DR)+[-of,of,0]
                            x2, y2, z2 = grid[i2][j2].get_corner(DR)+[-of,of,0]
                            x3, y3, z3 = grid[i][j].get_corner(UL)+[of,-of,0]
                            x4, y4, z4 = grid[i2][j2].get_corner(UL)+[of,-of,0]
                            if di == 2:
                                ok = -1
                                
                            ang = PI/3-0.265
                            radd = math.dist([x1,y1],[x5,y5])
                            arc1 = Arc(radius = radd, start_angle = -ang, angle = PI*ok, arc_center=[x5, y5, z5])
                            arc2 = Arc(radius = radd, start_angle = -ang, angle = -PI*ok, arc_center=[x6, y6, z6])
                        elif di<6:
                            x1, y1, z1 = grid[i][j].get_right()+[-of,0,0]
                            x2, y2, z2 = grid[i2][j2].get_right()+[-of,0,0]
                            x3, y3, z3 = grid[i][j].get_left()+[of,0,0]
                            x4, y4, z4 = grid[i2][j2].get_left()+[of,0,0]
                            if di == 4:
                                ok = -1
                                
                            radd = math.dist([x1,y1],[x5,y5])
                            arc1 = Arc(radius = radd, start_angle = 0, angle = PI*ok, arc_center=[x5, y5, z5])
                            arc2 = Arc(radius = radd, start_angle = 0, angle = -PI*ok, arc_center=[x6, y6, z6])
                        else:
                            x1, y1, z1 = grid[i][j].get_top()+[0,-of,0]
                            x2, y2, z2 = grid[i2][j2].get_top()+[0,-of,0]
                            x3, y3, z3 = grid[i][j].get_bottom()+[0,of,0]
                            x4, y4, z4 = grid[i2][j2].get_bottom()+[0,of,0]
                            if di == 7:
                                ok = -1
                            
                            radd = math.dist([x1,y1],[x5,y5])
                            arc1 = Arc(radius = radd, start_angle = PI/2, angle = -PI*ok, arc_center=[x5, y5, z5])
                            arc2 = Arc(radius = radd, start_angle = PI/2, angle = PI*ok, arc_center=[x6, y6, z6])

                        line1, line2 = Line([x1,y1,z1], [x2,y2,z2]), Line([x3,y3,z3], [x4,y4,z4])
                        line1.color=line2.color=arc1.color=arc2.color=ORANGE
                        rounded_rect = VGroup(arc1, line1, arc2, line2)

                        self.play(FadeIn(rounded_rect))
                        self.play(counter_tracker.animate.increment_value(1))
        self.wait()
