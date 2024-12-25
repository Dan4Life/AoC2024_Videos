from manim import *

# manim -pqh --disable_caching scene.py Day25 

class Day25(Scene):

    def getType(self, s):
        if s[0][0]=='#': return 0
        return 1
    
    def create_grid(self, s,col,sideLength=0.45):
        grid = VGroup()

        color_map = {
            "#": col,    # Obstacle
            ".": BLACK,  # Empty space
        }

        for i in range(self.n):
            row = VGroup()
            for j in range(self.m):
                char = s[i][j]
                square = Square(side_length=sideLength, color=WHITE)
                square.set_fill(color=color_map.get(char, WHITE), opacity=0.8)
                row.add(square)
            row.arrange(RIGHT, buff=0)
            grid.add(row)
        grid.arrange(DOWN, aligned_edge=LEFT, buff=0)
        grid.move_to(ORIGIN)
        return grid
    
    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []
        self.n, self.m = 0, 0

        def clearCounters():
            self.counter, self.counter_tracker, self.cnt = [], [], []

        def addCounter(text, pos):
            self.cnt.append(0)
            self.counter.append(Variable(self.cnt[-1], text, num_decimal_places=0))
            self.counter[-1].label.scale(0.6)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*3.6)
            self.counter[-1].move_to(pos)
            self.counter_tracker.append(self.counter[-1].tracker)

        def solver(grids):
            clearCounters()
            addCounter(Text("Number of fits", color=GREEN), UP*3.3+RIGHT*3.1)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*7)

            self.n, self.m = len(grids[0]), len(grids[0][0])
            grid = [VGroup(),VGroup()]
            a = [[],[]]
            for s in grids:
                xd = self.getType(s)
                col = RED 
                if xd: col = BLUE
                a[xd].append(s)
                grid[xd].add(self.create_grid(s,col))        
            
            grid[0].arrange(RIGHT,buff=0.5).move_to(LEFT*3+UP*2)
            grid[1].arrange(RIGHT,buff=0.5).move_to(LEFT*3+DOWN*2)
            self.play(Write(grid[0]), Write(grid[1]))

            s = ['.'*self.m]*self.n
            cur_grid = self.create_grid(s,WHITE,0.8).move_to(RIGHT*3.5+DOWN*0.5)
            self.play(Write(cur_grid), Write(self.counter[0]))
            
            pointers = [
                Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.15),
                Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.15),
                Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.25)
            ]
            pointers[0].next_to(grid[0][0][self.n-1][0], DOWN).set_y(grid[0][0][self.n-1][0].get_y()-0.5)
            pointers[1].next_to(grid[1][0][self.n-1][0], DOWN).set_y(grid[1][0][self.n-1][0].get_y()-0.5)
            pointers[2].next_to(cur_grid[self.n-1][0], DOWN).set_y(cur_grid[self.n-1][0].get_y()-0.65)
            self.play(*[Create(pointer) for pointer in pointers])
            
            for I in range(len(a[0])):
                for J in range(len(a[1])):
                    cur = a[0][I]
                    cur2 = a[1][J]
                    for i in range(len(cur_grid)):
                        for j in range(len(cur_grid[i])):
                            cur_grid[i][j].save_state()
                    ok = 1
                    for j in range(self.m):
                        self.play(pointers[0].animate.set_x(grid[0][I][0][j].get_center()[0]),
                                  pointers[1].animate.set_x(grid[1][J][0][j].get_center()[0]),
                                  pointers[2].animate.set_x(cur_grid[0][j].get_center()[0]),
                                  run_time=0.5)
                        animations = []
                        for i in range(self.n):
                            cnt = 0
                            if cur[i][j]=='#': cnt+=1
                            if cur2[i][j]=='#': cnt+=2
                            col = BLACK
                            if cnt==1: col=RED
                            elif cnt==2: col=BLUE
                            elif cnt==3: ok=0;col=PURPLE
                            if col!=BLACK:
                                animations.append(cur_grid[i][j].animate.set_color(col))
                        if len(animations): self.play(*animations,run_time=0.5)
                    if ok:
                        text = Tex("Good",color=GREEN).move_to(self.counter[0].get_center()+DOWN*0.5)
                        self.cnt[0]+=1
                        self.play(Write(text),self.counter_tracker[0].animate.set_value(self.cnt[0]))
                        self.play(Unwrite(text),run_time=0.5)
                    else: 
                        text = Tex("Bad",color=RED).move_to(self.counter[0].get_center()+DOWN*0.5)
                        self.play(Write(text),run_time=0.5)
                        self.play(Unwrite(text),run_time=0.5)
                    self.wait(0.5)
                    animations = []
                    for i in range(len(cur_grid)):
                        for j in range(len(cur_grid[i])):
                            animations.append(cur_grid[i][j].animate.restore())
                    if len(animations): self.play(*animations,run_time=0.5)
            self.wait();self.clear();self.wait(0.5);return


        grids = [
            [
             '#####', 
             '.####', 
             '.####', 
             '.####', 
             '.#.#.', 
             '.#...', 
             '.....'
            ],
            [
             '#####', 
             '##.##', 
             '.#.##', 
             '...##', 
             '...#.', 
             '...#.', 
             '.....'
            ],
            [
             '.....', 
             '#....', 
             '#....', 
             '#...#', 
             '#.#.#', 
             '#.###', 
             '#####'
            ],
            [
             '.....', 
             '.....', 
             '#.#..', 
             '###..', 
             '###.#', 
             '###.#', 
             '#####'
            ],
            [
             '.....', 
             '.....', 
             '.....', 
             '#....', 
             '#.#..', 
             '#.#.#', 
             '#####'
            ]
        ]
        solver(grids)
        self.wait(0.5)
