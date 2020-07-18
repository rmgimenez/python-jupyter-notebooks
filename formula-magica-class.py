import pandas as pd
import numpy as np

# Obter os dados do site: https://statusinvest.com.br/acoes/busca-avancada

class FormulaMagica:
    
    # lista de ações que devem ser excluídas da fórmula
    acoes_e = []
    
    # lista das ações que possuo
    acoes_p = ['ITSA4', 'FLRY3']
    
    # dataframe com todos os dados
    df_total = []
    
    # dataframe utilizado para mostrar os resultados
    df = []
    
    def _obter_dados(self):
        self.df_total = pd.read_clipboard()
    
    def _filtrar_campos(self):
        self.df = self.df_total[['TICKER', 'P/L', 'EV/EBIT', 'ROE', ' LIQUIDEZ MEDIA DIARIA', 'LIQ. CORRENTE']]
        
    def _corrigir_campos(self):
        self.df[' LIQUIDEZ MEDIA DIARIA'] = self.df[' LIQUIDEZ MEDIA DIARIA'].str.replace('.', '').str.replace(',', '.').astype('float64')
        self.df['P/L'] = self.df['P/L'].str.replace('.', '').str.replace(',', '.').astype('float64')
        self.df['EV/EBIT'] = self.df['EV/EBIT'].str.replace('.', '').str.replace(',', '.').astype('float64')
        self.df['ROE'] = self.df['ROE'].str.replace('.', '').str.replace(',', '.').astype('float64')
        
    def _filtrar_acoes(self, forma):
        if forma == 1:
            for x in self.acoes_e:
                self.df = self.df[self.df['TICKER'] != x]
        
    def _filtrar_dados(self, pl_min, evebit_min, roe_min):
        self.df = self.df[self.df[' LIQUIDEZ MEDIA DIARIA'] > 0]
        self.df = self.df[self.df['ROE'] > roe_min]
        self.df = self.df[self.df['P/L'] > pl_min]
        self.df = self.df[self.df['EV/EBIT'] > evebit_min]
        
    def _calcular_ranking(self):
        self.df.sort_values(by='P/L', inplace=True)
        self.df.insert(2, 'P/L Ordem', range(1, + len(self.df) + 1))
        self.df.sort_values(by='EV/EBIT', inplace=True)
        self.df.insert(4, 'EV/EBIT Ordem', range(1, + len(self.df) + 1))
        self.df.sort_values(by='ROE', inplace=True, ascending=False)
        self.df.insert(6, 'ROE Ordem', range(1, + len(self.df) + 1))
        
        self.df['Ordem Formula'] = self.df['ROE Ordem'] + self.df['EV/EBIT Ordem'] 
        self.df.sort_values(by='Ordem Formula', inplace=True)
        
        self.df['Ordem Formula Media'] = ((self.df['ROE Ordem'] + self.df['P/L Ordem'])/2) + self.df['EV/EBIT Ordem']
        
    def retorna_df_calculado(self):
        self._obter_dados()
        self._filtrar_campos()
        self._corrigir_campos()
        self._filtrar_acoes(1)
        self._filtrar_dados(0, 0, 10)
        self._calcular_ranking()
        return self.df
        
fm = FormulaMagica()
df = fm.retorna_df_calculado()
df.head(20)   
