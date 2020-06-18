import openmc
import plotly.graph_objects as go
import sys

# brings statepoint file from command line argument into the script
results_filename = sys.argv[1] 

# open the results file
results = openmc.StatePoint(results_filename)

#extracts the tally values from the simulation results
cell_tally = results.get_tally(name='energy_spectra')
cell_tally = cell_tally.get_pandas_dataframe()
cell_tally_values = cell_tally['mean']
cell_tally_std_dev = cell_tally['std. dev.']


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
    fig.write_html("/opt/openmc/results/blanket_neutron_spectra.html")
except (FileNotFoundError, NotADirectoryError):  # for both inside and outside docker container
    pass

fig.show()
