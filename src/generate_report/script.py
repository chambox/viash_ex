#imports 
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px 
import plotly.offline as py_offline
import os 
import seaborn as sns

import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader

from weasyprint import HTML
# import logging 
# import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logging.info('Generating report.pdf file ...')

# Report template
env = Environment(loader=FileSystemLoader('.')) 
report_template = env.get_template("data/templates/report.html")


#get data  and year boolean (I will choose 2015)
data = pd.read_csv('data/filtered.csv')


results_proj_counts = data.groupby(['project','person'])['duration'].sum().reset_index()
results_proj = results_proj_counts.groupby('project').sum().T
results_proj['Total'] = results_proj.T.sum()
results_proj = results_proj.T.reset_index()

year = pd.to_datetime(data.time_start).dt.year[0]
data['months'] = pd.to_datetime(data.time_start).dt.month

## create barplot 
fig = px.bar(data, x='months',
                   y="duration", color="person", title="Long-Form Input")
plot_data =[]
for person in data.person.unique():
    plot_data.append(go.Bar(name=person,
                             x=list(data[data.person==person]['months']),
                             y=list(data[data.person==person]['duration']))
    )
fig = go.Figure(plot_data)
fig.update_layout(
    barmode='stack',
    title="Figure",
    yaxis_title="Time(hours)",
    xaxis_title="Month",
    legend_title="Person",
    xaxis = dict(
        tickmode = 'array',
        tickvals = data['months'],
        ticktext = [str(k) for k in  pd.to_datetime(data.time_start).dt.to_period('M') ]
    )
);
## image paths 
image_path = 'data/images'
image_name = 'fig1.png'
if not os.path.exists(f"{image_path}"):
    os.mkdir(image_path)
fig.write_image(f"data/images/{image_name}")


### built html
template_vars = {"title1" :f"Project report anno {year}",
                 "table1": results_proj_counts.to_html(),
                 "num_worked":len(results_proj_counts.person.unique()),
                 "num_proj":len(results_proj_counts.project.unique()),
                 "total_num_hours":results_proj_counts.duration.sum(),
                 "table2":results_proj.to_html(),
                 "figure":f'{"file://"}{os.path.dirname(os.path.abspath(image_path))}/{image_path.split("/")[1]}/{image_name}'
                 }


#Render variables
html_out = report_template.render(template_vars)
HTML(string=html_out).write_pdf("output/report.pdf"
                                 ,stylesheets=["data/styles/stylesheet.css"]
                                )

logging.info('report.pdf file has been generated and placed into the output folder')
