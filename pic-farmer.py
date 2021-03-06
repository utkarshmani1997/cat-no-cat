#!/usr/bin/env python3
import os
import random
import sys
import requests


def farm_pics(lo, hi, pi):
    '''Ensures that *pi* number of images are created and stored in the current directory.

    :lo lower bound of picture dimension
    :hi higer bound of picture dimension
    :pi number of pics to be downloaded
    '''
    rnd = random.randint
    if os.path.isfile('runinfo.txt'):
        with open('runinfo.txt', 'w') as f:   # Adds previous info about, in the root of the repo.
            f.write("{},{},{}\n".format(lo, hi, pi))

    if not os.path.isdir('sample_images'):
        os.makedirs('sample_images')

    os.chdir('sample_images')

    for i in range(pi):
        L, H = rnd(lo, hi), rnd(lo, hi)
        x = requests.get('https://placekitten.com/g/' + str(L) + '/' + str(H))
        assert(x.status_code == 200), "Couldn't reach placeKitten in hit{}\n".format(i)

        if x.text is '':  # If image couldn't be served, get a boring image
            x = requests.get('https://placehold.it/' + str(L) + 'x' + str(H))
            assert(x.status_code == 200), "Couldn't reach placeHold in hit{}\n".format(i)

        filename = '{}.jpg'.format(i)

        # Writes it to a file
        with open(filename, "wb") as f:
            f.write(x.content)
        print('Wrote {}.jpg'.format(i))


if __name__ == '__main__':

    if len(sys.argv) != 4:
        sys.stderr.write('Usage ./pic-farmer.py <lower-limit> <higher-limit> <number of pics>\n')
        sys.exit(-1)

    try:
        low  = int(sys.argv[1])
        high = int(sys.argv[2])
        pics = int(sys.argv[3])
    except ValueError:
        sys.stderr.write('Wrong type of values given\n')
        sys.stdout.write('/path/to/program <integer> <integer> <integer>')
        sys.exit(-2)
    try:
        farm_pics(low, high, pics)
    except (KeyboardInterrupt, SystemExit):
        pass
