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
                        line = Line(grid[i][j].get_center(), grid[i2][j2].get_center())
                        line.set_color(ORANGE)
                        self.play(FadeIn(line))
                        self.play(counter_tracker.animate.increment_value(1))
        self.wait()
