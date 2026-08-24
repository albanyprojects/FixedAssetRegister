from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Employee, Department, Device, DeviceType, AuditLog 
from schemas import EmployeeCreate, EmployeeResponse
from schemas import DeviceTypeCreate, DeviceTypeResponse
from schemas import DeviceCreate, DeviceResponse    
from schemas import DepartmentCreate, DepartmentResponse                        # many imports
from fastapi.middleware.cors import CORSMiddleware #needed to allow cors code to work
from schemas import SearchRequest

from sqlalchemy import or_
app = FastAPI()    # fast api forms part of the server software, 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
     ], # this local machine
    allow_credentials=True,                #these conditions need to return a valid argument otherwise it throws an error
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")#----------------------------------------------------------------------------------------------------------------------------------------------
def home():
    return {                            # this is a test return, the idea is that instead of when the code here has an error, 
        "message": "Backend is running" # you enter data and get a 500 error, you instead see this message first to tell you if it even works
    }#---------------------------------------------------------------------------------------------------------------------------------------------------------

@app.get("/auditlogs")
def get_auditlogs(db: Session = Depends(get_db)):
    return db.query(AuditLog).all()

@app.get("/employees")   # gets the employee table, the name here isnt actual table name Employee; that doesnt matter though because it is equalled on models.py
def get_employees(db: Session = Depends(get_db)): # this runs when the sql server can be accessed by this python code. 
    employees = db.query(Employee).all()      #equvicorn main:app --reloadivelent of SELECT * FROM Employee;
    return employees                          # nessesary to complete function 

@app.get("/departments")
def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return departments

@app.get("/devices")
def get_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return devices 

@app.get("/devicetypes")
def get_devicetypes(db: Session = Depends(get_db)):
    devicetypes = db.query(DeviceType).all()
    return devicetypes

# this is just defining the variables and their place in the runtime, each one is its own sql table, above here is the "get" to 'get' the fields and their data
# below retrieves one item by its primary key ID in the database, it also gives a url root that connects it to the running sql server

@app.get("/employees/{employee_id}") #specifies an ID,each table has a primary key, this specifies a primary key, thus, to a max and min of 1 line of data, so here you select data from 1 employee
def get_employee(employee_id: int, db: Session = Depends(get_db)): # same as last time
    return db.query(Employee).filter( #the actual filtering that goes on here. 
        Employee.EmployeeID == employee_id # EmployeeID is the field name, employee_id is whats used here as a variable. 
    ).first()

@app.get("/devices/{device_id}")
def get_device(device_id: int, db: Session = Depends(get_db)):
    return db.query(Device).filter(
        Device.DeviceID == device_id
    ).first()

@app.get("/device-types/{device_type_id}")
def get_device_type(device_type_id: int, db: Session = Depends(get_db)):
    return db.query(DeviceType).filter(
        DeviceType.DeviceTypeID == device_type_id
    ).first()

@app.get("/departments/{department_id}")
def get_department(department_id: int, db: Session = Depends(get_db)):
    return db.query(Department).filter(
        Department.DepartmentID== department_id
    ).first()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# on confirmation of data validation, this then allows an input, formats  it, and adds it to the database, saves it. moves on 
@app.post("/employees", response_model=EmployeeResponse) #response model is an object that will contain variable EmployeeResponse, post just means add in backend CRUD, create, read, update, delete
def create_employee(  # function
    employee: EmployeeCreate,   #creates the employee
    db: Session = Depends(get_db) # creates the environment needed to add the employee
):
    new_employee = Employee( #begins the next Key ID, so if the list went to 100, running this code would create 101. 
        FirstName=employee.FirstName,  # a field
        LastName=employee.LastName, # field
        Email=employee.Email, #field, this is the string value, the code would change slightly when field data types are fully rectified
        DepartmentID=employee.DepartmentID # the relationship between department and employee, so you cant add employee with department id 65 because that number needs to be added with a name to the department table. 
    )

    db.add(new_employee) # finished off the create
    db.commit()  # executes it
    db.refresh(new_employee) #auto refresh so you dont have to manually do it when adding data

    audit = AuditLog(    #audit import
        TableName="Employee",    #the various items that need importing. 
        RecordID=new_employee.EmployeeID,
        FieldName="*",
        OldValue=None,
        NewValue="Employee created",
        Action="CREATE",
        ChangedBy="someone"
    )
