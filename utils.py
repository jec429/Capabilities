import pandas as pd
from random import randint, sample
import names
import numpy as np
from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(self, value)
                        for value in values)


def generate_fake_file():
    df = pd.DataFrame()
    df_ds = pd.read_csv('../data_scientists/clean_updated_data_June2.csv', delimiter=',')
    positions = list(df_ds[df_ds['FLAG']==True]['Position'].values)
    pos = [x.split('-')[0].upper() for x in positions]
    wwids = []
    mgr_wwids = []
    firsts = []
    lasts = []
    mgrs = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    c5 = []

    nrand = 50

    for x in range(nrand):
        print(randint(1063055, 1074166))
        wwids.append(randint(1063055, 1074166))
        mgr_wwids.append(randint(1063055, 1074166))
        firsts.append(names.get_first_name())
        lasts.append(names.get_last_name())
        mgrs.append(names.get_full_name())
        c1.append(np.random.poisson(5))
        c2.append(np.random.poisson(5))
        c3.append(np.random.poisson(5))
        c4.append(np.random.poisson(5))
        c5.append(np.random.poisson(5))

    jobs = sample(pos, nrand)

    df['WWID'] = wwids
    df['First_Name'] = firsts
    df['Last_Name'] = lasts
    df['Position'] = jobs
    df['Manager WWID'] = mgr_wwids
    df['Manager'] = mgrs
    df['Modeling'] = c1
    df['Analytics'] = c2
    df['Programming'] = c3
    df['Statistics'] = c4
    df['Insights'] = c5

    df.info()
    print(df.head(10))
    df.to_pickle('fake_data_scientists.pkl')
    df.to_csv('fake_data_scientists.csv', sep=',', encoding='utf-8')


def write_html(df):
    fn = open('./templates/key_results.html', 'w', encoding='utf-8')
    string = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>
<button onclick="goBack()">Go Back</button>
<script>
function goBack() {
window.history.back();
}
</script>
</h1>

    '''
    string += "<h1>Top " + str(df.shape[0]) + " results </h1> <ul>"

    for i, d in enumerate(df['WWID']):
        string += '<li><a href="http://localhost:5000/result/' + str(d) + '"> ' + df.iloc[i].Last_Name +\
                  ', ' + df.iloc[i].First_Name + '</a></li>\n'

    string += '''
</ul>
</body>
</html>
    '''
    fn.write(string)
