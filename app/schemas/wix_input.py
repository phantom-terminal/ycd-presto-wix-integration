"""Wix input schema

    This schema is used to parse data from the Wix API response.

    The schema contains the following classes:
    - `WebhookData` -- the model for the Wix webhook data.
    - `WebhookDataObject` -- the model for the Wix webhook data object.
    - `WebhookResponse` -- the model for the Wix webhook response.

    - `OrderWixModel` -- the model for the Wix order.
    - `ActionEvent` -- the model for the action event.
    - `BodyAsJson` -- the model for the body as json.
    - `WixOrderAsJson` -- the model for the Wix order as json.

    - `LineItems`-- the model for the line items.
    - `DishOption` -- the model for the dish option.
    - `AvailableChoices` -- the model for the available choices.
    - `SelectedChoices` -- the model for the selected choices.
    - `CatalogReference` -- the model for the catalog reference.

    - `Discounts` -- the model for the discounts.
    - `Payment` -- the model for the payment.
    - `Fulfillment` -- the model for the fulfillment.
    - `Customer` -- the model for the customer.
    - `Totals` -- the model for the totals.
    - `Activities` -- the model for the activities.
    - `ChannelInfo` -- the model for the channel info.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WebhookResponse(BaseModel):
    """Schema for the response of the webhook receiver

    Params:
        status: Status of the response
    """
    status: str = Field(..., description="Status of the response")


class WebhookDataObject(BaseModel):
    """Schema for the data object of the webhook

    Params:
        event_type: Type of the event.
        instance_id: ID of the instance.
        data: Data of the event.
    """
    event_type: str = Field(..., alias="eventType", description="Type of the event")
    instance_id: str = Field(..., alias="instanceId", description="Id of the instance")
    data: str = Field(..., description="Data of the event")


class WebhookData(BaseModel):
    """Schema for the data of the webhook

    Params:
        data: General data of the event.
    """
    data: WebhookDataObject = Field(..., description="Data of the event")


class AvailableChoices(BaseModel):
    """Schema for the available choices

    Params:
        item_id: ID of the item.
        price: Price of the item.
    """
    item_id: str = Field(..., alias="itemId", description="Id of the item")
    price: float = Field(..., description="Price of the item")


class CatalogReference(BaseModel):
    """Schema for the catalog reference

    Params:
        catalog_item_id: ID of the catalog item.
        catalog_item_name: Name of the catalog item.
        catalog_item_decision: Description of the catalog item.
        catalog_item_media: Media of the catalog item.
    """
    catalog_item_id: str = Field(
        ..., alias="catalogItemId", description="Catalog item id"
    )
    catalog_item_name: str = Field(
        ..., alias="catalogItemName", description="Catalog item name"
    )
    catalog_item_decision: str | None = Field(
        alias="catalogItemDecision",
        description="Catalog item decision",
    )
    catalog_item_media: str | None = Field(
        ..., alias="catalogItemMedia", description="Catalog item media"
    )


class SelectedChoices(BaseModel):
    """Schema for the selected choices

    Params:
        quantity: Quantity of the item.
        price: Price of the item.
        comment: Comment on the item.
        catalog_reference: Catalog reference of the item.
    """
    quantity: int = Field(..., description="Quantity of the choice")
    price: float = Field(..., description="Price of the choice")
    comment: str | None = Field(..., description="Comment on the choice")
    dish_options: Optional[list] = Field(description="Options of the choice")
    catalog_reference: CatalogReference = Field(
        ..., alias="catalogReference", description="Reference of the choice"
    )


class DishOption(BaseModel):
    """
    Schema for the dish option

    Params:
        name: Name of the option.
        min_choices: Minimum number of choices.
        max_choices: Maximum number of choices.
        type_: Type of the option.
        available_choices: Available choices of the option.
        default_choices: Default choices of the option.
        selected_choices: Selected choices of the option.
    """

    name: str = Field(..., description="Name of the option")
    min_choices: int = Field(
        ..., alias="minChoices", description="Minimum number of choices"
    )
    max_choices: int = Field(
        ..., alias="maxChoices", description="Maximum number of choices"
    )
    type_: str = Field(..., alias="type", description="Type of the option")
    available_choices: list[AvailableChoices] = Field(
        ..., alias="availableChoices", description="Available choices"
    )
    default_choices: list = Field(
        ..., alias="defaultChoices", description="Default choices"
    )
    selected_choices: list[SelectedChoices] = Field(
        ..., alias="selectedChoices", description="Selected choices"
    )


class LineItems(BaseModel):
    """Schema for the line items

    Params:
        quantity: Quantity of the item.
        price: Price of the item.
        comment: Comment on the item.
        dish_options: Options of the item.
        catalog_reference: Reference of the item.
    """
    quantity: int = Field(..., description="Quantity of the item")
    price: float = Field(..., description="Price of the item")
    comment: str | None = Field(..., description="Comment on the item")
    dish_options: list[DishOption] = Field(
        alias="dishOptions", description="Options of the item"
    )
    catalog_reference: CatalogReference = Field(
        ..., alias="catalogReference", description="Catalog reference of the item"
    )


class Discounts(BaseModel):
    """Schema for the discounts

    Params:
        catalog_discount_id: ID of the catalog discount.
        applied_amount: Amount of the discount.
        catalog_discount_type: Type of the discount.
        catalog_discount_name: Name of the discount.
    """
    catalog_discount_id: str = Field(
        ..., alias="catalogDiscountId", description="Catalog discount id"
    )
    applied_amount: float = Field(
        ..., alias="appliedAmount", description="Applied amount of the discount"
    )
    catalog_discount_type: str = Field(
        ..., alias="catalogDiscountType", description="Catalog discount type"
    )
    catalog_discount_name: str = Field(
        ..., alias="catalogDiscountName", description="Catalog discount name"
    )


class Payments(BaseModel):
    """Schema for the payments

    Params:
        type_: Type of the payment.
        amount: Amount of the payment.
        method: Method of the payment.
        provider_transaction_id: Provider transaction ID of the payment.
    """
    type_: str = Field(..., alias="type", description="Type of the payment")
    amount: float = Field(..., description="Amount of the payment")
    method: str = Field(..., description="Method of the payment")
    provider_transaction_id: str = Field(
        ..., alias="providerTransactionId", description="Provider transaction id"
    )


class Location(BaseModel):
    """Schema for the location
    Params:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
    """
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")


class AddressOfDelivery(BaseModel):
    """Schema for the address of delivery

    Params:
        formatted: Formatted address of the delivery.
        country: Country of the delivery.
        city: City of the delivery.
        street: Street of the delivery.
        street_number: Street number of the delivery.
        apt: Apartment of the delivery.
        floor: Floor of the delivery.
        entrance: Entrance of the delivery.
        zip_code: Zip code of the delivery.
        country_code: Country code of the delivery.
        on_arrival: On arrival of the delivery.
        approximate: Approximate of the delivery.
        location: Location of the delivery.
        address_line_2: Address line 2 of the delivery.
    """
    formatted: str = Field(..., description="Formatted address")
    country: str | None = Field(..., description="Country of the delivery")
    city: str = Field(..., description="City of the delivery")
    street: str = Field(..., description="Street of the delivery")
    street_number: int = Field(
        ..., alias="streetNumber", description="Street number of the delivery"
    )
    apt: int | str = Field(..., description="Apartment of the delivery")
    floor: int | str = Field(..., description="Floor of the delivery")
    entrance: int | str | None = Field(..., description="Entrance of the delivery")
    zip_code: str = Field(..., alias="zipCode", description="Zip code of the delivery")
    country_code: str = Field(
        ..., alias="countryCode", description="Country code of the delivery"
    )
    on_arrival: str = Field(
        ..., alias="onArrival", description="On arrival of the delivery"
    )
    approximate: bool = Field(..., description="Approximate of the delivery")
    comment: str | None = Field(..., description="Comment of the delivery")
    location: Location = Field(..., description="Location of the delivery")
    address_line_2: str | None = Field(
        ..., alias="addressLine2", description="Address line 2 of the delivery"
    )


class DeliveryDetails(BaseModel):
    """Schema for the delivery details

    Params:
        charge: Charge of the delivery.
        address_of_delivery: Address of the delivery.
    """
    charge: float = Field(..., description="Charge of the delivery")
    address_of_delivery: AddressOfDelivery = Field(
        ..., alias="address", description="Address of the delivery"
    )


class Fulfillment(BaseModel):
    """Schema for the fulfillment

    Params:
        type_: Type of the fulfillment.
        promised_time: Promised time of the fulfillment.
        asap: ASAP of the fulfillment.
        delivery_details: Delivery details of the fulfillment.
    """
    type_: str = Field(..., alias="type", description="Type of the fulfillment")
    promised_time: datetime = Field(
        ..., alias="promisedTime", description="Promised time of the fulfillment"
    )
    asap: bool = Field(..., description="Asap of the fulfillment")
    delivery_details: DeliveryDetails = Field(
        ..., alias="deliveryDetails", description="Delivery details of the fulfillment"
    )


class Customer(BaseModel):
    """Schema for the customer

    Params:
        first_name: First name of the customer.
        last_name: Last name of the customer.
        phone: Phone of the customer.
        email: Email of the customer.
        contact_id: Contact ID of the customer.
    """
    first_name: str = Field(
        ..., alias="firstName", description="First name of the customer"
    )
    last_name: str = Field(
        ..., alias="lastName", description="Last name of the customer"
    )
    phone: str = Field(..., description="Phone of the customer")
    email: str = Field(..., description="Email of the customer")
    contact_id: str = Field(
        ..., alias="contactId", description="Contact id of the customer"
    )


class Totals(BaseModel):
    """Schema for the totals

    Params:
        subtotal: Subtotal of the totals.
        total: Total of the totals.
        delivery: Delivery of the totals.
        tax: Tax of the totals.
        discount: Discount of the totals.
        loyalty_savings: Loyalty savings of the totals.
        quantity: Quantity of the totals.
        tip: Tip of the totals.
    """
    subtotal: float = Field(..., description="Subtotal of the order")
    total: float = Field(..., description="Total of the order")
    delivery: float | None = Field(..., description="Delivery of the order")
    tax: float | None = Field(..., description="Tax of the order")
    discount: float | None = Field(..., description="Discount of the order")
    loyalty_savings: float | None = Field(
        ..., alias="loyaltySavings", description="Loyalty savings of the order"
    )
    quantity: int = Field(..., description="Quantity of the order")
    tip: float | None = Field(..., description="Tip of the order")


class Activities(BaseModel):
    """Schema for the activities

    Params:
        timestamp: Timestamp of the activity.
        message: Message of the activity.
    """
    timestamp: datetime = Field(..., description="Timestamp of the activity")
    message: str = Field(..., description="Message of the activity")


class ChannelInfo(BaseModel):
    """Schema for the channel info

    Params:
        type_: Type of the channel info.
    """
    type_: str = Field(..., alias="type", description="Type of the channel")


class WixOrderAsJson(BaseModel):
    """Schema for the wix order as json

    Params:
        id_: ID of the order.
        created_date: Created date of the order.
        updated_date: Updated date of the order.
        comment: Comment of the order.
        status: Status of the order.
        line_items: Line items of the order.
        discounts: Discounts of the order.
        payments: Payments of the order.
        fulfillment: Fulfillment of the order.
        customer: Customer of the order.
        totals: Totals of the order.
        activities: Activities of the order.
        channel_info: Channel info of the order.
        coupon: Coupon of the order.
        loyalty_info: Loyalty info of the order.
    """
    id_: int = Field(..., alias="id", description="Id of the order")
    created_date: datetime = Field(
        ..., alias="createdDate", description="Date of the order"
    )
    updated_date: datetime = Field(
        ..., alias="updatedDate", description="Date of the order"
    )
    comment: str = Field(..., description="Comment to the order")
    currency: str = Field(..., description="Currency of the order")
    status: str = Field(..., description="Status of the order")
    line_items: list[LineItems] = Field(
        ..., alias="lineItems", description="Items of the order"
    )
    discounts: list[Discounts] = Field(
        ..., alias="discounts", description="Discounts of the order"
    )
    payments: list[Payments] = Field(
        ..., alias="payments", description="Payments of the order"
    )
    fulfillment: Fulfillment = Field(..., description="Fulfillment of the order")
    customer: Customer = Field(..., description="Customer of the order")
    totals: Totals = Field(..., description="Totals of the order")
    activities: list[Activities] = Field(..., description="Activities of the order")
    channel_info: ChannelInfo = Field(
        ..., alias="channelInfo", description="Channel info of the order"
    )
    coupon: str | None = Field(..., description="Coupon of the order")
    loyalty_info: str | None = Field(
        ..., alias="loyaltyInfo", description="Loyalty info of the order"
    )


class BodyAsJson(BaseModel):
    """Schema for the body as json

    Params:
        order: Order in the body of json.
    """
    order: WixOrderAsJson = Field(..., description="Order")


class ActionEvent(BaseModel):
    """Schema for the action event

    Params:
        body_as_json: Body as json of the action event.
    """
    body_as_json: BodyAsJson = Field(
        ..., alias="bodyAsJson", description="Body of the event"
    )


class OrderWixModel(BaseModel):
    """Schema for the order from the wix

    Params:
        id_: ID of the order.
        entity_fqdn: Entity FQDN of the order.
        slug: Slug of the order.
        action_event: Action event of the order.
        entity_id: Entity ID of the order.
        event_time: Event time of the order.
        triggered_by_anonymize_request: Triggered by anonymize request of the order.
    """
    id_: str = Field(..., alias="id", description="Id of the order")
    entity_fqdn: str = Field(
        ..., alias="entityFqdn", description="Entity fqdn of the order"
    )
    slug: str = Field(..., description="Slug of the order")
    action_event: ActionEvent = Field(
        ..., alias="actionEvent", description="Action event of the order"
    )
    entity_id: int = Field(..., alias="entityId", description="Entity id of the order")
    event_time: datetime = Field(
        ..., alias="eventTime", description="Event time of the order"
    )
    triggered_by_anonymize_request: bool = Field(
        ...,
        alias="triggeredByAnonymizeRequest",
        description="Trigger by anonymize request of the order",
    )
