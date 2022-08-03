"""Presto output schema

    This schema is used to parse data of the Presto.

    The schema contains the following classes:

    - `OrderPrestoModel` - the model for the Presto order.
    - `Contact` - the model for contact.
    - `Delivery` - the model for delivery.
    - `Address` - the model for address.
    - `Order` - the model for order.
    - `OrderItem` - the model for order item.
    - `OrderItemOption` - the model for order item option.
    - `OrderCharge` - the model for order charge.
    - `Payment` - the model for payment.
    - `PaymentCard` - the model for payment card.
"""

from pydantic import BaseModel, Field


class Contact(BaseModel):
    """Schema for the contact

    Params:
        first_name: First name of the contact
        last_name: Last name of the contact
        phone: Phone number of the contact
    """
    first_name: str = Field(
        ..., alias="firstName", description="First name of the contact"
    )
    last_name: str = Field(
        ..., alias="lastName", description="Last name of the contact"
    )
    phone: str = Field(..., description="Phone number of the contact")


class Address(BaseModel):
    """Schema for the address

    Params:
        formatted: Formatted address.
        city: City of the address.
        number: Number of the house.
        entrance: Entrance of the house.
        floor: Floor of the house.
        apt: Apartment of the house.
        comment: Comment about the address.
    """
    formatted: str = Field(..., description="Formatted address")
    city: str = Field(..., description="City of the client")
    number: str = Field(..., description="Number of house/flat of the client")
    entrance: str = Field(..., description="Entrance of the client")
    floor: str = Field(..., description="Floor of the client")
    apt: str = Field(..., description="Apartment of the client")
    comment: str = Field(..., description="Comment of the client")


class Delivery(BaseModel):
    """Schema for the delivery

    Params:
        type_: Type of the delivery.
        address: Address of the delivery.
        charge: Charge of the delivery.
        number_of_people: Number of people in the delivery.
        worker_code: Worker code of the delivery.
    """
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
    """Schema for the order item option

    Params:
        type_: Type of the option.
        id_: ID of the option.
        price: Price of the option.
        comment: Comment for the option.
    """
    type_: str = Field(..., alias="type", description="Type of option")
    id_: int = Field(..., alias="id", description="Id of the option")
    price: int = Field(..., description="Price for the option")
    comment: str = Field(..., description="Comment on the option")


class OrderItem(BaseModel):
    """Schema for the order item

    Params:
        type_: Type of the item.
        id_: ID of the item.
        price: Price of the item.
        comment: Comment for the item.
        options: Options for the item.
        count_of_items: Count of items in the order.
        count_of_options: Count of options in the order.
    """
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
    """Schema for the order charge

    Params:
        amount: Amount of the charge.
    """
    amount: int = Field(..., description="Amount of the charge")


class PaymentCard(BaseModel):
    """Schema for the payment card

    Params:
        number: Number of the card.
        expire_month: Expiration month of the card.
        expire_year: Expiration year of the card.
        holder_id: Holder ID of the card.
        holder_name: Holder name of the card.
    """
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
    """Schema for the payment

    Params:
        type_: Type of the payment.
        amount: Amount of the payment.
        card: Card of the payment.
    """
    type_: str = Field(..., alias="type", description="Type of the payment")
    amount: int = Field(..., description="Amount of the payment")
    card: PaymentCard = Field(..., description="Card of the payment")


class OrderPrestoModel(BaseModel):
    """Schema for the order

    Params:
        id_: ID of the order.
        contact: Contact of the order.
        delivery: Delivery of the order.
        order_items: Items in the order.
        comment: Comment for the order.
        takeout_packs: Takeout packs for the order.
        order_charges: Charges for the order.
        price: Price for the order.
        payment: Payment for the order.
    """
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
