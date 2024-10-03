import streamlit as st
import mysql.connector
import pandas as pd
import datetime
st.set_page_config(page_title="Customer Management System",page_icon="https://th.bing.com/th?id=OIP.eSkteX6oCLXDpYbbgmHc9AHaHa&w=250&h=250&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2")
st.title("CUSTOMER MANAGEMENT SYSTEM")
choice=st.sidebar.selectbox("My Menu",("Home","Customer","Orders","Manage Stocks","Invoice & Payments","Shipment Tracking"))
st.write(choice)
if choice=="Home":
    st.image("https://th.bing.com/th/id/OIP.Y3Q_AIMjdoYeRGA4hWBtIAHaEK?w=329&h=184&c=7&r=0&o=5&pid=1.7")
    st.markdown("<center><h1>WELCOME</h1></center>",unsafe_allow_html=True)
    st.write("This is a web application developed by Richa Kaushik as a part of Training Project")
elif choice=="Customer":
    customer_choice=st.selectbox("Customer Features",("None","View Customers","Add Customer","Remove Customer"))
    if customer_choice=="View Customers":
        mydb=mysql.connector.connect(host="localhost",user="root",password="datascience",database="Customerdata")
        df=pd.read_sql("select*from customers",mydb)
        st.dataframe(df)
    elif customer_choice=="Add Customer":
        st.header("Add A New Customer")
        st.markdown("Please fil out the customer details below")
        customer_id = st.text_input("Enter Customer ID")
        name = st.text_input("Enter Name")
        email = st.text_input("Enter Email")
        phone = st.text_input("Enter Phone Number")
        address = st.text_input("Enter Address")
        registration_date = str(datetime.datetime.now())
        btn = st.button("Add Customer")
        if btn:
            mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
            c = mydb.cursor()
            c.execute("insert into customers values(%s, %s, %s, %s, %s, %s)",(customer_id, name, email, phone, address, registration_date))
            mydb.commit()
            st.header("Customer Added Successfully")
    elif customer_choice=="Remove Customer":
        st.header("Remove Customer")
        customer_id = st.text_input("Enter Customer ID")
        btn = st.button("Remove Customer")
        if btn:
             mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
             c = mydb.cursor()
             c.execute("delete from customers where customer_id=%s",(customer_id,))
             mydb.commit()
             st.header("Customer ID{customer_id} Removed Succesfully")
elif choice == "Orders":
    order_choice = st.selectbox("Order Features", ("None", "View Orders", "Add Order","Cancel Order"))
    if order_choice == "View Orders":
        mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
        df = pd.read_sql("select*from orders",mydb)
        st.dataframe(df)
    elif order_choice == "Add Order":
        st.header("Place A New Order")
        st.markdown("Please fil out the order details below")
        order_id = st.text_input("Enter Order ID")
        customer_id = st.text_input("Enter Customer ID")
        product_id = st.text_input("Enter Product ID")
        order_date = str(datetime.datetime.now())
        order_amount = st.text_input("Enter Order Amount")
        shipment_status= st.text_input("Enter Shipment Status")
        btn = st.button("Add Order")
        if btn:
            mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
            c = mydb.cursor()
            c.execute("select customer_id from customers where customer_id = %s", (customer_id,))
            customer = c.fetchone()
            if customer:
                c.execute("insert into orders values(%s,%s,%s,%s,%s,%s)",(order_id,customer_id,product_id,order_date,order_amount,shipment_status))
                mydb.commit()
                st.header("Order Placed Successfully")
            else:
                st.error(f"Customer ID {customer_id} does not exist in the customers table.")
    elif order_choice=="Cancel Order":
        st.header("Cancel order")
        order_id = st.text_input("Enter Order ID")
        btn = st.button("Remove Order")
        if btn:
             mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
             c = mydb.cursor()
             c.execute("delete from order where order_id=%s",(order_id,))
             mydb.commit()
             st.header("Order ID{order_id} Removed Succesfully")
elif choice == "Manage Stocks":
    manage_choice = st.selectbox("Manage Stocks features", ("None", "Update Stock", "Low Stock Alert", "Search Products"))
    if manage_choice == "Update Stock":
        product_id = st.text_input("Enter Product ID")
        quantity = st.number_input("Enter Quantity", min_value=1, step=1)
        action = st.selectbox("Select Action", ("Add Stock", "Deduct Stock"))
        btn = st.button("Update Stock")
        if btn:
            mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
            c = mydb.cursor()
            if action == "Add Stock":
                c.execute("UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s", (quantity, product_id))
            elif action == "Deduct Stock":
                c.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s", (quantity, product_id))
            mydb.commit()
            st.header("Stock Updated Successfully")
    elif manage_choice=="Low Stock Alert":
        st.header("Low Stock")
        mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
        df = pd.read_sql("SELECT * FROM products WHERE stock_quantity < 10", mydb)
        st.dataframe(df)
    elif manage_choice == "Search Products":
        search_term = st.text_input("Search for a product (by ID or name):")
        if search_term:
            mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
            query = """SELECT * FROM products WHERE product_id LIKE %s OR product_name LIKE %s"""
            df = pd.read_sql(query, mydb, params=(f"%{search_term}%", f"%{search_term}%"))
            if not df.empty:
                st.dataframe(df)
            else:
                st.write("No products found.")


        
