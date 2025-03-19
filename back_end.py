import joblib as jb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import FastAPI
from fastapi.responses import FileResponse

#Load the model, dataframe, and assign FastAPI to app
model = jb.load('housing_predictor1.pkl')
saved_df = jb.load("dataframe1.csv")
cleaned_df = jb.load("df_with_entries.csv")
app = FastAPI()

#Create lists of worlds and dataframes for each datacenter
aether = ["Adamantoise", "Cactuar", "Faerie", "Gilgamesh", "Jenova", "Midgardsormr", "Sargatanas", "Siren"]
aether_df = saved_df[saved_df["world"].isin(aether)]
aether_df_entries = cleaned_df[cleaned_df["world"].isin(aether)]
crystal = ["Balmung", "Brynhildr", "Coeurl", "Diabolos", "Goblin", "Malboro", "Mateus", "Zalera"]
crystal_df = saved_df[saved_df["world"].isin(crystal)]
crystal_df_entries = cleaned_df[cleaned_df["world"].isin(crystal)]
primal = ["Behemoth", "Excalibur", "Exodus", "Famfrit", "Hyperion", "Lamia", "Leviathan", "Ultros"]
primal_df = saved_df[saved_df["world"].isin(primal)]
primal_df_entries = cleaned_df[cleaned_df["world"].isin(primal)]

#Future idea: Make it better by creating a function to be called for each datacenter as extra data for people to see.

#Histogram creation of spread of plot entries for the server for this plot number
@app.get("/stats")
def stats(data: dict):
      user_df = pd.DataFrame([data])
      #If the world is in the data center with the plot information, merge the datafromes.
      #Otherwise merge with the entire datacenter for statistical information.
      if data["world"] in aether:
            if ((aether_df["world"] == data["world"]) & (aether_df["district"] == data["district"]) & (aether_df["plot_number"] == data["plot_number"])).any():
                merged_df = pd.merge(user_df,aether_df_entries, on=["world", "district", "plot_number"], how="left")
            else:
                 merged_df = pd.merge(user_df,aether_df_entries, on=["district", "plot_number"], how="left")           
            print(merged_df["lotto_entries"])
      elif data["world"] in crystal:
            if ((crystal_df["world"] == data["world"]) & (crystal_df["district"] == data["district"]) & (crystal_df["plot_number"] == data["plot_number"])).any():
                merged_df = pd.merge(user_df,crystal_df_entries, on=["world", "district", "plot_number"], how="left")
            else:
                merged_df = pd.merge(user_df,crystal_df_entries, on=["district", "plot_number"], how="left")
            print(merged_df["lotto_entries"])
      elif data["world"] in primal:
            if((primal_df["world"] == data["world"]) & (primal_df["district"] == data["district"]) & (primal_df["plot_number"] == data["plot_number"])).any():
                  merged_df = pd.merge(user_df,primal_df_entries, on=["world", "district", "plot_number"], how="left")
            else: 
                  merged_df = pd.merge(user_df,primal_df_entries, on=["district", "plot_number"], how="left")
            print(merged_df["lotto_entries"])
      return {"house_plot_entries": merged_df["lotto_entries"].tolist()}


@app.post("/predict")
def predict(data: dict):
   user_df = pd.DataFrame([data])
   print("User Data: \n", user_df)
   merged_df = pd.merge(user_df,saved_df, on=["world", "district", "ward_number", "plot_number"], how="left")
   if pd.isna(merged_df["plot_popularity"].loc[0]):
       print("Entering if loop statemment")
       # Merge user dataframe with dataframe of server info.
       merged_df = pd.merge(user_df,saved_df, on=["world", "district", "plot_number"], how="left")
      # If specific plot history without ward identifier doesn't exist on the server, take average of all ward number from all servers in that datacenter.
       if len(merged_df) == 1 and merged_df["world"].iloc[0] in aether:
             print("Entering Aether if loop")
             merged_df= pd.merge(user_df,aether_df, on=["district", "plot_number"], how="left")
             print(merged_df)
             plot_popularity = merged_df["plot_popularity"].mean()
             print("Mean Plot popularity from merged DF",plot_popularity)
             plot_popularity = np.array(plot_popularity).reshape(1, -1)
             prediction = model.predict(plot_popularity)
             return (int(prediction[0]))       
       elif len(merged_df) == 1 and merged_df["world"].iloc[0] in crystal:
             merged_df= pd.merge(user_df,crystal_df, on=["district", "plot_number"], how="left")
             print(merged_df)
             plot_popularity = merged_df["plot_popularity"].mean()
             plot_popularity = np.array(plot_popularity).reshape(1, -1)
             prediction = model.predict(plot_popularity)
             return (int(prediction[0]))       
       elif len(merged_df) == 1 and merged_df["world"].iloc[0] in primal:
             merged_df= pd.merge(user_df,primal_df, on=["district", "plot_number"], how="left")
             print(merged_df)
             plot_popularity = merged_df["plot_popularity"].mean()
             plot_popularity = np.array(plot_popularity).reshape(1, -1)
             prediction = model.predict(plot_popularity)
             return (int(prediction[0]))
         
       # Plot number has been found, but ward number is missing. 
       # Take mean of plot popularity for all ward numbers for that specifc plot number from server.
       print("Plot history exists on server, but not the specific ward. Taking mean of plot popularity for all ward numbers.")
       print(merged_df)
       plot_popularity = merged_df["plot_popularity"].mean()
       plot_popularity = np.array(plot_popularity).reshape(1, -1)
       prediction = model.predict(plot_popularity)
       return (int(prediction[0]))
   else:
       print("Plot history exists on server for both ward and plot.")
       print(merged_df)
       plot_popularity = merged_df["plot_popularity"].mean()
       plot_popularity = np.array(plot_popularity).reshape(1, -1)
       prediction = model.predict(plot_popularity)
       print ("Prediction Type: ", type(prediction))
       return (int(prediction[0]))
      