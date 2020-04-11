import srs_resource_mapper
import cell_config
import ue_config
import srs_utilities as srs_3gpp
import numpy
import matplotlib.pyplot as pyplt

srs_cell_bandwidth_config = 0
srs_bandwidth_config = 3
transmission_comb = 0
cell_bandwidth = '10'
cell_type = 'FDD'

cell_configuration = cell_config.CellConfig(cell_bandwidth, cell_type, srs_cell_bandwidth_config)
ue_configuration = ue_config.UeConfig(srs_bandwidth_config, transmission_comb)

srs_resource_mapper_ent = srs_resource_mapper.SrsResourceMapper(cell_configuration, ue_configuration)
avail_freq_domain_pos = srs_resource_mapper_ent.get_available_freq_domain_pos()
resource_map = [0]*srs_3gpp.N_UL_sc.get(cell_bandwidth)

for freq_domain_pos in range(0, avail_freq_domain_pos):
    for tti in range(0, srs_3gpp.ttis_in_hyperframe):
        resource_map = srs_resource_mapper_ent.get_srs_resource_fd_map(tti, freq_domain_pos, resource_map)

x_axis = numpy.arange(0, srs_3gpp.N_UL_sc.get(cell_bandwidth))
y_axis = numpy.array(resource_map)
print(resource_map)

pyplt.bar(x_axis, y_axis)
pyplt.xlabel('Sub-carriers')
pyplt.show()
