from pydantic import BaseModel, Field
from typing import Literal

class CustomerData(BaseModel):
    # Categorical fields strictly limited to allowed options
    Gender: Literal['Male', 'Female']
    Senior_Citizen: Literal[0, 1] = Field(alias="Senior Citizen")
    Partner: Literal['Yes', 'No']
    Dependents: Literal['Yes', 'No']
    
    # Numeric fields with realistic minimum and maximum limits
    Tenure_Months: int = Field(alias="Tenure Months", ge=0, le=100, description="Months as a customer")
    
    Phone_Service: Literal['Yes', 'No'] = Field(alias="Phone Service")
    Multiple_Lines: Literal['Yes', 'No', 'No phone service'] = Field(alias="Multiple Lines")
    Internet_Service: Literal['DSL', 'Fiber optic', 'No'] = Field(alias="Internet Service")
    
    Online_Security: Literal['Yes', 'No', 'No internet service'] = Field(alias="Online Security")
    Online_Backup: Literal['Yes', 'No', 'No internet service'] = Field(alias="Online Backup")
    Device_Protection: Literal['Yes', 'No', 'No internet service'] = Field(alias="Device Protection")
    Tech_Support: Literal['Yes', 'No', 'No internet service'] = Field(alias="Tech Support")
    Streaming_TV: Literal['Yes', 'No', 'No internet service'] = Field(alias="Streaming TV")
    Streaming_Movies: Literal['Yes', 'No', 'No internet service'] = Field(alias="Streaming Movies")
    
    Contract: Literal['Month-to-month', 'One year', 'Two year']
    Paperless_Billing: Literal['Yes', 'No'] = Field(alias="Paperless Billing")
    Payment_Method: Literal['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'] = Field(alias="Payment Method")
    
    # Financial fields must be positive numbers
    Monthly_Charges: float = Field(alias="Monthly Charges", ge=0.0)
    Total_Charges: float = Field(alias="Total Charges", ge=0.0)
