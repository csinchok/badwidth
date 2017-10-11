# No, these aren't unit tests...

import logging
import subprocess
import re

logger = logging.getLogger('badwidth')

def ping(count=20):
    result = subprocess.run(['ping', '-qc', str(count), 'google.com'], stdout=subprocess.PIPE)
    lines = result.stdout.decode().split('\n')

    packet_line = lines[-3]

    match = re.search('(\d+)% packet loss', packet_line)
    packet_loss = match.groups()[0]
    yield 'ping.packet-loss', float(packet_loss), '%'

    speed_line = lines[-2]
    _, stats, _, counts, _ = speed_line.split(' ')
    for stat, count in zip(stats.split('/'), counts.split('/')):
        yield 'ping.{}'.format(stat), float(count), 'ms'


def curl():

    for filename in ['512k', '1m', '15m']:  # Maybe add the 50m at some point?
        url = 'https://s3.us-east-2.amazonaws.com/badwidth-speed-test/{}.bin'.format(filename)

        result = subprocess.run([
            'curl', '--silent',
            '--write-out', "%{speed_download} %{time_starttransfer} %{time_total}",
            '--output', '/dev/null',
            url],
            stdout=subprocess.PIPE
        )
        speed, starttransfer, total = map(float, result.stdout.decode().split())

        yield 'curl.{}.speed'.format(filename), speed, 'b/s'
        yield 'curl.{}.starttransfer'.format(filename), starttransfer * 1000, 'ms'
        yield 'curl.{}.total'.format(filename), total * 1000, 'ms'


def iter_stats():

    for test in [ping, curl]:
        for stat, value, unit in test():
            logger.info('{0}: {1:.2f}{2}'.format(stat.ljust(25), value, unit))
            yield stat, value, unit
