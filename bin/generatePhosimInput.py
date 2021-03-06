#!/usr/bin/env python
"""
Script to run the generation of phoSim instance catalogs
"""
from __future__ import with_statement, absolute_import, division, print_function
import time
import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from lsst.utils import getPackageDir
from lsst.sims.catUtils.utils import ObservationMetaDataGenerator
from desc.twinkles import TwinklesSky


def phoSimInputFileName(obsHistID,
                        prefix='InstanceCatalogs/PhoSim_input',
                        suffix='.txt',
                        location='./'):
    """
    function to return the absolute path to a filename for writing the phoSim
    input corresponding to obsHistID.

    Parameters
    ----------
    prefix : string, optional
    suffix : string, optional, defaults to '.txt'
    location : string, optional, defaults to './'
    """

    return os.path.join(location, prefix + '_{}'.format(obsHistID) + suffix)


def _sql_constraint(obsHistIDList):
    """
    sql constraint to get OpSim pointing records for a list of obsHistID

    Parameters
    ----------
    obsHistIDList : list of integers, mandatory
        list of obsHistIDs of interest
    """
    sql_string = 'SELECT * FROM Summary WHERE ObsHistID in ('
    sql_string += ', '.join(map(str, obsHistIDList))
    sql_string += ')'
    return sql_string


def generateSinglePointing(obs_metaData, availableConns, sntable,
                           fname,
                           sn_sed_file_dir,
                           db_config,
                           cache_dir):
    """
    obs_metaData : instance of `lsst.sims.utils.ObservationMetaData`
        observation metadata corresponding to an OpSim pointing
    availableConns : available connections to fatboy
    sntable : Table for SN on the fatboy database
    fname : output file for phoSim instance Catalog
    sn_sed_file_dir : directory to which the SN seds corresponding to this
        phoSim metadat
    db_config : the name of a file overriding the fatboy connection information
    cache_dir : the directory containing the source data of astrophysical objects
    """
    tstart = time.time()
    obs_metaData.boundLength = 0.3
    print(obs_metaData.summary)
    obsHistID = obs_metaData._OpsimMetaData['obsHistID']

    # all but first two are default values of optional parameters
    # Kept in script to emphasize inputs
    tSky = TwinklesSky(obs_metadata=obs_metaData,
                       availableConnections=availableConns,
                       brightestStar_gmag_inCat=11.0,
                       brightestGal_gmag_inCat=11.0,
                       sntable=sntable,
                       sn_sedfile_prefix=os.path.join(sn_sed_file_dir, 'specFile_'),
                       db_config=db_config,
                       cache_dir=cache_dir)
    # fname = phoSimInputFileName(obsHistID)
    # if not os.path.exists(os.path.dirname(fname)):
    #    os.makedirs(os.path.dirname(fname))
    if not os.path.exists(sn_sed_file_dir):
        os.makedirs(sn_sed_file_dir)
    tSky.writePhoSimCatalog(fname)
    availConns = tSky.availableConnections
    tend = time.time()
    print (obsHistID, tend - tstart)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Write phoSim Instance Catalogs'
                                     'and SN spectra to disk '
                                     'example : '
                                     'python generatePhosimInput.py 230\ '
                                     '--OpSimDBDir ~/data/LSST/OpSimData/\ '
                                     '--seddir "./"\ '
                                     '--outfile phosim_instance_catalog_220.txt')
    parser.add_argument('--opsimDB',
                        type=str,
                        help='OpSim database sqlite filename',
                        default='minion_1016_sqlite.db')
    parser.add_argument('visit',
                        type=int,
                        help='Visit number (obsHistID)')
    parser.add_argument('--OpSimDBDir',
                        help='absolute path to dir with the opsimBD',
                        type=str,
                        default='./')
    parser.add_argument('--outfile', type=str, default=None,
                        help='output filename for instance catalog')
    parser.add_argument('--seddir',
                        type=str,
                        default='.',
                        help='directory to contain SED files')
    parser.add_argument('--db_config', type=str, default=None,
                        help='config file overriding CatSim database connection information')
    parser.add_argument('--cache_dir', type=str,
                        default=os.path.join(getPackageDir('twinkles'), 'data'),
                        help='directory containing the source data for the InstanceCatalogs')
    args = parser.parse_args()

    # set the filename default to a sensible value using the obsHistID
    if args.outfile is None:
        args.outfile = phoSimInputFileName(args.visit,
                                           prefix='phosim_input',
                                           suffix='.txt',
                                           location='./')
    # Set up OpSim database
    opSimDBPath = os.path.join(args.OpSimDBDir, args.opsimDB)
    engine = create_engine('sqlite:///' + opSimDBPath)

    obs_gen = ObservationMetaDataGenerator(database=opSimDBPath)
    sql_query = 'SELECT * FROM Summary WHERE ObsHistID == {}'.format(args.visit)
    df = pd.read_sql_query(sql_query, engine)
    recs = df.to_records()
    obsMetaDataResults = obs_gen.ObservationMetaDataFromPointingArray(recs)
    obs_metaData = obsMetaDataResults[0]
    sn_sed_file_dir = os.path.join(args.seddir, 'spectra_files')

    availConns = None
    print('will generate pointing for {0} and write to filename {1}'.format(
          obs_metaData._OpsimMetaData['obsHistID'], args.outfile))
    generateSinglePointing(obs_metaData,
                           availableConns=availConns,
                           sntable='TwinkSN_run3',
                           fname=args.outfile,
                           sn_sed_file_dir=sn_sed_file_dir,
                           db_config=args.db_config,
                           cache_dir=args.cache_dir)
