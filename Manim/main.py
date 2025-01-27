from manim import *

class ThalesTheoremImproved(Scene):
    def construct(self):
        circle = Circle(radius=3, color=BLUE)
        center = circle.get_center()
        A = Dot(circle.point_at_angle(0), color=RED)
        C = Dot(circle.point_at_angle(PI), color=RED)
        diameter = Line(A.get_center(), C.get_center(), color=RED)
        A_label = MathTex("A", color=RED).next_to(A, DOWN)
        C_label = MathTex("C", color=RED).next_to(C, DOWN)
        self.play(Create(circle), run_time=2)
        self.play(Create(diameter), Write(A_label), Write(C_label))
        self.wait(1)
        theta = ValueTracker(PI / 2)
        B = Dot(circle.point_at_angle(theta.get_value()), color=GREEN)
        B.add_updater(lambda m: m.move_to(circle.point_at_angle(theta.get_value())))
        B_label = always_redraw(lambda: MathTex("B", color=GREEN).next_to(B, UP))
        triangle = always_redraw(lambda: Polygon(A.get_center(), B.get_center(), C.get_center(), color=YELLOW, fill_opacity=0.3))
        # Corrected RightAngle lines to emanate from B
        right_angle = always_redraw(lambda: RightAngle(
            Line(B.get_center(), A.get_center()), 
            Line(B.get_center(), C.get_center()), 
            length=0.4, color=WHITE
        ))
        self.add(B, B_label, triangle, right_angle)
        self.play(Create(triangle), Write(B_label), Create(right_angle), run_time=2)
        self.wait(1)
        theorem_text = VGroup(
            Tex("Thales' Theorem:").scale(1.2), 
            Tex("If AC is a diameter of a circle,"), 
            Tex("then any triangle ABC with B on the circle,"), 
            Tex("has a right angle at B.")
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        self.play(Write(theorem_text), run_time=3)
        self.wait(2)
        angles = [PI / 2, PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 6, 5 * PI / 3]
        for angle in angles:
            self.play(theta.animate.set_value(angle), run_time=3)
            self.wait(1)
        self.play(FadeOut(theorem_text))
        proof_text = VGroup(
            Tex("Why does this work?", color=YELLOW).scale(1.1), 
            Tex("1. OA = OB = OC (radii)").scale(0.9), 
            Tex("2. Triangles OAB and OBC are isosceles").scale(0.9), 
            Tex("3. Angle sums = 180\u00b0 imply right angle at B").scale(0.9)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        self.play(Write(proof_text), run_time=3)
        self.wait(4)
        angles_smooth = [PI / 3, 2 * PI / 3, 4 * PI / 3, 5 * PI / 3]
        for angle in angles_smooth:
            self.play(theta.animate.set_value(angle), run_time=2)
        self.play(FadeOut(proof_text))
        conclusion = Tex("Thales' Theorem always holds for any point B on the circle!", color=GREEN).scale(1.1)
        self.play(Write(conclusion), run_time=3)
        self.wait(3)
        self.play(theta.animate.set_value(2 * PI), run_time=5)
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(circle), FadeOut(diameter), FadeOut(A), FadeOut(C), FadeOut(B), FadeOut(triangle), FadeOut(right_angle))
        self.wait(1)