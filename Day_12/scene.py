from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day12

class Day12(Scene):

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []
        self.COLOR_PALETTE = [
            "#1F77B4",  # Deep Blue
            "#FF7F0E",  # Vibrant Orange
            "#2CA02C",  # Bright Green
            "#D62728",  # Bold Red
            "#9467BD",  # Purple
            "#8C564B",  # Brown
            "#E377C2",  # Pink
            "#7F7F7F",  # Neutral Gray
            "#4682B4",  # Steel Blue
            "#17BECF",  # Teal
            "#F5A623",  # Light Orange
            "#4A90E2",  # Sky Blue
            "#50E3C2",  # Aqua
            "#9B9B9B",  # Silver Gray
            "#B22222",  # Firebrick Red
            "#228B22",  # Forest Green
            "#BCBD22",  # Yellow-Green
            "#FFD700",  # Gold
            "#EE82EE",  # Violet
            "#40E0D0",  # Turquoise
            "#FFA07A",  # Light Salmon
            "#A52A2A",  # Red Brown
            "#00FA9A",  # Medium Spring Green
            "#CD5C5C",  # Indian Red
            "#6495ED",  # Cornflower Blue
            "#6A5ACD"   # Slate Blue
        ]

        def addCounter(text, pos):
            self.cnt.append(0)
            self.counter.append(Variable(self.cnt[-1], text, num_decimal_places=0))
            self.counter[-1].label.scale(0.6)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*3.6)
            self.counter[-1].move_to(pos)
            self.counter_tracker.append(self.counter[-1].tracker)

        def drawMiddleLine():
            line = Line(4*DOWN, UP * 10)
            line.set_color(WHITE)

            self.play(FadeIn(line),run_time=0.5)
            self.wait()

        def createGridVGroup(s, sideLength, fontSize):
            def createSquare(side_length, side_colors, side_opacities, stroke_width, fill_color, fill_opacity):
                """Creates a square with customizable fill and independently styled overlay sides."""
                # Create the base square
                base_square = Square(side_length=side_length)
                base_square.set_fill(color=fill_color, opacity=fill_opacity)
                base_square.set_stroke(color=WHITE, width=1)  # Base stroke

                # Define vertices for overlaying lines
                vertices = base_square.get_vertices()

                top_line = Line(vertices[0], vertices[1], color=side_colors[0]).set_stroke(width=stroke_width, opacity=side_opacities[0])
                right_line = Line(vertices[1], vertices[2], color=side_colors[1]).set_stroke(width=stroke_width, opacity=side_opacities[1])
                bottom_line = Line(vertices[2], vertices[3], color=side_colors[2]).set_stroke(width=stroke_width, opacity=side_opacities[2])
                left_line = Line(vertices[3], vertices[0], color=side_colors[3]).set_stroke(width=stroke_width, opacity=side_opacities[3])
                

                # Group overlay lines together
                overlay_lines = VGroup(top_line, right_line, bottom_line, left_line)

                # Group base square and overlay lines together
                custom_square = VGroup(base_square, overlay_lines)

                # Add a method to dynamically change stroke color of an individual side
                def change_single_side(index, color, opacity=None):
                    """Change the color and opacity of a specific side by index (0: top, 1: right, 2: bottom, 3: left)."""
                    if 0 <= index < len(overlay_lines):
                        anim = overlay_lines[index].animate.set_color(color)
                        if opacity is not None:
                            anim = anim.set_opacity(opacity)
                        return anim
                    raise IndexError("Index out of range. Must be between 0 and 3.")

                custom_square.change_single_side = change_single_side

                return custom_square



            newGrid = VGroup()
            for row in s:
                w = VGroup(*[
                    VGroup(
                        createSquare(
                            side_length=sideLength,
                            side_colors=[WHITE, WHITE, WHITE, WHITE],
                            side_opacities=[0.1,0.1,0.1,0.1],
                            stroke_width=5,  fill_color=WHITE, fill_opacity=0.4
                        ),
                        Text(str(c), font_size=fontSize, color=BLACK).move_to(ORIGIN)
                    ) for c in row
                ])
                w.arrange(RIGHT, buff=0.04).center()
                newGrid.add(w)

            newGrid.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            return newGrid

        addCounter(Text("Sum", color=GREEN), UP*3.7+LEFT*3.8)
        addCounter(Text("Area", color=GREEN), UP*3+LEFT*6)
        addCounter(Text("Per", color=GREEN), UP*3+LEFT*1.5)

        addCounter(Text("Sum", color=RED), UP*3.7+RIGHT*3.8)
        addCounter(Text("Area", color=RED), UP*3+RIGHT*1.5)
        addCounter(Text("Per", color=RED), UP*3+RIGHT*6)

        drawMiddleLine()
        self.play(Write(self.counter[0]), Write(self.counter[1]), Write(self.counter[2]), run_time=0.5)
        
        
        s = ['RRRRIICCFF', 'RRRRIICCCF', 'VVRRRCCFFF', 'VVRCCCJFFF', 'VVVVCJJCFE', 'VVIVCCJJEE', 'VVIIICJJEE', 'MIIIIIJJEE', 'MIIISIJEEE', 'MMMISSJEEE']
        n, m = len(s), len(s[0])
        vis = [[0 for j in range(m)] for i in range(n) ]

        grid = createGridVGroup(s,0.6,30)
        grid.move_to(LEFT*3.8+DOWN*0.6)
        self.play(Write(grid),run_time=0.5)
        
        X = [1,-1,0,0]
        Y = [0,0,1,-1]
        self.cc = 1

        def dfs(i, j):

            self.cnt[1]+=1
            vis[i][j] = self.cc 

            col = self.COLOR_PALETTE[ord(curC)-ord('A')]
            self.play(
                grid[i][j][0][0].animate.set_fill(col,opacity=0.5),
                grid[i][j][0].change_single_side(0, col, 0.2),
                grid[i][j][0].change_single_side(1, col, 0.2),
                grid[i][j][0].change_single_side(2, col, 0.2),
                grid[i][j][0].change_single_side(3, col, 0.2),
                grid[i][j][1].animate.set_color(WHITE), 
                self.counter_tracker[1].animate.set_value(self.cnt[1]),
                run_time=0.5)
            
            animations = []
            for k in range(4):
                ni, nj = i+X[k], j+Y[k]
                if ni<0 or nj<0 or ni>=n or nj>=m or s[ni][nj]!=curC:
                    if k==0: side=2
                    elif k==1: side=0
                    elif k==2: side=3
                    else: side = 1
                    animations.append(grid[i][j][0].change_single_side(side, col, 1.0))
                    self.cnt[2]+=1
            
            if len(animations):
                self.play(*animations, self.counter_tracker[2].animate.set_value(self.cnt[2]), run_time=0.5)

            for k in range(4):
                ni, nj = i+X[k], j+Y[k]
                if ni<0 or nj<0 or ni>=n or nj>=m or s[ni][nj]!=curC or vis[ni][nj]:
                    continue
                arrow = Arrow(grid[i][j].get_center(), grid[ni][nj].get_center(), buff=0.2, color=WHITE)
                self.add(arrow)
                dfs(ni,nj)
                self.remove(arrow)


        for i in range(n):
            for j in range(m):
                if vis[i][j]:
                    continue
                curC = s[i][j]
                self.cc+=1
                dfs(i,j)

                number = DecimalNumber(self.cnt[1]*self.cnt[2], num_decimal_places=0).move_to(UP*3+LEFT*4)

                self.cnt[0]+=self.cnt[1]*self.cnt[2]

                self.play( self.counter_tracker[0].animate.set_value(self.cnt[0]),
                            number.animate.set_value(self.cnt[1]*self.cnt[2]),
                            UpdateFromFunc(number, lambda m: m.set_value(number.get_value())),
                          run_time=0.5)
                

                self.cnt[1]=self.cnt[2]=0

                self.play(
                    Uncreate(number),
                    self.counter_tracker[1].animate.set_value(self.cnt[1]), 
                    self.counter_tracker[2].animate.set_value(self.cnt[2]),     
                    run_time=0.5
                )

    
        ok = [ [ [0 for k in range(5)] for j in range(m) ] for i in range(n) ]
        vis = [[0 for j in range(m)] for i in range(n) ]

        grid2 = createGridVGroup(s,0.6,30)
        grid2.move_to(RIGHT*3.8+DOWN*0.6)
        self.play(Write(self.counter[3]), Write(self.counter[4]), Write(self.counter[5]), run_time=0.5)
        self.play(Write(grid2),run_time=0.5)

        animationsFast = []

        self.cc = 0

        def dfs2(i, j):

            self.cnt[4]+=1
            vis[i][j] = self.cc 

            col = self.COLOR_PALETTE[ord(curC)-ord('A')]
            animationsFast.append(grid2[i][j][0][0].animate.set_fill(col,opacity=0.5))
            animationsFast.append(grid2[i][j][0].change_single_side(0, col, 0.2))
            animationsFast.append(grid2[i][j][0].change_single_side(1, col, 0.2))
            animationsFast.append(grid2[i][j][0].change_single_side(2, col, 0.2))
            animationsFast.append(grid2[i][j][0].change_single_side(3, col, 0.2))
            animationsFast.append(grid2[i][j][1].animate.set_color(WHITE))

            for k in range(4):
                ni, nj = i+X[k], j+Y[k]
                if ni<0 or nj<0 or ni>=n or nj>=m or s[ni][nj]!=curC:
                    ok[i][j][k] = 1
                    continue
                if vis[ni][nj]==0:
                    dfs2(ni,nj)

        def dfs3(i, j):
            vis[i][j] = self.cc 

            col = self.COLOR_PALETTE[ord(curC)-ord('A')]
            
            for k in [0,2,1,3]:
                if ok[i][j][k]!=1:
                    continue 

                ni, nj = i+X[k], j+Y[k]
                if ni<0 or nj<0 or ni>=n or nj>=m or s[ni][nj]!=curC:

                    xi, xj = i, j
                    if k < 2: xj-=1
                    else: xi-=1

                    if xi>=0 and xj>=0 and xi<n and xj<m and s[xi][xj]==curC and ok[xi][xj][k]:
                        continue

                    xi,xj = i,j
                    animations = []
                    while xi>=0 and xj>=0 and xi<n and xj<m and s[xi][xj]==curC and ok[xi][xj][k]:
                        if k==0: side=2
                        elif k==1: side=0
                        elif k==2: side=3
                        else: side = 1

                        animations.append(grid2[xi][xj][0].change_single_side(side, col, 1.0))
                        if k < 2: xj+=1
                        else: xi+=1

                    self.cnt[5]+=1
                    animations.append(self.counter_tracker[5].animate.set_value(self.cnt[5]))

                    if len(animations): self.play(*animations, run_time=0.5)



            for k in [0,2,1,3]:
                ni, nj = i+X[k], j+Y[k]
                if ni<0 or nj<0 or ni>=n or nj>=m or s[ni][nj]!=curC:
                    continue
                if vis[ni][nj]==0:
                    dfs3(ni,nj)


        for i in range(n):
            for j in range(m):
                if vis[i][j]:
                    continue
                curC = s[i][j]
                self.cc+=1
                animationsFast = []
                dfs2(i,j)
                animationsFast.append(self.counter_tracker[4].animate.set_value(self.cnt[4]))
                self.play(*animationsFast, run_time=0.5)


                for ii in range(n):
                    for jj in range(m):
                        if vis[ii][jj]==self.cc:
                            vis[ii][jj] = 0    

                dfs3(i,j)

                number = DecimalNumber(self.cnt[1]*self.cnt[2], num_decimal_places=0).move_to(UP*3+RIGHT*4)

                self.cnt[3]+=self.cnt[4]*self.cnt[5]

                self.play( self.counter_tracker[3].animate.set_value(self.cnt[3]),
                            number.animate.set_value(self.cnt[4]*self.cnt[5]),
                            UpdateFromFunc(number, lambda m: m.set_value(number.get_value())),
                          run_time=0.5)
                

                self.cnt[4]=self.cnt[5]=0

                self.play(
                    Uncreate(number),
                    self.counter_tracker[4].animate.set_value(self.cnt[4]), 
                    self.counter_tracker[5].animate.set_value(self.cnt[5]),     
                    run_time=0.5
                )
                
        self.wait()
