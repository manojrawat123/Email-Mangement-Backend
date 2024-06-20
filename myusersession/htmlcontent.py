def emailVerifyContent(message):
    return f'''
                          <html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .container {{
         
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h3 {{
            color: #333333;
        }}
        p {{
            color: #666666;
        }}
        a {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
        }}
        a:hover {{
            background-color: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h3>Hii,</h3>
        <p>Please click on the below link to verify your email</p>
        <p><a href="{message}" style="color: #ffffff;">Click To Verify</a></p>
        <p>Thanks & Regards,</p>
        <p>Customer Care</p>
        <p>Intern Monster</p>
    </div>
</body>
</html>'''