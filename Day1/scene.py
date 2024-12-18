from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day1

class Day1(Scene):
    def construct(self):
        a = [3, 4, 2, 1, 3, 3]
        b = [4, 3, 5, 3, 9, 3]
        n = len(a)

        line = Line(4*DOWN, UP * 10)
        line.set_color(WHITE)

        self.play(FadeIn(line))
        self.wait()

        counter, counter_tracker, cnt = [], [], [0,0]
        counter.append(Variable(cnt[0],Text("Sum",color=GREEN), num_decimal_places=0))
        counter.append(Variable(cnt[1],Text("Sum",color=RED), num_decimal_places=0))

        for i in range(2):
            counter[i].label.scale(0.6)
            counter[i].value.next_to(counter[i].label.get_center(),RIGHT*3.6)

        counter[0].move_to(UP*3+LEFT*4)
        counter[1].move_to(UP*3+RIGHT*4)

        for i in range(2):
            counter_tracker.append(counter[i].tracker)

        self.wait()

        v1 = VGroup(*[Square(side_length=0.5, color=WHITE).add(Text(str(x), font_size=16)) for x in a])
        v1.arrange(DOWN, buff=0.2).move_to(LEFT*6)

        v2 = VGroup(*[Square(side_length=0.5, color=WHITE).add(Text(str(x), font_size=16)) for x in b])
        v2.arrange(DOWN, buff=0.2).move_to(LEFT*2)
        
        self.play(Create(v1), Create(v2))
        self.play(Write(counter[0]))
        self.wait()

        mapping = [0] * n
        c = sorted(range(n), key=lambda i: (a[i], i))
        d = sorted(range(n), key=lambda i: (b[i], i))
 
        for i in range(n):
            mapping[c[i]] = d[i]
        print(mapping)
        
        pointer = Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.1).rotate(-PI/2)
        pointer.next_to(v1[0], LEFT).move_to(v1[0].get_left()+LEFT*0.2)
        self.play(FadeIn(pointer))
        
        for i in range(n):
            self.play(pointer.animate.set_y(v1[i].get_center()[1]))
            line = Line(v1[i].get_right(), v2[mapping[i]].get_left(), buff=0.1)
            line.set_color(ORANGE)
            self.play(Create(line))
            weight = DecimalNumber(int(abs(b[mapping[i]]-a[i])), num_decimal_places=0)
            weight.next_to(line.get_center(), UP*0.3).set_color(YELLOW).scale(0.8)
            self.play(Write(weight))
            self.wait()
            self.play(FadeOut(weight))
            cnt[0]+=weight.get_value()
            self.play(counter_tracker[0].animate.set_value(cnt[0]))

        self.play(FadeOut(pointer))

        v3 = VGroup(*[Square(side_length=0.5, color=WHITE).add(Text(str(x), font_size=16)) for x in a])
        v3.arrange(DOWN, buff=0.2).move_to(RIGHT*2)

        v4 = VGroup(*[Square(side_length=0.5, color=WHITE).add(Text(str(x), font_size=16)) for x in b])
        v4.arrange(DOWN, buff=0.2).move_to(RIGHT*6)

        self.play(Create(v3), Create(v4))
        self.play(Write(counter[1]))
        self.wait()


        pointer.next_to(v3[0], LEFT).move_to(v3[0].get_left()+LEFT*0.2)
        self.play(FadeIn(pointer))
        
        for i in range(n):
            self.play(pointer.animate.set_y(v3[i].get_center()[1]))

            tot = 0
            v = []
            for j in range(n):
                if a[i]==b[j]:
                    tot+=1
                    v.append(j)

            Animations = []
            for j in v:
                Animations.append(v4[j].animate.set_color(YELLOW))
            if len(Animations):
                self.play(*Animations)

            weight = DecimalNumber(tot, num_decimal_places=0)
            weight.move_to((v3.get_center()+v4.get_center())/2).set_color(YELLOW)
            self.play(Write(weight))
            
            Animations = []

            for j in v:
                Animations.append(v4[j].animate.set_color(WHITE))
            if len(Animations):
                self.play(*Animations)

            self.play(FadeOut(weight))

            cnt[1]+=tot*a[i]
            self.play(counter_tracker[1].animate.set_value(cnt[1]))
        
        self.play(FadeOut(pointer))
