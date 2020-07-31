#!/usr/bin/env python3
import shutil
import os
from pathlib import Path
import sys
from cmd import Cmd

stage_dir = '_sarsoo.xyz'
scss_rel_path = Path('src', 'scss', 'style.scss')
css_rel_path = Path('build', 'style.css')

folders_to_ignore = ['venv', 'docs', '.git', '.idea', 'node_modules']


class Admin(Cmd):
    intro = 'Sarsoo.xyz Admin... ? for help'
    prompt = '> '

    def prepare_stage(self):
        print('>> backing up a directory')
        os.chdir(Path(__file__).absolute().parent.parent)

        print('>> deleting old deployment stage')
        shutil.rmtree(stage_dir, ignore_errors=True)

        print('>> copying main source')
        shutil.copytree('sarsoo.xyz',
                        stage_dir,
                        ignore=lambda path, contents:
                            contents if any(i in Path(path).parts for i in folders_to_ignore) else []
                        )

        for dependency in ['fmframework']:
            print(f'>> injecting {dependency}')
            shutil.copytree(
                Path(dependency, dependency),
                Path(stage_dir, dependency)
            )

        os.chdir(stage_dir)
        os.system('gcloud config set project sarsooxyz')

    def prepare_frontend(self):
        print('>> building css')
        os.system(f'sass --style=compressed {scss_rel_path} {css_rel_path}')

        print('>> building javascript')
        os.system('npm run build')

    def do_api(self, args):
        self.prepare_frontend()
        self.prepare_stage()

        print('>> deploying')
        os.system('gcloud app deploy')

    def do_exit(self, args):
        exit(0)

    def do_sass(self, args):
        os.system(f'sass --style=compressed {scss_rel_path} {css_rel_path}')

    def do_watchsass(self, args):
        os.system(f'sass --style=compressed --watch {scss_rel_path} {css_rel_path}')


if __name__ == '__main__':
    console = Admin()
    if len(sys.argv) > 1:
        console.onecmd(' '.join(sys.argv[1:]))
    else:
        console.cmdloop()
