def operation():
    import os
    from dotenv import load_dotenv
    import paramiko
    import pandas as pd
    import datetime

    # Read from .env file.
    load_dotenv()
    env = os.environ.get

    # Create SSH client.
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())




    # Establish SFTP connection to origin remote server.
    ssh.connect(hostname=env("ORIGIN_HOSTNAME"), username=env("ORIGIN_USERNAME"), password=env("ORIGIN_PASSWORD"), port=22)
    print("SSH connection to origin remote server complete.")
    sftp_client = ssh.open_sftp()
    print("SFTP connection to origin remote server complete.")

    # Download "input_file.xlsx" from origin remote server.
    sftp_client.get(env("ORIGIN_FILE_PATH"), "/tmp/input_file.xlsx")
    print("Successfully downloaded 'input_file.xlsx'.")

    # Close SFTP connection to origin remote server.
    sftp_client.close()
    print("SFTP connection to origin remote server terminated.")
    ssh.close()
    print("SSH connection to origin remote server terminated.")



    # Create Pandas dataframe with downloaded file.
    df = pd.read_excel(r"/tmp/input_file.xlsx")

    # Create df that will be the first output file.
    df_output_1 = df

    # Create function that takes two columns (date & time) and creates a new single date_time column.
    def get_datetime(date, time):
        date_time = date.strftime("%Y-%m-%d") + " " + str(time)
        return date_time

    # Apply above function.
    df_output_1["SampleReceivedDate_Time"] = df_output_1.apply(lambda row: get_datetime(
        row["Received Date\n(YYYY-MM-DD)"],
        row["Received Time\n(24-hour format)"],
    ), axis = 1)

    # Add "AccessionOrderID" column, rename some columns, and select the desired columns for output.
    df_output_1["AccessionOrderID"] = ""
    df_output_1 = df_output_1.rename(columns={"Accession No. or\nClient Sample ID": "AccessionNumber"})
    df_output_1 = df_output_1[[
        "AccessionOrderID",
        "SampleReceivedDate_Time",
        "AccessionNumber",
    ]]

    # Write df_output_1 to "SampleReceiptFile.csv".
    df_output_1.to_csv(r"/tmp/SampleReceiptFile.csv")
    print("Successfully written df_output_1 to 'SampleReceiptFile.csv'.")



    # Create df that will be the second output file.
    df_output_2 = df

    # Add "AccessionOrderID" column, rename some columns, and select the desired columns for output.
    df_output_2["AccessionOrderID"] = ""
    df_output_2 = df_output_2.rename(columns={
        "Received Date\n(YYYY-MM-DD)": "SampleReceiptDate",
        "Reported Date\n(YYYY-MM-DD)": "ResultCompleteDate",
        "Result\n(Detected / Undetected)": "Result"
    })
    df_output_2 = df_output_2[[
        "AccessionOrderID",
        "Result",
        "SampleReceiptDate",
        "ResultCompleteDate",
    ]]

    # Write df_output_2 to "SampleResultResponse.csv".
    df_output_2.to_csv(r"/tmp/SampleResultResponse.csv")
    print("Successfully written df_output_2 to 'SampleResultResponse.csv'.")



    # Establish SFTP connection to destination remote server.
    ssh.connect(hostname=env("DESTINATION_HOSTNAME"), username=env("DESTINATION_USERNAME"), password=env("DESTINATION_PASSWORD"), port=22)
    print("SSH connection to destination complete.")
    sftp_client = ssh.open_sftp()
    print("SFTP connection to destination complete.")

    # Upload "SampleReceiptFile.csv" and "SampleResultResponse.csv" to destination remote server.
    sftp_client.put("/tmp/SampleReceiptFile.csv", env("DESTINATION_FILE_PATH_1"))
    sftp_client.put("/tmp/SampleResultResponse.csv", env("DESTINATION_FILE_PATH_2"))
    print("Successfully uploaded 'SampleReceiptFile.csv' and 'SampleResultResponse.csv' to destination remote server.")

    # Close SFTP connection to destination remote server.
    sftp_client.close()
    print("SFTP connection to destination terminated.")
    ssh.close()
    print("SSH connection to destination terminated.")

    print('\nOperation complete.')

operation()