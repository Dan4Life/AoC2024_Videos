from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day5

class Day5(Scene):
    def construct(self):
        list1 = [[75, 47, 61, 53, 29], [97, 61, 53, 29, 13], [75, 29, 13], [75, 97, 47, 61, 53], [61, 13, 29], [97, 13, 75, 29, 47]]
        list2 = [[75, 47, 61, 53, 29], [97, 61, 53, 29, 13], [75, 29, 13], [97, 75, 47, 61, 53], [61, 29, 13], [97, 75, 47, 29, 13]]

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

        for cur, (init_list, trans_list) in enumerate(zip(list1, list2)):
            n = len(init_list)
            notSame = init_list!=trans_list

            mapping = [ ]
            vis = [0 for i in range(n)]
            for i in range(n):
                for j in range(n):
                    if vis[j] or init_list[i]!=trans_list[j]:
                        continue
                    mapping.append(j)
                    vis[j] = 1
                    break
            
            mid = -1
            for j in range(n):
                if(mapping[j]==n//2):
                    mid = j

            v = VGroup(*[Square(side_length=0.5, color=WHITE).add(Text(str(x), font_size=16)) for x in init_list])
            v.arrange(RIGHT, buff=0.2).move_to(UP*(2-cur))
            
            self.play(FadeIn(v))

            animations = [
                v[i].animate.move_to(v[j].get_center())
                for i, j in enumerate(mapping) if i!=j
            ]
            self.play(AnimationGroup(*animations, lag_ratio=0.0, run_time=1))

            if notSame:
                v[mid].set_color(RED)
            else:
                v[mid].set_color(GREEN)

            cnt[notSame] += trans_list[n//2]
            self.play(counter_tracker[notSame].animate.set_value(cnt[notSame]))

        counter[0].value.set_color(GREEN)
        counter[1].value.set_color(RED)
        self.wait(1)
