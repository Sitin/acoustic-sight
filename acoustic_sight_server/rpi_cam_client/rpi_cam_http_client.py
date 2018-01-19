from json import JSONDecodeError
import sys

import requests

from acoustic_sight_server.rpi_cam_client.remote_image_client import RemoteImageClient


class RPiCamHttpClient(RemoteImageClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        pass

    def stop(self):
        pass

    def get_latest_image_url(self):
        r = requests.get('http://{host}:{port}/latest'.format(host=self.host, port=self.port))
        try:
            src = r.json().get('src')
            return 'http://{host}:{port}{url}'.format(host=self.host, port=self.port, url=src)
        except JSONDecodeError:
            return None


if __name__ == '__main__':
    print(RPiCamHttpClient(*sys.argv[1:]).get_latest_image_url())
