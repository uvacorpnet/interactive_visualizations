import os
import pandas as pd
from shutil import copyfile

#Takes a filename, creates all the files 
def returnFilter(df,variable_name):
    t1 = "\nsvg.selectAll(\".dot2\")\n\t.filter(function(d) {{\n\t\tconsole.log(d.{0});\n\t\treturn selected == d.{0};\n\n\t}})\n\t.attr(\"display\", display);\n\t}});\n\n\n".format(variable_name)
  
    t2 = "\t<div id=\"filter\">\n\t\t<b>{0} Filter:</b><br>".format(variable_name)
    
    for i in sorted(list(set(df[variable_name]))):
        t2 += "\n\t\t<input name='v' value=\"{0}\" type=\"checkbox\" checked>{0}</input><br>".format(i)
    t2 += "\n\t</div>"
    
    return t1,t2
    
def returnQunatit(df,legends,filename):
    t1 = "<div id=\"label\"><b>x-Axis:</b></div>\n\t<select name=\"xAX\" id=\"xAXs\">"
    t2 = "<div id=\"labels\"><b>y-Axis:</b></div>\n\t<select name=\"yAX\" id=\"yAXs\">"
    t0 = "<form id=\"mark\">\n<b>Size of Mark:</b>\n<div><input type=\"radio\" name=\"sepal\" value='reset' checked=\"checked\">reset</div>"
    axisNames = "var axisNames = {"
    readData = "d3.csv(\"{0}\", function(error, data) {{\n\t data.forEach(function(d) {{".format(filename)
    
    
    
    for type_col,col,leg in zip(df.dtypes,df.columns,legends):
        if "float" in str(type_col) or "int" in str(type_col):
            t1 += "\n\t\t<option value =\"{0}\">{1}</option>".format(col,leg)
            t2 += "\n\t\t<option value =\"{0}\">{1}</option>".format(col,leg)
            t0 += "\n\t\t<div><input type=\"radio\" name=\"sepal\" value='{0}'>{1}</div>".format(col,leg)
            axisNames += "\n\t {0}: '{1}',".format(col,leg)
            readData += "\n\t\td.{0} = +d.{0};".format(col)
    t1 += "\n</select>"
    t2 += "\n</select>"
    
        
    axisNames = axisNames[:-1] + "\n\t};\n"
    readData += "\n});\n\n"
        
    return readData,axisNames, t0,t1,t2

