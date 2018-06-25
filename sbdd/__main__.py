if __name__ == "__main__":
    from sbdd import SBDDaemonFromConfig
    import logging
    import sys
    logging.basicConfig(
        format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', 
        level = logging.DEBUG,
        stream=sys.stdout)
    daemon = SBDDaemonFromConfig("sbdd.conf")
    daemon.run()
