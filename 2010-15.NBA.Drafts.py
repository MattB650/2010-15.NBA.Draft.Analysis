import pandas as pd
import plotly.express as px

sheet = pd.read_csv('~/Desktop/College.Draft.Project/Combined.Draft.csv', index_col=0, encoding='cp1252')

#Remove Rows Where WS is null (Did not play in NBA)
#sheet = sheet[sheet['WS'].notna()]

#Remove Rows Where FIC is null(Did not have pre-draft season that met requirements)
sheet = sheet.query('FIC!=0')

sheet['Adjusted Draft Score'] = sheet['Z-Score']

fig = px.scatter(sheet, x='FIC', y='Adjusted Draft Score', color='Adjusted Draft Score',
                 title='NBA 2010-15 Drafts: Floor Impact Counter vs Adjusted Draft Score',
                 hover_data=(['Player', 'Pos', 'Year', 'FIC', 'Adjusted Draft Score']))

fig.update_traces(mode='markers', marker_size=15)

fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)

fig.show()

cc = sheet[['VA', 'Draft Score']]

correlation = cc.corr(method='pearson')

#print(correlation)