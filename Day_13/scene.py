from manim import *
from math import gcd
# manim -pqh --resolution 1920,1080 scene.py Day13

class Day13(Scene):
    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []
        def addCounter(text, pos):
            self.cnt.append(0)
            self.counter.append(Variable(self.cnt[-1], text, num_decimal_places=0))
            self.counter[-1].label.scale(0.6)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*3.6)
            self.counter[-1].move_to(pos)
            self.counter_tracker.append(self.counter[-1].tracker)

        arr = [[94, 34, 22, 67, 8400, 5400], 
               [26, 66, 67, 21, 12748, 12176], 
               [17, 86, 84, 37, 7870, 6450], 
               [69, 23, 27, 71, 18641, 10279]]

        addCounter(Text("usedA", color=RED), DOWN*0.5+LEFT*6)
        addCounter(Text("usedB", color=BLUE), DOWN*1+LEFT*6)
        addCounter(Text("X", color=YELLOW), DOWN*1.5+LEFT*6)
        addCounter(Text("Y", color=YELLOW), DOWN*2+LEFT*6)
        addCounter(Text("Ans", color=GREEN), DOWN*2.5+LEFT*6)
        for i in [0,1]: self.counter[i].scale(0.7).move_to(self.counter[i].get_center()+LEFT*0.1)
        for i in [-1,-2,-3]:
            self.counter[i].value.next_to(self.counter[i].label.get_center(),RIGHT*2)
            self.counter[i].scale(0.7).move_to(self.counter[i].get_center()+LEFT*0.2)
        self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*2.5)
        
        plane = NumberPlane(
            x_range=[0, 8500, 500],
            y_range=[0, 6500, 500],
            x_length=11, y_length=7,
            background_line_style={"stroke_opacity": 0.5, "stroke_width": 2, "stroke_color": TEAL}
        ).move_to(RIGHT)
        plane.add_coordinates()

        for label in plane.x_axis.numbers:
            label.scale(0.8)
            label.move_to(plane.x_axis.number_to_point(label.get_value()) + DOWN * 0.2)

        for label in plane.y_axis.numbers:
            label.scale(0.8)
            label.move_to(plane.y_axis.number_to_point(label.get_value()) + LEFT * 0.25)

        self.play(Write(self.counter[-1]), run_time=0.5)
        def simulate(a0,a1,a2,a3,a4,a5):
            A0,A1,A2,A3,A4,A5 = a0,a1,a2,a3,a4,a5
            button_a = Circle(color=RED,stroke_width=5).shift(UP*3 + LEFT * 6).scale(0.3)
            button_b = Circle(color=BLUE,stroke_width=5).shift(UP*1.5 + LEFT * 6).scale(0.3)
            label_a = MathTex("A").move_to(button_a.get_center())
            label_b = MathTex("B").move_to(button_b.get_center())
            info_ax = MathTex(f"X \gets X+{A0}").move_to(button_a.get_bottom()+DOWN*0.3+UP*0.1).scale(0.5)
            info_ay = MathTex(f"Y \gets Y+{A1}").move_to(button_a.get_bottom()+DOWN*0.3+DOWN*0.3+UP*0.1).scale(0.5)
            info_bx = MathTex(f"X \gets X+{A2}").move_to(button_b.get_bottom()+DOWN*0.3+UP*0.1).scale(0.5)
            info_by = MathTex(f"Y \gets Y+{A3}").move_to(button_b.get_bottom()+DOWN*0.3+DOWN*0.3+UP*0.1).scale(0.5)
            dest_x = MathTex(f"Dest_X: {A4}",color=GREEN).move_to(button_b.get_bottom()+DOWN*0.3*3.5+UP*0.1+LEFT*0.05).scale(0.5)
            dest_y = MathTex(f"Dest_Y: {A5}",color=GREEN).move_to(button_b.get_bottom()+DOWN*0.3*4.5+UP*0.1+LEFT*0.05).scale(0.5)

            A = VGroup(button_a, label_a, info_ax, info_ay)
            B = VGroup(button_b, label_b, info_bx, info_by)
            boxA = SurroundingRectangle(A, color=RED)
            boxB = SurroundingRectangle(B, color=BLUE)

            start_dot = Dot(plane.c2p(0, 0), color=YELLOW).scale(0.9)
            start_label = MathTex("(0, 0)").move_to(start_dot.get_center()+UP*0.15).scale(0.45)
            end_dot = Dot(plane.c2p(A4, A5), color=GREEN).scale(0.9)
            end_label = MathTex(f"({A4}, {A5})").move_to(end_dot.get_center()+UP*0.15).scale(0.45)

            def update_label_content(lbl):
                coord = plane.p2c(start_dot.get_center())
                lbl.become(MathTex(f"({int(coord[0]+0.001)}, {int(coord[1]+0.001)})")
                           .scale(0.45).move_to(start_dot.get_center() + UP * 0.15))

            start_label.add_updater(update_label_content)

            self.play(FadeIn(boxA, A, boxB,B, dest_x, dest_y),
                    Write(self.counter[0]), Write(self.counter[1]), Write(self.counter[2]), Write(self.counter[3]), run_time=0.5
            )

            xd = a0*a1/gcd(a0,a1)
            mul1 = xd/a0; mul2 = xd/a1
            a0*=mul1; a2*=mul1; a4*=mul1
            a1*=mul2; a3*=mul2; a5*=mul2

            bad = 0
            if a3==a2 or (a5-a4) % (a3-a2):
                bad = 1 
            else:
                j = (a5-a4) // (a3-a2)
                i = a4-j*a2 
                if a0==0 or i%a0: bad = 1
                elif i < 0 or j < 0: bad = 1
                else: i//=a0
            
            self.play(FadeIn(plane, start_dot, start_label, end_dot, end_label), run_time=0.5)
            if bad==1:
                impossible = MathTex("IMPOSSIBLE",color=RED).move_to(RIGHT).scale(3)
                self.play(Write(impossible),run_time=0.5)
            else:
                
                x1,y1 = 0,0
                
                while i>0:
                    i-=1
                    x1+=A0
                    y1+=A1
                    new_dot_a = Dot(plane.c2p(x1, y1), color=YELLOW)
                    path_a = Line(start_dot.get_center(), new_dot_a.get_center(), color=RED)
                    self.cnt[-3],self.cnt[-2]=x1,y1
                    self.cnt[0]+=1
                    self.play(FadeIn(path_a), MoveAlongPath(start_dot, path_a),
                              self.counter_tracker[-3].animate.set_value(self.cnt[-3]),
                              self.counter_tracker[-2].animate.set_value(self.cnt[-2]),
                              self.counter_tracker[0].animate.set_value(self.cnt[0]),
                               run_time = 0.1)
                self.wait(0.5)
                
                while j>0:
                    j-=1
                    x1+=A2
                    y1+=A3
                    new_dot_b = Dot(plane.c2p(x1, y1), color=YELLOW)
                    path_b = Line(start_dot.get_center(), new_dot_b.get_center(), color=BLUE)
                    self.cnt[-3],self.cnt[-2]=x1,y1
                    self.cnt[1]+=1
                    self.play(FadeIn(path_b), MoveAlongPath(start_dot, path_b),
                              self.counter_tracker[-3].animate.set_value(self.cnt[-3]),
                              self.counter_tracker[-2].animate.set_value(self.cnt[-2]),
                              self.counter_tracker[1].animate.set_value(self.cnt[1]),
                               run_time = 0.1)
            
                show = MathTex(f"{self.cnt[0]}*3+{self.cnt[1]}={self.cnt[0]*3+self.cnt[1]}")\
                .move_to(self.counter[-1].get_bottom()+DOWN*0.3+RIGHT*0.2).scale(0.5)
                self.cnt[-1]+=self.cnt[0]*3+self.cnt[1]
                self.play(FadeIn(show), self.counter_tracker[-1].animate.set_value(self.cnt[-1]), run_time=0.5)

            self.wait(); self.clear(); 
            self.add(self.counter[-1])
            self.wait(0.5)
            for j in range(len(self.cnt)-1): 
                self.cnt[j]=0
                self.counter_tracker[j].set_value(self.cnt[j])

        for lis in arr: simulate(*lis)
        self.wait()
