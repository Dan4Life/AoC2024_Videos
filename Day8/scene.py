from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day8

class Day8(Scene):

    def construct(self):
        def drawMiddleLine():
            line = Line(4*DOWN, UP * 10)
            line.set_color(WHITE)

            self.play(FadeIn(line),run_time=0.5)
            self.wait()

        def createGridVGroup(s, sideLength, fontSize, Color=WHITE):
            newGrid = VGroup()
            for row in s:
                w = VGroup(
                    *[
                        VGroup(
                            Square(
                                side_length=sideLength,
                                color=Color,
                                fill_color=ORANGE,
                                fill_opacity=0.05
                            ),
                            Text(str(c), font_size=fontSize)
                        ) for c in row
                    ]
                )
                w.arrange(RIGHT, buff=0.0).center()
                newGrid.add(w)
            newGrid.arrange(DOWN, aligned_edge=LEFT, buff=0.0)
            return newGrid

        
        s = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '0', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '0', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '0', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '0', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', 'A', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', 'A', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'A', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
        n = 12
        m = len(s[0])

        for i in range(n):
            for j in range(m):
                if s[i][j] == '.':
                    s[i][j] = ' '

        M = {}
        for i in range(n):
            for j in range(m):
                if s[i][j] not in M:
                    M[s[i][j]] = []
                M[s[i][j]].append((i,j))

        S = set()

        drawMiddleLine()

        counter, counter_tracker, cnt = [], [], [0,0]
        counter.append(Variable(cnt[0],Text("Sum",color=GREEN), num_decimal_places=0))
        counter.append(Variable(cnt[1],Text("Sum2",color=RED), num_decimal_places=0))

        for i in range(2):
            counter[i].label.scale(0.6)
            counter[i].value.next_to(counter[i].label.get_center(),RIGHT*3.6)

        counter[0].move_to(UP*3+LEFT*4)
        counter[1].move_to(UP*3+RIGHT*4)

        for i in range(2):
            counter_tracker.append(counter[i].tracker)

        grid = createGridVGroup(s,0.53,25)
        grid.move_to(LEFT*3.8+DOWN*0.5)

        self.play(Write(grid),run_time=0.5)
        self.play(Write(counter[0]),run_time=0.5)

        for key,v in M.items():
            if key==' ':
                continue
            for i in range(len(v)):
                for j in range(i+1,len(v)):
                    x1,y1 = v[i]
                    x2,y2 = v[j]
                    disx = x2-x1 
                    disy = y2-y1 
                    nx = x1-disx 
                    ny = y1-disy
                    w = []

                    
                    if nx>=0 and nx<n and ny>=0 and ny<m:
                        w.append((nx,ny))

                    nx = x2+disx 
                    ny = y2+disy

                    if nx>=0 and nx<n and ny>=0 and ny<m:
                        w.append((nx,ny))

                    
                    self.play(
                        grid[x1][y1][0].animate.set_fill(RED, opacity=1.0),  # Access the square and set its fill
                        grid[x2][y2][0].animate.set_fill(RED, opacity=1.0),  # Access the square and set its fill
                        grid[x1][y1][1].animate.set_color(WHITE),  # Access the text and set its color
                        grid[x2][y2][1].animate.set_color(WHITE),  # Access the text and set its color
                        run_time=0.5
                    )

                    for a,b in w:
                        if (a,b) not in S:
                            S.add((a,b))
                            self.play(grid[a][b][0].animate.set_fill(YELLOW, opacity=1.0),
                                      grid[a][b][1].animate.set_color(BLACK),
                                      counter_tracker[0].animate.increment_value(1),
                                      run_time=0.5)
                    
                    animations = []

                    if (x1,y1) in S:
                        animations.append(grid[x1][y1][0].animate.set_fill(YELLOW, opacity=1.0))
                        animations.append(grid[x1][y1][1].animate.set_color(BLACK))
                    else:
                        animations.append(grid[x1][y1][0].animate.set_fill(ORANGE, opacity=0.05))
                        animations.append(grid[x1][y1][1].animate.set_color(WHITE))

                    if (x2,y2) in S:
                        animations.append(grid[x2][y2][0].animate.set_fill(YELLOW, opacity=1.0))
                        animations.append(grid[x2][y2][1].animate.set_color(BLACK))
                    else:
                        animations.append(grid[x2][y2][0].animate.set_fill(ORANGE, opacity=0.05))
                        animations.append(grid[x2][y2][1].animate.set_color(WHITE))

                    self.play( *animations ,run_time=0.5)
        





        S = set()

        grid2 = createGridVGroup(s,0.53,25)
        grid2.move_to(RIGHT*3.8+DOWN*0.5)

        self.play(Write(grid2),run_time=0.5)
        self.play(Write(counter[1]),run_time=0.5)

        for key,v in M.items():
            if key==' ':
                continue
            for i in range(len(v)):
                for j in range(i+1,len(v)):
                    x1,y1 = v[i]
                    x2,y2 = v[j]
                    disx = x2-x1 
                    disy = y2-y1 
                    w = []

                    nx = x1 
                    ny = y1
                    while nx>=0 and nx<n and ny>=0 and ny<m:
                        w.append((nx,ny))
                        nx-=disx
                        ny-=disy

                    nx = x1+disx
                    ny = y1+disy
                    while nx>=0 and nx<n and ny>=0 and ny<m:
                        w.append((nx,ny))
                        nx+=disx
                        ny+=disy

                    self.play(
                        grid2[x1][y1][0].animate.set_fill(RED, opacity=1.0),  # Access the square and set its fill
                        grid2[x2][y2][0].animate.set_fill(RED, opacity=1.0),  # Access the square and set its fill
                        grid2[x1][y1][1].animate.set_color(WHITE),  # Access the text and set its color
                        grid2[x2][y2][1].animate.set_color(WHITE),  # Access the text and set its color
                        run_time=0.5
                    )
                    
                    w.sort()
                    line = Line(grid2[w[0][0]][w[0][1]].get_center(), grid2[w[len(w)-1][0]][w[len(w)-1][1]].get_center())
                    line.set_color(ORANGE)
                    self.play(Create(line),run_time=0.5)

                    for a,b in w:
                        if (a,b) not in S:
                            S.add((a,b))
                            self.play(grid2[a][b][0].animate.set_fill(YELLOW, opacity=1.0),
                                      grid2[a][b][1].animate.set_color(BLACK),
                                      counter_tracker[1].animate.increment_value(1),
                                      run_time=0.5)

                    self.play(Uncreate(line),run_time=0.5)
                    animations = []

                    if (x1,y1) in S:
                        animations.append(grid2[x1][y1][0].animate.set_fill(YELLOW, opacity=1.0))
                        animations.append(grid2[x1][y1][1].animate.set_color(BLACK))
                    else:
                        animations.append(grid2[x1][y1][0].animate.set_fill(ORANGE, opacity=0.05))
                        animations.append(grid2[x1][y1][1].animate.set_color(WHITE))

                    if (x2,y2) in S:
                        animations.append(grid2[x2][y2][0].animate.set_fill(YELLOW, opacity=1.0))
                        animations.append(grid2[x2][y2][1].animate.set_color(BLACK))
                    else:
                        animations.append(grid2[x2][y2][0].animate.set_fill(ORANGE, opacity=0.05))
                        animations.append(grid2[x2][y2][1].animate.set_color(WHITE))

                    self.play( *animations,run_time=0.5 )
        self.wait()
