#!/usr/bin/python3
import lirc
import logging
import time

import soco

logging.basicConfig(
    format='%(levelname)s:%(message)s', 
    level=logging.INFO
)

VOL_TRESHOLD = 2

class SonosRemote(object):

    def __init__(self):
        self.lirc_sockid = lirc.init("sonos")  # Init lirc
        self.zones = list(soco.discover())  # Sonos device discovery

        logging.info(self.zones)

    @property
    def sonos(self):
        if len(self.zones) >= 1:
            return self.zones[0]

    def loop(self):
        key = self.get_ir()
        if key:
            logging.info('pressed: {}'.format( key ))
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

        commands = dict(
                volumeup = True,
                volumedown = True,
                play = sonos.play,
                pause = sonos.pause, 
        )

        action = commands.get(key)
        if key == 'play' and not self.sonos_playing() or\
                key == 'pause' and self.sonos_playing():
            action()        
        elif key == 'volumeup' or key == 'volumedown':
            v = volume = sonos.volume

            if key == 'volumeup':
                v += VOL_TRESHOLD
            else:
                v -= VOL_TRESHOLD

            sonos.volume = v
            logging.info('Volume from {0} to {1}'.format(volume, v)) 
            
        logging.info('{0}: {1}'.format(key, action))

if __name__ == '__main__':
    logging.info('IR remote interface for Sonos speakers')

    remote = SonosRemote()
    while True:
        remote.loop()
        time.sleep(0.1)
