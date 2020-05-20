This two scripts are for measuring subsctration between columns .
- Please check the below instructions to use the script :
- The scripts is using panda and bokeh python libraries for calculations and draw plots

Step 1) 
You will run the mcast-latency.py script as a daemon process .
Usage:

    ~ python /mcast-latency.py -i multicast-ip  -p port -e $(hostname -i) &
    -i  multicast IP
    -p multicast port
    -e IP of the server that you are running the script.

Output on Shell will create a CSV file plus some instructions :

        CSV File output_Date_time.csv has been created!
        Please note that CSV files will be named the same as with/without the -R Flag! 


Step 2)
Then to create the delta/subsctraction graphs after a period of time recording traffic  please run it as python3 as follows :

    ~ pthon3 csv-plot.py CSV-file-that-was-created-from-above
    
    Output on Shell will create a HTML :
    Please download plot_date-time.html and open it in your local machine
    Open the htlm file and you see bokeh 3 graphs in one row measurements
    

