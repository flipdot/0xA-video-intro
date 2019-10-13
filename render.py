#!/usr/bin/env python3

import os
import re
import subprocess
import random
from textwrap import dedent
from collections import namedtuple
import urllib.parse

Talk = namedtuple('Talk', ['speaker', 'title', 'seed'])

TALKS = {
    # Day 0
    Talk('soerface / AI', 'Opening', '717855'),
    Talk('dargmuesli', 'CUDA Basics', '83634'),
    Talk('aiko', 'Die dreckige Empirie', '960604'),
    # Talk('typ_o', 'flipdot - was bisher geschah', None),

    # Day 1
    Talk('BinaerBube', 'Mechanische Zeichenmaschine', '1000'),
    Talk('nikeee', 'Was andere Sprachen von TypeScript lernen können', '882746'),
    Talk('typ\_o', 'Chemie und Physik beim Kochen und Brot backen', '879286'),
    Talk('unsurv', 'Biometrische Überwachung in Deutschland', '497125'),

    # Day 2
    Talk('dargmuesli', 'DargStack: Ein Strauß Microservices', '187721'),
    Talk('Antares', 'Blast Procedure - Wie man Party und Videogames vereinen kann', '449339'),
    Talk('Sven', 'Esperanto: Wie funktioniert eine Plansprache?', '563460'),
    Talk('nikeee', 'Wie zählt man bei \$BIG\_SITE die Seitenaufrufe?', '519098'),
    Talk('analogmultiplizierer', 'flipdot Badge PCB Design', '600089'),
    # Talk('DmB', 'Diskordischer Göttinendienst', None),

    Talk('Outro', 'Outro', '545513'),

    # Takes long to render - set playtime a few lines below
    # Talk('Background', 'Background', '620613'),
}


def sanitize_file_name(file_name: str) -> str:
    """
    Ref: https://stackoverflow.com/a/13593932
    """
    return re.sub('[^\w\-_\. ]', '_', file_name)


def render_talks(talks):
    files = []
    counter = 0
    for speaker, title, seed in TALKS:
        counter += 1
        print(f'Rendering {counter}/{len(TALKS)}')

        env = os.environ.copy()
        env['TALK_CONFERENCE'] = 'hackumenta'
        env['TALK_CONFERENCE_SLOGAN'] = '10 years in space'
        env['TALK_SPEAKER'] = speaker
        env['TALK_TITLE'] = title
        env['SEED'] = str(seed) if seed is not None else str(random.randint(0, 1000000))
        if speaker == title == 'Background':
            env['RUN_TIME'] = '120'
            # env['RUN_TIME'] = str(60 * 60 * 2)  # 2 hours of background blinking

        file_name_title = title.replace(' ', '.')
        file_name = sanitize_file_name(f'{speaker}-{file_name_title}-{env["SEED"]}.mp4')

        print(f'Rendering: {speaker}_{title}')

        p = subprocess.Popen([
            'manim',
            '--file_name', file_name,
            # '-r', '1080,1920',
            '-l',
            '0xa.py',
            'Intro',
        ],
            env=env,
        )
        p.wait()
        files.append((Talk(speaker, title, seed), file_name))
    return files


def main():
    files = render_talks(TALKS)

    with open('index.html', 'w') as index_html:
        links = ''.join(map(
            lambda file: f'<li><a href="{urllib.parse.quote(file[1])}">{file[0].speaker} - {file[0].title}</a>',
            files
        ))

        index_html.write(
            dedent(
                f'''\
                <!doctype html>
                <meta charset=utf-8>
                <h1>Intros</h1>
                <ul>
                {links}
                </ul>
                '''
            )
        )


if __name__ == '__main__':
    main()
