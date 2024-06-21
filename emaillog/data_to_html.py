def data_to_styled_html_table_react(data):
    headers = [
                {"label" : "Route", "name" : "top_route_name"},
                {"label" :"Profile", "name" : "profile"}, 
                {"label" :"Rate", "name" : "rate"}, 
                {"label" :"ASR", "name" : "asr"}, 
                {"label" :"ACD", "name" : "acd"},
                {"label" :"Increment", "name" : "increment"}
    ]
    html_table = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        </head>
         <style>
        @media (max-width: 768px) {
            table {
                display: none;
            }
            .divdata-grid {
            display: grid;
            grid-template-columns: auto auto auto;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            color: #4a5568;
            overflow-x: auto;
            padding: 8px;
        }}

        @media (min-width: 768px) {
            .divdata {
                display: none;
            }
        }

        </style>
        </head>
        <body>
    '''
    html_table += '''
    <table border="1" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; 
    }">
        <tr style="background-color: #FFFF00;">
    '''
    
    # Add table headers
    for header in headers:
        html_table += f'<th style="padding: 8px; text-align: left; border: 1px solid #dddddd;">{header.get("label")}</th>'
    html_table += '</tr>'
    
    # Add table rows
    for row in data:
        html_table += '<tr>'
        for header in headers:
            html_table += f'<td style="padding: 8px; border: 1px solid #dddddd;">{row[header.get("name")]}</td>'
        html_table += '</tr>'
    
    html_table += '</table>  </body></html>'
    
    for row in data:
            
        html_table += '<div class="divdata" style="margin: 5px; border: 3px solid #e2e8f0; border-radius: 0.25rem;"><div>'
        for header in headers:
            html_table += f' <div class="divdata-grid"> <div class="" style="color : gray; font-weight: 800;">{header.get("label")} </div> <div class="" style="grid-column: span 2; font-weight: 800;">{row.get(header.get("name"))} </div></div>'
        html_table += '</div></div>'

    return html_table

def data_to_styled_html_table(data):
    headers = [
        {"label": "Route", "name": "top_route_name"},
        {"label": "Profile", "name": "profile"}, 
        {"label": "Rate", "name": "rate"}, 
        {"label": "ASR", "name": "asr"}, 
        {"label": "ACD", "name": "acd"},
        {"label": "Increment", "name": "increment"}
    ]

    html_table = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        </head>
        <body>
    '''

    # Table for desktop view
    html_table += '''
    <table border="1" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
        <tr style="background-color: #FFFF00;">
    '''

    # Add table headers
    for header in headers:
        html_table += f'<th style="padding: 8px; text-align: left; border: 1px solid #dddddd;">{header.get("label")}</th>'
    html_table += '</tr>'

    # Add table rows
    for row in data:
        html_table += '<tr>'
        for header in headers:
            html_table += f'<td style="padding: 8px; border: 1px solid #dddddd;">{row[header.get("name")]}</td>'
        html_table += '</tr>'
    html_table += '</table>'

    # Div data for mobile view
    for row in data:
        html_table += '''
        <div class="divdata" style="margin: 5px; border: 3px solid #e2e8f0; border-radius: 0.25rem; display: none;">
        '''
        for header in headers:
            html_table += f'''
            <div style="display: grid; grid-template-columns: auto auto auto; margin-top: 0.5rem; margin-bottom: 0.5rem; color: #4a5568; overflow-x: auto; padding: 8px;">
                <div style="color: gray; font-weight: 800;">{header.get("label")}</div>
                <div style="grid-column: span 2; font-weight: 800;">{row.get(header.get("name"))}</div>
            </div>
            '''
        html_table += '</div>'

    html_table += '''
    <script>
    if (window.innerWidth <= 768) {
        document.querySelector('table').style.display = 'none';
        document.querySelectorAll('.divdata').forEach(function(div) {
            div.style.display = 'block';
        });
    } else {
        document.querySelector('table').style.display = 'block';
        document.querySelectorAll('.divdata').forEach(function(div) {
            div.style.display = 'none';
        });
    }
    </script>
    </body>
    </html>
    '''

    return html_table



def data_to_styled_html_table_rate(data):
    try:
        headers =[
            {"label" : "Country Code", "name" : "country_code"},
            {"label" :"Country Name", "name" : "country_name"}, 
            {"label" :"Rate", "name" : "rate"}, 
            {"label" :"Increment", "name" : "increment"}, 
            {"label" :"Status", "name" : "status"},
            {"label" :"Effective Date", "name" : "effective_date"}
        ]
        html_table = '''
        <table border="1" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
            <tr style="background-color: #FFFF00;">
        '''
        
        # Add table headers
        for header in headers:
            html_table += f'<th style="padding: 8px; text-align: left; border: 1px solid #dddddd;">{header.get("label")}</th>'
        html_table += '</tr>'
        
        # Add table rows
        for row in data:
            html_table += '<tr>'
            for header in headers:
                html_table += f'<td style="padding: 8px; border: 1px solid #dddddd;">{row[header.get("name")]}</td>'
            html_table += '</tr>'
        
        html_table += '</table>'
        return html_table
    except Exception as e:
        print(e)
        return e    