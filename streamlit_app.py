import streamlit as st
import pandas as pd
from PIL import Image

def main():
    st.title("Welcome to the Philosophy Discipline LO Report Aggregator")
    
    # File uploader
    uploaded_files = st.file_uploader("Choose Excel files", type="xlsx", accept_multiple_files=True)
    
    if uploaded_files:
        # Combine all uploaded files into a single dataframe
        df_list = []
        for file in uploaded_files:
            df = pd.read_excel(file)
            df['term'] = df['term'].astype(str)
            df['class_number'] = df['class_number'].astype(str)
            df_list.append(df)
        
        total_table = pd.concat(df_list, ignore_index=True)

        #It might be a good idea to rename the columns here eg. from EXEMPLARY_TOTAL to just EXEMPLARY (since summing happens later)
        total_table.rename(columns={"exemplary_total":"exemplary", "proficient_total":"proficient", "developing_total":"developing", "emerging_total":"emerging"}, inplace = True)

        #add total number of students column to dataframe
        total_table["student_total"] = total_table[["exemplary", "proficient", "developing", "emerging"]].sum\
            (axis=1)

        #Display happy image
        happy_adam = Image.open(r"https://github.com/AdamHauptfeld/learning_outcomes_webapp/blob/master/it_works.jpg")
        st.image(happy_adam)
        
        # Display the combined dataframe
        st.subheader("Combined Table")
        st.dataframe(total_table, height = 250)

        filtered_tables = filter_table(total_table)
        perform_and_display_aggregations(filtered_tables)

#creates a different dataframe for each value found in the COURSE column
def filter_table(table):

    #create a list with unique values in the COURSE columns
    course_list = []
    for course in table['course']:
        if course not in course_list:
            course_list.append(course)

    #create a dictionary with each course paired with its filtered table
    filtered_tables = {}
    for course in course_list:
        filtered_table = table.loc[table['course']== course]
        filtered_tables[course] = filtered_table

    return filtered_tables


def perform_and_display_aggregations(table_dict):
        
    eval_columns = ["exemplary", "proficient", "developing", "emerging", "student_total"]
    
    #create dictionary with each course paired with it's table of aggregable columns
    eval_tables_dict = {}
    for table in table_dict:
        temp_table = table_dict[table]
        eval_table = temp_table[eval_columns]
        eval_tables_dict[table] = eval_table

    #For each course, display the sums and means of their aggregable columns
    
    # for eval_table in eval_tables_dict:
    #     st.header(eval_table + " totals")
    #     table = eval_tables_dict[eval_table]
    #     summary = table.agg(['sum'])
    #     st.write(summary)
    #     st.header(eval_table + " means")
    #     table = eval_tables_dict[eval_table]
    #     summary = table.agg(['mean'])
    #     st.write(summary)
    
    
    for eval_table in eval_tables_dict:
        st.header(eval_table+" Data")
        summary = eval_tables_dict[eval_table].agg(['sum', 'mean'])
        st.write(summary)
      
        

if __name__ == "__main__":
    main()
