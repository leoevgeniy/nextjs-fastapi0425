from datetime import datetime
from sqlalchemy import (Boolean, Column, Integer, TIMESTAMP, BIGINT, String, TEXT, FLOAT, ForeignKey, Text, Float)
from sqlalchemy.orm import relationship
from api.database.database import Base

   
class Order(Base):
    __tablename__ = "Order"
    id = Column(Integer, primary_key=True, index=True)
    paymentMethod = Column(String, nullable=False)
    deliveryMethod = Column(String, nullable=False)
    shippingAddress = Column(String, nullable=True, default=None)
    total_cost = Column(Float, nullable=False)
    delivery_cost = Column(FLOAT, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    delivered_at = Column(TIMESTAMP, nullable=True)
    is_paid = Column(Boolean, nullable=False, default=False)
    paid_at = Column(TIMESTAMP, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comments = Column(Text, nullable=True)
    status = Column(TEXT, nullable=True, default='Новый Заказ')
    user = relationship("User", back_populates="orders")
    orderItems = relationship("OrderItems", cascade='all, delete', back_populates="order")

    class Config:
        orm_mode = True

    def __str__(self):
        return str(self.id)
    
class OrderItems(Base):
    __tablename__ = "OrderItems"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Product.index"), nullable=False)
    product_name = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    qty = Column(Integer, nullable=False, default=0)
    cost = Column(Float, nullable=True, default=0)
    user = relationship("User", back_populates="orderItems")
    order = relationship("Order", back_populates="orderItems")
    # product = relationship("Product", back_populates="orderItem")

    class Config:
        orm_mode = True

    def __str__(self):

        return str(self.product_name)

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, nullable=True)
    order = Column(Integer, ForeignKey("Order.id"), nullable=True)
    amount = Column(String, nullable=True)
    income_amount = Column(String, nullable=True)
    confirmation_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    payment_method = Column(String, nullable=True)
    payment_method_id = Column(String, nullable=True)
    payment_method_saved = Column(Boolean, default=False)
    payment_method_title = Column(String)
    refundable = Column(Boolean, default=False)
    payment_card_data_expiry_year = Column(String, nullable=True)
    payment_card_data_expiry_month = Column(String, nullable=True)
    payment_card_data_card_type = Column(String, nullable=True)
    payment_card_data_issuer_country = Column(String,  nullable=True)
    payment_card_data_issuer_name = Column(String, nullable=True)
    payment_card_data_source = Column(String,  nullable=True)
    captured_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    expires_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    test = Column(Boolean,  default=False)
    refunded_amount = Column(String, nullable=True)
    terminal_key = Column(String, nullable=True)
    success = Column(Boolean, default=False)
    status = Column(String, default='CREATED')
    is_paid = Column(Boolean, default=False)
    auth_code = Column(String, nullable=True)
    three_d_secure_applied = Column(Boolean, default=False)
    rrn = Column(String, nullable=True)
    merchant_customer_id = Column(String, nullable=True)
    is_status_changed = Column(Boolean, default=False)
    error_code = Column(String, nullable=True)
    message = Column(String, nullable=True)
    details = Column(String, nullable=True)


class P5sOrder(Base):
    __tablename__ = "p5sorder"
    id = Column(Integer, primary_key=True, index=True)
    ResultStatus = Column(Integer, nullable=True, default=0)
    ResultStatusMsg = Column(String, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    orderID = Column(Integer, nullable=True, default=0)
    ExtOrderID = Column(Integer, ForeignKey("Order.id"), nullable=True)
    ExtDateOfAdded = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    ExtOrderPaid = Column(String, nullable=True)
    ExtOrderTotal = Column(String, nullable=True)
    ExtDeliveryCost = Column(String, nullable=True)
    dsDeliveryPriceTo = Column(String, nullable=True)
    dsDeliveryPriceBack = Column(String, nullable=True)
    dsDeliveryAgentMoney = Column(String, nullable=True)
    dsDelivery = Column(String, nullable=True)
    dsDeliveryDate = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    dsComments = Column(String, nullable=True)
    dsPickPointID = Column(String, nullable=True)
    dsFullAddress = Column(String,  nullable=True)
    orderDate = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    pickupDate = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    status = Column(String, nullable=True)
    orderTotal = Column(String, nullable=True)
    postDataCode = Column(String, nullable=True)
    postDataStatusName = Column(String, nullable=True)
    postDataTrackingUrl = Column(String, nullable=True)
    StatusHistoryId = Column(String,  nullable=True)
    StatusHistoryDate = Column(TIMESTAMP, nullable=True, default=datetime.utcnow())
    StatusHistoryLabel = Column(String,  nullable=True)
    MoneyHistoryID = Column(String, nullable=True)
    MoneyHistoryMoney = Column(String, nullable=True)
    MoneyHistoryDescription = Column(String, nullable=True)
    MoneyHistorytype = Column(String, nullable=True)
    MoneyHistoryDate = Column(TIMESTAMP,  nullable=True, default=datetime.utcnow())
    totalSum = Column(FLOAT, nullable=True)
    ExtTotalSum = Column(FLOAT, nullable=True)
    ExtDeliveryCost = Column(FLOAT, nullable=True)
    messages = Column(String, nullable=True)

    def __str__(self):
        return str(self.orderID)


class P5SOrderItems(Base):
    __tablename__ = 'p5sOrderItems'
    id = Column(Integer, primary_key=True, index=True)
    p5sorder_id = Column(Integer, ForeignKey("p5sorder.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Product.index"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    qty = Column(Integer, nullable=False, default=0)
    cost = Column(Float, nullable=True, default=0)