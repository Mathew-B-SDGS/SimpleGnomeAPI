import pandas as pd 

class Parser:
    def __init__(self):
        self.df_gnomad = pd.read_csv('gnomad.v4.0.constraint_metrics.tsv', delimiter='\t')
        self.df_genes = pd.read_csv('gene_names_list.csv')

    def parse(self, output_file):
        df_filtered = self.df_gnomad[self.df_gnomad['gene'].isin(self.df_genes['gene_symbol'])]
        df_filtered.to_csv(output_file, sep='\t', index=False)

obj = Parser()
obj.parse('output.tsv')







