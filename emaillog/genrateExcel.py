import pandas as pd
import io

def generate_excel(rate_data):
    df = pd.DataFrame(list(rate_data))

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Rates')
    output.seek(0)
    return output
