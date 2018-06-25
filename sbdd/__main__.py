if __name__ == "__main__":
    from sbdd import SBDDaemonFromConfig
    daemon = SBDDaemonFromConfig("sbdd.conf")
    daemon.run()
