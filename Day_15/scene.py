from manim import *

# manim -pqh --resolution 1920,1080 scene.py Day15

class Day15(Scene):

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []
        X = [-1,0,1,0]
        Y = [0,1,0,-1]
        M = {'^':0, '>':1, 'v':2, '<':3}

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
                ".": None,   # Empty space has no text
                "@": YELLOW, # Player
                "O": BLUE,   # Single-cell box
                "[": BLUE,   # Left part of two-cell box
                "]": BLUE,   # Right part of two-cell box
            }
            text_color_map = {
                "@": BLACK,
                "O": WHITE,
                "[": WHITE,
                "]": WHITE,
            }

            for i in range(n):
                row = VGroup()
                for j in range(m):
                    char = s[i][j]
                    square = Square(side_length=0.6, color=WHITE)
                    
                    if char == ".": square.set_fill(color=BLACK, opacity=0.8)
                    else: square.set_fill(color=color_map.get(char, WHITE), opacity=0.8)
                    
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
            """Updates the grid_vgroup based on the new state list `s`."""
            n, m = len(s), len(s[0])

            color_map = {
                "#": RED,
                ".": None,  # Empty spaces
                "@": YELLOW,
                "O": BLUE,
                "[": BLUE,
                "]": BLUE,
            }
            text_color_map = {
                "@": BLACK,
                "O": WHITE,
                "[": WHITE,
                "]": WHITE,
            }

            for i in range(n):
                for j in range(m):
                    char = s[i][j]
                    square_group = grid_vgroup[i][j]

                    # Update square color
                    square = square_group[0] if isinstance(square_group, VGroup) else square_group
                    if char == ".":
                        square.set_fill(color=BLACK, opacity=0)  # Transparent for empty spaces
                    else:
                        square.set_fill(color=color_map.get(char, WHITE), opacity=0.75)

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


        def part_one_solver(arr, moves, fast=False):
            RUNTIME = 0.5
            if fast: RUNTIME = 0.125
            clearCounters()
            addCounter(Text("Sum", color=GREEN), UP*3.3)

            s = []
            for a in arr:
                s.append(list(a))
            n, m = len(s), len(s[0])
            x, y=-1,-1
            for i in range(n):
                for j in range(m):
                    if s[i][j]=='@':
                        x,y = i,j
            
            grid = create_grid(s)
            self.play(Create(grid),run_time=0.5)

            
            cur = Text("dir",color=YELLOW).move_to(RIGHT*6.5)
            self.add(cur)
            for u in moves:
                D, no_upd = M[u], 0
                nx, ny = x+X[D], y+Y[D]
                lx,ly = nx,ny
                while s[lx][ly]=='O': lx+=X[D];ly+=Y[D]
                if s[lx][ly]=='#': no_upd = 1
                else:
                    while lx!=x or ly!=y:
                        s[lx][ly],s[lx-X[D]][ly-Y[D]]=s[lx-X[D]][ly-Y[D]],s[lx][ly]
                        lx-=X[D]; ly-=Y[D]
                    x,y=nx, ny

                
                if no_upd: col=RED
                else:col=YELLOW
                cur.become(Text(f"{u}",color=col).move_to(RIGHT*5).scale(3))
                update_grid(grid,s);self.wait(RUNTIME)
            self.remove(cur)

            self.play(Write(self.counter[0]),run_time=0.25)
            for i in range(n):
                for j in range(m):
                    if s[i][j]=='O':
                        self.play(grid[i][j][0].animate.set_color(GREEN),run_time=0.25)
                        sum = MathTex(f"+ {i}*100+{j}={i*100+j}").move_to(self.counter[0].get_right()+RIGHT*2.5)
                        self.play(Write(sum),run_time=0.25)
                        self.cnt[0]+=i*100+j
                        self.play(self.counter_tracker[0].animate.set_value(self.cnt[0]),Unwrite(sum),run_time=0.25)

            self.wait();self.clear();self.wait(0.5)

        def part_two_solver(arr, moves, fast=False):
            RUNTIME = 0.5
            if fast: RUNTIME = 0.125
            clearCounters()
            addCounter(Text("Sum", color=GREEN), UP*3.3)

            s = []
            for a in arr:
                v = ""
                for b in a:
                    if b == '#':v+="##"
                    elif b=='@':v+="@."
                    elif b=='O':v+="[]"
                    else: v+=".."
                s.append(list(v))
            
            grid = create_grid(arr) 
            self.play(Create(grid),run_time=0.5)
            self.wait(0.5)
            self.play(Transform(grid, create_grid(s)))

            n, m = len(s), len(s[0])
            x, y=-1,-1

            for i in range(n):
                for j in range(m):
                    if s[i][j]=='@':
                        x,y = i,j

            cur = Text("dir",color=YELLOW).move_to(RIGHT*6)
            self.add(cur)
            for u in moves:
                D = M[u]
                nx,ny = x+X[D], y+Y[D]
                lx,ly = nx,ny 
                no_upd = 0
                if u=='<' or u=='>':
                    while s[lx][ly]=='[' or s[lx][ly]==']': ly+=Y[D]
                    if s[lx][ly]!='#':
                        while ly!=y: 
                            s[lx][ly],s[lx][ly-Y[D]]=s[lx][ly-Y[D]],s[lx][ly]
                            ly-=Y[D]
                        x, y = nx, ny
                    else: no_upd = 1
                else:
                    bad = 0
                    Q,v = [],[]
                    Q.append((x,y))
                    vis = [[0 for j in range(m)] for i in range(n)]
                    while len(Q)>0:
                        i,j = Q.pop(0)
                        if vis[i][j]: continue 
                        v.append((i,j)); vis[i][j]=1
                        ni = i+X[D]
                        if s[ni][j]=='#': bad=1
                        elif s[ni][j]!='.': Q.append((ni,j))
                        if s[ni][j-1]=='[': Q.append((ni,j-1))
                        if s[ni][j+1]==']': Q.append((ni,j+1))

                    for i,j in v: vis[i][j]=0
                    if not bad:
                        v.sort()
                        if u=='v': v.reverse()
                        for i,j in v: s[i][j],s[i+X[D]][j]=s[i+X[D]][j],s[i][j]
                        x, y = nx, ny
                    else: no_upd = 1
            
                if no_upd:col=RED
                else:col=YELLOW
                cur.become(Text(f"{u}",color=col).move_to(RIGHT*6).scale(3))
                update_grid(grid,s);self.wait(RUNTIME)
            self.remove(cur)
            
            self.play(Write(self.counter[0]),run_time=0.25)
            for i in range(n):
                for j in range(m):
                    if s[i][j]=='[':
                        self.play(grid[i][j][0].animate.set_color(GREEN),run_time=0.25)
                        sum = MathTex(f"+ {i}*100+{j}={i*100+j}").move_to(self.counter[0].get_right()+RIGHT*2.5)
                        self.play(Write(sum),run_time=0.25)
                        self.cnt[0]+=i*100+j
                        self.play(self.counter_tracker[0].animate.set_value(self.cnt[0]),Unwrite(sum),run_time=0.25)
            
            self.wait();self.clear();self.wait(0.5)


        grid = ['########', 
                '#..O.O.#', 
                '##@.O..#', 
                '#...O..#', 
                '#.#.O..#', 
                '#...O..#', 
                '#......#', 
                '########']
        
        moves = "<^^>>>vv<v>>v<<"

        grid2 = ['##########', 
                '#..O..O.O#', 
                '#......O.#', 
                '#.OO..O.O#', 
                '#..O@..O.#', 
                '#O#..O...#', 
                '#O..O..O.#', 
                '#.OO.O.OO#', 
                '#....O...#', 
                '##########']
        
        moves2 = "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"

        part_one_solver(grid,moves)
        part_one_solver(grid2,moves2,True)
        part_two_solver(grid,moves)     
        part_two_solver(grid2,moves2,True)
        self.wait(0.5)
