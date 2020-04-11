class CellConfig:
    def __init__(self, cell_bandwidth, cell_type, srs_cell_bw_config):
        self.__cell_bandwidth = cell_bandwidth
        self.__cell_type = cell_type
        self.__srs_cell_bw_config = srs_cell_bw_config
        print('SrsCommonConfig')

    def get_cell_bw(self):
        return self.__cell_bandwidth

    def get_cell_type(self):
        return self.__cell_type

    def get_srs_cell_bw_config(self):
        return self.__srs_cell_bw_config

    __cell_bandwidth = []
    __cell_type = []
    __srs_cell_bw_config = 0
