import logging


def logByModuleLevelLogger():
    logging.debug("root-debug")
    logging.info("root-info")
    logging.warning("root-warn")
    logging.error("root-error")
    logging.critical("root-critical")


def logByDefaultLogger():
    a = logging.getLogger()
    a.debug("default-debug")
    a.info("default-info")
    a.warning("default-warn")
    a.error("default-error")
    a.critical("default-critical")
    a.setLevel(logging.DEBUG)
    a.debug("default-debug")


def logByNamedLogger():
    b = logging.getLogger("b")
    b.debug("b-debug")
    b.info("b-info")
    b.warning("b-warn")
    b.error("b-error")
    b.critical("b-critical")
    b.setLevel(logging.DEBUG)
    b.debug("b-debug")


class ClassA(object):
    def __init__(self):
        self.logger = logging.getLogger("ClassA")
        self.logger.setLevel(logging.DEBUG)

    def methodA(self):
        self.logger.debug("%s debug" % "ClassA.methodA")
        self.logger.info("%s info" % "ClassA.methodA")
        self.logger.warning("%s warning" % "ClassA.methodA")
        self.logger.error("%s error" % "ClassA.methodA")
        self.logger.critical("%s critical" % "ClassA.methodA")


class ClassB(object):
    logger = logging.getLogger("ClassB")

    def __init__(self):
        self.logger.warning("ClassB.__init__")
        self.logger.setLevel(logging.DEBUG)

    def methodB(self):
        self.logger.debug("%s debug" % "ClassB.methodB")
        self.logger.info("%s info" % "ClassB.methodB")
        self.logger.warning("%s warning" % "ClassB.methodB")
        self.logger.error("%s error" % "ClassB.methodB")
        self.logger.critical("%s critical" % "ClassB.methodB")


if __name__ == "__main__":
    logging.basicConfig()
    class_a = ClassA()
    class_a.methodA()
    class_b = ClassB()
    class_b.methodB()