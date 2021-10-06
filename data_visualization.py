import numpy as np  # numpy used to create data from plotting
import seaborn as sns  # common form of importing seaborn

# Generate normally distributed data
data = np.random.randn ( 1000 )
# Plot a histogram with both a rugplot and kde graph superimposed
sns.distplot ( data , kde = True , rug = True )
# Using previously created imports and data.
# Use a dark background with no grid.
sns.set_style ( 'dark' )
# Create the plot again
sns.distplot ( data , kde = True , rug = True )

# Using previously created data and style
# Access to matplotlib commands
import matplotlib.pyplot as plt

# The previously created plot.
sns.distplot ( data , kde = True , rug = True )
# Set the axis labels.
plt.xlabel ( 'This is my x-axis' )
plt.ylabel ( 'This is my y-axis' )
