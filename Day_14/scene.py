from manim import *

# manim -pqh --resolution 1920,1080 scene.py Day14

class Day14(Scene):

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []

        def addCounter(text, pos):
            self.cnt.append(0)
            self.counter.append(Variable(self.cnt[-1], text, num_decimal_places=0))
            self.counter[-1].label.scale(0.6)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*3.6)
            self.counter[-1].move_to(pos)
            self.counter_tracker.append(self.counter[-1].tracker)


        def createGridVGroup(s, sideLength, fontSize):
            newGrid = VGroup()

            for row in s:
                row_group = VGroup()
                for cell_content in row:
                    # Create the square
                    square = Square(
                        side_length=sideLength,
                        stroke_width=4,
                        fill_color=ORANGE,
                        fill_opacity=0.1
                    )

                    content = MathTex(str(cell_content), font_size=fontSize, color=WHITE).move_to(square)
                    if cell_content == 0:
                        content.set_opacity(0)

                    square_content = VGroup(square, content)
                    row_group.add(square_content)

                row_group.arrange(RIGHT, buff=0).center()
                newGrid.add(row_group)

            newGrid.arrange(DOWN, aligned_edge=LEFT, buff=0)
            return newGrid

        def increment_grid_cell(grid, i, j, Q, ok):
            square_content = grid[i][j]
            square, content = square_content
            val = int(content.get_tex_string()) + 1
            self.remove(grid[i][j][1])
            grid[i][j][1] = MathTex(str(val), font_size=40, color=WHITE).move_to(square)
            self.add(grid[i][j][1])
            if ok == 1: self.play(self.counter_tracker[Q].animate.set_value(self.cnt[Q]), run_time=0.5)

        addCounter(Text("Q1", color=RED), UP*2+LEFT*6)
        addCounter(Text("Q2", color=BLUE), UP*2+LEFT*2)
        addCounter(Text("Q3", color=YELLOW), UP*2+RIGHT*2)
        addCounter(Text("Q4", color=GREEN), UP*2+RIGHT*6)
        addCounter(Text("Ans", color=GREEN), UP*3)

        self.play(Write(self.counter[0]), Write(self.counter[1]), Write(self.counter[2]), Write(self.counter[3]), Write(self.counter[4]), run_time=0.5)
        
        n, m = 11, 7
        arr = [
                [0, 4, 3, -3], [6, 3, -1, -3], [10, 3, -1, 2], [2, 0, 2, -1], 
                [0, 0, 1, 3], [3, 0, -2, -2], [7, 6, -1, -3], [3, 0, -1, -2], 
                [9, 3, 2, 3], [7, 3, -1, 2], [2, 4, 2, -3], [9, 5, -3, -3]
            ]
        k = len(arr)
        s = [[0 for j in range(n)] for i in range(m)]

        grid = createGridVGroup(s,0.6,50)
        grid.move_to(LEFT*3.8+DOWN*0.6)

        
        grid2 = createGridVGroup(s,0.6,40)
        grid2.move_to(RIGHT*3.8+DOWN*0.6)

        col = [RED, BLUE, YELLOW, GREEN]
        for i in range(m):
            for j in range(n):
                Q, x, y = -1,j,i
                if x < n//2:
                    if y < m//2: Q=0
                    elif y > m//2: Q=2
                elif x > n//2:
                    if y < m//2: Q=1
                    elif y > m//2: Q=3
                if Q!=-1:  grid2[i][j][0].set_fill(col[Q],opacity=0.7)

        self.play(Write(grid), Write(grid2), run_time=0.5)
        self.wait()
        
        for i in range(k):
            x,y,dx,dy = arr[i]
            tot_cnt = 0

            start_x = MathTex(f"Start_X: {x}",color=YELLOW).move_to(grid2.get_bottom()+DOWN*0.3+LEFT*9.5).scale(0.75)
            start_y = MathTex(f"Start_Y: {y}",color=YELLOW).move_to(grid2.get_bottom()+DOWN*0.3+LEFT*7).scale(0.75)
            DX = MathTex(f"dx: {dx}").move_to(grid2.get_bottom()+DOWN*0.3*3+LEFT*9.5).scale(0.75)
            DY = MathTex(f"dy: {dy}").move_to(grid2.get_bottom()+DOWN*0.3*3+LEFT*7).scale(0.75)
            
            COUNT = MathTex(f"Seconds = {tot_cnt}").move_to(grid2.get_bottom()+DOWN*0.3*1.5+LEFT*4).scale(0.75)


            def update_content(lbl):
                lbl.become(MathTex(f"Seconds = {tot_cnt}").move_to(grid2.get_bottom()+DOWN*0.3*1.5+LEFT*4)).scale(0.75)

            COUNT.add_updater(update_content)

            robot_circle = Circle(radius=0.25, color=BLUE, fill_opacity=0.5).set_fill(BLUE, opacity=0.8)
            robot_text = MathTex(str(i+1), font_size=50*0.7, color=WHITE).move_to(robot_circle)
            robot = VGroup(robot_circle, robot_text).move_to(grid[y][x].get_center())
            
            self.play(Create(robot),Write(start_x), Write(start_y), Write(DX),Write(DY), Write(COUNT), run_time=0.5)
            
            
        
            num = 100
            while num>0:
                num-=1
                nx=(x+dx+n)%n 
                ny=(y+dy+m)%m

                if x+dx>=n or x+dx<0 or y+dy>=m or y+dy<0:
                    if dx<0:signx=-1
                    elif dx>0: signx=1
                    else: signx=0
                    if dy<0:signy=-1
                    elif dy>0: signy=1
                    else: signy=0

                    dif = max(n,m)
                    if x+dx>=n: dif = min(dif, n-1-x)
                    elif x+dx<0: dif=min(dif,x)
                    if y+dy>=m: dif = min(dif, m-1-y)
                    elif y+dy<0: dif=min(dif,y)

                    tx=x+min(dif,abs(dx))*signx 
                    ty=y+min(dif,abs(dy))*signy

                    if dif>0:
                        path = Line(grid[y][x].get_center(), grid[ty][tx].get_center(), color=RED)
                        self.play(FadeIn(path), MoveAlongPath(robot, path), run_time=0.2)
                        self.remove(path)

                    if abs(dx)>dif: tx+=signx 
                    if abs(dy)>dif: ty+=signy
                    
                    tx+=n; ty+=m; tx%=n; ty%=m

                    self.wait(0.2)
                    self.remove(robot)
                    robot.move_to(grid[ty][tx].get_center())
                    self.add(robot)

                    remX = max(0,abs(dx)-dif-1)
                    remY = max(0,abs(dy)-dif-1)
                    


                    if tx+remX*signx < 0 or tx+remX*signx >=n or ty+remY*signy < 0 or ty+remY*signy>=m:
                        
                        dif = max(n,m)
                        x,y=tx,ty
                        
                        if x+remX*signx>=n: dif = min(dif, n-1-x)
                        elif x+remX*signx<0: dif=min(dif,x)
                        if y+remY*signy>=m: dif = min(dif, m-1-y)
                        elif y+remY*signy<0: dif=min(dif,y)

                        tx=x+min(dif,remX)*signx 
                        ty=y+min(dif,remY)*signy

                        if dif>0:
                            path = Line(grid[y][x].get_center(), grid[ty][tx].get_center(), color=RED)
                            self.play(FadeIn(path), MoveAlongPath(robot, path), run_time=0.2)
                            self.remove(path)

                        if remX>dif: tx+=signx 
                        if remY>dif: ty+=signy
                        
                        tx+=n; ty+=m; tx%=n; ty%=m

                        self.wait(0.2)
                        self.remove(robot)
                        robot.move_to(grid[ty][tx].get_center())
                        self.add(robot)

                        if ty!=ny or tx!=nx:
                            path = Line(grid[ty][tx].get_center(), grid[ny][nx].get_center(), color=RED)
                            self.play(FadeIn(path), MoveAlongPath(robot, path), run_time=0.2)
                            self.remove(path)

                    elif ty!=ny or tx!=nx:
                        path = Line(grid[ty][tx].get_center(), grid[ny][nx].get_center(), color=RED)
                        self.play(FadeIn(path), MoveAlongPath(robot, path), run_time=0.2)
                        self.remove(path)

                elif y!=ny or x!=nx:
                    path = Line(grid[y][x].get_center(), grid[ny][nx].get_center(), color=YELLOW)
                    self.play(FadeIn(path), MoveAlongPath(robot, path), run_time=0.2)
                    self.remove(path)
                x,y = nx,ny
                tot_cnt+=1
            
            COUNT.become(MathTex(f"Seconds = {tot_cnt}").move_to(grid2.get_bottom()+DOWN*0.3*1.5+LEFT*4)).scale(0.75)
            self.wait(0.5)
            
            
            self.play(Uncreate(robot),  Unwrite(start_x), Unwrite(start_y), Unwrite(DX),Unwrite(DY), Unwrite(COUNT), run_time=0.5)

            Q = -1
            if x < n//2:
                if y < m//2: Q=0
                elif y > m//2: Q=2
            elif x > n//2:
                if y < m//2: Q=1
                elif y > m//2: Q=3

            if Q!=-1:
                self.cnt[Q]+=1
                increment_grid_cell(grid2,y,x,Q,1)
            else:
                increment_grid_cell(grid2,y,x,Q,0)

        self.cnt[4]=self.cnt[0]*self.cnt[1]*self.cnt[2]*self.cnt[3]
        self.play(self.counter_tracker[4].animate.set_value(self.cnt[4]))
        self.wait()
