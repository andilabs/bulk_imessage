
iMessage = 1
SMS = 2

SERVICE_CHOICES = (
    (iMessage, 'iMessage'),
    (SMS, 'SMS')
)

SERVICE_CHOICES_INVERTED = {v: k for k, v in dict(SERVICE_CHOICES).items()}
