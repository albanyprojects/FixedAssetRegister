from pydantic import BaseModel    #import this software, otherwise this would take much longer to code. 
from datetime import date
from datetime import datetime
class EmployeeCreate(BaseModel):   #basemodel because you are literally defining the items in the class
    FirstName: str     #notice how the primary key isnt here. this is because a human shouldnt have to, and no frontend will support someone manually puttin in a primary key ID, when inserting the next set of data will just do it for you,  and with 100 percent accuracy. 
    LastName: str
    Email: str
    DepartmentID: int   # a foreign key will be specified here. it currently doesnt exist in the sql table itself. 



class EmployeeResponse(BaseModel):
    EmployeeID: int
    FirstName: str
    LastName: str
    Email: str
    DepartmentID: int

    model_config = {
        "from_attributes": True #this is the format of the test data you can enter on the api, its also the internal format the entered data will be stored as
    }



class DeviceTypeCreate(BaseModel):
    DeviceTypeName: str


class DeviceTypeResponse(BaseModel):
    DeviceTypeID: int
    DeviceTypeName: str

    model_config = {
        "from_attributes": True
    }

class DeviceCreate(BaseModel):
    DeviceTypeID: int
    AssetTag: str
    Model: str
    Manufacturer: str
    SerialNumber: str
    PurchaseDate: date
    PurchaseCost: int
    DepartmentID: int
    EmployeeID: int

class DeviceResponse(BaseModel):
    DeviceID: int
    DeviceTypeID: int
    AssetTag: str
    Model: str
    Manufacturer: str
    SerialNumber: str
    PurchaseDate: date
    PurchaseCost: int
    DepartmentID: int
    EmployeeID: int
    model_config = {
        "from_attributes": True
    }

class DepartmentCreate(BaseModel):
    DepartmentName: str

class DepartmentResponse(BaseModel):
    DepartmentID: int
    DepartmentName: str
    model_config = {
        "from_attributes": True
    }




class AuditLogResponse(BaseModel):
    AuditID: int
    TableName: str
    RecordID: int
    FieldName: str
    OldValue: str | None
    NewValue: str | None
    Action: str
    ChangedBy: str
    ChangeDate: datetime

    model_config = {
        "from_attributes": True
    }






class SearchCondition(BaseModel):
    table: str
    field: str
    operator: str
    value: str

class SearchRequest(BaseModel):
    conditions: list[SearchCondition]
