from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day3

class Day3(Scene):
    def construct(self):
        s = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
        s2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        n, m = len(s), len(s2)

        counter, counter_tracker, cnt = [], [], [0,0]
        counter.append(Variable(cnt[0],Text("Sum",color=GREEN), num_decimal_places=0))
        counter.append(Variable(cnt[1],Text("Sum2",color=RED), num_decimal_places=0))
        
        enabledText = Text("Enabled", color=GREEN).move_to(UP*3).scale(0.5)
        disabledText = Text("Disabled", color=RED).move_to(UP*3).scale(0.5)
        
        for i in range(2):
            counter[i].label.scale(0.6)
            counter[i].value.next_to(counter[i].label.get_center(),RIGHT*3.6)

        counter[0].move_to(UP*3+LEFT*3)
        counter[1].move_to(UP*3+RIGHT*3)

        for i in range(2):
            self.play(Write(counter[i]))
            counter_tracker.append(counter[i].tracker)
        
        v = VGroup(*[Text(str(x), font_size=30, color=WHITE, font="Courier New") for x in s])
        w = VGroup(*[Text(str(x), font_size=30, color=WHITE, font="Courier New") for x in s2])
       
        v.arrange(RIGHT, buff=0.1).move_to(RIGHT*3+UP)
        bottom = v.get_y()-0.5
        self.play(Write(v))

        w.arrange(RIGHT, buff=0.1).move_to(RIGHT*3+DOWN)
        bottom2 = w.get_y()-0.5
        self.play(Write(w))

        pointer = Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.1)
        pointer.next_to(v[0], DOWN).set_y(bottom)
        self.play(FadeIn(pointer))

        i = 0
        while i < n-3:

            width = v[i+1].get_x()-v[i].get_x()
            oldi = i
            sz, bad = 0, 0

            if i+4<=n and s[i:i + 4] == "mul(":
                i += 4
                sz+=4
                x, y, ok = 0, 0, 0

                while i < n and s[i].isdigit():
                    x = x * 10 + int(s[i])
                    i += 1
                    sz+=1
                    ok = 1

                if i < n and ok and s[i] == ',':
                    i += 1
                    sz+=1
                    ok = 0
                    xd=i
                    
                    while i < n and s[i].isdigit():
                        y = y * 10 + int(s[i])
                        i += 1
                        sz+=1
                        ok = 1

                    if i < n and ok and s[i] == ')':
                        i += 1
                        sz+=1

                        for j in range(oldi, i):
                            self.play(v[j].animate.set_color(YELLOW),run_time=0.1)

                        self.play(pointer.animate.set_x(v[i-1].get_center()[0]), rate_func=there_and_back_with_pause)

                        number1 = DecimalNumber(x,num_decimal_places=0).scale(0.5)
                        number1.move_to(v[oldi+4].get_top()+UP*0.2)

                        number2 = DecimalNumber(y,num_decimal_places=0).scale(0.5)
                        number2.move_to(v[xd].get_top()+UP*0.2)

                        average_x = (number1.get_center()[0]+number2.get_center()[0])/2

                        self.play(
                            number1.animate.set_value(x * y).move_to([average_x, number1.get_y() + 0.2, 0]),
                            number2.animate.set_value(x * y).move_to([average_x, number1.get_y() + 0.2, 0]),
                            UpdateFromFunc(number1, lambda m: m.set_value(number1.get_value())),
                            UpdateFromFunc(number2, lambda m: m.set_value(number2.get_value()))
                        )
                        self.wait()
                        self.remove(number1, number2)


                        cnt[0] += x * y
                        self.play(counter_tracker[0].animate.set_value(cnt[0]))
                        self.wait()
                        self.play(v.animate.shift(LEFT*(v[i].get_x()-v[oldi].get_x())), run_time=0.7)
                    else:
                        bad = 1
                else:
                    bad = 1
            else:
                bad = 1

            if bad:
                i = oldi+1
                self.play(v.animate.shift(LEFT * width),run_time=0.7)
        
        self.play(v.animate.shift(LEFT), run_time=0.7)
        counter[0].value.set_color(GREEN)
        self.play(pointer.animate.next_to(w[0], DOWN).set_y(bottom2))

        i = 0
        enabled = 1

        disabledText.set_opacity(0)
        self.play(Write(enabledText), Write(disabledText))
        self.play(pointer.animate.set_color(GREEN))

        while i < m-3:

            width = w[i+1].get_x()-w[i].get_x()
            oldi = i
            sz, bad = 0, 0

            if i+4<=m and s2[i:i+4] == "do()":
                i+=4
                for j in range(oldi, i):
                    self.play(w[j].animate.set_color(GREEN),run_time=0.1)

                self.play(pointer.animate.set_x(w[i-1].get_center()[0]), rate_func=there_and_back_with_pause)

                if not enabled:
                    self.play(enabledText.animate.set_opacity(1), disabledText.animate.set_opacity(0))
                    self.play(pointer.animate.set_color(GREEN))
                enabled = 1

                self.wait()
                self.play(w.animate.shift(LEFT*(w[i].get_x()-w[oldi].get_x())), run_time=0.7)
            elif i+7<=m and s2[i:i+7] == "don't()":
                i+=7
                for j in range(oldi, i):
                    self.play(w[j].animate.set_color(RED),run_time=0.1)

                self.play(pointer.animate.set_x(w[i-1].get_center()[0]), rate_func=there_and_back_with_pause)

                if enabled:
                    self.play(enabledText.animate.set_opacity(0), disabledText.animate.set_opacity(1))
                    self.play(pointer.animate.set_color(RED))
                enabled = 0

                self.wait()
                self.play(w.animate.shift(LEFT*(w[i].get_x()-w[oldi].get_x())), run_time=0.7)
            elif i+4<=m and enabled and s2[i:i + 4] == "mul(":
                i += 4
                sz+=4
                x, y, ok = 0, 0, 0

                while i < m and s2[i].isdigit():
                    x = x * 10 + int(s2[i])
                    i += 1
                    sz+=1
                    ok = 1

                if i < m and ok and s2[i] == ',':
                    i += 1
                    sz+=1
                    ok = 0
                    xd = i
                    
                    while i < m and s2[i].isdigit():
                        y = y * 10 + int(s2[i])
                        i += 1
                        sz+=1
                        ok = 1

                    if i < m and ok and s2[i] == ')':
                        i += 1
                        sz+=1

                        for j in range(oldi, i):
                            self.play(w[j].animate.set_color(YELLOW),run_time=0.1)

                        self.play(pointer.animate.set_x(w[i-1].get_center()[0]), rate_func=there_and_back_with_pause)

                        number1 = DecimalNumber(x,num_decimal_places=0).scale(0.5)
                        number1.move_to(w[oldi+4].get_top()+UP*0.2)

                        number2 = DecimalNumber(y,num_decimal_places=0).scale(0.5)
                        number2.move_to(w[xd].get_top()+UP*0.2)

                        average_x = (number1.get_center()[0]+number2.get_center()[0])/2

                        self.play(
                            number1.animate.set_value(x * y).move_to([average_x, number1.get_y() + 0.2, 0]),
                            number2.animate.set_value(x * y).move_to([average_x, number1.get_y() + 0.2, 0]),
                            UpdateFromFunc(number1, lambda m: m.set_value(number1.get_value())),
                            UpdateFromFunc(number2, lambda m: m.set_value(number2.get_value()))
                        )
                        self.wait()
                        self.remove(number1, number2)


                        cnt[1] += x * y
                        self.play(counter_tracker[1].animate.set_value(cnt[1]))

                        self.wait()
                        self.play(w.animate.shift(LEFT*(w[i].get_x()-w[oldi].get_x())), run_time=0.7)
                    else:
                        bad = 1
                else:
                    bad = 1
            else:
                bad = 1

            if bad:
                i = oldi+1
                self.play(w.animate.shift(LEFT * width),run_time=0.7)
        self.play(w.animate.shift(LEFT), run_time=0.7)
        counter[1].value.set_color(RED)
        self.play(FadeOut(pointer))
        self.wait()
