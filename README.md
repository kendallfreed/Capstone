# Capstone Overview

## Solution Summary
    
&nbsp; &nbsp; &nbsp; With the current state of housing in Final Fantasy 14 frustrating players and developers, third-party tools and illegal in-game house transactions have increased. Square Enix has also struggled to crack down on this and understand how popular housing truly is.


&nbsp; &nbsp; &nbsp; This application helps address both issues. It gives some power to the players by allowing them to see how many bids will likely be placed on each house. This gives players confidence to place a bid and walk away without checking the number of bids at each house throughout the period. It also decreases the usage of third-party tools and illegal purchasing of in-game houses with real money. Likewise, it also gives Square Enix information on which house combinations are most popular, how many bids are placed on each house, and the availability of particular houses.	


&nbsp; &nbsp; &nbsp; This application has users enter the data for the house they want to bid on and returns the predicted number of entries along with a histogram for that particular plot. Using a machine learning model with Linear Regression, the model takes the housing data and returns a predicted number of lottery entries. The model is loaded into the Python back-end, and the front-end uses Streamlit with Python. 


## Data Summary

&nbsp; &nbsp; &nbsp; The data for the housing was all graciously collected by Paissa DB, a tool used to store the number of bids on each plot throughout the lottery period process. This Excel sheet of data was made publicly available to the Final Fantasy 14 housing community members.


&nbsp; &nbsp; &nbsp; The data was trimmed down so that only the necessary columns and rows were needed. For this application, we limited our data set to only the North American worlds and removed the newest worlds since they did not have sufficient data. We examined this with our model and got a very low score of lottery entry predictions (20%, when 80% and above is ideal). Thus, we tried one-hot encoding the worlds and districts, as the machine learning model can examine relationships with categorical data more easily once it’s one-hot encoded. This did not help much, and we still got a very low score (25%). We then looked at engineering features. At first, we added average district and average ward entries. This helped, and we got a higher score (75%) but wanted a more accurate model. We then decided that each world would be examined by taking a plot's number of entries and dividing it by the total entries in the world it was on. This gave us our new feature, 'plot popularity.' The plot popularity gave us a high score of 90.86%. 


&nbsp; &nbsp; &nbsp; The plot popularity was the main feature we used for our model after finding the score. However, because the popularity of a plot is the main feature of our model, we needed to generate this in the Python file after a user entered their plot information. The user does not know the 'plot popularity' and shouldn't need to. We downloaded the data frame for the world and plot's plot popularity and used this in the back end to feed the model. 

 
 &nbsp; &nbsp; &nbsp; Along with giving the user the number of entries, we also wanted them to see the number of entries on a plot historically. We added the data frame that included lottery entry numbers into the Python backend and generated a histogram that shows the historical number of lottery entries for their particular plot. If there isn't a history for that plot, it uses the history of the worlds from that particular data center.

 
 &nbsp; &nbsp; &nbsp; The model will be updated periodically to maintain the application as new housing data is collected through Paissa DB. The current housing data was from a year and a half ago. The number of entries for each plot could have shifted since then and should be evaluated regularly.  


## Machine Learning  
	
&nbsp; &nbsp; &nbsp; For our machine learning model, we used Linear Regression. Linear regression takes plotted data points and attempts to find the best fit 'line' for the data. Because we have some direct correlation with our data points, linear regression seemed the best model. For example, a large house in the beach district on a popular world would receive the most lottery entries based on those features. A small house in a desert district in a low-popular world wouldn't receive many entries. 

&nbsp; &nbsp; &nbsp; We took advantage of the Python library sklearn and its linear regression model to develop the machine learning model. This library also allows you to 'score' the model which gives you several how well the model is fitting to the data. This score is how we created features and worked with our data to find the best way to model it accurately.

## Validation 

&nbsp; &nbsp; &nbsp; We validated the linear regression in various ways. We first used the score() function to score the model. Anything above .8 was what we wanted to see (this equates to an 80% accuracy). With our feature engineering we generated a score of 90.86% accuracy. This gave us the confidence that our model was ready and valid.

&nbsp; &nbsp; &nbsp; We also used a heatmap to look at all the features while working with the data. We found that house size and average district entries had some correlation but were not strong enough for a model. When we added plot popularity as the new feature, that's when we saw a strong correlation of .96 in the heatmap. 
	
&nbsp; &nbsp; &nbsp; We also validated the model by testing it with various user entries. This was where we discovered some plots didn't have a history on their world, and thus we needed to take an average of the plot popularity from that plot in the worlds on that data center. Once we did that, we found it worked for each entry. 

## Visualizations  

 &nbsp; &nbsp; &nbsp; Here is the heatmap we used, which is also included in the attachments:

 
 &nbsp; &nbsp; &nbsp; This is a histogram we used to also visualize the data and their correlations and is included in the attachments: 

 
&nbsp; &nbsp; &nbsp; When a user selects their plot information, a histogram of previous house entries is returned on the front end. Here is an example:
 
## User Guide to Download and Run Application  


1.	Download the zip file and extract it.  


2.	Download Python, pip packet manager, and Visual Studio Code (or preferred IDE).  
> a.	Python download: https://www.python.org/downloads/windows/  
> b.	Pip instructions (if not included in Python installation): https://pip.pypa.io/en/stable/installation/  
> c.	Visual Studio Code: https://code.visualstudio.com/download  


3.	Open Visual Studio Code (or preferred IDE) and open the ‘app.py’ file.   


4.	Create a terminal window in your IDE and navigate to the folder where app.py and other files are. Type these commands to install the necessary packages and start the front-end:   
> a.	venv mlenv  
> b.	.mlenv\Scripts\activate  
> c.	pip install scikit-learn  
> d.	pip install joblib  
> e.	pip install numpy  
> f.	pip install pandas  
> g.	pip install matplotlit  
> h.	pip install fastapi  
> i.	pip install streamlit  
> j.	streamlit run app.py  


5.	Create another terminal window in your IDE. Navigate to the folder where app.py and the other files are and type:  
> a.	pip install uvicorn  
> b.	uvicorn back_end:app –reload  
> 6.	A browser window should pop up with the application. You can now select different inputs for the plot you wish to receive predictions on and see the output below after hitting the 'Predict Lottery Entries' button.  


 
## Reference Page

Zhu, Andrew. “Zhudotexe/FFXIV_PAISSADB: Companion API for the Paissahouse Plugin.” GitHub, github.com/zhudotexe/FFXIV_PaissaDB. Accessed March 13 2025. 


Zhu, Andrew. Paissa DB, zhu.codes/paissa. Accessed 13 Mar. 2025.
