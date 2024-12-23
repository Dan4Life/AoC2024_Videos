from manim import *
from heapq import heappush,heappop

# manim -pqh --resolution 1920,1080 --disable_caching scene.py Day20 

class Day20(Scene):

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []
        self.X = [-1,0,1,0]
        self.Y = [0,1,0,-1]
        self.n, self.m, self.LINF = 0, 0, 1e9
        self.S = set()
        self.DI = 0
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
                    square = Square(side_length=0.45, color=WHITE)
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

        def relax(pq,dis,par,nt,nx,ny,ndi,t,x,y,di,w):
            if dis[nt][nx][ny][ndi] > dis[t][x][y][di]+w:
                dis[nt][nx][ny][ndi] = dis[t][x][y][di]+w
                par[nt][nx][ny][ndi] = (x,y,di)
                heappush(pq,(dis[nt][nx][ny][ndi],nx,ny,ndi))

        def dijkstra(s,pq,dis,par,sx,sy,d,t):
            pq = []
            for i in range(self.n):
                for j in range(self.m):
                    for k in range(4):
                        dis[t][i][j][k]=self.LINF

            dis[t][sx][sy][d]=0
            heappush(pq,(0,sx,sy,d))

            while len(pq):
                D,x,y,di = heappop(pq)
                if dis[t][x][y][di]!=D: continue
                nx,ny = x+self.X[di], y+self.Y[di]
                if nx>=0 and nx<self.n and ny>=0 and ny<self.m and s[nx][ny]!='#':
                    relax(pq,dis,par,t,nx,ny,di,t,x,y,di,1)

                ndi = (di+1)%4
                if dis[t][x][y][ndi] > dis[t][x][y][di]:
                    relax(pq,dis,par,t,x,y,ndi,t,x,y,di,0)

                ndi = (di+3)%4
                if dis[t][x][y][ndi] > dis[t][x][y][di]:
                    relax(pq,dis,par,t,x,y,ndi,t,x,y,di,0)

        def getPath(par,x,y,di,sx,sy,sdi,t):
            v = []
            while True:
                v.append((x,y,di))
                if x==sx and y==sy and sdi==di: break
                x,y,di = par[t][x][y][di]
            v.reverse()
            return v
        
        def create_player():
            line1 = Line(ORIGIN, [-0.2, -0.2, 0], color=WHITE, stroke_width=10)
            line2 = Line(ORIGIN, [-0.2, 0.2, 0], color=WHITE, stroke_width=10)
            line1.move_to(line1.get_center()+UP*0.05)
            player = VGroup(line1, line2)
            return player

        def rotate_player(player, angle):
            if angle < 0: self.DI+=1
            else: self.DI-=1
            self.play(player.animate.rotate(angle), run_time=0.1)

        def move_player(player, grid, oldx, oldy, new_x, new_y):
            grid[oldx][oldy][0].save_state()
            self.S.add((oldx,oldy))
            self.play(player.animate.move_to(grid[new_x][new_y][0].get_center()),
                      grid[oldx][oldy][0].animate.set_color(GREEN),
                      run_time=0.125)

        def display_shorter_path(grid,par,dis,s,player,l,i,j,nx,ny):
            if nx<0 or ny<0 or nx>=self.n or ny>=self.m or s[nx][ny]=='#': return
            if dis[0][i][j][0]+dis[1][nx][ny][0]+l >= dis[0][self.endx][self.endy][0]: return
            
            cost = dis[0][self.endx][self.endy][0]-(dis[0][i][j][0]+dis[1][nx][ny][0]+l)
            saved_text = Tex(f"Saved {cost} picoseconds",color=GREEN).move_to(UP*2.3+RIGHT*3.3).scale(0.8)

            avgi, avgj = (i+nx)//2, (j+ny)//2
            grid[avgi][avgj][0].save_state()
            player.save_state()
            self.play(grid[avgi][avgj][0].animate.set_color(BLACK),run_time=0.1)
            

            path2 = getPath(par,nx,ny,0,self.endx,self.endy,1,1)+ getPath(par,i,j,0,self.stx,self.sty,0,0)

            
            S2 = set()
            for a,b,c in path2: S2.add((a,b))
            
            oldDi = self.DI 
            ddi = -1
            for k in range(4):  
                if avgi-i==self.X[k] and avgj-j==self.Y[k]: ddi=k
            
            ang = 0
            if (self.DI+1)%4==ddi: ang=-PI/2
            else:
                while self.DI!=ddi:
                    ang+=PI/2
                    self.DI=(self.DI+3)%4
            rotate_player(player,ang)
            self.DI = oldDi

            animations = []

            for a,b in self.S:
                if (a,b) in S2: continue
                grid[a][b][0].save_state()
                animations.append(grid[a][b][0].animate.set_color(YELLOW))

            for a,b in S2:
                grid[a][b][0].save_state()
                animations.append(grid[a][b][0].animate.set_color(GREEN))
        
            if len(animations): self.play(animations,Create(saved_text),run_time=0.25)

            animations = []
            for a,b in self.S:
                if (a,b) in S2: continue
                animations.append(grid[a][b][0].animate.restore())
            if len(animations): self.play(*animations,run_time=0.25)

            animations = []
            for a,b in S2: animations.append(grid[a][b][0].animate.restore())
            if len(animations): self.play(*animations,run_time=0.25)

            self.play(Uncreate(saved_text),grid[avgi][avgj][0].animate.restore(),player.animate.restore(),run_time=0.1)

        def solver(arr):
            clearCounters(); self.S = set()
            addCounter(Text("Track Length", color=GREEN), UP*3.3+RIGHT*3.1)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*7)

            dis = [ [ [ [ self.LINF for l in range(4) ] for k in range(30) ] for j in range(30) ] for i in range(2) ] 
            par = [ [ [ [ (0,0,0) for l in range(4) ] for k in range(30) ] for j in range(30) ] for i in range(2) ]
            self.DI = 1

            s = []
            for a in arr: s.append(list(a))
            self.n, self.m = len(s), len(s[0])

            sx,sy,tx,ty = 0,0,0,0
            for i in range(self.n):
                for j in range(self.m):
                    if s[i][j]=='S':sx,sy=i,j
                    if s[i][j]=='E':tx,ty=i,j

            dijkstra(s,pq,dis,par,sx,sy,1,0)
            dijkstra(s,pq,dis,par,tx,ty,1,1)
            

            grid = create_grid(s).move_to(LEFT*3)
            player = create_player().move_to(grid[sx][sy][0].get_center())

            self.play(Create(grid),run_time=0.5)
            self.play(Write(self.counter[0]),run_time=0.5)
            
            
            path = getPath(par,tx,ty,1,sx,sy,1,0)
            path.pop(0)

            oldA,oldB,oldC = sx,sy,1
            self.S = set()

            for a,b,c in path: self.S.add((a,b))

            animations = []
            for a,b in self.S:
                grid[a][b][0].save_state()
                animations.append(grid[a][b][0].animate.set_color(GREEN))
            if len(animations): 
                self.cnt[0]+=len(self.S)
                self.wait(0.5)
                self.play(*animations, self.counter_tracker[0].animate.set_value(self.cnt[0]), run_time=1.0)
            
            animations = []
            for a,b in self.S:
                animations.append(grid[a][b][0].animate.restore())
            if len(animations): self.play(*animations,run_time=0.5)

            self.stx, self.sty = sx,sy
            self.endx, self.endy = tx, ty
            self.play(Create(player),run_time=0.5)

            path.insert(0,(sx,sy,1))

            for a,b,c in path:
                if oldC!=c: 
                    ang = -PI/2 
                    if c!=(oldC+1)%4: ang*=-1
                    rotate_player(player,ang)
                else:
                    move_player(player, grid, oldA,oldB,a,b)
                    i,j = a,b
                    for i2 in range(max(0,i-2),min(self.n,i+2+1)):
                        rem = 2-abs(i2-i)
                        j2 = j+rem  
                        display_shorter_path(grid,par,dis,s,player,2,i,j,i2,j2)
                        if rem: display_shorter_path(grid,par,dis,s,player,2,i,j,i2,j-rem)
                oldA,oldB,oldC = a,b,c
            self.wait();self.clear();self.wait(0.5);return


        grid = ['###############', 
                '#...#...#.....#', 
                '#.#.#.#.#.###.#', 
                '#S#...#.#.#...#', 
                '#######.#.#.###', 
                '#######.#.#...#', 
                '#######.#.###.#', 
                '###..E#...#...#', 
                '###.#######.###', 
                '#...###...#...#', 
                '#.#####.#.###.#', 
                '#.#...#.#.#...#', 
                '#.#.#.#.#.#.###', 
                '#...#...#...###', 
                '###############']

        solver(grid)
        self.wait(0.5)
