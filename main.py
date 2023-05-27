import pandas as pd
from abc import ABC, abstractmethod

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df['id'] == self.hotel_id, 'available'] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if a hotel is available"""
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        return availability == 'yes'

    @classmethod
    def get_hotel_count(cls, data):
        print(cls)
        return len(data)

    def __eq__(self, other):
        return self.hotel_id == other.hotel_id;


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class Ticket(ABC):

    @abstractmethod
    def generate(self):
        pass


class ReservationTicket(Ticket):
    def __init__(self, customer_name, hotel):
        self.customer_name = customer_name
        self.hotel = hotel

    def generate(self):
        return f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel Name: {self.hotel.name}
        """


class SpaReservationTicket:
    def __init__(self, customer_name, hotel):
        self.customer_name = customer_name
        self.hotel = hotel

    def generate(self):
        return f"""
        Thank you for your SPA reservation!
        Here are your SPA booking data:
        Name: {self.the_customer_name}
        Hotel Name: {self.hotel.name}
        """

    @property
    def the_customer_name(self):
        name = self.customer_name.strip()
        name = name.title()
        return name

    @staticmethod
    def convert(amount):
        return amount * 1.2


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = dict(number=self.number, expiration=expiration, holder=holder, cvc=cvc)
        return card_data in df_cards


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        return password == given_password


print(df)
hotel_id = input("Enter the id of the hotel: ")
hotel = SpaHotel(hotel_id)
if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate("mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(name, hotel)
            print(reservation_ticket.generate())
            spa_input = input("Do you want to book a spa package? ")
            if spa_input == "yes":
                hotel.book_spa_package()
                spa_reservation_ticket = SpaReservationTicket(name, hotel)
                print(spa_reservation_ticket.generate())
        else:
            print("Credit card authentication failed")
    else:
        print("There was a problem with your payment")
else:
    print("Hotel is not available.")
