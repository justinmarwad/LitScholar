# LitScholar # 

This is a project that will help you automate your literature review during the research gap process of PhD research. 

This project uses the library scholarly to search for papers and then Pandas to create a dataframe with the results and save them as an excel file.

## Usage

1. Install the requirements.txt file with `pip install -r requirements.txt`
2. Run the code with `python litscholar.py --query "your query here" --num_results 10`. You can add "--cited_by" to add a row that shows the number of citations for each paper.

3. Optional: Create Exe. `pyinstaller --onefile -w 'litscholar.py'`

Files will automatically be saved in the folder "results" as an Excel file and named the same as your query but with underscores.