from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Date     #
from datetime import date       # these 2 are the different date imports we can use, datetime would just be for this backend, the sql database would remain int. sqlalchemy will use the literal formatting of the database.  
from sqlalchemy import DateTime


class Employee(Base):
    __tablename__ = "Employee"

    EmployeeID = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(50))
    LastName = Column(String(90))
    Email = Column(String, unique=True, nullable=False)   # 1 user will have 1 email address, 
    DepartmentID = Column(Integer, ForeignKey("Department.DepartmentID"))


class DeviceType(Base):
     __tablename__ = "DeviceType"

     DeviceTypeID = Column(Integer, primary_key=True, index=True)
     DeviceTypeName = Column(String(20))



  

class Device(Base):
    __tablename__ = "Device"

    DeviceID = Column(Integer, primary_key=True, index=True)
    DeviceTypeID = Column(Integer, ForeignKey("DeviceType.DeviceTypeID"))
    AssetTag = Column(String(1000), unique = True)
    Manufacturer = Column(String(100))
    Model = Column(String(100))
    SerialNumber = Column(String(1000000), unique = True)  #serial numbers are unique per device, they should never be the same. 
    PurchaseDate = Column(Date)
    DepartmentID = Column(Integer, ForeignKey("Department.DepartmentID"))
    EmployeeID = Column(Integer, ForeignKey("Employee.EmployeeID"))
    PurchaseCost = Column(Integer)



class Department(Base):
    __tablename__ = "Department"
    DepartmentID = Column(Integer, primary_key=True, index=True)
    DepartmentName = Column(String)


class AuditLog(Base):
    __tablename__ = "AuditLog"

    AuditID = Column(Integer, primary_key=True, index=True)
    TableName = Column(String(100))
    RecordID = Column(Integer)
    FieldName = Column(String(1000))
    OldValue = Column(String(1000))
    NewValue = Column(String(1000))
    Action = Column(String(1000))
    ChangedBy = Column(String(10000000))
    ChangeDate = Column(DateTime)
