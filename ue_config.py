class UeConfig:
    def __init__(self, srs_bw_config, transmission_comb):
        self.__srs_bw_config = srs_bw_config
        self.__transmission_comb = transmission_comb

        print('UeConfig')

    def get_srs_bw_config(self):
        return self.__srs_bw_config

    def get_transmission_comb(self):
        return self.__transmission_comb

    __srs_bw_config = 0
    __transmission_comb = 0


