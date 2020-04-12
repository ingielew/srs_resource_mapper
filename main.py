import srs_resource_mapper
import cell_config
import ue_config
import srs_utilities as srs_3gpp
import numpy
import matplotlib.pyplot as pyplt

#srs_cell_bandwidth_config = 0
#srs_bandwidth_config = 3
transmission_comb = 0
cell_bandwidth = '20'
cell_type = 'FDD'

resource_map = [0]*srs_3gpp.N_UL_sc.get(cell_bandwidth)
y_axis = numpy.array(resource_map)

for csrs in range(len(srs_3gpp.srs_bandwidth_config)):
    for bsrs in range(len(srs_3gpp.srs_bandwidth)):

        cell_configuration = cell_config.CellConfig(cell_bandwidth, cell_type, csrs)
        ue_configuration = ue_config.UeConfig(bsrs, transmission_comb)

        srs_resource_mapper_ent = srs_resource_mapper.SrsResourceMapper(cell_configuration, ue_configuration)
        avail_freq_domain_pos = 1#srs_resource_mapper_ent.get_available_freq_domain_pos()

        # Plot and save
        pyplt.xlabel('Sub-carriers')
        x_axis = numpy.arange(0, srs_3gpp.N_UL_sc.get(cell_bandwidth))
        y_axis = numpy.zeros_like(resource_map)
        fig, axs = pyplt.subplots(avail_freq_domain_pos)

        label = "SRS_resource_util_single_freqDomainPos_(bw:", cell_bandwidth,"Csrs:", csrs, "Bsrs:", bsrs
        fig.suptitle(label)
        for freq_domain_pos in range(0, avail_freq_domain_pos):
            plot_title = "Distribution for freqDomainPosition:", freq_domain_pos
            current_freq_group_val = 0
            for tti in range(0, srs_3gpp.ttis_in_hyperframe):
                resource_map = srs_resource_mapper_ent.get_srs_resource_fd_map(tti, freq_domain_pos, resource_map)

            lowest_freq_group_index = 1200
            highest_freq_group_index = 0
            for i in range(len(resource_map)):
                if current_freq_group_val != resource_map[i] and resource_map[i] > 0:
                    if avail_freq_domain_pos > 1:
                        axs[freq_domain_pos].bar(x_axis, y_axis)
                        axs[freq_domain_pos].set_title(plot_title)
                    else:
                        axs.bar(x_axis, y_axis)
                        axs.set_title(plot_title)

                    if lowest_freq_group_index > resource_map[i]:
                        lowest_freq_group_index = resource_map[i]

                    if highest_freq_group_index < resource_map[i]:
                        sc_util = srs_3gpp.bw_config_dict.get(cell_bandwidth)[csrs][bsrs][srs_3gpp.m_srs_position]*srs_3gpp.N_sc_RB
                        highest_freq_group_index = resource_map[i] + sc_util

                    y_axis = numpy.zeros_like(resource_map)
                    current_freq_group_val = resource_map[i]

                if resource_map[i] != 0:
                    y_axis[i] = 1

                resource_map[i] = 0
            if avail_freq_domain_pos > 1:
                axs[freq_domain_pos].bar(x_axis, y_axis)
            else:
                axs.bar(x_axis, y_axis)

            filename = str(label)+".txt"
            text_file = open(filename, "w")
            text_to_write = "lowest_freq_group_index", lowest_freq_group_index, "highest_freq_group_index", highest_freq_group_index
            text_file.write(str(text_to_write))
            text_file.close()
            print("lowest_freq_group_index", lowest_freq_group_index, "highest_freq_group_index", highest_freq_group_index)

        del srs_resource_mapper_ent

        figname = str(label)+".eps"
        pyplt.savefig(figname, format='eps')
