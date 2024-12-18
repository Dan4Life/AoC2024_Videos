from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day6

class Day6(Scene):
    def construct(self):
        X = [-1,0,1,0]
        Y = [0,1,0,-1]
        player = ['^', '>', 'v', '<']
        n = 10
        di, ok = 0, 1
        s = [['.', '.', '.', '.', '#', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '#'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '#', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '#', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '#', '.', '.', '^', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'], 
             ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
             ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.']]
        for i in range(len(s)):
            for j in range(len(s[0])):
                if s[i][j] == '.':
                    s[i][j] = ' '
        x,y = 6,4
        m = len(s[0])

        cnt, counter_tracker = 1, 1
        counter = Variable(cnt,Text("Count"), num_decimal_places=0)
        counter.label.scale(0.5)
        counter.value.next_to(counter.label.get_center(),RIGHT*3.3)

        counter.move_to(UP*3.5)
        counter_tracker = counter.tracker

        grid = VGroup()
        for row in s:
            w = VGroup(*[Square(side_length=0.65, color=WHITE, fill_color=ORANGE, fill_opacity=0.05).add(Text(str(c))) for c in row])
            w.arrange(RIGHT, buff=0.0).center()
            grid.add(w)

        grid.arrange(DOWN, aligned_edge=LEFT, buff=0.0)
        vis = [[0 for j in range(m)] for i in range(n)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j].submobjects[0].text=='#':
                    grid[i][j].submobjects[0].color = RED
                elif grid[i][j].submobjects[0].text=='.':
                    grid[i][j].submobjects[0].color = GREEN
                elif grid[i][j].submobjects[0].text!=' ':
                    grid[i][j].submobjects[0].color = BLUE

        self.play(Write(grid))
        self.wait()
        self.play(Write(counter))
        self.wait()

        def update_cell(i, j, symbol, col):
            cell = grid[i][j]
            new_text = Text(symbol, color=col).move_to(grid[i][j].get_center())
            cell.submobjects[0] = new_text

        vis[x][y] = 1
        while True:
            nx = x+X[di]
            ny = y+Y[di]

            if nx<0 or nx>=n or ny<0 or ny>=m:
                update_cell(x, y, '.', GREEN)
                break
            
            if s[nx][ny] == '#':
                di = (di + 1) % 4
                update_cell(x, y, player[di], BLUE)
            else:
                oldX, oldY, oldZ = grid[x][y].get_center()
                placeHolder = Text('.',color=GREEN).move_to(grid[x][y].get_center())
                self.add(placeHolder)

                self.remove(grid[x][y])
                self.play(grid[x][y].submobjects[0].animate.move_to(grid[nx][ny].get_center()))
                self.add(grid[x][y])
                grid[nx][ny].submobjects[0] = grid[x][y].submobjects[0].copy()
                grid[x][y].submobjects[0].text = ' '
                grid[x][y].submobjects[0].move_to([oldX, oldY, oldZ])
                update_cell(x, y, '.', GREEN)
                self.remove(placeHolder)
                x, y = nx, ny
                if not vis[x][y]:
                    vis[x][y] = 1
                    self.play(counter_tracker.animate.increment_value(1))
        self.wait()
