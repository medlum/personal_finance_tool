import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
from datetime import datetime
from utils import *

# ---------set up page config -------------#
st.set_page_config(page_title="income and expenses",
                   layout="wide", page_icon="👾")


st.header("Income and expenses dashboard")

# ------ download data from gdrive -----#

# locate id at 'share -> copy link' in gdrive
file_id = "1eySOPRbCI1_gkcb0FKj6VUkPnNBiNTBH"

# file path to host downloaded file from gdrive
destination_path = "data.csv"

with st.spinner("Reading data..."):
    download_file(file_id=file_id,
                  destination_path=destination_path)

# ------ setup parameters for uploadFile() -----#
filepath = 'data.csv'
mimetype = 'text/csv'
file_id = "1eySOPRbCI1_gkcb0FKj6VUkPnNBiNTBH"
# folderid = '12KLDxTeNbUyc7cZjSO5E7KueaCsBnSZh'

# ---- read data after download ----#
df = pd.read_csv("data.csv")

# ---- create streamlit tabs ----#
view_tab, form_tab, edit_tab, cpf_tab = st.tabs(
    ["view", "entry", "edit", "cpf"])

with form_tab:
    # income or expense button
    type_btn = st.radio("type",
                        options=["Income", "Expense"],
                        horizontal=True,
                        index=0,
                        label_visibility="hidden"
                        )
    # create form for data entry
    with st.form(key="data_entry", clear_on_submit=True):

        col1, col2 = st.columns([1, 1])

        # dropdown box to select location, spouse
        location = col1.selectbox(label="Location",
                                  options=data_dict["location"],
                                  index=1)

        spouse = col2.selectbox(label="Spouse",
                                options=data_dict["spouse"],
                                index=0)

        col1, col2 = st.columns([1, 1])

        # change to income option from data_dict["income"]
        if type_btn == "Income":

            select_opt = col1.selectbox(
                label="Select an option", options=data_dict["income"], index=0)

         # change to expense option from data_dict["expense"]
        elif type_btn == "Expense":

            select_opt = col1.selectbox(label="Select an option",
                                        options=data_dict["expense"],
                                        index=0,
                                        key='select_opt')
        # text input for $$$$
        amount = col2.text_input(label="Amount",
                                 placeholder="Enter monthly amount",
                                 key="expenses")

        # text input for entry details
        details = st.text_input(label="Details",
                                placeholder="Details of insurance policy, subscription type etc",
                                )

        submitted = st.form_submit_button("Submit")

    if submitted:

        # if spouse and select_opt from dropdown is not "select one"
        # and amount in text_input is a digit

        if "select one" not in [spouse, select_opt] and is_number(amount) is not ValueError:

            # set expense to negative
            if type_btn == "Expense":
                amount = -float(amount)
             # set income to positive
            elif type_btn == "Income":
                amount = float(amount)

            # put new entry to a list
            new_data = [type_btn,
                        select_opt,
                        amount,
                        spouse,
                        location,
                        details,
                        datetime.now().date()]

            # add new entry to last row of df
            df.loc[len(df)] = new_data
            # save df to csv file
            df.to_csv('data.csv', index=False)
            # upload to gdrive
            uploadFile(filepath, mimetype, file_id)
            st.toast("Done!")
            # st.cache_resource.clear()

        else:
            # if spouse and select_opt is not "select one" and amount is not a digit
            st.error("Check entry", icon="🚨")


with view_tab:

    # create csv after download
    df = pd.read_csv("data.csv")

    dynamic_filters = DynamicFilters(
        df=df, filters=['Type', 'Option', 'Spouse', 'Location'])

    dynamic_filters.display_filters(
        location='columns', num_columns=2, gap='large')

    dynamic_filters.display_df()

    # .filter_df() is the return df after filtering
    # by dynamic_filters.

    # assign .filter_df() to variable to perform arithmetic op.
    filter_df = dynamic_filters.filter_df()
    # write total amount of the filtered df
    st.write(f"Total : {str(filter_df['Amount'].sum())}")


with edit_tab:

    # use data_editor to change value or delete rows
    df = st.data_editor(df, hide_index=None, num_rows="dynamic")
    df.to_csv('data.csv', index=False)

    if st.button("Proceed"):

        uploadFile(filepath, mimetype, file_id)
        st.toast("Done!")
        # st.cache_resource.clear()


with cpf_tab:
    st.subheader("WIP")
