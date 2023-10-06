#!/bin/bash


# Define the directory containing your notebooks and the Python interpreter path
NOTEBOOK_DIR="/Users/harrisonward/Desktop/CS/Git/xG/models"
SCRIPT_DIR="/Users/harrisonward/Desktop/CS/Git/xG/scripts"
PYTHON_INTERPRETER="/opt/anaconda3/envs/cs109b/bin/python"

# Run updater.py using the specified Python interpreter
"$PYTHON_INTERPRETER" "$SCRIPT_DIR/updater.py"

# List of notebooks to be converted and executed in order
NOTEBOOKS=("xG_model.ipynb" "xP_model.ipynb")

# Convert specified notebooks to Python scripts and execute them in order
for notebook_name in "${NOTEBOOKS[@]}"
do
    notebook_path="$NOTEBOOK_DIR/$notebook_name"
    
    # Check if notebook file exists
    if [ -f "$notebook_path" ]; then
        # Convert notebook to Python script
        jupyter nbconvert --to script "$notebook_path" --output-dir="$NOTEBOOK_DIR"
        
        # Extract the filename without extension
        filename_no_ext="${notebook_name%.*}"
        
        # Define the path to the generated Python script
        script_path="$NOTEBOOK_DIR/$filename_no_ext.py"
        
        # Execute the Python script
        if [ -f "$script_path" ]; then
            echo "Executing $script_path..."
            $PYTHON_INTERPRETER "$script_path"
        else
            echo "Error: Script $script_path not found!"
        fi
    else
        echo "Error: Notebook $notebook_path not found!"
    fi
done
