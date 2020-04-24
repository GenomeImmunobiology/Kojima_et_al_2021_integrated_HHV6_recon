#!/usr/bin/env python

'''
Copyright (c) 2020 RIKEN
All Rights Reserved
See file LICENSE for details.
'''


import os,sys,datetime,multiprocessing
import os
from os.path import abspath,dirname,realpath,join
import log,traceback

# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    elif 'PATH' in os.environ:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

def check(args, argv):
    log.logger.debug('started')
    try:
        log.logger.debug('command line:\n'+ ' '.join(argv))
        # check python version
        version=sys.version_info
        if (version[0] >= 3) and (version[1] >= 7):
            log.logger.debug('Python version=%d.%d.%d' % (version[0], version[1], version[2]))
        else:
            log.logger.error('Please use Python 3.7 or later. Your Python is version %d.%d.' % (version[0], version[1]))
            exit(1)
        
        # check cpu num
        cpu_num=multiprocessing.cpu_count()
        if args.p > cpu_num:
            log.logger.error('Too many thread number. Please specify the number less than your cpu cores. You specified = %d, cpu cores = %d.' % (args.p, cpu_num))
            exit(1)
        
        # check PATH
        for i in ['bwa', 'bamCoverage']:
            if which(i) is None:
                log.logger.error('%s not found in $PATH. Please check %s is installed and added to PATH.' % (i, i))
                exit(1)

        # check prerequisite modules
        from Bio.Seq import Seq
        import gzip
        import matplotlib
        import pysam
        
        # check file paths
        if os.path.exists(args.bwaindex +'.bwt') is False:
            log.logger.error('bwa index (%s) was not found.' % args.ht2db)
            exit(1)
        if os.path.exists(args.fa) is False:
            log.logger.error('Reference genome (%s) was not found.' % args.fa)
            exit(1)
        if args.alignmentin is False and args.unmappedin is False:
            log.logger.error('Please specify either -alignmentin or -unmappedin.')
            exit(1)
        elif args.alignmentin is True and args.unmappedin is True:
            log.logger.error('Please specify either -alignmentin or -unmappedin.')
            exit(1)
        elif args.alignmentin is True:
            if args.c is not None:
                if os.path.exists(args.c) is False:
                    log.logger.error('CRAM file (%s) was not found.' % args.c)
                    exit(1)
            elif args.b is not None:
                if os.path.exists(args.b) is False:
                    log.logger.error('BAM file (%s) was not found.' % args.b)
                    exit(1)
            else:
                log.logger.error('Please specify BAM or CRAM file (-b or -c option).')
                exit(1)
        elif args.unmappedin is True:
            if args.unmap1 is None:
                log.logger.error('Please specify unmapped file.')
                exit(1)
            elif os.path.exists(args.unmap1) is False:
                log.logger.error('Unmapped file (%s) was not found.' % args.unmap1)
                exit(1)
            if args.unmap2 is None:
                log.logger.error('Please specify unmapped file.')
                exit(1)
            elif os.path.exists(args.unmap2) is False:
                log.logger.error('Unmapped file (%s) was not found.' % args.unmap2)
                exit(1)

    except:
        log.logger.error('\n'+ traceback.format_exc())
        exit(1)
