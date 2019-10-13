import pathlib

from manimlib.imports import *
from manimlib.animation.specialized import WHITE
from manimlib.utils.rate_functions import linear
import random
import os
from typing import List

DEBUG = False

seed = os.environ.get('SEED', None)
if seed is not None:
    print(f'Using seed: {seed}')
np.random.seed(int(seed) if seed else None)

X_MIN = -7
X_MAX = 8
Y_MIN = -4
Y_MAX = 5

STAR_RADIUS = 14
STAR_CENTER = np.random.normal(0, [3, 5, 0], 3)

TEXT_BOX_COLOR = '#111111'
TEXT_BOX_OPACITY = 1.0

OUTRO_TITLE = 'Outro'
BACKGROUND_TITLE = 'Background'

SVG = pathlib.Path('media')

LETTER_ORIGIN = {
    'f': ORIGIN + LEFT * .4,
    'd': ORIGIN + RIGHT * .25,
}


def random_point():
    x = random.uniform(X_MIN, X_MAX)
    y = random.uniform(Y_MIN, Y_MAX)

    return np.array((x, y, 0.))


def random_star_size():
    return np.random.normal(0.02, 0.005)


def get_star_count():
    return int(np.random.normal(240, 50))


def get_rocket_path(min_length=1, max_length=2.5):
    start = BOTTOM + 4 * DOWN + np.random.normal(0, [FRAME_X_RADIUS, 0, 0], 3)
    center = np.random.normal(0, [1, 1, 0], 3)
    end = start + (min_length + (max_length - min_length) * np.random.rand()) * (center - start)
    return Line(start, end, stroke_color='#00ffff', stroke_opacity=0.5)


