import os
import pandas as pd

def execute():
    # Define the folder containing the data files
    folder_path = '2023-24/gamelogs/'

    # Define the output folder for new files
    output_folder = '2023-24/averages/'

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize an empty DataFrame to store the combined data
    combined_data = pd.DataFrame()

    # Iterate through files in the folder
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):  # Assuming your files are in CSV format
                file_path = os.path.join(folder_path, filename)

                # Read data from the current file into a DataFrame
                current_data = pd.read_csv(file_path, delimiter='\t')  # You may need to adjust read_csv options
                selected_model_cols = current_data.loc[:, ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'REB', 'AST', 'STL', 'BLK', 'PTS', 'PLUS_MINUS']]
                column_averages = selected_model_cols.mean().round(2)

                # Create a new DataFrame with column names and averages
                averages_df = pd.DataFrame([column_averages], columns=selected_model_cols.columns)

                # Create a new file with the same name in the output folder
                output_file_path = os.path.join(output_folder, filename)
                averages_df.to_csv(output_file_path, index=False)

    except UnicodeDecodeError:
        pass
