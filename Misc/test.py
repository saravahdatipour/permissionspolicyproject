import pandas as pd

# read the excel file into a pandas dataframe
df = pd.read_excel('file.xlsx')

# add new columns for Firefox and Chrome Warning Scenarios
df['Firefox Warning Scenario'] = False
df['Chrome Warning Scenario'] = False

# loop through each row in the dataframe
for i, row in df.iterrows():
    header_policy = row['Has Header Policy']
    cross_origin_iframe_policy = row['Cross-Origin Iframe Policy']

    # check if header policy was true and cross-origin iframe policy was not empty
    if cross_origin_iframe_policy != '[]':
        if  header_policy == True:
            print(row['Cross-Origin Iframe Policy'])
            df.at[i, 'Firefox Warning Scenario'] = True
        else :
            df.at[i, 'Chrome Warning Scenario'] = True

# write the updated dataframe back to the excel file
df.to_excel('your_updated_excel_file.xlsx', index=False)
