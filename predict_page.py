import streamlit as st
import requests
import joblib as jb
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO

#Function to show the prediction application
def show_predict_page():
    st.title("Final Fantasy 14 Housing Lottery Entry Predictor")
    st.write("This application predicts the likely amount of lottery entries for a house in Final Fantasy 14 based on the popularity of the plot.")
    
    world = (
        "Adamantoise",
        "Balmung",
        "Behemoth",
        "Brynhildr",
        "Cactuar",
        "Coeurl",
        "Diabolos",
        "Excalibur",
        "Exodus",
        "Faerie",
        "Famfrit",
        "Gilgamesh",
        "Goblin",
        "Hyperion",
        "Jenova",
        "Lamia",
        "Leviathan",
        "Malboro",
        "Mateus",
        "Midgardsormr",
        "Sargatanas",
        "Siren",
        "Ultros",
        "Zalera"
    )

    district = (
        "Mist",
        "The Lavender Beds",
        "The Goblet",
        "Shirogane",
        "Empyreum"
    )

    ward_number = (
        "1","2","3","4","5","6","7","8","9","10",
        "11","12","13","14","15","16","17","18","19","20",
        "21","22","23","24","25","26","27","28","29","30"
    )

    plot_number = (
        "1","2","3","4","5","6","7","8","9","10",
        "11","12","13","14","15","16","17","18","19","20",
        "21","22","23","24","25","26","27","28","29","30",
        "31","32","33","34","35","36","37","38","39","40",
        "41","42","43","44","45","46","47","48","49","50",
        "51","52","53","54","55","56","57","58","59","60"
    )
    #Container holding the user input value options
    with st.container(border=True):
        world = st.selectbox("Server", world)

        district = st.selectbox("District", district)

        ward_number = st.number_input("Ward Number (1 - 30)", min_value=1, max_value=30, value=1, step=1, label_visibility="visible")
        plot_number = st.number_input("Plot Number (1-60)", min_value=1, max_value=60, value=1, step=1, label_visibility="visible")   
    
    st.write("You've selected: ", world, district, "  -  Ward:", ward_number, "Plot:", plot_number)
    if st.button("Predict Lottery Entries"):
        #Predict the number of entries
        get_prediction(world, district, ward_number, plot_number)
 


#Function to send data to backend API
def get_prediction(world, district, ward_number, plot_number):
    #Collect user input data in dict
    user_data = {
        "world": world,
        "district": district,
        "ward_number": ward_number,
        "plot_number": plot_number
    }

    #Send data as a POST request to FastAPI, address is what uvicorn sets as default address, adjust if needed
    response = requests.post("http://127.0.0.1:8000/predict", json=user_data)

    #Display prediction result or error
    if response.status_code == 200:
        #prediction = response.json()["prediction"]
        prediction = response.json()
        st.write("The predicted number of entries for this plot is ", prediction)
        st.write("Good luck!\n")
        show_stats(user_data)

    else:
        st.write(f"Error: {response.json()['error']}")
        st.write("Uh-oh. Something went wrong on our end. Please try again later.")

#Function to show the stats
def show_stats(user_data):
    response = requests.get("http://127.0.0.1:8000/stats", json=user_data)
    if response.status_code == 200:    
        #Get the data from the response
        data = response.json()
        data = data['house_plot_entries']
        #data = data.reshape(-1,1)
        #Create a histogram of the data
        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        height, bins, patches = ax.hist(data, bins=10, edgecolor='black')
        
        #To do: Fix ticks

        ticks = [(patch.get_x() + (patch.get_x() + patch.get_width()))/2 for patch in patches]
        ticklabels = (bins[1:] + bins[:-1]) / 2
        ax.set_xticks(ticks)
        plt.xticks(ticks, np.round(ticklabels, 2), rotation=90)
        #ax.bar(range(len(data)), height, width = 1, align = 'center')
        
        #ax.set(xticks = range(len(data)), xlim = [0, len(data)])
        #ax.set_xticks(np.arange(0, max(bins), (int(max(bins)/6))))
        
        #Add data labels to the bars and center bars around ticks
        for i, patch in enumerate(patches):
            bin_center = (bins[i] + bins[i+1]) / 2
            height = patch.get_height()
            if height > 0:
                ax.text(bin_center, height/2, f'{int(bin_center)}', ha='center', va='bottom', fontsize=9)
        
        #for bin_edge, patch in zip(bins[:-1], patches):
            #height = patch.get_height()
            #if height > 0:
               # ax.text(patch.get_x() + patch.get_width()/2, height/2, 
                #        f'{int(bin_edge)}', ha='center', fontsize=9)
        
        #Labels and titles for histogram
        ax.set_title("Distribution of Plot Entries for Plot Number")
        ax.set_xlabel("Number of Entries")
        ax.set_ylabel("Frequency of Exact Entries")
        
        #Render histogram via Streamlit
        st.pyplot(fig)
    else:
        st.write("Uh-oh. Something went wrong on our end. Chart unable to load. Please try again later.")
    



    