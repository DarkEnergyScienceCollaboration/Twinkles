''' Utilities to calculate naive signal to noise ratios '''
from __future__ import absolute_import, division, print_function
import os, math
from lsst.sims.photUtils import Sed, Bandpass

class fake_phot_params(object):
    exptime = 30.
    nexp = 1
    effarea = 1.
    gain = 1.

def calc_adu(mag, bandpass):
    sed = Sed()
    sed.setFlatSED()
    fluxNorm = sed.calcFluxNorm(mag, bandpass)
    sed.multiplyFluxNorm(fluxNorm)
    return sed.calcADU(bandpass, fake_phot_params())

def flat_sed_snr(mag, bandpass, m5):
    source_counts = calc_adu(mag, bandpass)
    # assuming sky limited at the 5 sigma limit
    sky_counts = calc_adu(m5, bandpass)/5.
    return source_counts/sky_counts

def make_invsnr_arr(mag_bright=16., mag_dim=27., mag_delta=0.1, floor=0.02, m5=24.5):
    filterdir = os.getenv('LSST_THROUGHPUTS_BASELINE')
    bandpass = Bandpass()
    bandpass.readThroughput(os.path.join(filterdir, 'total_r.dat'))
    mag = mag_bright
    mag_arr = []
    invsnr_arr = []
    while mag < mag_dim:
        snr = flat_sed_snr(mag, bandpass, m5)
        mag_arr.append(mag)
        invsnr_arr.append(math.hypot(1./snr, floor))
        mag += mag_delta
    return mag_arr, invsnr_arr

def fit_invsnr(mags, floor, m5, bandpass_name='r'):
    filterdir = os.getenv('LSST_THROUGHPUTS_BASELINE')
    bandpass = Bandpass()
    bandpass.readThroughput(os.path.join(filterdir, 'total_%s.dat'%bandpass_name))
    invsnr_arr = []
    for mag in mags:
        snr = flat_sed_snr(mag, bandpass, m5)
        invsnr_arr.append(math.hypot(1./snr, floor))
    return invsnr_arr
