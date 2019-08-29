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
    df_ds = pd.read_csv('../clean_updated_data_June2.csv', delimiter=',')
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
        p = np.random.poisson(5)
        c1.append(p if p < 10 else 9)
        p = np.random.poisson(5)
        c2.append(p if p < 10 else 9)
        p = np.random.poisson(5)
        c3.append(p if p < 10 else 9)
        p = np.random.poisson(5)
        c4.append(p if p < 10 else 9)
        p = np.random.poisson(5)
        c5.append(p if p < 10 else 9)

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
    df.to_pickle('static/fake_data_scientists.pkl')
    df.to_csv('static/fake_data_scientists.csv', sep=',', encoding='utf-8')


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
        string += '''<li><a href="{{ url_for('result', name = ''' + str(d) + ') }}"> ' + df.iloc[i].Last_Name +\
                  ', ' + df.iloc[i].First_Name + '</a></li>\n'

    string += '''
</ul>
</body>
</html>
    '''
    fn.write(string)


def write_string(df):
    string = '''
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
        string += '''<li><a href="{{ url_for('result', name = ''' + str(d) + ') }}"> ' + df.iloc[i].Last_Name + \
                  ', ' + df.iloc[i].First_Name + '</a></li>\n'

    string += '''
    </ul>
    '''
    return string


def write_table(df):
    columns = df.columns
    string = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 90%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #dddddd;
    }
    </style>
    </head>
    <body>

    <h1>
    <button onclick="goBack()" class="btn">Go Back</button>
    <button onclick="exportTableToCSV('selected_data_scientists.csv')" class="btn">Export HTML Table To CSV File</button>
    <script>
    function goBack() {
    window.history.back();
    }
    </script>
    </h1>
    <script src="https://www.w3schools.com/lib/w3.js"></script>
    <link href="https://www.w3schools.com/w3css/4/w3.css" rel="stylesheet" />
    '''
    string += "<h1>Top " + str(df.shape[0]) + ' results </h1> <ul>\n<table align="center" id="usersTable" class="w3-table-all">\n<tr>'

    for i, c in enumerate(columns):
        string += '''<th onclick="w3.sortHTML('#usersTable', '.item', 'td:nth-child(''' + str(i+1) + ''')')" style="cursor:pointer">''' +\
                  c.replace('_', ' ')+'</th>\n'
    string += '</tr>\n'
    for vs in df.values:
        string += '<tr class="item">\n'
        for v in vs:
            string += '<td>'+str(v).replace(',', ' ')+'</td>\n'
        string += '</tr>\n'

    string += '''
    </table>

    <script>
        function downloadCSV(csv, filename) {
        var csvFile;
        var downloadLink;
    
        // CSV file
        csvFile = new Blob([csv], {type: "text/csv"});
    
        // Download link
        downloadLink = document.createElement("a");
    
        // File name
        downloadLink.download = filename;
    
        // Create a link to the file
        downloadLink.href = window.URL.createObjectURL(csvFile);
    
        // Hide download link
        downloadLink.style.display = "none";
    
        // Add the link to DOM
        document.body.appendChild(downloadLink);
    
        // Click download link
        downloadLink.click();
    }

    function exportTableToCSV(filename) {
        var csv = [];
        var rows = document.querySelectorAll("table tr");
    
        for (var i = 0; i < rows.length; i++) {
            var row = [], cols = rows[i].querySelectorAll("td, th");
    
            for (var j = 0; j < cols.length; j++)
                row.push(cols[j].innerText);
    
            csv.push(row.join(","));
        }
    
        // Download CSV file
        downloadCSV(csv.join("\\n"), filename);
    }


    </script>

    </ul>
    </body>
    </html>
    '''
    return string


def calculate_proficiency():
    import json
    import operator

    df_ds = pd.read_excel(r'C:\Users\jchaves6\PycharmProjects\Capabilities\DataAnalyticsEEs-Updated.3.xlsx',
                          sheet_name='Email')

    print(df_ds.head())

    df_ds.drop_duplicates(subset="WWID", keep='first', inplace=True)

    print(df_ds.head())
    with open(r'C:\Users\jchaves6\PycharmProjects\Capabilities\capability.json') as json_file:
        data = json.load(json_file)

    profs = {}

    analytics = data['analytics'] + [['analytics', 1.0]]
    prof_anas = []
    df_ds = df_ds.replace(np.nan, '')
    for w, ed, ind, eq, inq in zip(df_ds['WWID'], df_ds['Ext Desc'], df_ds['Int Desc'], df_ds['Ext Qual'], df_ds['Int Qual']):
        prof_ana = 0
        for a in analytics:
            # print(ed)
            prof_ana += ed.count(a[0])*a[1]*.09
            prof_ana += ind.count(a[0]) * a[1]*0.9
            prof_ana += eq.count(a[0]) * a[1]*1.1
            prof_ana += inq.count(a[0]) * a[1]*1.1
        prof_anas.append(prof_ana)
        profs[w] = prof_ana

    sorted_profs = sorted(profs.items(), key=operator.itemgetter(1), reverse=True)

    print(sorted_profs)
