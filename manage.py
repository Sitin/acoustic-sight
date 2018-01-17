#!/usr/bin/env python3

import os

from jinja2 import Template
from manager import Manager

from acoustic_sight.tools import PROJECT_DIR, SERVICES_DIR
from acoustic_sight import sound_drivers
from acoustic_sight_server.remote_image_sonificator import RemoteImageSonificator
from acoustic_sight_server.rpi_cam_client.rpi_cam_client import ClientTypes
import acoustic_sight_server.server

manager = Manager()


ASS_SERVICE_SETTINGS = {
    'conf_template': os.path.join(SERVICES_DIR, 'supervisor.conf.tmpl'),
    'default_conf_file': os.path.join(SERVICES_DIR, 'acoustic_sight_server-supervisor.conf'),
    'command': os.path.join(PROJECT_DIR, 'manage.py') + ' runserver',
    'args': ''.join([
        '--log-level INFO',
    ]),
}


JUPYTER_SERVICE_SETTINGS = {
    'conf_template': os.path.join(SERVICES_DIR, 'supervisor.conf.tmpl'),
    'default_conf_file': os.path.join(SERVICES_DIR, 'jupyter-supervisor.conf'),
    'command': '/usr/bin/env jupyter-notebook',
    'args': ''.join([
        '--no-browser',
    ]),
}


@manager.command
def remote_image_sonificator(remote_host='localhost', remote_port=80, frame_rate=24,
                             side_in=2**3, sonify=True, show_image=False,
                             synth_type=sound_drivers.PY_GAME,
                             rpi_cam_client_type=ClientTypes.Direct,
                             ):
    """Runs remote image sonificator (cobbects to RPi Camera application)"""
    sonificator = RemoteImageSonificator(remote_host=remote_host, remote_port=remote_port,
                                         frame_rate=frame_rate, side_in=side_in,
                                         sonify=sonify, show_image=show_image,
                                         synth_type=synth_type,
                                         rpi_cam_client_type=rpi_cam_client_type,
                                         )
    sonificator.run()


@manager.command
def runserver(host=None, port=8090, remote_host='localhost',
              remote_port=80, frame_rate=24, side_in=2**3,
              synth_type=sound_drivers.PY_GAME,
              rpi_cam_client_type=ClientTypes.Direct,
              ):
    acoustic_sight_server.server.run(host=host, port=port,
                                     remote_host=remote_host, remote_port=remote_port,
                                     frame_rate=frame_rate, side_in=side_in,
                                     synth_type=synth_type,
                                     rpi_cam_client_type=rpi_cam_client_type,
                                     )


def crete_config(path, command, args, log_dir, program_name):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    with open(JUPYTER_SERVICE_SETTINGS['conf_template']) as tmpl:
        template = Template(tmpl.read())
        config = template.render(
            command=command, args=args,
            project_dir=PROJECT_DIR, log_dir=log_dir,
            program_name=program_name,
        )

        with open(path, 'w') as conf:
            conf.write(config)


@manager.command
def server_supervisor_conf(
        path=ASS_SERVICE_SETTINGS['default_conf_file'],
        command=ASS_SERVICE_SETTINGS['command'],
        args=ASS_SERVICE_SETTINGS['args'],
        log_dir=SERVICES_DIR,
):
    """Generates Supervisor config for Jupyter"""
    crete_config(path, command, args, log_dir, 'asoustic_sight_server')


@manager.command
def jupyter_supervisor_conf(
        path=JUPYTER_SERVICE_SETTINGS['default_conf_file'],
        command=JUPYTER_SERVICE_SETTINGS['command'],
        args=JUPYTER_SERVICE_SETTINGS['args'],
        log_dir=SERVICES_DIR,
):
    """Generates Supervisor config for Jupyter"""
    crete_config(path, command, args, log_dir, 'jupyter')


@manager.command
def make_configs():
    server_supervisor_conf()
    jupyter_supervisor_conf()


@manager.command
def pg_tools_test():
    from acoustic_sight.sound_drivers.pg_tools import test
    test()


@manager.command
def sc_tools_test():
    from acoustic_sight.sound_drivers.sc_tools import test
    test()


@manager.command
def pa_tools_test():
    from acoustic_sight.sound_drivers.pa_tools import test
    test()


if __name__ == '__main__':
    manager.main()
