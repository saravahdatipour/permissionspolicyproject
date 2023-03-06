import pandas as pd
import os

def define_df(url, HasHeaderPolicy,headerpolicy ,HasInlinePolicy, HasConflict, NumberOfConflicts, ConflictedFeatures, ThirdPartyDomain):
    data = {
        'Website': [url],
        'Has Header Policy': [HasHeaderPolicy],
        'Header Policy': [headerpolicy], 
        'Inline Policy': [HasInlinePolicy],
        'Conflict': [HasConflict],
        'Number of Conflicts': [NumberOfConflicts],
        'Conflicting Features': [ConflictedFeatures],
        'Third Party Domains': [ThirdPartyDomain]
    }
    df = pd.DataFrame(data)
    return df

def append_data(df, url, HasHeaderPolicy,headerpolicy, HasInlinePolicy, HasConflict, NumberOfConflicts, ConflictedFeatures, ThirdPartyDomain):
    new_row = [url, HasHeaderPolicy,headerpolicy, HasInlinePolicy, HasConflict, NumberOfConflicts, ConflictedFeatures, ThirdPartyDomain]
    new_df = pd.DataFrame([new_row], columns=df.columns)
    df = pd.concat([df, new_df], ignore_index=True)
    return df

def save_data(df, filename):
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, index=False)
    return df


# df1 = define_df('https://www.google.com', True, True, False, 2, ['camera', 'geolocation'], "google.com")
# df1 = append_data(df1,'https://www.facebook.com', True, True, False, 2, ['camera', 'geolocation'], "google.com")
# df1 = append_data(df1,'https://www.media.com', True, True, False, 2, ['geolocation'], "google.com")
# filename = 'crawlresults.xlsx'
# df1 = save_data(df1, filename)
