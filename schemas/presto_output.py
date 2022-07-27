from pydantic import BaseModel, Field


class Contact(BaseModel):
    first_name: str = Field(
        ..., alias="firstName", description="First name of the contact"
    )
    last_name: str = Field(
        ..., alias="lastName", description="Last name of the contact"
    )
    phone: str = Field(..., description="Phone number of the contact")


class Address(BaseModel):
    formatted: str = Field(..., description="Formatted address")
    city: str = Field(..., description="City of the client")
    number: str = Field(..., description="Number of house/flat of the client")
    entrance: str = Field(..., description="Entrance of the client")
    floor: str = Field(..., description="Floor of the client")
    apt: str = Field(..., description="Apartment of the client")
    comment: str = Field(..., description="Comment of the client")


class Delivery(BaseModel):
    type_: str = Field(..., alias="type", description="Type of delivery")
    address: Address = Field(..., description="Address of the delivery")
    charge: str = Field(..., description="Charge of the delivery")
    number_of_people: str = Field(
        ..., alias="numppl", description="Number of people in the delivery"
    )
    worker_code: int = Field(
        ..., alias="workercode", description="Worker code of the delivery"
    )


class OrderItemOption(BaseModel):
    type_: str = Field(..., alias="type", description="Type of option")
    id_: int = Field(..., alias="id", description="Id of the option")
    price: int = Field(..., description="Price for the option")
    comment: str = Field(..., description="Comment on the option")


class OrderItem(BaseModel):
    type_: str = Field(..., alias="type", description="Type of the item")
    id_: int = Field(..., alias="id", description="Id of the item")
    price: int = Field(..., description="Price for the item")
    comment: str = Field(..., description="Comment on the item")
    options: list[OrderItemOption] = Field(
        ..., alias="children", description="Options of the item"
    )
    count_of_items: int = Field(..., alias="itemcount", description="Number of items")
    count_of_options: int = Field(
        ..., alias="childrencount", description="Number of options"
    )


class OrderCharge(BaseModel):
    amount: int = Field(..., description="Amount of the charge")


class PaymentCard(BaseModel):
    number: str = Field(..., description="Number of the card")
    expire_month: int = Field(
        ..., alias="expireMonth", description="Expire month of the card"
    )
    expire_year: int = Field(
        ..., alias="expireYear", description="Expire year of the card"
    )
    holder_id: str = Field(..., alias="holderId", description="Holder id of the card")
    holder_name: str = Field(
        ..., alias="holderName", description="Holder name on the card"
    )


class Payment(BaseModel):
    type_: str = Field(..., alias="type", description="Type of the payment")
    amount: int = Field(..., description="Amount of the payment")
    card: PaymentCard = Field(..., description="Card of the payment")


class OrderPrestoModel(BaseModel):
    id_: int = Field(..., alias="id", description="Id of the order")
    contact: Contact = Field(..., description="Contact of the order")
    delivery: Delivery = Field(..., description="Delivery of the order")
    order_items: list[OrderItem] = Field(
        ..., alias="orderItems", description="Items of the order"
    )
    comment: str = Field(..., description="Comment to the order")
    takeout_packs: str = Field(
        ..., alias="takeoutPacks", description="Takeout packs of the order"
    )
    order_charges: list[OrderCharge] = Field(
        ..., alias="orderCharges", description="Charges of the order"
    )
    price: str = Field(..., description="Price of the order")
    payments: list[Payment] = Field(..., description="Payments of the order")