# end of importing random items. 
    db.add(audit)
    db.commit()

    return new_employee  # serves 2 purposes, returns employee which is nessesary for completing function, also gives the employee back in the data variable, so you can view it. 



@app.post("/departments", response_model=DepartmentResponse) # when you create a department, because there are only 2 fields, and one returned because its a primary key, you only have to enter 1 field. 
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    new_department = Department(
        DepartmentName=department.DepartmentName
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    audit = AuditLog(
        TableName="Department",
        RecordID=new_department.DepartmentID,
        FieldName="*",
        OldValue=None,
        NewValue="Department created",
        Action="CREATE",
        ChangedBy="someone"
    )

    db.add(audit)
    db.commit()

    return new_department

@app.post("/device-types", response_model=DeviceTypeResponse)
def create_device_type(
    device_type: DeviceTypeCreate,
    db: Session = Depends(get_db)
):
    new_device_type = DeviceType(
        DeviceTypeName=device_type.DeviceTypeName
    )

    db.add(new_device_type)
    db.commit()
    db.refresh(new_device_type)

    audit = AuditLog(
        TableName="DeviceType",
        RecordID=new_device_type.DeviceTypeID,
        FieldName="*",
        OldValue=None,
        NewValue="Device type created",
        Action="CREATE",
        ChangedBy="someone"
    )

    db.add(audit)
    db.commit()

    return new_device_type

@app.post("/devices", response_model=DeviceResponse)
def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db)
):
    new_device = Device(
        DeviceTypeID=device.DeviceTypeID,
        AssetTag=device.AssetTag,
        Model=device.Model,
        Manufacturer=device.Manufacturer,
        SerialNumber=device.SerialNumber,
        PurchaseDate=device.PurchaseDate,
        DepartmentID=device.DepartmentID,
        EmployeeID=device.EmployeeID,
        PurchaseCost=device.PurchaseCost,
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    audit = AuditLog(
        TableName="Device",
        RecordID=new_device.DeviceID,
        FieldName="*",
        OldValue=None,
        NewValue="Device created",
        Action="CREATE",
        ChangedBy="someone"
    )

    db.add(audit)
    db.commit()
    return new_device

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#this is the update part of the code, notice the "audit" stuff, update means to edit already existing data
@app.put("/employees/{employee_id}", response_model=EmployeeResponse)  #same as last time, PUT means update in crud.  the red in {} references the old already existing variable, because you are updating that rather than the way i was going to do this where you delete the old record and "replace" it with the new one. which i didnt do because that would flair up the audit table which comes after which records each individual field on all tables because of course it does. 
def update_employee(   # update function,
    employee_id: int, #is specified as primary key at "EmployeeID = Column(Integer, primary_key=True, index=True)" 
    employee: EmployeeCreate, #just the line you need to start editing, fast api uses it for simplicity. 
    db: Session = Depends(get_db)  #vs code debug recommended this line im still not sure what it does. 
):  
    existing_employee = db.query(Employee).filter( #filters for one, just like the read function, because your only selecting 1 set of data
        Employee.EmployeeID == employee_id # links these objects. 
    ).first()

    if existing_employee is None:
        raise HTTPException(  
            status_code=404,
            detail="Employee not found"
        )
  
    
    if existing_employee.FirstName != employee.FirstName: #start of the auditing for updat function, records those fields and labels it as an update. on the sql table you should see 
        audit = AuditLog(
            TableName="Employee",
            RecordID=existing_employee.EmployeeID,
            FieldName="FirstName",
            OldValue=existing_employee.FirstName,
            NewValue=employee.FirstName,
            Action="UPDATE",
            ChangedBy="someone" #this is just a placeholder. i wouldnt change this for now but you can still change it to match credential login details for the frontend so you can see who updated the table, 
        ) # it might not be a bad idea to make it so the login details part is part of the audit function itself rather than a seperate property each time you use it. 
        db.add(audit) #vs code reccomended this be removed, for some reason, ive still yet to test the api without it but im sure it would return a 500 error. 

    if existing_employee.LastName != employee.LastName:
        audit = AuditLog(
            TableName="Employee",
            RecordID=existing_employee.EmployeeID,
            FieldName="LastName",
            OldValue=existing_employee.LastName,
            NewValue=employee.LastName,
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_employee.Email != employee.Email:
        audit = AuditLog(
            TableName="Employee",
            RecordID=existing_employee.EmployeeID,
            FieldName="Email",
            OldValue=existing_employee.Email,
            NewValue=employee.Email,
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_employee.DepartmentID != employee.DepartmentID:
        audit = AuditLog(
            TableName="Employee",
            RecordID=existing_employee.EmployeeID,
            FieldName="DepartmentID",
            OldValue=str(existing_employee.DepartmentID),
            NewValue=str(employee.DepartmentID),
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    existing_employee.FirstName = employee.FirstName     # seperates new field from former field, reuses variable, optimisation or something
    existing_employee.LastName = employee.LastName
    existing_employee.Email = employee.Email
    existing_employee.DepartmentID = employee.DepartmentID

    
    db.commit()
    db.refresh(existing_employee)

    return existing_employee  
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.delete("/employees/{employee_id}") # self explanitory, deletes employee data from the class thus the table afterwards. 
def delete_employee(  # function, 
    employee_id: int, # primary key specified, not related to other foreign keys, will do that later. 
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.EmployeeID == employee_id
    ).first()

    if employee is None:
        return {"error": "Employee not found"}

    audit = AuditLog(
        TableName="Employee",
        RecordID=employee.EmployeeID,
        FieldName="*",
        OldValue=f"{employee.FirstName} {employee.LastName}",
        NewValue=None,
        Action="DELETE",  # will specify delete in the audit log, 
        ChangedBy="someone"
    )

    db.add(audit)

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted"}


@app.put("/devices/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    device: DeviceCreate,
    db: Session = Depends(get_db)
):
    existing_device = db.query(Device).filter(
        Device.DeviceID == device_id
    ).first()

    if existing_device is None:
        return {"error": "Device not found"}

    if existing_device.DeviceTypeID != device.DeviceTypeID:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="DeviceTypeID",
            OldValue=str(existing_device.DeviceTypeID),
            NewValue=str(device.DeviceTypeID),
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_device.AssetTag != device.AssetTag:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="AssetTag",
            OldValue=existing_device.AssetTag,
            NewValue=device.AssetTag,
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_device.Manufacturer != device.Manufacturer:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="Manufacturer",
            OldValue=existing_device.Manufacturer,
            NewValue=device.Manufacturer,
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_device.Model != device.Model:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="Model",
            OldValue=existing_device.Model,
            NewValue=device.Model,
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_device.SerialNumber != device.SerialNumber:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="SerialNumber",
            OldValue=existing_device.SerialNumber,
            NewValue=device.SerialNumber,
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_device.PurchaseDate != device.PurchaseDate:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="PurchaseDate",
            OldValue=existing_device.PurchaseDate,
            NewValue=device.PurchaseDate,
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_device.PurchaseCost != device.PurchaseCost:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="PurchaseCost",
            OldValue=str(existing_device.PurchaseCost),
            NewValue=str(device.PurchaseCost),
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_device.DepartmentID != device.DepartmentID:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="DepartmentID",
            OldValue=str(existing_device.DepartmentID),
            NewValue=str(device.DepartmentID),
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    if existing_device.EmployeeID != device.EmployeeID:
        audit = AuditLog(
            TableName="Device",
            RecordID=existing_device.DeviceID,
            FieldName="EmployeeID",
            OldValue=str(existing_device.EmployeeID),
            NewValue=str(device.EmployeeID),
            Action="UPDATE",
            ChangedBy="someone"
        )
        db.add(audit)

    existing_device.DeviceTypeID = device.DeviceTypeID
    existing_device.AssetTag = device.AssetTag
    existing_device.Manufacturer = device.Manufacturer
    existing_device.Model = device.Model
    existing_device.SerialNumber = device.SerialNumber
    existing_device.PurchaseDate = device.PurchaseDate
    existing_device.PurchaseCost = device.PurchaseCost
    existing_device.DepartmentID = device.DepartmentID
    existing_device.EmployeeID = device.EmployeeID

    db.commit()
    db.refresh(existing_device)

    return existing_device
        
# will update existing device. to distinguish between this and new type. splits variable
 

@app.delete("/devices/{device_id}")  #deleting the deviceID should not delete all data that uses it on the table or related tables. 
def delete_device(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = db.query(Device).filter(
        Device.DeviceID == device_id
    ).first()

    if device is None:
        return {"error": "Device not found"}

    audit = AuditLog(
        TableName="Device",
        RecordID=device.DeviceID,
        FieldName="*",
        OldValue=f"{device.Manufacturer} {device.Model} ({device.AssetTag})",
        NewValue=None,
        Action="DELETE",
        ChangedBy="someone"
    )

    db.add(audit)

    db.delete(device)
    db.commit()

    return {"message": "Device deleted"}

@app.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    existing_department = db.query(Department).filter(
        Department.DepartmentID == department_id
    ).first()

    if existing_department is None:
        return {"error": "Department not found"}

    if existing_department.DepartmentName != department.DepartmentName:
        audit = AuditLog(
            TableName="Department",
            RecordID=existing_department.DepartmentID,
            FieldName="DepartmentName",
            OldValue=existing_department.DepartmentName,
            NewValue=department.DepartmentName,
            Action="UPDATE",
            ChangedBy="someone"
        )

        db.add(audit)

    existing_department.DepartmentName = department.DepartmentName

    db.commit()
    db.refresh(existing_department)

    return existing_department

@app.delete("/departments/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.DepartmentID == department_id
    ).first()

    if department is None:
        return {"error": "Department not found"} # this error means that a department simply isnt found either it was mistyped or it did not return properly. 

    audit = AuditLog(
        TableName="Department",
        RecordID=department.DepartmentID,
        FieldName="*",
        OldValue=department.DepartmentName,
        NewValue=None,
        Action="DELETE",
        ChangedBy="someone"
    )

    db.add(audit)

    db.delete(department)
    db.commit()

    return {"message": "Department deleted"}

@app.put("/device-types/{device_type_id}", response_model=DeviceTypeResponse)
def update_device_type(
    device_type_id: int,
    device_type: DeviceTypeCreate,
    db: Session = Depends(get_db)
):
    existing_device_type = db.query(DeviceType).filter(
        DeviceType.DeviceTypeID == device_type_id
    ).first()

    if existing_device_type is None:
        return {"error": "Device type not found"}

    if existing_device_type.DeviceTypeName != device_type.DeviceTypeName:
        audit = AuditLog(
            TableName="DeviceType",
            RecordID=existing_device_type.DeviceTypeID,
            FieldName="DeviceTypeName",
            OldValue=existing_device_type.DeviceTypeName,
            NewValue=device_type.DeviceTypeName,
            Action="UPDATE",
            ChangedBy="someone"
        )

        db.add(audit)

    existing_device_type.DeviceTypeName = device_type.DeviceTypeName

    db.commit()
    db.refresh(existing_device_type)

    return existing_device_type

@app.delete("/device-types/{device_type_id}") # dangerous one to delete. 
def delete_device_type(
    device_type_id: int,
    db: Session = Depends(get_db)
):
    device_type = db.query(DeviceType).filter(
        DeviceType.DeviceTypeID == device_type_id
    ).first()

    if device_type is None:
        return {"error": "Device type not found"}

    audit = AuditLog(
        TableName="DeviceType",
        RecordID=device_type.DeviceTypeID,
        FieldName="*",
        
        OldValue=device_type.DeviceTypeName,
        NewValue=None,
        Action="DELETE",
        ChangedBy="someone"
    )

    db.add(audit)

    db.delete(device_type)
    db.commit()

    return {"message": "Device type deleted why did you do that?"} #because this was either a test, or its just deleted every row of device data that used that device type. 


TABLE_MAP = {
    "employees": Employee,
    "devices": Device,
    "departments": Department,
    "devicetypes": DeviceType,
    "auditlogs": AuditLog

}


@app.post("/search")
def search_database(
    search: SearchRequest,
    db: Session = Depends(get_db)
):

    results = []



    table_names = set(
        condition.table
        for condition in search.conditions
    )




    if len(table_names) == 1:

        table_name = next(iter(table_names))

        model = TABLE_MAP.get(table_name)

        if model is None:
            return []


        query = db.query(model)


        for condition in search.conditions:

            column = getattr(
                model,
                condition.field,
                None
            )

            if column is None:
                continue


            if condition.operator == "contains":

                query = query.filter(
                    column.contains(condition.value)
                )


            elif condition.operator == "equals":

                query = query.filter(
                    column == condition.value
                )


            elif condition.operator == "greater":

                query = query.filter(
                    column > condition.value
                )


            elif condition.operator == "less":

                query = query.filter(
                    column < condition.value
                )


        rows = query.all()


        for row in rows:

            row_data = {
                "Table": table_name
            }

            for column_name in row.__table__.columns.keys():

                row_data[column_name] = getattr(
                    row,
                    column_name
                )

            results.append(row_data)


        return results




    # Employee + Device
    if "employees" in table_names and "devices" in table_names:

        query = (
            db.query(Employee, Device)
            .join(
                Device,
                Employee.EmployeeID == Device.EmployeeID
            )
        )


        for condition in search.conditions:

            model = TABLE_MAP.get(condition.table)

            if model is None:
                continue


            column = getattr(
                model,
                condition.field,
                None
            )

            if column is None:
                continue


            if condition.operator == "contains":

                query = query.filter(
                    column.contains(condition.value)
                )


            elif condition.operator == "equals":

                query = query.filter(
                    column == condition.value
                )


            elif condition.operator == "greater":

                query = query.filter(
                    column > condition.value
                )


            elif condition.operator == "less":

                query = query.filter(
                    column < condition.value
                )


        rows = query.all()


        for employee, device in rows:

            row_data = {}

            for column_name in Employee.__table__.columns.keys():

                row_data[
                    f"Employee.{column_name}"
                ] = getattr(
                    employee,
                    column_name
                )


            for column_name in Device.__table__.columns.keys():

                row_data[
                    f"Device.{column_name}"
                ] = getattr(
                    device,
                    column_name
                )


            results.append(row_data)


        return results



    if "employees" in table_names and "departments" in table_names:

        query = (
            db.query(Employee, Department)
            .join(
                Department,
                Employee.DepartmentID == Department.DepartmentID
            )
        )


        for condition in search.conditions:

            model = TABLE_MAP.get(condition.table)

            if model is None:
                continue


            column = getattr(
                model,
                condition.field,
                None
            )

            if column is None:
                continue


            if condition.operator == "contains":

                query = query.filter(
                    column.contains(condition.value)
                )


            elif condition.operator == "equals":

                query = query.filter(
                    column == condition.value
                )


            elif condition.operator == "greater":

                query = query.filter(
                    column > condition.value
                )


            elif condition.operator == "less":

                query = query.filter(
                    column < condition.value
                )


        rows = query.all()


        for employee, department in rows:

            row_data = {}

            for column_name in Employee.__table__.columns.keys():

                row_data[
                    f"Employee.{column_name}"
                ] = getattr(
                    employee,
                    column_name
                )


            for column_name in Department.__table__.columns.keys():

                row_data[
                    f"Department.{column_name}"
                ] = getattr(
                    department,
                    column_name
                )


            results.append(row_data)


        return results



    if "devices" in table_names and "departments" in table_names:

        query = (
            db.query(Device, Department)
            .join(
                Department,
                Device.DepartmentID == Department.DepartmentID
            )
        )


        for condition in search.conditions:

            model = TABLE_MAP.get(condition.table)

            if model is None:
                continue


            column = getattr(
                model,
                condition.field,
                None
            )

            if column is None:
                continue


            if condition.operator == "contains":

                query = query.filter(
                    column.contains(condition.value)
                )


            elif condition.operator == "equals":

                query = query.filter(
                    column == condition.value
                )


            elif condition.operator == "greater":

                query = query.filter(
                    column > condition.value
                )


            elif condition.operator == "less":

                query = query.filter(
                    column < condition.value
                )


        rows = query.all()


        for device, department in rows:

            row_data = {}

            for column_name in Device.__table__.columns.keys():

                row_data[
                    f"Device.{column_name}"
                ] = getattr(
                    device,
                    column_name
                )


            for column_name in Department.__table__.columns.keys():

                row_data[
                    f"Department.{column_name}"
                ] = getattr(
                    department,
                    column_name
                )


            results.append(row_data)


        return results




    if "devices" in table_names and "devicetypes" in table_names:

        query = (
            db.query(Device, DeviceType)
            .join(
                DeviceType,
                Device.DeviceTypeID == DeviceType.DeviceTypeID
            )
        )


        for condition in search.conditions:

            model = TABLE_MAP.get(condition.table)

            if model is None:
                continue


            column = getattr(
                model,
                condition.field,
                None
            )

            if column is None:
                continue


            if condition.operator == "contains":

                query = query.filter(
                    column.contains(condition.value)
                )


            elif condition.operator == "equals":

                query = query.filter(
                    column == condition.value
                )


            elif condition.operator == "greater":

                query = query.filter(
                    column > condition.value
                )


            elif condition.operator == "less":

                query = query.filter(
                    column < condition.value
                )


        rows = query.all()


        for device, device_type in rows:

            row_data = {}

            for column_name in Device.__table__.columns.keys():

                row_data[
                    f"Device.{column_name}"
                ] = getattr(
                    device,
                    column_name
                )


            for column_name in DeviceType.__table__.columns.keys():

                row_data[
                    f"DeviceType.{column_name}"
                ] = getattr(
                    device_type,
                    column_name
                )


            results.append(row_data)


        return results




    if (
        "employees" in table_names
        and "devices" in table_names
        and "departments" in table_names
    ):

        query = (
            db.query(
                Employee,
                Device,
                Department
            )
            .join(
                Device,
                Employee.EmployeeID == Device.EmployeeID
            )
            .join(
                Department,
                Device.DepartmentID == Department.DepartmentID
            )
        )


        for condition in search.conditions:

            model = TABLE_MAP.get(condition.table)

            if model is None:
                continue


            column = getattr(
                model,
                condition.field,
                None
            )

            if column is None:
                continue


            if condition.operator == "contains":

                query = query.filter(
                    column.contains(condition.value)
                )


            elif condition.operator == "equals":

                query = query.filter(
                    column == condition.value
                )


            elif condition.operator == "greater":

                query = query.filter(
                    column > condition.value
                )


            elif condition.operator == "less":

                query = query.filter(
                    column < condition.value
                )


        rows = query.all()


        for employee, device, department in rows:

            row_data = {}


            for column_name in Employee.__table__.columns.keys():

                row_data[
                    f"Employee.{column_name}"
                ] = getattr(
                    employee,
                    column_name
                )


            for column_name in Device.__table__.columns.keys():

                row_data[
                    f"Device.{column_name}"
                ] = getattr(
                    device,
                    column_name
                )


            for column_name in Department.__table__.columns.keys():

                row_data[
                    f"Department.{column_name}"
                ] = getattr(
                    department,
                    column_name
                )


            results.append(row_data)


        return results



    return []

