create database CustomerData;
use CustomerData;
create table customers(customer_id varchar(50),customer_name varchar(50),email varchar(100),phone_number varchar(20),adress varchar(250),registeration_date varchar(100),primary key(customer_id));
insert into customers values("C003","Keshav","keshav@gmail.com","9879843210","janakpuri,Delhi","25-07-2024");
create table products(product_id varchar(50),product_name varchar(50),category varchar(100),price decimal(10,2),stock_quantity int,primary key(product_id));
insert into products values("P003","LED","Electronics","20000","98");
create table orders(order_id varchar(50),customer_id varchar(50),product_id varchar(50),order_date datetime(6),order_amount decimal(10,2), foreign key(customer_id) references customers(customer_id), foreign key(product_id) references products(product_id),primary key (order_id));
insert into orders values("0003","C002","P003","7-08-2024","20000");
alter table orders add column shipment_status varchar(50);
create table payments(payment_id varchar(20),order_id varchar(50),payment_amount decimal(10,2),payment_date date,foreign key(order_id) references orders(order_id),primary key(payment_id));
select*from customers;
select*from products;
select*from orders;
delete from customers where customer_id="C004";
update products set stock_quantity=stock_quantity-1 where product_id="P003";
update products set stock_quantity=stock_quantity+1 where product_id="P003";
create table shipments (shipment_id VARCHAR(50),order_id VARCHAR(50),shipment_status VARCHAR(50),estimated_delivery_date DATE,carrier_name VARCHAR(50),tracking_link VARCHAR(255),FOREIGN KEY (order_id) REFERENCES orders(order_id),primary key(shipment_id));
insert into shipments values("S001","0001","Unshipped","12-09-24","Pushpak courier","xyxz")