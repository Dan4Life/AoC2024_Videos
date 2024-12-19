from manim import *
# manim -pql --resolution 1920,1080 scene.py Day7

class Day7(Scene):
    def construct(self):
        Y = [190, 3267, 83, 156, 7290, 161011, 192, 21037, 292]
        A = [[10, 19], [81, 40, 27], [17, 5], [15, 6], [6, 8, 6, 15], [16, 10, 13], [17, 8, 14], [9, 7, 18, 13], [11, 6, 16, 20]]
        
        counter, counter_tracker, cnt = [], [], [0,0]
        counter.append(Variable(cnt[0],Text("Sum",color=GREEN), num_decimal_places=0))
        counter.append(Variable(cnt[1],Text("Sum2",color=RED), num_decimal_places=0))
        
        for i in range(2):
            counter[i].label.scale(0.6)
            counter[i].value.next_to(counter[i].label.get_center(),RIGHT*3.6)

        counter[0].move_to(UP*3+LEFT*3)
        counter[1].move_to(UP*3+RIGHT*3)

        for i in range(2):
            self.play(Write(counter[i]))
            counter_tracker.append(counter[i].tracker)

        self.wait()
        op = ["+", "*", "||"]

        for ind,(y,a) in enumerate(zip(Y, A)):
            n = len(a)
            p = 3 ** (n - 1)
            num = -1
            actualUse = 0

            v = VGroup(*[Text(str(x), font_size=30, color=YELLOW) for x in a])
            v.add(Text('=', font_size=30, color=YELLOW))
            v.add(Text(str(y), font_size=30, color=YELLOW))
            v.arrange(RIGHT, buff=0.5).move_to(UP*0.75*(3-ind))

            self.play(FadeIn(v))

            for i in range(p):
                j = i
                cur = a[0]
                usedCat = 0
                for k in range(n-1):
                    if j % 3 == 0:
                        cur = cur+ a[k + 1]
                    elif j % 3 == 1:
                        cur = cur* a[k + 1]
                    else:
                        usedCat = 1
                        cur = int(str(cur) + str(a[k + 1]))
                    j //= 3
                    if cur > y: break

                if cur == y:
                    actualUse = usedCat
                    num = i
                    break

            if num==-1:
                self.play(v.animate.scale(1.1).set_color(RED))
            else:
                number = DecimalNumber(int(v[0].text),num_decimal_places=0)
                number.scale(0.5).move_to(v[0].get_top()+UP*0.2)

                operator = Text(' ', color = BLUE, font_size = 30)
                operator.scale(1.1)
                operator.move_to(v[0].get_center())

                self.add(operator, number)
                cur = a[0]
                for i in range(n-1):
                    xd = op[num%3]
                    if num%3==0: cur+=a[i+1]
                    elif num%3==1: cur*=a[i+1]
                    else: cur = int(str(cur) + str(a[i+1]))

                    pos = (v[i].get_right() + v[i+1].get_left()) / 2
                    newOperator = Text(xd,font_size=30, color=BLUE).scale(1.1).move_to(pos)
                    self.play(ReplacementTransform(operator,newOperator))
                    
                    self.play(
                        number.animate.set_value(cur).move_to(operator.get_top()+UP*0.2),
                        UpdateFromFunc(number, lambda m: m.set_value(number.get_value()))
                    )

                    num//=3

                self.play(Unwrite(number))

                if not actualUse:
                    cnt[0] += y
                    cnt[1] += y
                    self.play(counter_tracker[0].animate.set_value(cnt[0]),
                                counter_tracker[1].animate.set_value(cnt[1]))
                else:
                    cnt[1] += y
                    self.play(counter_tracker[1].animate.set_value(cnt[1]))

        counter[0].value.set_color(GREEN)
        counter[1].value.set_color(RED)
        self.wait(1)
