from datetime import datetime

from pydantic import BaseModel, Field


class WebhookResponse(BaseModel):
    status: str = Field(..., description="Status of the response")


class WebhookDataObject(BaseModel):
    event_type: str = Field(..., alias="eventType", description="Type of the event")
    instance_id: str = Field(..., alias="instanceId", description="Id of the instance")
    data: str = Field(..., description="Data of the event")


class WebhookData(BaseModel):
    data: WebhookDataObject = Field(..., description="Data of the event")


class DishOption(BaseModel):
    """
    Schema for the dish option
    """


class CatalogReference(BaseModel):
    catalog_item_id: str = Field(alias="catalogItemId", description="Catalog item id")
    catalog_item_name: str = Field(
        alias="catalogItemName", description="Catalog item name"
    )
    catalog_item_decision: str | None = Field(
        alias="catalogItemDecision", description="Catalog item decision"
    )
    catalog_item_media: str | None = Field(
        alias="catalogItemMedia", description="Catalog item media"
    )


class LineItems(BaseModel):
    quantity: int = Field(..., description="Quantity of the item")
    price: float = Field(..., description="Price of the item")
    comment: str | None = Field(..., description="Comment on the item")
    dish_options: list = Field(alias="dishOptions", description="Options of the item")
    catalog_reference: CatalogReference = Field(
        alias="catalogReference", description="Catalog reference of the item"
    )


class Discounts(BaseModel):
    catalog_discount_id: str = Field(
        alias="catalogDiscountId", description="Catalog discount id"
    )
    applied_amount: float = Field(
        alias="appliedAmount", description="Applied amount of the discount"
    )
    catalog_discount_type: str = Field(
        alias="catalogDiscountType", description="Catalog discount type"
    )
    catalog_discount_name: str = Field(
        alias="catalogDiscountName", description="Catalog discount name"
    )


class Payments(BaseModel):
    type_: str = Field(alias="type", description="Type of the payment")
    amount: float = Field(..., description="Amount of the payment")
    method: str = Field(..., description="Method of the payment")
    provider_transaction_id: str = Field(
        alias="providerTransactionId", description="Provider transaction id"
    )


class Location(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")


class AddressOfDelivery(BaseModel):
    formatted: str = Field(..., description="Formatted address")
    country: str | None = Field(..., description="Country of the delivery")
    city: str = Field(..., description="City of the delivery")
    street: str = Field(..., description="Street of the delivery")
    street_number: int = Field(
        alias="streetNumber", description="Street number of the delivery"
    )
    apt: int | str = Field(..., description="Apartment of the delivery")
    floor: int | str = Field(..., description="Floor of the delivery")
    entrance: int | str | None = Field(..., description="Entrance of the delivery")
    zip_code: str = Field(alias="zipCode", description="Zip code of the delivery")
    country_code: str = Field(
        alias="countryCode", description="Country code of the delivery"
    )
    on_arrival: str = Field(alias="onArrival", description="On arrival of the delivery")
    approximate: bool = Field(..., description="Approximate of the delivery")
    comment: str | None = Field(..., description="Comment of the delivery")
    location: Location = Field(..., description="Location of the delivery")
    address_line_2: str | None = Field(
        alias="addressLine2", description="Address line 2 of the delivery"
    )


class DeliveryDetails(BaseModel):
    charge: float = Field(..., description="Charge of the delivery")
    address_of_delivery: AddressOfDelivery = Field(
        alias="address", description="Address of the delivery"
    )


class Fulfillment(BaseModel):
    type_: str = Field(alias="type", description="Type of the fulfillment")
    promised_time: datetime = Field(
        alias="promisedTime", description="Promised time of the fulfillment"
    )
    asap: bool = Field(..., description="Asap of the fulfillment")
    delivery_details: DeliveryDetails = Field(
        alias="deliveryDetails", description="Delivery details of the fulfillment"
    )


class Customer(BaseModel):
    first_name: str = Field(alias="firstName", description="First name of the customer")
    last_name: str = Field(alias="lastName", description="Last name of the customer")
    phone: str = Field(..., description="Phone of the customer")
    email: str = Field(..., description="Email of the customer")
    contact_id: str = Field(alias="contactId", description="Contact id of the customer")


class Totals(BaseModel):
    subtotal: float = Field(..., description="Subtotal of the order")
    total: float = Field(..., description="Total of the order")
    delivery: float | None = Field(..., description="Delivery of the order")
    tax: float | None = Field(..., description="Tax of the order")
    discount: float | None = Field(..., description="Discount of the order")
    loyalty_savings: float | None = Field(
        alias="loyaltySavings", description="Loyalty savings of the order"
    )
    quantity: int = Field(..., description="Quantity of the order")
    tip: float | None = Field(..., description="Tip of the order")


class Activities(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the activity")
    message: str = Field(..., description="Message of the activity")


class ChannelInfo(BaseModel):
    type_: str = Field(alias="type", description="Type of the channel")


class WixOrderAsJson(BaseModel):
    id_: int = Field(alias="id", description="Id of the order")
    created_date: datetime = Field(alias="createdDate", description="Date of the order")
    updated_date: datetime = Field(alias="updatedDate", description="Date of the order")
    comment: str = Field(..., description="Comment to the order")
    currency: str = Field(..., description="Currency of the order")
    status: str = Field(..., description="Status of the order")
    line_items: list[LineItems] = Field(
        alias="lineItems", description="Items of the order"
    )
    discounts: list[Discounts] = Field(
        alias="discounts", description="Discounts of the order"
    )
    payments: list[Payments] = Field(
        alias="payments", description="Payments of the order"
    )
    fulfillment: Fulfillment = Field(..., description="Fulfillment of the order")
    customer: Customer = Field(..., description="Customer of the order")
    totals: Totals = Field(..., description="Totals of the order")
    activities: list[Activities] = Field(..., description="Activities of the order")
    channel_info: ChannelInfo = Field(
        alias="channelInfo", description="Channel info of the order"
    )
    coupon: str | None = Field(..., description="Coupon of the order")
    loyalty_info: str | None = Field(
        alias="loyaltyInfo", description="Loyalty info of the order"
    )


class BodyAsJson(BaseModel):
    order: WixOrderAsJson = Field(..., description="Order")


class ActionEvent(BaseModel):
    body_as_json: BodyAsJson = Field(
        alias="bodyAsJson", description="Body of the event"
    )


class OrderWixModel(BaseModel):
    id_: str = Field(alias="id", description="Id of the order")
    entity_fqdn: str = Field(alias="entityFqdn", description="Entity fqdn of the order")
    slug: str = Field(..., description="Slug of the order")
    action_event: ActionEvent = Field(
        alias="actionEvent", description="Action event of the order"
    )
    entity_id: int = Field(alias="entityId", description="Entity id of the order")
    event_time: datetime = Field(
        alias="eventTime", description="Event time of the order"
    )
    triggered_by_anonymize_request: bool = Field(
        alias="triggeredByAnonymizeRequest",
        description="Trigger by anonymize request of the order",
    )
