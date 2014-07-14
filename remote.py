#!/usr/bin/python3
import lirc
import logging
from pprint import pprint
import time
import soco

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

VOL_TRESHOLD = 2

class SonosRemote(object):

    def __init__(self):
        self.lirc_sockid = lirc.init("sonos")  # Init lirc
        self.zones = list(soco.discover())  # Sonos device discovery

        if self.sonos:
            logger.info(pprint(self.sonos.get_speaker_info()))

    @property
    def sonos(self):
        if len(self.zones) >= 1:
            return self.zones[0]

    def loop(self):
        key = self.get_ir()
        if key:
            logger.info('pressed: {}'.format( key ))
            self.mapping(key)

    def get_ir(self):
        codes = lirc.nextcode()
        if codes:
            return codes[0]

    def sonos_playing(self):
        info = self.sonos.get_current_transport_info()
        if info.get('current_transport_state') == 'PLAYING':
            return True
        else:
            return False

    def mapping(self, key):
        sonos = self.sonos

        if key == 'power':
            logger.info('Power button is not implemented')
        elif key == 'stop':
            sonos.stop()
        elif key == 'rewind':
            sonos.mute
            muteness = sonos.mute
            if muteness:
                sonos.mute = False
            else:
                sonos.mute = True
        elif key == 'previous':
            sonos.previous()
        elif key == 'next':
            sonos.next()
        elif key == 'eq':
            loudness = sonos.loudness
            if loudness:
                sonos.loudness = False
            else:
                sonos.loudness = True
        elif key == 'play' and self.sonos_playing():
            sonos.pause()
        elif key == 'play' and not self.sonos_playing():
            sonos.play()
        elif key == 'volumeup' or key == 'volumedown':
            v = volume = sonos.volume

            if key == 'volumeup':
                v += VOL_TRESHOLD
            else:
                v -= VOL_TRESHOLD

            sonos.volume = v
            logger.info('Volume from {0} to {1}'.format(volume, v)) 
        else:
            logger.info('Key not found: {0}'.format(key))
            

if __name__ == '__main__':
    logger.info('IR remote interface for Sonos speakers')

    remote = SonosRemote()
    while True:
        remote.loop()
        time.sleep(0.5)