elif choice=="Invoice & Payments":
    invoice_choice=st.selectbox("Invoice & Payments Features",("Invoice Generation","Payment Methods","Tax Calculations"))
    if invoice_choice=="Invoice Generation":
        st.header("Generate Invoice & payments")
        order_id = st.text_input("Enter Order ID")
        btn = st.button("Generate Invoice")
        if btn:
            mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
            df = pd.read_sql(f"SELECT * FROM orders WHERE order_id = '{order_id}'", mydb)
            st.dataframe(df)
    elif invoice_choice == "Payment Methods":
        st.header("Choose Payment Method")
        payment_method = st.selectbox("Select Payment Method", ("Credit Card", "Debit Card", "PayPal", "Net Banking"))
        st.write(f"You have selected: {payment_method}")
        if st.button("Proceed to Payment"):
            if payment_method == "Credit Card":
                card_number = st.text_input("Enter Card Number", type="password")
                expiry_date = st.text_input("Enter Expiry Date (MM/YY)")
                cvv = st.text_input("Enter CVV", type="password")
                amount=st.text_input("Enter Amount")
                if st.button("Pay"):
                    st.success("Payment successful via Credit Card!")
            elif payment_method == "Debit Card":
                card_number = st.text_input("Enter Card Number", type="password")
                expiry_date = st.text_input("Enter Expiry Date (MM/YY)")
                cvv = st.text_input("Enter CVV", type="password")
                amount=st.text_input("Enter Amount")
                if st.button("Pay"):
                    st.success("Payment successful via Debit Card!")
            elif payment_method == "PayPal":
                paypal_email = st.text_input("Enter PayPal Email")
                amount=st.text_input("Enter Amount")
                if st.button("Pay"):
                    st.success("Payment successful via PayPal!")
            elif payment_method == "Net Banking":
                bank_name = st.text_input("Enter Bank Name")
                account_number = st.text_input("Enter Account Number", type="password")
                amount=st.text_input("Enter Amount")
                if st.button("Pay"):
                    st.success("Payment successful via Net Banking!")

    elif invoice_choice=="Tax Calculations":
        st.header("Calculate tax here")
        order_amount = st.number_input("Enter Order Amount", min_value=0.0)
        tax_rate = 0.18  # Example tax rate of 18%
        tax_amount = order_amount * tax_rate
        st.write(f"Tax Amount: {tax_amount}")


elif choice == "Shipment Tracking":
    shipment_choice=st.selectbox("Shipment Tracking Features",("Update Shipment Status","Track shipment"))
    if shipment_choice=="Update Shipment Status":
        st.header("Update Shipment Status")
        update_order_id = st.text_input("Enter Order ID to update status:")
        new_status = st.text_input("Enter New Shipment Status:")
        if st.button("Update Status"):
            mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
            c = mydb.cursor()
            c.execute("UPDATE shipments SET shipment_status = %s WHERE order_id = %s", (new_status, update_order_id))
            mydb.commit()
            if c.rowcount > 0:
                st.success("Shipment status updated successfully!")
            else:
                st.warning("No shipment found with that Order ID.")
    elif shipment_choice=="Track shipment":
        st.header("Track Your Shipment")
        order_id = st.text_input("Enter Order ID to track:")
        if st.button("Track Shipment"):
            mydb = mysql.connector.connect(host="localhost", user="root", password="datascience", database="CustomerData")
            c = mydb.cursor()
            c.execute("SELECT shipment_status, estimated_delivery_date, carrier_name, tracking_link FROM shipments WHERE order_id = %s", (order_id,))
            shipment_info = c.fetchone()
            if shipment_info:
                status, delivery_date, carrier, tracking_link = shipment_info
                st.write(f"**Shipment Status:** {status}")
                st.write(f"**Estimated Delivery Date:** {delivery_date}")
                st.write(f"**Carrier:** {carrier}")
                if tracking_link:
                    st.write(f"[Track Shipment Here]({tracking_link})")
                else:
                    st.write("No tracking link available.")
            else:
                st.write("No shipment found for this Order ID.")

        

        

         
     







