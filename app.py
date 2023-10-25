import json

#read beverages.json
with open("beverages.json","r") as file:
    data=json.load(file)

#available bill for use
accepted_bill=[1,5,10,20,50,100]
accepted_bill.sort(reverse=True)

#declaration of dictionary for money return to the customer
money_return={"100":0,
              "50":0,
              "20":0,
              "10":0,
              "5":0,
              "1":0}

#print the title
def printTitle():
    print("=========================================")
    print("           VENDING MACHINE MENU          ")
    print("=========================================")

#print the item in beverages.json
def printMenu():
    for item in data['beverages']:
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Price: {item['price']}")
        print(f"Stock: {item['stock']}")
        print()

#find beverage by id
def find_by_id(ind):
    for item in data['beverages']:
        if item['id']==ind:
            return item
    return None

#let customer insert the amount of money they wanted
def get_user_bill():
    user_balance=0
    #let customer insert money until they wish to proceed to the next step
    while True:
        user_input=int(input("\nPlease insert bill: "))
        if user_input not in accepted_bill:
            print("Please insert the correct amount of bill.")
        else:
            user_balance=user_balance+user_input
            while True:
                cont=input("Do you wish to insert more bill? (Enter Y to continue): ")
                if cont.lower()=='y':
                    break
                else:
                    return user_balance

#get the beverage selection                
def get_user_selection():
    #keep looping until the player enter a correct beverage ID
    while True:
        try:
            ind=int(input("\nEnter Beverage ID: "))
            selected_drink=find_by_id(ind)
            if selected_drink:
                if selected_drink['stock']<=0:
                    print(f"{selected_drink['name']} is out of stock. Please try again")
                else:
                    return selected_drink['id'],selected_drink['name'],selected_drink['price']
            else:
                print("ID not found. Please try again.")
        except ValueError:
            print("Please enter a numerical number.")

#get every order from the customer
def get_user_order(balance):
    order_items=[]
    print("\n=========================================")
    print(f"Your balance is RM {balance}")
    while True:
        #call get_user_selection to get each beverage they wanted
        b_id,b_name,b_price=get_user_selection()

        if balance<b_price:
               print("You don't have enough balance.")
        else:
            balance=balance-b_price
            order_items.append((b_id,b_name,b_price))
        print(f"Your current balance is {balance}")

        if balance<=0:
              print("You will be proceed to the next step.")
              return order_items, balance
        else:
            cont=input(f"Do you wish to continue? (Enter Y to continue): ")
            if cont.lower()!='y':
                return order_items,balance

#display the receipt to customer
def print_receipt(order_items,balance):
    print("\nHere is your receipt.")
    print("=========================================")
    total=0
    ori_balance=balance

    #display each item order by customer
    for item in order_items:
        print(f"ID: {item[0]}, Name: {item[1]}, Price: RM {item[2]}")
        total=total+item[2]
        
    #to decide the best combination to dispense money back to customer 
    #by comparing largest bill to smallest with the available balance
    #e.g if balance is larger than RM50, then minus 50 from balance and increase the amount of RM50 in money_return by 1
    #greedy algorithm
    for i in accepted_bill:
        while balance>=i:
            balance=balance-i
            money_return[str(i)]=money_return[str(i)]+1

    print(f"\nTotal is RM {total}.")
    print("=========================================\n")

    if ori_balance>0:
        print("The machine will return: ")
        for key, quantity in money_return.items():
            if quantity>0:
                print(f"{quantity} piece(s) of RM {key}")

    print("\nEnjoy your drink!")

def main():
    #calling all functions
    printTitle()
    printMenu()
    balance=get_user_bill()
    order_items,balance=get_user_order(balance)
    print_receipt(order_items,balance)

main()