import srs_utilities as srs_3gpp
import math


class SrsResourceMapper:
    def __init__(self, cell_config, ue_config):
        self.__cell_bandwidth = cell_config.get_cell_bw()
        self.__cell_type = cell_config.get_cell_type()
        self.__srs_cell_bw_config = cell_config.get_srs_cell_bw_config()
        self.__srs_bw_config = ue_config.get_srs_bw_config()
        self.__k_tc = ue_config.get_transmission_comb()
        self.__m_srs_bw_config = srs_3gpp.bw_config_dict.get(self.__cell_bandwidth)
        self.__get_srs_config()
        self.__freq_domain_positions.clear()
        print("SrsResourceMapper: cell_bw", self.__cell_bandwidth, 'cell_type', self.__cell_type, 'srs_cell_bw_config', self.__srs_cell_bw_config, \
            'srs_bw_config', self.__srs_bw_config, 'k_tc', self.__k_tc, 'm_srs', self.__m_srs, 'N_b', self.__N_b)

    def __get_srs_config(self):
        self.__m_srs = self.__m_srs_bw_config[self.__srs_cell_bw_config][self.__srs_bw_config][srs_3gpp.m_srs_position]
        self.__N_b = self.__m_srs_bw_config[self.__srs_cell_bw_config][self.__srs_bw_config][srs_3gpp.N_b_position]

    def __calc_k_0_region_start(self, tti):
        m_srs_0 = self.__m_srs_bw_config[self.__srs_cell_bw_config][0][srs_3gpp.m_srs_position]
        if self.__cell_type == 'FDD':
            return srs_3gpp.N_sc_RB * (math.floor(srs_3gpp.N_UL_RB.get(self.__cell_bandwidth) / 2) - (m_srs_0 / 2))
        else:
            m_srs_max = m_srs_0
            #sub_fn = tti % 10
            #n_half_frame = sub_fn/(srs_3gpp.ttis_in_frame/2)

            #if n_half_frame % 2 == 0:
            return srs_3gpp.N_sc_RB*(srs_3gpp.N_UL_RB.get(self.__cell_bandwidth)-m_srs_max)
            #else:
            #return 0

    def __calc_sounding_sequence_length(self, b):
        m_srs_b = self.__m_srs_bw_config[self.__srs_cell_bw_config][b][srs_3gpp.m_srs_position]
        m_sc_b_rs = m_srs_b*srs_3gpp.N_sc_RB/srs_3gpp.K_tc
        return m_sc_b_rs

    def __calc_freq_domain_starting_point(self, freq_domain_config, tti):
        k_0_reg_start = self.__calc_k_0_region_start(tti)

        srs_position = 0
        for b in range(0, (self.__srs_bw_config+1)):
            srs_sounding_seq_len = self.__calc_sounding_sequence_length(b)
            freq_pos_index_n_b = self.__calc_freq_position_index(b, freq_domain_config, tti)
            srs_position = srs_position + (srs_sounding_seq_len*freq_pos_index_n_b*srs_3gpp.K_tc)
        return srs_position + k_0_reg_start

    def __calc_freq_position_index(self, b, freq_domain_position, tti):
        m_srs_b = self.__m_srs_bw_config[self.__srs_cell_bw_config][b][srs_3gpp.m_srs_position]
        n_b = self.__m_srs_bw_config[self.__srs_cell_bw_config][b][srs_3gpp.N_b_position]
        n_srs = math.floor(tti/self.__T_srs)
        if b <= self.__b_hop:
            return math.floor(4*freq_domain_position/m_srs_b) % n_b
        else:
            f_b = self.__calc_f_b(b, n_srs)
            return (f_b + math.floor(4*freq_domain_position/m_srs_b)) % n_b

    def __calc_f_b(self, b, n_srs):
        n_b = self.__m_srs_bw_config[self.__srs_cell_bw_config][b][srs_3gpp.N_b_position]

        if n_b % 2 == 0:
            n_b_prim = self.__calc_n_b_prim(b)
            n_b_prim_m_1 = self.__calc_n_b_prim(b - 1)
            return (n_b/2)*math.floor((n_srs % n_b_prim)/n_b_prim_m_1) + math.floor((n_srs % n_b_prim)/(2*n_b_prim_m_1))
        else:
            n_b_prim_m_1 = self.__calc_n_b_prim(b - 1)
            return math.floor(n_b/2)*math.floor(n_srs/n_b_prim_m_1)

    def __calc_n_b_prim(self, b):
        n_b_prim = 0

        if b < self.__b_hop:
            n_b_prim = 1
        else:
            for i in range(self.__b_hop, (b+1)):
                if i == self.__b_hop:
                    n_b_prim = 1
                else:
                    n_b_prim = n_b_prim * self.__m_srs_bw_config[self.__srs_cell_bw_config][i][srs_3gpp.N_b_position]
        return n_b_prim

    def get_available_freq_domain_pos(self):
        return math.floor(self.__m_srs_bw_config[self.__srs_cell_bw_config][0][srs_3gpp.m_srs_position]/self.__m_srs)

    def get_srs_resource_fd_map(self, tti, freq_domain_config, resource_map_fd):
        freq_domain_starting_point = self.__calc_freq_domain_starting_point(freq_domain_config, tti)
        freq_domain_seq_length = self.__calc_sounding_sequence_length(self.__srs_bw_config)

        if all(x != freq_domain_starting_point for x in self.__freq_domain_positions):
            self.__freq_domain_positions.append(freq_domain_starting_point)
            print("cell_srsbw", self.__srs_cell_bw_config, "bwsrs", self.__srs_bw_config,  "freq_domain_starting_point", freq_domain_starting_point)

        for k in range(int(freq_domain_starting_point), int(freq_domain_starting_point+freq_domain_seq_length*2), 2):
            resource_map_fd[k] = freq_domain_starting_point
        return resource_map_fd

    __m_srs_bw_config = None
    __cell_bandwidth = []
    __cell_type = []
    __srs_cell_bw_config = None
    __srs_bw_config = None
    __T_srs = 20
    __m_srs = None
    __N_b = None
    __k_tc = None
    __srs_cyclic_shift = 0
    __b_hop = 0
    __freq_domain_positions = []


