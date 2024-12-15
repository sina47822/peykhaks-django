# product/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Order, OrderItem  # Make sure Order is correctly imported
from weasyprint import HTML  # Assuming you're using WeasyPrint to generate the PDF
import jdatetime  # Import the jdatetime library

def generate_pdf(request, order_id):
    # Fetch Order
    order = get_object_or_404(Order, id=order_id)
    
    # Convert created_at to Jalali
    created_at_jalali = jdatetime.date.fromgregorian(date=order.created_at)

    # Initialize products and grand total calculation
    products = []
    grand_total = 0

    for order_item in order.orderitem_set.all():
        price = order_item.product.price
        offer_price = order_item.product.offer_price
        quantity = order_item.quantity
        discount_percentage = 0
        total_price = price * quantity

        if offer_price:
            if offer_price > 0:
                discount_percentage = ((price - offer_price) / price) * 100
                total_price = offer_price * quantity

        grand_total += total_price

        products.append({
            'title': order_item.product.title,
            'quantity': quantity,
            'price': price,
            'discount_percentage': f"{discount_percentage:.0f}%" if discount_percentage > 0 else "تخفیف ندارد",
            'total_price': f"{total_price:.0f} تومان"
        })

    # Render HTML template for the PDF content
    html_content = render_to_string('order/pdf_template.html', {
        'order': order,
        'products': products,
        'grand_total': f"{grand_total:.0f} تومان",
        'created_at_jalali': created_at_jalali.strftime('%Y/%m/%d'),  # Format the Jalali date
        'is_pdf': True,  # Optional flag for template customization
    })

    # Generate PDF from HTML
    pdf_file = HTML(string=html_content).write_pdf()

    # Return the PDF response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="فاکتور شماره {order.factor_number} آقای {order.customer.name}.pdf"'
    return response
