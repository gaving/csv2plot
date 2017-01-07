import glob
import os
import click
import pandas
import numpy as np
import seaborn as sbn

@click.command()
@click.option('--date-column', default='Date', prompt='Date column')
@click.option('--date-format', default='%d/%m/%Y', prompt='Date format')
@click.option('--path', prompt='Directory', help='Path to CSV files')
@click.option('--search-column', default=' Description', help='Search column')
@click.option('--value-column', default=' Value', prompt='Value column', help='Value column')
@click.option('--pattern', help='Pattern to query')
def run(date_column, date_format, path, search_column, value_column, pattern):
    files = glob.glob(os.path.join(path, '*.csv'))
    dfs = (pandas.read_csv(f) for f in files)
    df = pandas.concat(dfs, ignore_index=True)
    df.info()

    df['Time'] = pandas.to_datetime(df[date_column], format=date_format)
    df['Month'] = df['Time'].dt.strftime('%m/%y')

    if pattern:
        if not (df[search_column].dtype in [np.float64, np.int64]):
            df = df[df[search_column].str.contains(pattern)]
        elif (df[search_column].dtype in [np.int64]):
            df = df.loc[df[search_column].isin([int(pattern)])]
        else:
            df = df.loc[df[search_column].isin([float(pattern)])]

    df = df.sort('Time')

    print df[[date_column, value_column]]

    total = df[value_column].sum()

    sbn.set(style='darkgrid', palette='Set2')
    sbn.set(font='Verdana')
    sbn.set_style('whitegrid', {
        'ytick.major.size': 0.1,
        'ytick.minor.size': 0.05,
        'grid.linestyle': '--'
    })

    plot = df.plot(title=total, x='Month', y=value_column, figsize=(12, 14))
    plot.figure.savefig('plot.png')
    print 'Wrote plot.png'

if __name__ == '__main__':
    run()
