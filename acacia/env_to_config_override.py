import os
from ConfigParser import ConfigParser

if __name__ == '__main__':

    with open('/app/config', 'a') as ofile:
        ofile.write('\n[override]\n')

    config = ConfigParser()

    with open('/app/config') as fp:
        config.readfp(fp)

    for par, val in sorted(os.environ.items()):
        if par in config.options('override'):
            with open('/app/config', 'a') as ofile:
                ofile.write('{}={}\n'.format(par, val))
