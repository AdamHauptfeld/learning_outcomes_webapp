import streamlit as st
import pandas as pd


# py -m streamlit run "g:/My Drive/Data Nerd/Projects/learning_outcomes_webapp/learning_outcomes_webapp.py"

def main():
    st.title("Welcome to the Philosophy Discipline LO Report Aggregator")
    
    # File uploader
    uploaded_files = st.file_uploader("Choose Excel files", type="xlsx", accept_multiple_files=True)
    
    if uploaded_files:
        # Combine all uploaded files into a single dataframe
        df_list = []
        for file in uploaded_files:
            df = pd.read_excel(file)
            df_list.append(df)
        
        total_table = pd.concat(df_list, ignore_index=True)

        #convert TERM and CLASS_NUMBER column datatype to string
        total_table['term'] = df['term'].astype(str)
        total_table['class_number'] = df['class_number'].astype(str)

        #add total number of students column to dataframe
        total_table["student_total"] = total_table[["exemplary_total", "proficient_total", "developing_total", "emerging_total"]].sum\
            (axis=1)

        #It might be a good idea to rename the columns here eg. from EXEMPLARY_TOTAL to just EXEMPLARY (since summing happens later)
        
        # Display the combined dataframe
        st.subheader("Combined Dataframe")
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
        
    eval_columns = ["exemplary_total", "proficient_total", "developing_total", "emerging_total", "student_total"]
    
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
        st.header(eval_table)
        summary = eval_tables_dict[eval_table].agg(['sum', 'mean'])
        st.write(summary)
      
        

if __name__ == "__main__":
    main()
