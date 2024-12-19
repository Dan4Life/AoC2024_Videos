from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day9

class Day9(Scene):
    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], [0,0]
        def addTwoCounters():
            self.counter.append(Variable(self.cnt[0],Text("Sum",color=GREEN), num_decimal_places=0))
            self.counter.append(Variable(self.cnt[1],Text("Sum2",color=RED), num_decimal_places=0))
            
            for i in range(2):
                self.counter[i].label.scale(0.6)
                self.counter[i].value.next_to(self.counter[i].label.get_center(),RIGHT*3.6)

            self.counter[0].move_to(UP*3+LEFT*3)
            self.counter[1].move_to(UP*3+RIGHT*3)

            for i in range(2):
                self.play(Write(self.counter[i]), run_time=0.5)
                self.counter_tracker.append(self.counter[i].tracker)

        def ArrayVGroup(s, sideLength, fontSize, Color=WHITE):
            newGrid = VGroup(
                *[
                    VGroup(
                        Square(
                            side_length=sideLength,
                            color=Color,
                            fill_color=ORANGE,
                            fill_opacity=0.05
                        ),
                        Text(str(c), font_size=fontSize, color=RED, fill_opacity=0) #notice i changed fill_opacity
                    ) for c in s
                ]
            )
            newGrid.arrange(RIGHT, buff=0.0).center()
            return newGrid

        def animateSwap(arrVG, i, j):
            self.play(
                arrVG[i][1].animate.set_opacity(0),
                arrVG[j][1].animate.set_opacity(0),
                run_time=0.5
            )

            arrVG[i][1] = Text(arrVG[j][1].text, font_size=18, color=YELLOW).move_to(arrVG[i].get_center())
            arrVG[j][1] = Text(' ')
            self.add(arrVG[i][1])
            self.play(
                arrVG[i][1].animate.set_opacity(1),
                arrVG[j][1].animate.set_opacity(1),
                run_time=0.5
            )

    
        def iterateThroughDisk(disk, DISK, t):
            bottom = DISK.get_y()-0.3
            pointer = Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.1)
            pointer.next_to(DISK[0], DOWN).set_y(bottom)
            self.play(Create(pointer), run_time=0.5)
            
            self.cnt[t] = 0
            for i,j in enumerate(disk):
                if j!=-1: 
                    self.play(pointer.animate.set_x(DISK[i].get_center()[0]), run_time = 0.5)

                    number1 = DecimalNumber(i,num_decimal_places=0).scale(0.5).move_to(DISK[i].get_top()+UP*0.2+LEFT*0.15)
                    number2 = DecimalNumber(j,num_decimal_places=0).scale(0.5).move_to(DISK[i].get_top()+UP*0.2+RIGHT*0.15)
                    operator = Text('*', color = BLUE, font_size = 16).move_to((number1.get_center()+number2.get_center())/2)

                    self.play(
                            number1.animate.set_value(i*j).move_to(operator.get_top()+UP*0.2),
                            number2.animate.set_value(i*j).move_to(operator.get_top()+UP*0.2),
                            Uncreate(operator),
                            UpdateFromFunc(number1, lambda m: m.set_value(number1.get_value())),
                            UpdateFromFunc(number2, lambda m: m.set_value(number2.get_value())),
                            run_time = 0.5
                    )
                    
                    self.cnt[t]+=i*j
                    self.play(self.counter_tracker[t].animate.set_value(self.cnt[t]), 
                            Uncreate(number1), Uncreate(number2), run_time = 0.5)
                    
            self.play(Uncreate(pointer), run_time=0.5)

        addTwoCounters()
        disk_map = "2333133121414131402"
        n = 0

        for c in disk_map: n+=int(c)

        isFile, ID = 1, -1
        disk, disk2 = [], []
        
        for i,c in enumerate(disk_map):
            ID+=isFile
            disk+=[ID if isFile else -1]*int(c)
            disk2+=[ID if isFile else -1]*int(c)            
            isFile^=1

        DISKMAP = VGroup(*[Text(str(x), font_size=30, color=WHITE, font="Courier New") for x in disk_map])
        DISKMAP.arrange(RIGHT, buff=0.1).move_to(2*UP)

        bottom = DISKMAP.get_y()-0.3

        pointer = Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.1)
        pointer.next_to(DISKMAP[0], DOWN).set_y(bottom)

        DISK = ArrayVGroup(disk,0.325,18)
        DISK2 = ArrayVGroup(disk2,0.325,18).move_to(DOWN*2)

        for i in range(len(disk)):
            if disk[i]==-1: DISK[i][1] = Text(' ')
        for i in range(len(disk2)):
            if disk2[i]==-1: DISK2[i][1] = Text(' ')

        self.play(Create(DISKMAP), Create(DISK), Create(DISK2), run_time=0.5)
        self.play(FadeIn(pointer), run_time=0.5)

        bottom = DISK.get_y()-0.3
        pointers = [Triangle(color=RED, fill_opacity=1, fill_color=RED).scale(0.1), 
                    Triangle(color=BLUE, fill_opacity=1, fill_color=BLUE).scale(0.1),
                    Triangle(color=RED, fill_opacity=1, fill_color=RED).scale(0.1).flip(LEFT),
                    Triangle(color=BLUE, fill_opacity=1, fill_color=BLUE).scale(0.1)]

        idx, isFile = 0, 1
        for i,c in enumerate(disk_map):
            self.play(pointer.animate.set_x(DISKMAP[i].get_center()[0]),
                      DISKMAP[i].animate.set_color(YELLOW),
                      run_time = 0.5)
            xd = int(c)
            animations = []

            if isFile:
                while xd:
                    animations.append(DISK[idx][1].animate.set_opacity(1.0))
                    animations.append(DISK2[idx][1].animate.set_opacity(1.0))
                    xd-=1; idx+=1
                if len(animations):
                    self.play(*animations, run_time=0.5)
            else:
                while xd:
                    animations.append(DISK[idx].animate.set_opacity(1.0))
                    animations.append(DISK2[idx].animate.set_opacity(1.0))
                    xd-=1; idx+=1
                if len(animations):
                    self.play(*animations, run_time=0.5, rate_func=there_and_back)
            
            self.play(DISKMAP[i].animate.set_color(WHITE), run_time=0.5)
            isFile^=1

        self.play(Uncreate(pointer),run_time=0.5)

        pointers = [Triangle(color=RED, fill_opacity=1, fill_color=RED).scale(0.1), 
                    Triangle(color=BLUE, fill_opacity=1, fill_color=BLUE).scale(0.1),
                    Triangle(color=RED, fill_opacity=1, fill_color=RED).scale(0.1).flip(LEFT),
                    Triangle(color=BLUE, fill_opacity=1, fill_color=BLUE).scale(0.1)]
        
        bottom = DISK.get_y()-0.3
        pointers[0].next_to(DISK[0], DOWN).set_y(bottom)
        pointers[1].next_to(DISK[n-1], DOWN).set_y(bottom)

        bottom = DISK2.get_y()-0.3
        pointers[2].next_to(DISK2[0], UP).move_to(DISK2[0].get_top()+0.2)
        pointers[3].next_to(DISK2[n-1], DOWN).set_y(bottom)

        self.play(Create(pointers[0]), Create(pointers[1]), run_time=0.5)
        L, R = 0, n-1

        while L<R:
            if disk[L]==-1 and disk[R]!=-1:
                disk[L], disk[R] = disk[R],disk[L]
                animateSwap(DISK, L,R)
                L+=1; R-=1
                self.play(pointers[0].animate.set_x(DISK[L].get_center()[0]),
                          pointers[1].animate.set_x(DISK[R].get_center()[0]),run_time = 0.5)
            elif disk[L]!=-1:
                L+=1
                self.play(pointers[0].animate.set_x(DISK[L].get_center()[0]), run_time = 0.5)

            elif disk[R]==-1:
                R-=1
                self.play(pointers[1].animate.set_x(DISK[R].get_center()[0]),run_time = 0.5)
        
        self.play(Uncreate(pointers[0]), Uncreate(pointers[1]),run_time=0.5)

        iterateThroughDisk(disk, DISK,0)

        self.play(Create(pointers[2]), Create(pointers[3]), run_time=0.5)
        k = n-1

        while k >= 0:
            if disk2[k]==-1:
                k-=1
                self.play(pointers[3].animate.set_x(DISK2[k].get_center()[0]),run_time = 0.5)
                continue 

            oldK = k
            dig = disk2[k]
            usedSpaces = 0
            while k>=0 and disk2[k]==dig:
                k-=1
                usedSpaces+=1

            i, ok = 0, 0
            while i <= k:
                if disk2[i] != -1:
                    i+=1
                    continue 
                spaces = 0
                st = i
                while i<=k and disk2[i]==-1:
                    i+=1
                    spaces+=1

                if spaces >= usedSpaces:
                    self.play(pointers[3].animate.set_x(DISK2[k+1].get_center()[0]),run_time = 1,rate_func=there_and_back)
                    k = oldK
                    self.play(pointers[2].animate.set_x(DISK2[st].get_center()[0]),
                              pointers[3].animate.set_x(DISK2[k].get_center()[0]),run_time = 0.5)
                    while usedSpaces:
                        disk2[st],disk2[k] = disk2[k],disk2[st]
                        animateSwap(DISK2, st, k)
                        st+=1; k-=1; usedSpaces-=1
                        self.play(pointers[2].animate.set_x(DISK2[st].get_center()[0]),
                                  pointers[3].animate.set_x(DISK2[k].get_center()[0]),
                                  DISK2[st-1][1].animate.set_color(YELLOW),
                                  DISK2[k+1][1].animate.set_color(YELLOW),
                                  run_time = 0.5)

                    ok = 1
                    break
            if not ok:
                self.play(pointers[3].animate.set_x(DISK2[k].get_center()[0]),run_time = 0.5)
        self.play(Uncreate(pointers[2]), Uncreate(pointers[3]),run_time=0.5)
            
        iterateThroughDisk(disk2, DISK2,1)
        self.wait()
