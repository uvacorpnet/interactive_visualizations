# interactive_visualizations
Python wrapper for D3 scatter plots using pandas dataframes


## To use
1. Add your csv file (with header) to the folder visualizations
2. Edit "interactive_viusalizations.py" (or "interactive_viusalizations.ipynb" if you use jupyter notebooks)
3. In the example part, write the column_names you want to study and it's legends (optional)
4. Edit the call to createHTML()

createHTML("test","data.pd",sep=",",column_names = column_names, legends = legends, x_col="gdp",y_col="sumR",label="country",fillby="incomeLevel",filterby="incomeLevel")

The first variable is the neame of your project
The second variable is the name of your dataframe
sep = separator
legends (optional)
x_col = default variable in the x axis
y_col = default variable in the y axis
label = identifiers
fillby and filterby = which variable to color and filter by

5. Run it (python interactive_visualizations.py)
