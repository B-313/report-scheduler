import streamlit as st
import pandas as pd

def main():
    data = pd.read_excel('data/sample_data.xlsx')
    data.columns = data.columns.str.strip()
    print(data.columns)
    
if __name__ == "__main__":
    main()