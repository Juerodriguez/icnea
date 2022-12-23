MODEL_PATH = "./models/"


class Config:
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
