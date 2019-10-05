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
    Talk('AI', 'Opening', None),
    Talk('dargmuesli', 'CUDA Basics', None),
    Talk('aiko', 'Die dreckige Empirie', None),
    # Talk('typ_o', 'flipdot - was bisher geschah', None),

    # Day 1
    Talk('BinaerBube', 'Mechanische Zeichenmaschine', None),
    Talk('nikeee', 'Was andere Sprachen von TypeScript lernen können', None),
    Talk('typ_o', 'Chemie und Physik beim Kochen und Brot backen', None),
    Talk('unsurv', 'Biometrische Überwachung in Deutschland', None),

    # Day 2
    Talk('dargmuesli', 'DargStack: Ein Strauß Microservices', None),
    Talk('Antares', 'Blast Procedure – Wie man Party und Videogames vereinen kann', None),
    Talk('Sven', 'Esperanto: Wie funktioniert eine Plansprache?', None),
    Talk('nikeee', 'Wie zählt man bei \$BIG\_SITE die Seitenaufrufe?', None),
    Talk('analogmultiplizierer', 'flipdot Badge PCB Design', None),
    Talk('DmB', 'Diskordischer Göttinendienst', None),

    Talk('Outro', 'Outro', None),
}


def sanitize_file_name(file_name: str) -> str:
    '''
    Ref: https://stackoverflow.com/a/13593932
    '''
    return re.sub('[^\w\-_\. ]', '_', file_name)


def render_talks(talks):
    files = []
    counter = 0
    for speaker, title, seed in TALKS:
        counter += 1
        print(f'Rendering {counter}/{len(TALKS)}')

        env = os.environ.copy()
        env['TALK_CONFERENCE'] = 'hackumenta'
        env['TALK_SPEAKER'] = speaker
        env['TALK_TITLE'] = title
        env['SEED'] = str(seed) if seed is not None else str(random.randint(0, 1000000))

        file_name_title = title.replace(' ', '.')
        file_name = sanitize_file_name(f'{speaker}-{file_name_title}-{env["SEED"]}.mp4')

        print(f'Rendering: {speaker}_{title}')

        p = subprocess.Popen([
            'manim',
            '--file_name', file_name,
            '-r', '1080,1920',
            # '-l',
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