class Rocket(SVGMobject):
    CONFIG = {
        'file_name': 'images/rocket.svg',
        'stroke_width': 0,
        'fill_color': '#ffffff',
        'fill_opacity': 1,
        'height': 0.5,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submobjects[3].set_fill('#000000', 1)


class Constellation(SVGMobject):
    CONFIG = {
        'file_name': 'images/constellation.svg',
        'stroke_width': 2,
        'fill_color': '#ffffff',
        'fill_opacity': 1,
        'height': 3,
    }


class License(SVGMobject):
    CONFIG = {
        'file_name': 'images/by-sa.svg',
        'stroke_width': 1,
        # 'fill_color': '#000000',
        'fill_opacity': 1,
        'height': 2.5,
    }


class TalkInfo(VMobject):
    def __init__(self, speaker, title):
        VMobject.__init__(self)

        session_title = TextMobject(title, height=0.4)
        session_title.shift(2 * DOWN)
        session_title.align_to(np.array((X_MAX - 2, 0, 0)), direction=RIGHT)
        session_title.add_background_rectangle(
            color=TEXT_BOX_COLOR,
            buff=0.15,
            opacity=TEXT_BOX_OPACITY,
        )
        self.session_title = session_title

        session_speaker = TextMobject(speaker, height=0.2)
        session_speaker.shift(3 * DOWN + np.array((0.0, 0.4, 0.0)))
        session_speaker.align_to(np.array((X_MAX - 2, 0, 0)), direction=RIGHT)
        session_speaker.shift(0.05 * LEFT)
        session_speaker.add_background_rectangle(
            color=TEXT_BOX_COLOR,
            buff=0.2,
            opacity=TEXT_BOX_OPACITY,
        )
        self.session_speaker = session_speaker


class Intro(Scene):
    CONFIG = {
        'camera_config': {
            'background_color': '#030303' if DEBUG else '#000000'
        }
    }

    def create_twinkle_animation(self, run_time: float) -> Animation:
        twinkle_overlay = ImageMobject('images/overlay-tiled.png')
        twinkle_overlay.scale(15)
        # self.add(twinkle_overlay)

        twinkle_down_line = Line(ORIGIN + UP * run_time / 10, ORIGIN, stroke_color='#00aa00', stroke_opacity=0.5)

        if DEBUG:
            self.add(twinkle_down_line)

        return MoveAlongPath(twinkle_overlay, twinkle_down_line, run_time=run_time, rate_func=linear)

    def create_circling_animations(self, star_count: int, run_time: float) -> List[Animation]:
        orbits = [
            Arc(
                radius=(i / star_count) * STAR_RADIUS,
                arc_center=STAR_CENTER,
                # only for debug relevant
                stroke_color='#aa0000',
                stroke_opacity=0.5,
                # Stars at the outside should make shorter distances than those in the middle
                angle=(TAU / (10 + (i / 10))) * np.random.rand() * run_time / 10,
                start_angle=TAU * np.random.rand(),
            )
            for i in range(star_count)
        ]

        if DEBUG:
            for orbit in orbits:
                # orbit.rotate(PI * np.random.uniform(0, 360))
                self.add(orbit)

        stars = [
            Dot(
                radius=random_star_size(),
                color=WHITE,
                fill=WHITE,
            )
            for _ in range(star_count)
        ]

        self.stars = stars

        return [
            MoveAlongPath(
                star,
                orbit,
                rate_func=linear,
                run_time=run_time,
            )
            for star, orbit in zip(stars, orbits)
        ]

    def create_rocket_with_path(self, **kwargs):
        rocket = Rocket(height=np.random.normal(3, 1))

        rocket_path = get_rocket_path(**kwargs)
        if DEBUG:
            self.add(rocket_path)

        rocket.rotate(rocket_path.get_angle() - PI / 2)

        return rocket, rocket_path

    def construct(self):
        talk_speaker = os.environ.get('TALK_SPEAKER', 'Frank Nord')
        talk_title = os.environ.get('TALK_TITLE', 'Debugging down in the deep web')
        is_outro = talk_speaker == talk_title == OUTRO_TITLE
        is_background = talk_speaker == talk_title == BACKGROUND_TITLE

        star_count = get_star_count()

        constellation = Constellation()
        constellation.move_to(np.array((-4, 0, 0)))

        self.add(constellation)

        conference_name = TextMobject(
            os.environ.get('TALK_CONFERENCE', 'hackumenta'),
            height=0.5,
        )
        conference_name.add_background_rectangle(
            color=TEXT_BOX_COLOR,
            buff=0.25,
            opacity=TEXT_BOX_OPACITY,
        )
        conference_name.to_corner(corner=LEFT + UP)

        conference_slogan = TextMobject(
            os.environ.get('TALK_CONFERENCE_SLOGAN', '10 years in space'),
            height=0.3,
        )
        conference_slogan.add_background_rectangle(
            color=TEXT_BOX_COLOR,
            buff=0.15,
            opacity=TEXT_BOX_OPACITY,
        )
        conference_slogan.to_corner(corner=RIGHT + UP)

        if is_outro:

            license_image = ImageMobject('images/by-sa.png', height=0.8)
            # license_text = TextMobject('CC-BY-SA 4.0', height=0.2)
            license_image.shift(DOWN * 2.5)
            # license_text.shift(DOWN * 3.7)

            run_time = 8.5
            twinkle_animation = self.create_twinkle_animation(run_time)
            circling_animations = self.create_circling_animations(star_count, run_time)

            circle_write, fd_write, circle_transform = self.get_fd_circle_animations()

            self.play(
                *circling_animations,
                twinkle_animation,
                LaggedStart(
                    Succession(
                        AnimationGroup(
                            FadeIn(license_image, run_time=2),
                            # FadeIn(license_text, run_time=3),
                            circle_write,
                            fd_write,
                            run_time=3,
                        ),
                        circle_transform,
                        AnimationGroup(run_time=1),
                        # AnimationGroup(
                        #     FadeOut(license_image),
                        #     FadeOut(license_text),
                        #     # FadeOut(constellation),
                        #     # *[FadeOut(star) for star in self.stars],
                        #     run_time=0.5,
                        # ),
                        AnimationGroup(
                            FadeOutAndShift(conference_slogan, direction=0.2 * LEFT, run_time=0.5, lag_ratio=0.05,
                                            rate_func=rush_from),
                            FadeOutAndShift(conference_name, direction=0.2 * LEFT, run_time=0.5, lag_ratio=0.05,
                                            rate_func=rush_from),
                            run_time=1,
                        ),
                        AnimationGroup(
                            FadeOut(license_image),
                            # FadeOut(license_text),
                            run_time=1,
                        ),
                        AnimationGroup(run_time=1),
                    ),
                    lag_ratio=0.4,
                ),
            )

        else:
            run_time = float(os.environ.get('RUN_TIME', '10.0'))
            twinkle_animation = self.create_twinkle_animation(run_time)
            circling_animations = self.create_circling_animations(star_count, run_time)

            if is_background:
                NEW_ROCKET_EVERY_N_SECONDS = 60
                rockets = [
                    self.create_rocket_with_path(min_length=2.3, max_length=4)
                    for _ in range(int(run_time // NEW_ROCKET_EVERY_N_SECONDS) + 1)
                ]
                rocket_animations = [MoveAlongPath(r, p, run_time=NEW_ROCKET_EVERY_N_SECONDS, rate_func=linear) for r, p in rockets]
                self.play(
                    *circling_animations,
                    twinkle_animation,
                    LaggedStart(*rocket_animations, lag_ratio=1)
                )
            else:
                rocket, rocket_path = self.create_rocket_with_path()
                rocket_animation = MoveAlongPath(rocket, rocket_path, run_time=run_time, rate_func=linear)

                talk_info = TalkInfo(talk_speaker, talk_title)
                talk_info_animation = LaggedStart(
                    FadeInFrom(talk_info.session_title, 0.1 * LEFT, run_time=3.5, lag_ratio=0.7, rate_func=smooth),
                    FadeInFrom(talk_info.session_speaker, 0.1 * LEFT, run_time=2.0, lag_ratio=0.9, rate_func=smooth),
                    lag_ratio=0.1,
                )

                self.play(
                    *circling_animations,
                    twinkle_animation,
                    rocket_animation,
                    LaggedStart(
                        FadeInFrom(conference_name, 0.1 * LEFT, run_time=1.5, lag_ratio=0.2, rate_func=slow_into),
                        FadeInFrom(conference_slogan, 0.1 * LEFT, run_time=2.0, lag_ratio=0.6, rate_func=slow_into),
                        talk_info_animation,
                        lag_ratio=0.5,
                    ),
                )

    def get_fd_circle_animations(self, origin=ORIGIN, *args, **kwargs):
        circle = self.load_fd_circle('circle', origin=origin)
        circle_dent = self.load_fd_circle('circle_dent', origin=origin)
        letter_f = self.load_fd_letter('f', origin=origin)
        letter_d = self.load_fd_letter('d', origin=origin)

        # group both letters together, so the "Write()" animation works smoothly
        letters = VMobject()
        letters.add(letter_f)
        letters.add(letter_d)

        return (
            Write(circle, stroke_width=7.5, run_time=3),
            Write(letters, run_time=3,),
            Transform(circle, circle_dent, run_time=1.5),
        )

    def fade_out(self, *args, **kwargs):
        self.play(*[FadeToColor(x, self.camera_config['background_color'], **kwargs) for x in args if x is not None])

    def load_fd_circle(self, filename, origin=ORIGIN) -> SVGMobject:
        obj = SVGMobject(file_name=f'images/{filename}.svg')
        obj.set_width(2.8)
        obj.set_stroke('#f6c600', width=7.5)
        obj.set_fill('#000000', 0)
        obj.move_to(origin)
        return obj

    def load_fd_letter(self, letter, origin=ORIGIN) -> SVGMobject:
        obj = SVGMobject(file_name=f'images/letter_{letter}.svg')
        height = 1.1
        obj.set_height(height)
        obj.move_to(LETTER_ORIGIN[letter] + origin)
        obj.set_stroke('#f6c600', width=1)
        obj.set_fill('#f6c600')
        return obj
