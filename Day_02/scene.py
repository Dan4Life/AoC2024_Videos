from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day2

class Day2(Scene):
    def construct(self):
        a = [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1], [1, 3, 2, 4, 5], [8, 6, 4, 4, 1], [1, 3, 6, 7, 9]]

        cnt, counter_tracker = 0, 0
        counter = Variable(cnt,Text("Count"), num_decimal_places=0)
        counter.label.scale(0.5)
        counter.value.next_to(counter.label.get_center(),RIGHT*3.3)

        counter.move_to(UP*3.5)
        counter_tracker = counter.tracker

        self.play(Write(counter))
        self.wait()
        
        for cur,curA in enumerate(a):
            
            n = len(curA)

            v = VGroup(*[Square(side_length=0.5, color=WHITE).add(Text(str(x), font_size=16)) for x in curA])
            v.arrange(RIGHT, buff=0.2).move_to(UP*(2-cur))
            
            self.play(FadeIn(v))

            pointer = Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.1).flip(LEFT)
            pointer.next_to(v[0], UP).move_to(v[0].get_top()+UP*0.2)
            self.play(FadeIn(pointer))

            incr = 0
            decr = 0

            number = DecimalNumber(0,num_decimal_places=0)
            number.scale(0.5)
            number.move_to((v[0].get_top()+v[1].get_top())/2+UP*0.2)
            bad = 0
            for i in range(1,n):
                curDif = curA[i]-curA[i-1]
                if i == 1:
                    number.set_value(curDif)
                newPos = (v[i-1].get_top()+v[i].get_top())/2

                if incr and curDif<0:
                    bad = 1
                elif decr and curDif>0:
                    bad = 1
                elif abs(curDif)<1 or abs(curDif)>3:
                    bad = 1

                if curDif>0:
                    incr=1
                    number.set_color(GREEN)
                elif curDif<0:
                    decr=1
                    number.set_color(RED)
                
                self.play(pointer.animate.set_x(v[i].get_center()[0]))
                self.play(
                    number.animate.set_value(curDif).move_to(newPos+UP*0.2),
                    UpdateFromFunc(number, lambda m: m.set_value(number.get_value()))
                )
                if bad:
                    self.play(pointer.animate.set_color(RED))
                    break
            if not bad:
                self.play(pointer.animate.set_color(GREEN))
                self.play(counter_tracker.animate.increment_value(1))
            self.wait(0.5)
        self.wait()
