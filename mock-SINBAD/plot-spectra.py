import openmc
import plotly.graph_objects as go
import sys

# brings statepoint file from command line argument into the script
# open the results file
results =  openmc.StatePoint(sys.argv[1]) 

#extracts the tally values from the simulation results
cell_tally = results.get_tally(name='mesh')
cell_tally = cell_tally.get_pandas_dataframe()
cell_tally_values = cell_tally['mean']
cell_tally_std_dev = cell_tally['std. dev.']

# extracts values for plot
energy_bins = openmc.mgxs.GROUP_STRUCTURES['CCFE-709']

# this section plots the results
fig = go.Figure()

# adds a line for the upper stanadard deviation bound
fig.add_trace(go.Scatter(x=energy_bins,
                         y=cell_tally_values+cell_tally_std_dev,
                         line=dict(shape='hv', width=0)
                        )
              )

# adds a line for the lower stanadard deviation bound
fig.add_trace(go.Scatter(x=energy_bins,
                         y=cell_tally_values-cell_tally_std_dev,
                         name='std. dev.',
                         fill='tonext',
                         line=dict(shape='hv', width=0)
                        )
              )

# adds a line for the tally result
fig.add_trace(go.Scatter(x=energy_bins,
                         y=cell_tally_values,
                         name='breeder_blanket_spectra',
                         line=dict(shape='hv')
                        )
              )

fig.update_layout(title='Neutron energy spectra',
                  xaxis={'title': 'Energy (eV)',
                         'type': 'log'},
                  yaxis={'title': 'Neutrons per cm2 per source neutron',
                         'type': 'log'}
                 )

fig.write_html("neutron_spectra.html")
try:
    fig.write_html("/my_openmc_workshop/neutron_spectra.html")
except (FileNotFoundError, NotADirectoryError):  # for both inside and outside docker container
    pass

fig.show()
