from datetime import datetime
from gettext import Catalog

from pydantic import BaseModel, ValidationError, Field
from starlette import status

INPUT_JSON = """
{
    "id" : "52269077-05f2-4b59-ba4f-36ef8c4c1e11",
    "entityFqdn" : "wix.restaurants.v3.order",
    "slug" : "new_order",
    "actionEvent" : {
      "bodyAsJson" : {
        "order" : {
          "id" : "64783425355",
          "createdDate" : "2021-07-07T10:37:44.994Z",
          "updatedDate" : "2021-07-07T10:39:46.994Z",
          "comment" : "No peanuts please",
          "currency" : "USD",
          "status" : "NEW",
          "lineItems" : [ {
            "quantity" : 5,
            "price" : "2.00",
            "comment" : null,
            "dishOptions" : [ {
              "name" : "Taco Options",
              "minChoices" : 0,
              "maxChoices" : 3,
              "type" : "EXTRAS",
              "availableChoices" : [ {
                "itemId" : "2b5131cd-7872-4ee8-ae40-cb00c6dcaec1",
                "price" : "1.00"
              }, {
                "itemId" : "d5e1b8f4-f18e-4fba-8ef4-33ad632b6c40",
                "price" : "1.50"
              }, {
                "itemId" : "0f3fee4d-1b4a-4cfd-9c79-11a52e8e4024",
                "price" : "1.50"
              } ],
              "defaultChoices" : [ ],
              "selectedChoices" : [ {
                "quantity" : 1,
                "price" : "1.50",
                "comment" : null,
                "dishOptions" : [ ],
                "catalogReference" : {
                  "catalogItemId" : "d5e1b8f4-f18e-4fba-8ef4-33ad632b6c40",
                  "catalogItemName" : "Fried Beans",
                  "catalogItemDescription" : null,
                  "catalogItemMedia" : null
                }
              } ]
            } ],
            "catalogReference" : {
              "catalogItemId" : "81cddf94-dcad-4f0e-9c3c-7556e3dbd4d8",
              "catalogItemName" : "Chicken Taco",
              "catalogItemDescription" : "with fresh veggies and Roasted Tomato Salsa",
              "catalogItemMedia" : "https://static.wixstatic.com/media/11062bA4cabfdc2652413d92990cfac29777cc~mv2.jpg"
            }
          } ],
          "discounts" : [ {
            "catalogDiscountId" : "bc697347-c180-494b-b68d-bc63ac63a84b",
            "appliedAmount" : "15.00",
            "catalogDiscountType" : "OFF_ORDER",
            "catalogDiscountName" : "Sunday Order Discount"
          } ],
          "payments" : [ {
            "type" : "CASH",
            "amount" : "10.00",
            "method" : "offline",
            "providerTransactionId" : "d9ef0f0c-e81a-4017-9d6a-977089eb411f"
          } ],
          "fulfillment" : {
            "type" : "DELIVERY",
            "promisedTime" : "2021-07-07T11:17:44.994Z",
            "asap" : true,
            "deliveryDetails" : {
              "charge" : "0.00",
              "address" : {
                "formatted" : "235 W 23rd St, New York, NY 10011, United States",
                "country" : null,
                "city" : "New York",
                "street" : "West 23rd Street",
                "streetNumber" : "235",
                "apt" : "1",
                "floor" : "3",
                "entrance" : null,
                "zipCode" : "10011-2302",
                "countryCode" : "US",
                "onArrival" : "UNSPECIFIED_ON_ARRIVAL_TYPE",
                "approximate" : false,
                "comment" : null,
                "location" : {
                  "latitude" : 40.7448484,
                  "longitude" : -73.9967498
                },
                "addressLine2" : null
              }
            }
          },
          "customer" : {
            "firstName" : "John",
            "lastName" : "Smith",
            "phone" : "2075556300",
            "email" : "john@example.com",
            "contactId" : "8046df3c-7575-4098-a5ab-c91ad8f33c47"
          },
          "totals" : {
            "subtotal" : "10.00",
            "total" : "10.00",
            "delivery" : null,
            "tax" : null,
            "discount" : null,
            "loyaltySavings" : null,
            "quantity" : 1,
            "tip" : null
          },
          "activities" : [ {
            "timestamp" : "2021-07-07T10:37:44.994Z",
            "message" : "new"
          }, {
            "timestamp" : "2021-07-07T10:39:46.994Z",
            "message" : "accepted []"
          } ],
          "channelInfo" : {
            "type" : "WEB"
          },
          "coupon" : null,
          "loyaltyInfo" : null
        }
      }
    },
    "entityId" : "64783425355",
    "eventTime" : "2021-07-07T10:47:44.994Z",
    "triggeredByAnonymizeRequest" : false
  } 
"""
OUTPUT_JSON = """{"id":459840,"contact":{"firstName":"test","lastName":"test","phone":"0544520187"},"delivery":{"type":"delivery","address":{"formatted":"��� ����, test 1 \/ 1","city":"��� ����","street":"test","number":"1","entrance":"","floor":"","apt":"1","comment":""},"charge":"8","numppl":"1","workercode":1},"orderItems":[{"type":"item","id":762,"price":0,"comment":"0","children":[],"itemcount":1,"childrencount":0},{"type":"item","id":101,"price":0,"comment":"0","children":[],"itemcount":1,"childrencount":0},{"type":"item","id":761,"price":0,"comment":"","children":[],"itemcount":2,"childrencount":0},{"type":"item","id":765,"price":0,"comment":"","children":[],"itemcount":2,"childrencount":0},{"type":"item","id":74,"price":42,"comment":" \/\/ ��� ������","children":[{"type":"option","id":290,"price":0,"comment":""}],"itemcount":1,"childrencount":1},{"type":"item","id":74,"price":42,"comment":" \/\/ ��� ������","children":[{"type":"option","id":290,"price":0,"comment":""}],"itemcount":1,"childrencount":1}],"comment":"","takeoutPacks":"1","orderCharges":[{"amount":0}],"price":"92","payments":[{"type":"cash","amount":92,"card":{"number":"","expireMonth":1,"expireYear":1,"holderId":"","holderName":""}}]}"""

