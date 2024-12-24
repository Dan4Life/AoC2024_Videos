from manim import *

#manim -pqh --resolution 1920,1080 --disable_caching scene.py

class Day21(Scene):
    def createGridVGroup(self, s, sideLength, fontSize, Color=WHITE):
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

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []

        def clearCounters():
            self.counter, self.counter_tracker, self.cnt = [], [], []

        def addCounter(text, pos):
            self.cnt.append(0)
            self.counter.append(Variable(self.cnt[-1], text, num_decimal_places=0))
            self.counter[-1].label.scale(0.6)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*3.6)
            self.counter[-1].move_to(pos)
            self.counter_tracker.append(self.counter[-1].tracker)

        self.answer = 0
        def solver(output, instructions):
            RUN_TIME=0.22
            clearCounters()
            numeric_layout = [
                ["7", "8", "9"],
                ["4", "5", "6"],
                ["1", "2", "3"],
                ["", "0", "A"]
            ]
            directional_layout = [
                ["", "^", "A"],
                ["<", "v", ">"]
            ]

            X = [0,-1,0,1]
            Y = [-1,0,1,0]
            expected_output_text = Text(f"Expected Output: {output}",color=GREEN).move_to(UP*3+LEFT*3).scale(0.6)
            output_text = Text("Output: ",color=GREEN).move_to(UP*2.3+LEFT*4.5).scale(0.6)
            addCounter(Text("Count", color=GREEN), DOWN*1.5+LEFT*4.3)
            answer_text = Text(f"Answer = {self.answer}", color=GREEN).move_to(DOWN*2.5+LEFT*4).scale(0.6)

            directional_keypad_1 = self.createGridVGroup(directional_layout, sideLength=0.8, fontSize=40,Color=YELLOW).to_edge(LEFT)
            directional_keypad_2 = self.createGridVGroup(directional_layout, sideLength=0.8, fontSize=40,Color=BLUE).next_to(directional_keypad_1, RIGHT, buff=1)
            directional_keypad_3 = self.createGridVGroup(directional_layout, sideLength=0.8, fontSize=40,Color=RED).next_to(directional_keypad_2, RIGHT, buff=1)
            numeric_keypad = self.createGridVGroup(numeric_layout, sideLength=1, fontSize=45,Color=GREEN).to_corner(RIGHT)
            
            directional_label_1 = Text("Directional Keypad 1",color=YELLOW).next_to(directional_keypad_1, UP).scale(0.3)
            directional_label_2 = Text("Directional Keypad 2",color=BLUE).next_to(directional_keypad_2, UP).scale(0.3)
            directional_label_3 = Text("Directional Keypad 3",color=RED).next_to(directional_keypad_3, UP).scale(0.3)
            numeric_label = Text("Numeric Keypad",color=GREEN).next_to(numeric_keypad, UP).scale(0.4)
            
            arrow_1 = Arrow(directional_keypad_1.get_right(), directional_keypad_2.get_left(),buff=0.2)
            arrow_2 = Arrow(directional_keypad_2.get_right(), directional_keypad_3.get_left(),buff=0.2)
            arrow_3 = Arrow(directional_keypad_3.get_right(), numeric_keypad.get_left(),buff=0.2)

            robot_1 = Circle(radius=0.3, color=YELLOW).move_to(directional_keypad_1[0][2][0].get_center())
            robot_2 = Circle(radius=0.3, color=BLUE).move_to(directional_keypad_2[0][2][0].get_center())
            robot_3 = Circle(radius=0.3, color=RED).move_to(directional_keypad_3[0][2][0].get_center())
            robot_main = Circle(radius=0.35, color=GREEN).move_to(numeric_keypad[3][2][0].get_center())

            self.play(Create(numeric_keypad), Create(directional_keypad_1), Create(directional_keypad_2), Create(directional_keypad_3),run_time=RUN_TIME)
            self.play(Write(numeric_label), Write(directional_label_1), Write(directional_label_2), Write(directional_label_3), run_time=RUN_TIME)
            self.play(Create(arrow_1), Create(arrow_2), Create(arrow_3), run_time=RUN_TIME)
            self.play(Create(robot_2), Create(robot_3), Create(robot_main), run_time=RUN_TIME)
            self.play(Write(expected_output_text), Write(output_text), Write(self.counter[0]), run_time=RUN_TIME)
            self.add(answer_text)
            
            i2,j2,i3,j3,i4,j4 = 0,2,0,2,3,2
            cur_output = ""
            for c in instructions:
                if c=='<': 
                    i1,j1 = 1,0
                    i2+=X[0]
                    j2+=Y[0]
                elif c=='^':
                    i1,j1 = 0,1
                    i2+=X[1]
                    j2+=Y[1]
                elif c=='>':
                    i1,j1 = 1,2
                    i2+=X[2]
                    j2+=Y[2]
                elif c=='v':
                    i1,j1 = 1,1
                    i2+=X[3]
                    j2+=Y[3]
                else: 
                    i1,j1 = 0,2
                
                xd = 0
                self.remove(robot_1)
                robot_1.move_to(directional_keypad_1[i1][j1][0].get_center())
                self.add(robot_1)
                self.play(directional_keypad_1[i1][j1][0].animate.set_fill(color=YELLOW,opacity=0.75),rate_func=there_and_back,run_time=RUN_TIME)
                self.cnt[0]+=1
                self.play(self.counter_tracker[0].animate.set_value(self.cnt[0]),run_time=RUN_TIME)
                if c!='A':
                    self.play(robot_2.animate.move_to(directional_keypad_2[i2][j2][0].get_center()),run_time=RUN_TIME)
                else:
                    self.play(directional_keypad_2[i2][j2][0].animate.set_fill(color=directional_keypad_2.get_color(),opacity=0.75),rate_func=there_and_back,run_time=RUN_TIME)
                    c = directional_layout[i2][j2]
                    if c=='<': 
                        i3+=X[0]
                        j3+=Y[0]
                    elif c=='^':
                        i3+=X[1]
                        j3+=Y[1]
                    elif c=='>':
                        i3+=X[2]
                        j3+=Y[2]
                    elif c=='v':
                        i3+=X[3]
                        j3+=Y[3]
                        
                    if c!='A':
                        self.play(robot_3.animate.move_to(directional_keypad_3[i3][j3][0].get_center()),run_time=RUN_TIME)
                    else:
                        self.play(directional_keypad_3[i3][j3][0].animate.set_fill(color=directional_keypad_3.get_color(),opacity=0.75),rate_func=there_and_back,run_time=RUN_TIME)
                        c = directional_layout[i3][j3]
                        if c=='<': 
                            i4+=X[0]
                            j4+=Y[0]
                        elif c=='^':
                            i4+=X[1]
                            j4+=Y[1]
                        elif c=='>':
                            i4+=X[2]
                            j4+=Y[2]
                        elif c=='v':
                            i4+=X[3]
                            j4+=Y[3]
                        if c!='A':
                            self.play(robot_main.animate.move_to(numeric_keypad[i4][j4][0].get_center()),run_time=RUN_TIME)
                        else:
                            xd+=1
                            cur_output+=numeric_layout[i4][j4]
                            self.play(numeric_keypad[i4][j4][0].animate.set_fill(color=numeric_keypad.get_color(),opacity=0.75),rate_func=there_and_back,run_time=RUN_TIME)
                            output_text.become(Text(f"Output: {cur_output}",color=GREEN).move_to(UP*2.3+LEFT*4.5+0.2*RIGHT*xd).scale(0.6))
                
                             
            
            mult_text = MathTex(f" * {int(output[:-1])} = {self.cnt[0]*int(output[:-1])}").next_to(self.counter[0],RIGHT*0.6)
            self.play(Write(mult_text),run_time=RUN_TIME)
            self.answer+=self.cnt[0]*int(output[:-1])    
            answer_text.become(Text(f"Answer = {self.answer}", color=GREEN).move_to(DOWN*2.5+LEFT*4).scale(0.6))
            self.wait();self.clear();self.add(answer_text);self.wait(0.5);return
        
        test_cases = [
            ("029A", "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"),
            ("980A", "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A"),
            ("179A", "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"),
            ("456A", "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"),
            ("379A", "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")
        ]
        for a,b in test_cases: solver(a,b)
        self.wait(0.5)
