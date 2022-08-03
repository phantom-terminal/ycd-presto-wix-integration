"""The module contains the general function for working with data from Wix webhook:

- `create_file_for_presto(data: str)` -- Creates a data file in the working directory.
- `print_data_from_wix_order(data: str)` -- Prints data from Wix API order.
- `create_data_for_presto(data_in: str, data_out: str)` -- Creates data for Presto.
"""

from pydantic import ValidationError

from app.schemas.presto_output import OrderPrestoModel, OrderItem
from app.schemas.wix_input import OrderWixModel


def create_file_for_presto(data: str):
    """Creates a data file in the working directory

    Args:
        data: Ready-made data from Wix API to be parsed for Presto

    Returns:
        None -- Creates a file in the working directory
    """
    try:
        order = OrderPrestoModel.parse_raw(data)
    except ValidationError as e:
        print(e.json())
    else:
        print(order.json(by_alias=True))
        with open(f"{order.id_}.bok", "w") as order_file:
            order_file.write(order.json(by_alias=True).replace(" ", ""))


def print_data_from_wix_order(data: str):
    """Prints data from Wix API order

    Args:
        data: Raw data from Wix API

    Returns:
        None -- Prints data from Wix API
    """
    try:
        order = OrderWixModel.parse_raw(data)
    except ValidationError as e:
        print(e.json())
    else:
        print(order.json(by_alias=True))


def create_data_for_presto(data_in: str, data_out: str):
    """Validates the received data and prepares the data for Presto

    Args:
        data_in: Data received from Wix
        data_out: Data to be sent to Presto

    Returns:
        Data to be sent to Presto
    """
    try:
        order_from_wix = OrderWixModel.parse_raw(data_in)
        order_to_presto = OrderPrestoModel.parse_raw(data_out)
    except ValidationError as e:
        print(e.json())
    else:
        print(order_from_wix.json(by_alias=True))
        print(order_to_presto.json(by_alias=True))

        order_to_presto.id_ = order_from_wix.action_event.body_as_json.order.id_

        # order_to_presto.contact = Contact

        order_to_presto.contact.first_name = (
            order_from_wix.action_event.body_as_json.order.customer.first_name
        )
        order_to_presto.contact.last_name = (
            order_from_wix.action_event.body_as_json.order.customer.last_name
        )
        order_to_presto.contact.phone = (
            order_from_wix.action_event.body_as_json.order.customer.phone
        )

        # order_to_presto.delivery = Delivery

        order_to_presto.delivery.type_ = (
            order_from_wix.action_event.body_as_json.order.fulfillment.type_
        )

        # order_to_presto.delivery.address = Address

        order_to_presto.delivery.address.formatted = (
            order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.address_of_delivery.formatted
        )
        order_to_presto.delivery.address.city = (
            order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.address_of_delivery.city
        )
        # order_to_presto.delivery.address.street = (
        #     order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.address_of_delivery.street
        # )
        order_to_presto.delivery.address.number = (
            order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.address_of_delivery.street_number
        )
        order_to_presto.delivery.address.entrance = (
            order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.address_of_delivery.entrance
        )
        order_to_presto.delivery.address.floor = (
            order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.address_of_delivery.floor
        )
        order_to_presto.delivery.address.apt = (
            order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.address_of_delivery.apt
        )
        order_to_presto.delivery.address.comment = (
            order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.address_of_delivery.comment
        )

        order_to_presto.delivery.charge = (
            order_from_wix.action_event.body_as_json.order.fulfillment.delivery_details.charge
        )

        order_to_presto.delivery.number_of_people = (
            "N/A"  # find data in wix or another source
        )

        order_to_presto.delivery.worker_code = (
            "N/A"  # find data in wix or another source
        )

        # order_to_presto.order_items = []
        presto_order_item = OrderItem(**order_to_presto.order_items[0].dict(by_alias=True))
        # presto_order_option = OrderItemOption(**order_to_presto.order_items[0].options[0].dict(by_alias=True))
        for order_item in order_from_wix.action_event.body_as_json.order.line_items:
            presto_order_item.type_ = "item"
            presto_order_item.id_ = "N/A"
            presto_order_item.price = order_item.price
            presto_order_item.comment = order_item.comment
            presto_order_item.options = []
            # for option in order_item.dish_options:
            #     presto_order_option.id_ = "N/A"
            #     presto_order_option.price = option.price
            #     presto_order_option.comment = option.comment
            #     presto_order_item.options.append(presto_order_option)
            presto_order_item.count_of_items = order_item.quantity
            presto_order_item.count_of_options = len(presto_order_item.options)

            order_to_presto.order_items.append(presto_order_item)

        order_to_presto.comment = order_from_wix.action_event.body_as_json.order.comment

        order_to_presto.takeout_packs = "N/A"  # find data in wix or another source

        order_to_presto.order_charges = []
        """
        Here need "for" statement, but not clear what is "amount" in presto exactly
        in wix order.
        """

        order_to_presto.price = (
            order_from_wix.action_event.body_as_json.order.totals.total
        )

        # order_to_presto.payments = Payment
        # order_to_presto.payments.card = PaymentCard

        # order_to_presto.payments = []
        # for payment in order_from_wix.action_event.body_as_json.order.payments:
        #     payment_in_order_for_presto = Payment
        #     payment_in_order_for_presto.type_ = payment.type_
        #     payment_in_order_for_presto.amount = payment.amount
        #
        #     payment_in_order_for_presto.card.number = (
        #         "N/A"  # wix doesn't have card number
        #     )
        #     payment_in_order_for_presto.card.expiration_month = (
        #         "N/A"  # wix doesn't have card expiration date
        #     )
        #     payment_in_order_for_presto.card.expiration_year = (
        #         "N/A"  # wix doesn't have card expiration
        #     )
        #     payment_in_order_for_presto.card.holder_id = (
        #         "N/A"  # wix doesn't have card holder id
        #     )
        #     payment_in_order_for_presto.card.holder_name = (
        #         "N/A"  # wix doesn't have card holder name
        #     )
        #
        #     order_to_presto.payments.append(payment_in_order_for_presto)
        print(order_to_presto.json(by_alias=True))


