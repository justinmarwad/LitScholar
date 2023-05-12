from scholarly import scholarly, ProxyGenerator
import pandas as pd
import os, sys, argparse

class LitScholar(): 
    def __init__(self, num_papers, enable_cited_by=False, folder="results"): 
        if num_papers is None:
            num_papers = 100
        
        self.num_papers         = int(num_papers)
        self.enable_cited_by    = enable_cited_by
        self.folder             = folder
        self.dataset            = pd.DataFrame()

        # if folder doesn't exist, create it
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
    
    def enable_proxy(self): 
        """ Set up a ProxyGenerator object to use free proxies. This needs to be done only once per session"""
        pg = ProxyGenerator()
        pg.FreeProxies()
        scholarly.use_proxy(pg)

    def search(self, query):
        self.query = query

        print(f"[*] Searching for papers for {query} Google Scholar...")

        # Search Google Scholar for the query and scrape the papers
        search_query = scholarly.search_pubs(query)
        for i in range(self.num_papers):
            try:
                # Get the paper's information
                paper = next(search_query)
                scholarly.pprint(paper)

                bib = paper.get('bib')
                

                if bib: 

                    if self.enable_cited_by: 
                        citations = [citation['bib']['title'] for citation in scholarly.citedby(paper)]
                    else: 
                        citations = "N/A"
                    
                    # Add the paper's information to the dataset
                    self.dataset = self.dataset.append({
                        'Title': bib.get('title'),
                        'Authors': ', '.join(bib.get('author')),
                        'Year': bib.get('pub_year'),
                        "Venue": bib.get('venue'),
                        "Abstract": bib.get('abstract'),

                        "cited_by": citations,
                        'URL': "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=" + bib.get('title').replace(" ", "+") + "&btnG=&oq=" + bib.get('title').replace(" ", "+") + "&gs_l=" + bib.get('title').replace(" ", "+") + "&as_vis=1", 
                    }, ignore_index=True)

                else: 
                    print("No bib found for this paper")
                
            except StopIteration:
                break

    def export(self): 
        file_path = f"{self.folder}/{self.query.lower().replace(' ', '_')}.xlsx"

        # Create a pandas DataFrame with the scraped data and save it to an Excel file 
        # which is named after the query but with underscores instead of spaces
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

        # Write the dataframe data to XlsxWriter. Turn off the default header and
        # index and skip one row to allow us to insert a user defined header.
        self.dataset.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Get the dimensions of the dataframe.
        (max_row, max_col) = self.dataset.shape

        # Create a list of column headers, to use in add_table().
        column_settings = [{"header": column} for column in self.dataset.columns]

        # Add the Excel table structure. Pandas will add the data.
        worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

        # Make the columns wider for clarity.
        worksheet.set_column(0, max_col - 1, 12)

        # Close the Pandas Excel writer and output the Excel file.
        writer.close()

        print(f"[+] Wrote {self.num_papers} papers to {file_path}")

        return file_path
 
if __name__ == "__main__": 
    # get the query from the command line argument -q or --query
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', help='Query to search for', required=True)
    parser.add_argument('-n', '--num_results', help='Number of results to return', required=False)
    parser.add_argument('-c', '--cited_by', help='Enable cited by', required=False, action='store_true')
    args = parser.parse_args()

    lit_scholar = LitScholar(num_papers=args.num_results, enable_cited_by=args.cited_by)

    lit_scholar.search(args.query)
    lit_scholar.export()