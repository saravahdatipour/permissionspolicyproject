
import pandas as pd
from openpyxl import Workbook


def get_data(url, HasHeaderPolicy, HasInlinePolicy, HasConflict, ConflictedFeatures, NumberOfConflicts,ThirdPartyFrames):

    data = {
        'Website': [url],
        'Header Policy': [HasHeaderPolicy],
        'Inline Policy': [HasInlinePolicy],
        'Conflict': [HasConflict],
        'Number of Conflicts': [NumberOfConflicts],
        'Conflicted Features': [ConflictedFeatures],
        'Third Party Frames': [ThirdPartyFrames]
    }

    df = pd.DataFrame(data)

    df.to_excel('crawlresults.xlsx', index=False)

# get_data('https://www.google.com', True, True, False, True, ['camera', 'geolocation'], 2)