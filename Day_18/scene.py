from manim import *
from heapq import heappush,heappop

# manim -pqh --resolution 1920,1080 scene.py Day18
# I solved today's problem using bfs, but I could just spam my Dijkstra solution from Day 16...

class Day18(Scene):

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []
        self.X = [1,0,-1,0]
        self.Y = [0,-1,0,1]
        self.S = set()
        self.n, self.m, self.LINF = 0, 0, 1e9
        pq = []

        def clearCounters():
            self.counter, self.counter_tracker, self.cnt = [], [], []

        def addCounter(text, pos):
            self.cnt.append(0)
            self.counter.append(Variable(self.cnt[-1], text, num_decimal_places=0))
            self.counter[-1].label.scale(0.6)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*3.6)
            self.counter[-1].move_to(pos)
            self.counter_tracker.append(self.counter[-1].tracker)

        def create_grid(s):
            n, m = len(s), len(s[0])
            grid = VGroup()

            color_map = {
                "#": RED,    # Obstacle
                ".": BLACK,  # Empty space
                'S': YELLOW, # Player
                "E": GREEN,  # Destination
                "O": BLUE,   # Single-cell box
            }
            text_color_map = {
                "O": WHITE,
            }

            for i in range(n):
                row = VGroup()
                for j in range(m):
                    char = s[i][j]
                    square = Square(side_length=0.7, color=BLUE)
                    square.set_fill(color=color_map.get(char, WHITE), opacity=0.8)
                    
                    if char in text_color_map:
                        label = Text(char, color=text_color_map[char], font_size=30)
                        label.move_to(square.get_center())
                        row.add(VGroup(square, label))
                    else: row.add(square)
                row.arrange(RIGHT, buff=0)
                grid.add(row)
            grid.arrange(DOWN, aligned_edge=LEFT, buff=0)
            grid.move_to(ORIGIN)
            return grid

        def update_grid(grid_vgroup, s):
            n, m = len(s), len(s[0])

            color_map = {
                "#": RED,    # Obstacle
                ".": BLACK,  # Empty space
                'S': YELLOW, # Player
                "E": GREEN,  # Destination
                "O": BLUE,   # Single-cell box
            }
            text_color_map = {
                "O": WHITE,
            }

            for i in range(n):
                for j in range(m):
                    char = s[i][j]
                    square_group = grid_vgroup[i][j]

                    # Update square color
                    square = square_group[0] if isinstance(square_group, VGroup) else square_group
                    square.set_fill(color=color_map.get(char, WHITE), opacity=0.8)

                    # Update or remove label
                    if char in text_color_map:
                        label = Text(char, color=text_color_map[char], font_size=30).move_to(square.get_center())
                        if isinstance(square_group, VGroup) and len(square_group) > 1:
                            square_group[1].become(label)  # Update label if it exists
                        else:
                            grid_vgroup[i][j] = VGroup(square, label)  # Add label to square
                    else:
                        if isinstance(square_group, VGroup) and len(square_group) > 1:
                            grid_vgroup[i][j] = square  # Remove label if updating to '.'

        def relax(pq,dis,par,nx,ny,ndi,x,y,di,w):
            if dis[nx][ny][ndi] > dis[x][y][di]+w:
                dis[nx][ny][ndi] = dis[x][y][di]+w
                par[nx][ny][ndi] = (x,y,di)
                heappush(pq,(dis[nx][ny][ndi],nx,ny,ndi))

        def dijkstra(s,pq,dis,par,sx,sy,d):
            pq = []
            for i in range(self.n):
                for j in range(self.m):
                    for k in range(4):
                        dis[i][j][k]=self.LINF

            dis[sx][sy][d]=0
            heappush(pq,(0,sx,sy,d))

            while len(pq):
                D,x,y,di = heappop(pq)
                if dis[x][y][di]!=D: continue
                nx,ny = x+self.X[di], y+self.Y[di]
                if nx>=0 and nx<self.n and ny>=0 and ny<self.m and s[nx][ny]!='#':
                    relax(pq,dis,par,nx,ny,di,x,y,di,1)

                ndi = (di+1)%4
                if dis[x][y][ndi] > dis[x][y][di]:
                    relax(pq,dis,par,x,y,ndi,x,y,di,0)

                ndi = (di+3)%4
                if dis[x][y][ndi] > dis[x][y][di]:
                    relax(pq,dis,par,x,y,ndi,x,y,di,0)

        def getPath(par,x,y,di,sx,sy,sdi):
            v = []
            while True:
                v.append((x,y,di))
                if x==sx and y==sy and di==sdi: break
                x,y,di = par[x][y][di]
            v.reverse()
            return v
        
        def create_player():
            line1 = Line(ORIGIN, [-0.3, -0.3, 0], color=WHITE, stroke_width=15)
            line2 = Line(ORIGIN, [-0.3, 0.3, 0], color=WHITE, stroke_width=15)
            line1.move_to(line1.get_center()+UP*0.08)
            player = VGroup(line1, line2)
            return player

        def rotate_player(player, angle):
            self.play(player.animate.rotate(angle), run_time=0.2)

        def move_player(player, grid, oldx, oldy, new_x, new_y):
            self.cnt[0]+=1
            self.S.add((oldx,oldy))
            self.S.add((new_x,new_y))
            self.play(player.animate.move_to(grid[new_x][new_y][0].get_center()), 
                      self.counter_tracker[0].animate.set_value(self.cnt[0]),
                      grid[oldx][oldy][0].animate.set_color(BLUE),
                      run_time=0.125)

        def solver(n,m,obstacles):
            clearCounters()
            addCounter(Text("Min-cost path", color=GREEN), UP*2+RIGHT*3.1)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*7)

            dis = [ [ [ self.LINF for l in range(4) ] for k in range(20) ] for j in range(20) ] 
            par = [ [ [ (0,0,0) for l in range(4) ] for k in range(20) ] for j in range(20) ] 
            
            s = []
            for i in range(n): s.append(['.']*m)
            self.n, self.m = len(s), len(s[0])
            s[0][0],s[n-1][m-1]='S','E'
            sx,sy,tx,ty = 0,0,n-1,m-1

            grid = create_grid(s).move_to(LEFT*3.5)
            self.play(Create(grid),Write(self.counter[0]),run_time=0.5)
            
            obstacle_text = Text(f"After 0 obstacles",color=RED).move_to(UP*3+RIGHT*3.2).scale(0.6)
            self.play(Write(obstacle_text),run_time=0.5)
            _ = 0
            while _ <= len(obstacles):
                if _==1: obstacle_text.become(Text(f"After {_} obstacle",color=RED).move_to(UP*3+RIGHT*3.1)).scale(0.6)
                else: obstacle_text.become(Text(f"After {_} obstacles",color=RED).move_to(UP*3+RIGHT*3.2)).scale(0.6)
                update_grid(grid,s);self.cnt[0] = 0; self.wait(0.1)
                player = create_player().move_to(grid[sx][sy][0].get_center()).rotate(-PI/2)
                self.play(Create(player),run_time=0.5)
            
                dijkstra(s,pq,dis,par,sx,sy,0)

                ans = dis[tx][ty][1]
                self.S = set()
                if ans > n*m:
                    x,y = obstacles[_-1]
                    final_obstacle_text = Text(f"Obstacle at ({x},{y}) removes all paths",color=RED).move_to(UP*2+RIGHT*3.1).scale(0.6)
                    self.play(Write(final_obstacle_text),Uncreate(self.counter[0]),run_time=0.5)
                    break
                else:
                    v = getPath(par,tx,ty,1,sx,sy,0)
                    v.pop(0)
                    oldA,oldB,oldC = sx,sy,0
                    for a,b,c in v:
                        if oldC!=c: 
                            ang = -PI/2 
                            if c!=(oldC+1)%4: ang*=-1
                            rotate_player(player,ang)
                        else: move_player(player, grid, oldA,oldB,a,b)
                        if a==tx and b==ty: break
                        oldA,oldB,oldC = a,b,c

                self.play(Uncreate(player),run_time=0.5)
                while _ !=len(obstacles): 
                    y,x = obstacles[_]
                    s[x][y]='#'
                    self.play(grid[x][y][0].animate.set_color(RED))
                    if (x,y) not in self.S: 
                        _+=1
                        if _==1: obstacle_text.become(Text(f"After {_} obstacle",color=RED).move_to(UP*3+RIGHT*3.1)).scale(0.6)
                        else: obstacle_text.become(Text(f"After {_} obstacles",color=RED).move_to(UP*3+RIGHT*3.2)).scale(0.6)
                    else: break
                _+=1

            self.wait();self.clear();self.wait(0.5);return

        s = [[5, 4], [4, 2], [4, 5], [3, 0], [2, 1], [6, 3], [2, 4], [1, 5], 
             [0, 6], [3, 3], [2, 6], [5, 1], [1, 2], [5, 5], [2, 5], [6, 5], 
             [1, 4], [0, 4], [6, 4], [1, 1], [6, 1], [1, 0], [0, 5], [1, 6], [2, 0]]
        solver(7,7,s)
        self.wait(0.5)
        
        
