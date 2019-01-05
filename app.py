from flask import Flask,render_template,request,redirect,session
import requests, pandas
import simplejson as json
from bokeh.plotting import figure
from bokeh.embed import components 

app = Flask(__name__)

app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/stocks', methods=['POST'])
def graph():

        app.vars['ticker'] = request.form['ticker'] 
        # Pass the ticker to the Quandl URL to get the raw data. Use the key obtained from the Quandl website       
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/{}.json?api_key=XFqCpJrHuCwSuEs8h94z'.format(app.vars['ticker'])
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)
        # Get the raw json data
        a = raw_data.json()
        # Save the stocks data in pandas dataframe
        df = pandas.DataFrame(a['data'], columns=a['column_names'])
        # Convert data to datetime format for plotting
        df['Date'] = pandas.to_datetime(df['Date'])

        p = figure(title='Stock price variation for {}'.format(app.vars['ticker']), x_axis_label='date', x_axis_type='datetime')
        
        # Add a line to the figure corresponding to the type of data selected
        if request.form.get('Close'):
            p.line(x=df['Date'].values, y=df['Close'].values,line_width=2, legend='Close')
        if request.form.get('Adj. Close'):
            p.line(x=df['Date'].values, y=df['Adj. Close'].values,line_width=2, line_color="green", legend='Adj. Close')
        if request.form.get('Open'):
            p.line(x=df['Date'].values, y=df['Open'].values,line_width=2, line_color="red", legend='Open')
        if request.form.get('Adj. Open'):
            p.line(x=df['Date'].values, y=df['Adj. Open'].values,line_width=2, line_color="purple", legend='Adj. Open')

        # Use bokeh's components function to get the plot data (script) and the <div> tag (div) for the figure to be built
        script, div = components(p)
      
        return render_template('stocks.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507, debug=True, use_reloader=False)