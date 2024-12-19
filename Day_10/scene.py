from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day10

class Day10(Scene):

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], [0,0]
        def addTwoCounters():
            self.counter.append(Variable(self.cnt[0],Text("Sum",color=GREEN), num_decimal_places=0))
            self.counter.append(Variable(self.cnt[1],Text("Sum2",color=RED), num_decimal_places=0))
            
            for i in range(2):
                self.counter[i].label.scale(0.6)
                self.counter[i].value.next_to(self.counter[i].label.get_center(),RIGHT*3.6)

            self.counter[0].move_to(UP*3.3+LEFT*3.8)
            self.counter[1].move_to(UP*3.3+RIGHT*3.8)

            for i in range(2):
                self.play(Write(self.counter[i]), run_time=0.5)
                self.counter_tracker.append(self.counter[i].tracker)

        def drawMiddleLine():
            line = Line(4*DOWN, UP * 10)
            line.set_color(WHITE)

            self.play(FadeIn(line),run_time=0.5)
            self.wait()

        def createGridVGroup(s, sideLength, fontSize, low_color, high_color):
            newGrid = VGroup()
            for row in s:
                w = VGroup(
                    *[
                        VGroup(
                            Square(
                                side_length=sideLength,
                                color=WHITE,
                                fill_color=interpolate_color(low_color, high_color, int(c) / 9),
                                fill_opacity=0.75
                            ),
                            Text(str(c), font_size=fontSize, color=BLACK)
                        ) for c in row
                    ]
                )
                w.arrange(RIGHT, buff=0.0).center()
                newGrid.add(w)
            
            newGrid.arrange(DOWN, aligned_edge=LEFT, buff=0.0)
            return newGrid


        addTwoCounters()
        drawMiddleLine()
        
        s = ['89010123', '78121874', '87430965', '96549874', '45678903', '32019012', '01329801', '10456732']
        n, m = len(s), len(s[0])
        vis = [[0 for j in range(m)] for i in range(n) ]

        grid = createGridVGroup(s,0.8,34, WHITE, GREEN)
        grid.move_to(LEFT*3.8+DOWN*0.5)

        self.play(Write(grid),run_time=0.5)
        
        X = [1,-1,0,0]
        Y = [0,0,1,-1]

        def dfs(i,j,d):
            vis[i][j] = 1
            self.play(grid[i][j][1].animate.set_color(YELLOW), run_time=0.2)

            if d==9:
                self.cnt[0]+=1
                self.play(grid[i][j][1].animate.set_color(WHITE),
                          self.counter_tracker[0].animate.set_value(self.cnt[0]), run_time=0.2)
                return

            for k in range(4):
                ni, nj = i+X[k], j+Y[k]
                if ni<0 or nj<0 or ni>=n or nj>=m or vis[ni][nj] or int(s[ni][nj])!=d+1:
                    continue
                arrow = Arrow(grid[i][j].get_center(), grid[ni][nj].get_center(), buff=0.2, color=BLACK)
                self.add(arrow)
                dfs(ni,nj,d+1)
                self.remove(arrow)
            self.play(grid[i][j][1].animate.set_color(BLACK), run_time=0.2)




        for i in range(n):
            for j in range(m):
                if s[i][j]!='0':
                    continue
                vis = [[0 for j in range(m)] for i in range(n) ]
                dfs(i,j,0)
                animations = []
                for k in range(n):
                    for l in range(m):
                        if vis[k][l]:
                            animations.append(grid[k][l][1].animate.set_color(BLACK))
                if len(animations): self.play(*animations, run_time=0.5)

                
        #PART 2


        vis = [[0 for j in range(m)] for i in range(n) ]

        grid2 = createGridVGroup(s,0.8,34, WHITE, GREEN)
        grid2.move_to(RIGHT*3.8+DOWN*0.5)

        self.play(Write(grid2),run_time=0.5)
        self.play(Write(self.counter[1]),run_time=0.5)

        def dfs2(i,j,d):
            vis[i][j] = 1
            self.play(grid2[i][j][1].animate.set_color(YELLOW), run_time=0.1)

            if d==9:
                self.cnt[1]+=1
                self.play(grid2[i][j][1].animate.set_color(WHITE),
                          self.counter_tracker[1].animate.set_value(self.cnt[1]), run_time=0.1)
                vis[i][j] = 0
                self.play(grid2[i][j][1].animate.set_color(BLACK), run_time=0.1)
                return

            for k in range(4):
                ni, nj = i+X[k], j+Y[k]
                if ni<0 or nj<0 or ni>=n or nj>=m or vis[ni][nj] or int(s[ni][nj])!=d+1:
                    continue
                arrow = Arrow(grid2[i][j].get_center(), grid2[ni][nj].get_center(), buff=0.2, color=BLACK)
                self.add(arrow)
                dfs2(ni,nj,d+1)
                self.remove(arrow)

            vis[i][j] = 0
            self.play(grid2[i][j][1].animate.set_color(BLACK), run_time=0.1)

            

        for i in range(n):
            for j in range(m):
                if s[i][j]!='0':
                    continue
                vis = [[0 for j in range(m)] for i in range(n) ]
                dfs2(i,j,0)
                animations = []
                for k in range(n):
                    for l in range(m):
                        if vis[k][l]:
                            animations.append(grid2[k][l][1].animate.set_color(BLACK))
                if len(animations): self.play(*animations, run_time=0.5)

        self.wait()