if __name__ == "__main__":
    OUTPUT_JSON = """
    {
        "id": 45984,
        "contact": {
            "firstName": "test",
            "lastName": "test",
            "phone": "0544520187"
        },
        "delivery": {
            "type": "delivery",
            "address": {
                "formatted": "��� ����, test 1 \/ 1",
                "city": "��� ����",
                "street": "test",
                "number": "1",
                "entrance": "",
                "floor": "",
                "apt": "1",
                "comment": ""
            },
            "charge": "8",
            "numppl": "1",
            "workercode": 1
        },
        "orderItems": [
            {
                "type": "item",
                "id": 762,
                "price": 0,
                "comment": "0",
                "children": [],
                "itemcount": 1,
                "childrencount": 0
            },
            {
                "type": "item",
                "id": 101,
                "price": 0,
                "comment": "0",
                "children": [],
                "itemcount": 1,
                "childrencount": 0
            },
            {
                "type": "item",
                "id": 761,
                "price": 0,
                "comment": "",
                "children": [],
                "itemcount": 2,
                "childrencount": 0
            },
            {
                "type": "item",
                "id": 765,
                "price": 0,
                "comment": "",
                "children": [],
                "itemcount": 2,
                "childrencount": 0
            },
            {
                "type": "item",
                "id": 74,
                "price": 42,
                "comment": " \/\/ ��� ������",
                "children": [
                    {
                        "type": "option",
                        "id": 290,
                        "price": 0,
                        "comment": ""
                    }
                ],
                "itemcount": 1,
                "childrencount": 1
            },
            {
                "type": "item",
                "id": 74,
                "price": 42,
                "comment": " \/\/ ��� ������",
                "children": [
                    {
                        "type": "option",
                        "id": 290,
                        "price": 0,
                        "comment": ""
                    }
                ],
                "itemcount": 1,
                "childrencount": 1
            }
        ],
        "comment": "",
        "takeoutPacks": "1",
        "orderCharges": [
            {
                "amount": 0
            }
        ],
        "price": "92",
        "payments": [
            {
                "type": "cash",
                "amount": 92,
                "card": {
                    "number": "",
                    "expireMonth": 1,
                    "expireYear": 1,
                    "holderId": "",
                    "holderName": ""
                }
            }
        ]
    }
"""

    # create_file_for_presto(OUTPUT_JSON)

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

    # print_data_from_wix_order(INPUT_JSON)



    # order_test = OrderWixModel.parse_raw(INPUT_JSON)
    # print(order_test)
    # with open("cert/pubic_key.txt", "r") as f:
    #     public_key = serialization.load_ssh_public_key()
    #
    # gfj = jwt.decode("jhgkjgkjhlkhlljklnjuiolnkl.jbiougooyoigbiuoy.iuhouiguigugo", public_key, algorithms=["RS256"])
    # print(gfj)

    # data = create_data_for_presto(INPUT_JSON)
    # print(json.dumps(data, indent=4))
    create_data_for_presto(INPUT_JSON, OUTPUT_JSON)
