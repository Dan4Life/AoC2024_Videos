from manim import *
from heapq import heappush,heappop

# manim -pqh --resolution 1920,1080 scene.py Day16

class Day16(Scene):

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []
        self.X = [-1,0,1,0]
        self.Y = [0,1,0,-1]
        self.n, self.m, self.LINF = 0, 0, 1e9
        self.S = set()
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

            if t==1:
                for i in range(4):
                    dis[t][sx][sy][i]=0
                    heappush(pq,(0,sx,sy,i))
            else:
                dis[t][sx][sy][d]=0
                heappush(pq,(0,sx,sy,d))

            while len(pq):
                D,x,y,di = heappop(pq)
                if dis[t][x][y][di]!=D: continue
                nx,ny = x+self.X[di], y+self.Y[di]
                if t: nx,ny=x-self.X[di], y-self.Y[di]
                if nx>=0 and nx<self.n and ny>=0 and ny<self.m and s[nx][ny]!='#':
                    relax(pq,dis,par,t,nx,ny,di,t,x,y,di,1)

                ndi = (di+1)%4
                if dis[t][x][y][ndi] > dis[t][x][y][di]+1000:
                    relax(pq,dis,par,t,x,y,ndi,t,x,y,di,1000)

                ndi = (di+3)%4
                if dis[t][x][y][ndi] > dis[t][x][y][di]+1000:
                    relax(pq,dis,par,t,x,y,ndi,t,x,y,di,1000)

        def getPath(par,x,y,di,sx,sy,sdi,t):
            v = []
            while True:
                v.append((x,y,di))
                if x==sx and y==sy and di==sdi: break
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
            self.cnt[0]+=1000
            self.play(player.animate.rotate(angle), 
                      self.counter_tracker[0].animate.set_value(self.cnt[0]),
                       run_time=0.5)

        def move_player(player, grid, oldx, oldy, new_x, new_y):
            self.cnt[0]+=1; self.cnt[1]+=1
            self.S.add((oldx,oldy))
            self.play(player.animate.move_to(grid[new_x][new_y][0].get_center()), 
                      self.counter_tracker[0].animate.set_value(self.cnt[0]),
                      self.counter_tracker[1].animate.set_value(self.cnt[1]),
                      grid[oldx][oldy][0].animate.set_color(GREEN),
                      run_time=0.25)

        def solver(arr):
            clearCounters(); self.S = set()
            addCounter(Text("Min-cost path", color=GREEN), UP*3.3+RIGHT*3.1)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*7)

            addCounter(Text("Tiles on Min-cost path", color=GREEN), UP*2+RIGHT*4)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),DOWN*1.2)

            dis = [ [ [ [ self.LINF for l in range(4) ] for k in range(20) ] for j in range(20) ] for i in range(6) ] 
            par = [ [ [ [ (0,0,0) for l in range(4) ] for k in range(20) ] for j in range(20) ] for i in range(6) ]
            
            s = []
            for a in arr: s.append(list(a))
            self.n, self.m = len(s), len(s[0])

            sx,sy,tx,ty = 0,0,0,0
            for i in range(self.n):
                for j in range(self.m):
                    if s[i][j]=='S':sx,sy=i,j
                    if s[i][j]=='E':tx,ty=i,j

            grid = create_grid(s).move_to(LEFT*3)
            player = create_player().move_to(grid[sx][sy][0].get_center())
        
            self.play(Create(grid),run_time=0.5)
            self.play(Create(player),Write(self.counter[0]),Write(self.counter[1]),run_time=0.5)
            
            dijkstra(s,pq,dis,par,sx,sy,1,0)
            for i in range(1,5):
                dijkstra(s,pq,dis,par,tx,ty,i-1,i)

            ans = self.LINF
            for i in range(4):
                ans=min(ans,dis[0][tx][ty][i])

            for i in range(4):
                if dis[0][tx][ty][i]!=ans: continue
                v = getPath(par,tx,ty,i,sx,sy,1,0)
                v.pop(0)
                oldA,oldB,oldC = sx,sy,1
                for a,b,c in v:
                    if oldC!=c: 
                        ang = -PI/2 
                        if c!=(oldC+1)%4: ang*=-1
                        rotate_player(player,ang)
                    else: move_player(player, grid, oldA,oldB,a,b)
                    oldA,oldB,oldC = a,b,c

            self.cnt[1]+=1
            self.play(Uncreate(player), self.counter_tracker[1].animate.set_value(self.cnt[1]), run_time=0.5)

            self.S.add((tx,ty))

            num = 0
            for i in range(self.n):
                for j in range(self.m):
                    if (i,j) in self.S: continue
                    ok = 1
                    for k in range(4):
                        if not ok: break
                        for l in range(1,5):
                            if not ok: break
                            if dis[0][i][j][k]+dis[l][i][j][k]==ans:
                                num+=1; ok=0
                                v = getPath(par,i,j,k,sx,sy,1,0)+getPath(par,i,j,k,tx,ty,l-1,l)

                                S2 = set()
                                for a,b,c in v: S2.add((a,b))

                                animations = []
                                for a,b in S2:
                                    if (a,b) not in self.S: self.cnt[1]+=1
                                    animations.append(grid[a][b][0].animate.set_color(YELLOW))

                                if len(animations): self.play(*animations)

                                animations = []
                                for a,b in S2:
                                    if (a,b) in self.S:
                                        animations.append(grid[a][b][0].animate.set_color(GREEN))
                                if len(animations): self.play(*animations)

                                animations = []
                                for a,b in S2:
                                    if (a,b) not in self.S:
                                        animations.append(grid[a][b][0].animate.set_color(GREEN))
                                if len(animations): self.play(*animations, self.counter_tracker[1].animate.set_value(self.cnt[1]))

                                for a,b,c in v: self.S.add((a,b))

            print(num)

            self.wait();self.clear();self.wait(0.5);return


        grid = ['###############', 
                '#.......#....E#', 
                '#.#.###.#.###.#', 
                '#.....#.#...#.#', 
                '#.###.#####.#.#', 
                '#.#.#.......#.#', 
                '#.#.#####.###.#', 
                '#...........#.#', 
                '###.#.#####.#.#', 
                '#...#.....#.#.#', 
                '#.#.#.###.#.#.#', 
                '#.....#...#.#.#', 
                '#.###.#.#.#.#.#', 
                '#S..#.....#...#', 
                '###############']

        grid2 =['#################', 
                '#...#...#...#..E#', 
                '#.#.#.#.#.#.#.#.#', 
                '#.#.#.#...#...#.#', 
                '#.#.#.#.###.#.#.#', 
                '#...#.#.#.....#.#', 
                '#.#.#.#.#.#####.#', 
                '#.#...#.#.#.....#', 
                '#.#.#####.#.###.#', 
                '#.#.#.......#...#', 
                '#.#.###.#####.###', 
                '#.#.#...#.....#.#', 
                '#.#.#.#####.###.#', 
                '#.#.#.........#.#', 
                '#.#.#.#########.#', 
                '#S#.............#', 
                '#################']

        solver(grid)
        solver(grid2)
        self.wait(0.5)
        
        
