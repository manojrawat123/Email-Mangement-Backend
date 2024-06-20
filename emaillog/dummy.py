# print("---- atachments ----")
#         serializer = EmailLogSerializer(data=request.data)

#         if serializer.is_valid():
#             # Save data to the database
#             data = serializer.save()                                                                
#             try:
#                 email_lis = []
#                 schedul_customer = serializer.data.get('CustomerId')
#                 for i in schedul_customer:
#                     cemail = Customer.objects.get(id = i)
#                     email_lis.append(cemail.RatesEmail)
#                 print("Email List",email_lis)
#                 message_id = serializer.data.get('TemplateID')
#                 email_template = EmailTemplate.objects.get(TemplateID = message_id)
#                 my_message = email_template.TemplateMessage
#                 my_body = email_template.TemplateBody
#                 # Email sending logic
#                 email_from = settings.EMAIL_HOST_USER
#                 email = "positive.mind.123456789@gmail.com"
#                 recipient_list = email_lis
#                 subject = my_message
#                 attachment = request.FILES.get('Attachment') 
#                 message = f'''{my_body}'''
#                 email = EmailMessage(subject, message, email_from,recipient_list )
#                 email.attach(attachment.name, attachment.read(), attachment.content_type)
#                 email.send()
#                 # Return a success response
                
#                 return Response({"Msg ":"Registration and email send successfully"})
            
#             except Exception as e:
#                 # Handle exceptions related to email sending here
#                 # You can log the error for debugging purposes
#                 print(f"Email sending failed: {e}")
#             # Return a success response
#             return Response({"Msg ":"Registration successfully!!"})
#         return Response(serializer.errors, status=400)