import email, smtplib, ssl  # smtplib for creating server ,ssl for secure connection
from email import encoders  # specifes the format of the code-base64 for ASCII characters
from email.mime.base import MIMEBase  # image attachment in mails
from email.mime.multipart import MIMEMultipart  # combines plain text to HTML(used for hyperlinks,images,format)
# MIME:Multipurpose Internet Mail Extensions
from email.mime.text import MIMEText  #it contains html and plaintext versions of our message


def send_mail(rmail, car_num,file_path):

    subject = "Reg: Traffic Rules Violation"
    body = """Sir/Madam
            Vehicle number: {} involved in traffic violation. Find the vehicle photo attached, taken at the time of violation. Kindly pay the challan amount in the official website. If not paid, legal action will be taken. Please ignore if already paid.
'DRIVE SAFE'
         
From
State Police Integrated E-challan System """.format(car_num)
    sender_email = "echallan.B8@gmail.com"
    receiver_email = rmail
    password = input("Type your password and press enter:")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename =file_path

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")  # downloadable format
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)  # binary to ASCII to make it in human readable format

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",  # giving a name to the image attached
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()  # creating a ssl connection
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