def createHTML(name,filename,sep="\t",column_names = [], legends = [],scale="log",x_col="",y_col="",filterby="",fillby="",label=""):
    
    #make folder inside visualizations
    if not name in os.listdir("./visualizations/"):
        os.mkdir("./visualizations/{0}".format(name))
    
    #copy files from required_file there
    for file in os.listdir("./visualizations/required_files"):
        copyfile("./visualizations/required_files/{0}".format(file),"./visualizations/{1}/{0}".format(file,name))
    
    copyfile("./visualizations/{0}".format(filename),"./visualizations/{1}/{0}".format(filename,name))
    
    df = pd.read_csv("./visualizations/"+filename,sep=sep,index_col=None)
    #normalize that
    
       
    if len(column_names) > 0:
        df = df.loc[:,column_names]
    
    if len(legends) > 0 and len(legends) == len(column_names):
        pass
    else:
        legends = df.columns
    

    if scale == "log":
        scale = "\nvar x = d3.scale.log().range([0, width]); \nvar y = d3.scale.log().range([height, 0]);\n\n"
    else:
        scale = "\nvar x = d3.scale.linear().range([0, width]); \nvar y = d3.scale.linear().range([height, 0]);\n\n"    
        
    fillby = "\n.style(\"fill\", function(d) {{ return color(d.{0}); }})".format(fillby)    
    label = "\n.attr(\"id\", function(d) {{ return d.{0}; }})".format(label)        
    
   
    if not x_col or x_col not in df.columns: x_col = df.columns[0]
    if not y_col or y_col not in df.columns: y_col = df.columns[1]
    
    x_and_y = "x.domain(d3.extent(data, function(d) {{ return d.{0}; }})).nice();\ny.domain(d3.extent(data, function(d) {{ return d.{1}; }})).nice();".format(x_col,y_col)
    x_and_y_labels = "\n\n\tsvg.append(\"g\")\n\t\t.attr(\"class\", \"x axis\")\n\t\t.attr(\"transform\", \"translate(0,\" + height + \")\") \
                    \n\t\t.call(xAxis)\n\t\t.append(\"text\")\n\t\t.attr(\"class\", \"label\")\n\t\t.attr(\"x\", width)\n\t\t.attr(\"y\", -6)\n \
                    \t\t.style(\"text-anchor\", \"end\")\n\t\t.text(\"{0}\");\n\n\tsvg.append(\"g\")\n\t\t.attr(\"class\", \"y axis\")\n\t\t.call(yAxis)\n\t\t.append(\"text\") \
                    \n\t\t.attr(\"class\", \"label\")\n\t\t.attr(\"transform\", \"rotate(-90)\")\n\t\t.attr(\"y\", 6)\n\t\t.attr(\"dy\", \".71em\")\n\t\t.style(\"text-anchor\", \"end\") \
                    \n\t\t.text(\"{1}\");".format(x_col,y_col)
    line = "\n\nvar line = svg.append('line')\n\t  .data(data)\n\t\t  .attr(\"class\", \"line\")\n\t\t.attr('x1',x(1E-6))\n\t\t.attr('x2',x(0.3))\n\t\t.attr('y1',y(1E-6))\n\t\t.attr('y2',y(0.3))\n\t\t.attr(\"stroke-width\", 2)\n\t\t.attr(\"stroke\", \"black\");\n\t\t"

    circles = "\nvar circles = svg.selectAll(\".dot\")\n\t  .data(data)\n\t  .enter().append(\"circle\")\n  \
                .attr(\"class\", \"dot2\")\n\t  .attr(\"r\", 4.5)\n\t  .attr(\"cx\", function(d) {{ return x(d.{0}); }})\n\t  .attr(\"cy\", function(d) {{ return y(d.{1}); }})\n\t \
                {2}{3}\n  .style(\"opacity\", .8);\n\t".format(x_col,y_col,fillby,label)
    
    readData,axisNames,t_q0,t_q1,t_q2 = returnQunatit(df,legends,filename)
    t_f1,t_f2 = returnFilter(df,filterby)
    script = "</script>\n<br><br>\n{0}\n{1}\n{2}\n{3}\n<br>\</body>".format(t_f2,t_q0,t_q1,t_q2)
      

    html = ""
    html += open("./visualizations/header.txt").read()
    html += scale
    html += axisNames
    html += open("./visualizations/header2.txt").read()
    html += readData
    html += x_and_y
    html += x_and_y_labels
    html += line
    html += circles
    html += open("./visualizations/commonJS.txt").read()
    html += t_f1
    html += open("./visualizations/commonJS2.txt").read()
    html += script
    open("./visualizations/{0}/index.html".format(name),"w+").write(html)
    
    
    ## Example
column_names = ["sumR", "nNOTNull", "nNull", "gdp", "averageR", "stdR", "varR", "maxR", "gdppp", "fanoR", "percComp", "nOrbis", "percComp", "completeness", "Value", "scale", "mu","incomeLevel"]
legends =  ['Sum of company revenue',  'Number of available revenues',  'Number of missing revenues',  'gdp', 'Average Revenue', 'Revenue STD', 'Revenue Variance', 'Max revenue', 
      'gdp per capita', 'Fano factor revenue', 'Ratio available/missing revenues', 'number of companies in Orbis', 'perc of companies with info', 
      'perc of companies compared with ext. sources', 'number of companies in external sources', 'std fitted lognormal', 'mu fitted lognormal',"incomeLevel"]

createHTML("test","data.pd",sep=",",column_names = column_names, legends = legends, x_col="gdp",y_col="sumR",label="country",fillby="incomeLevel",filterby="incomeLevel")