"""
This is the schema for the data that is sent to the Presto.
"""


class Contact(BaseModel):
    first_name: str = Field(alias="firstName", description="First name of the contact")
    last_name: str = Field(alias="lastName", description="Last name of the contact")
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
    type_: str = Field(alias="type", description="Type of delivery")
    address: Address = Field(..., description="Address of the delivery")
    charge: str = Field(..., description="Charge of the delivery")
    number_of_people: str = Field(
        alias="numppl", description="Number of people in the delivery"
    )
    worker_code: int = Field(
        alias="workercode", description="Worker code of the delivery"
    )


class OrderItemOption(BaseModel):
    type_: str = Field(alias="type", description="Type of option")
    id_: int = Field(alias="id", description="Id of the option")
    price: int = Field(..., description="Price for the option")
    comment: str = Field(..., description="Comment on the option")


class OrderItem(BaseModel):
    type_: str = Field(alias="type", description="Type of the item")
    id_: int = Field(alias="id", description="Id of the item")
    price: int = Field(..., description="Price for the item")
    comment: str = Field(..., description="Comment on the item")
    options: list[OrderItemOption] = Field(
        alias="children", description="Options of the item"
    )
    count_of_items: int = Field(alias="itemcount", description="Number of items")
    count_of_options: int = Field(
        alias="childrencount", description="Number of options"
    )


class OrderCharge(BaseModel):
    amount: int = Field(..., description="Amount of the charge")


class PaymentCard(BaseModel):
    number: str = Field(..., description="Number of the card")
    expire_month: int = Field(
        alias="expireMonth", description="Expire month of the card"
    )
    expire_year: int = Field(alias="expireYear", description="Expire year of the card")
    holder_id: str = Field(alias="holderId", description="Holder id of the card")
    holder_name: str = Field(alias="holderName", description="Holder name on the card")


class Payment(BaseModel):
    type_: str = Field(alias="type", description="Type of the payment")
    amount: int = Field(..., description="Amount of the payment")
    card: PaymentCard = Field(..., description="Card of the payment")


class OrderPrestoModel(BaseModel):
    id_: int = Field(alias="id", description="Id of the order")
    contact: Contact = Field(..., description="Contact of the order")
    delivery: Delivery = Field(..., description="Delivery of the order")
    order_items: list[OrderItem] = Field(
        alias="orderItems", description="Items of the order"
    )
    comment: str = Field(..., description="Comment to the order")
    takeout_packs: str = Field(
        alias="takeoutPacks", description="Takeout packs of the order"
    )
    order_charges: list[OrderCharge] = Field(
        alias="orderCharges", description="Charges of the order"
    )
    price: str = Field(..., description="Price of the order")
    payments: list[Payment] = Field(..., description="Payments of the order")


"""
Schema for the order from Wix API webhook
"""


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


try:
    order = OrderPrestoModel.parse_raw(OUTPUT_JSON)
except ValidationError as e:
    print(e.json())
else:
    print(order.json(by_alias=True))
    with open(f"{order.id_}.bok", "w") as order_file:
        order_file.write(order.json(by_alias=True).replace(" ", ""))


try:
    order = OrderWixModel.parse_raw(INPUT_JSON)
except ValidationError as e:
    print(e.json())
else:
    print(order.json(by_alias=True))
