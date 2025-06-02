from django.shortcuts import render, redirect
from .models import Supplier, Product, Order

class SupplierAdmin:
    def index(request):
        return redirect('inventory:SupplierAdmin_list')
  
    def list(request):
        context = {
            'suppliers': Supplier.objects.all(),
        }
        return render(request, 'SupplierAdmin/list.html', context)
      
    def store(request):
        if request.method == 'POST':
            
            name = request.POST.get('name')
            contact_email = request.POST.get('contact_email')
            print(f"Received POST data: name={name}, contact_email={contact_email}")
            if name and contact_email:
                if int(request.POST.get('id')) > 0:
                    supplier_id = request.POST.get('id')
                    edited_supplier = Supplier.objects.filter(id=supplier_id).first()
                    edited_supplier.name = name
                    edited_supplier.contact_email = contact_email
                    edited_supplier.save()
                else:
                    Supplier.objects.create(name=name, contact_email=contact_email)

        return redirect('inventory:SupplierAdmin_list')
    
    def delete(request):
        if request.method == 'POST':
            id = request.POST.get('id')
            supplier = Supplier.objects.filter(id=id).first()
            if supplier:
                supplier.delete()
        return redirect('inventory:SupplierAdmin_list')
      
class ProductAdmin:
    def index(request):
        return redirect('inventory:ProductAdmin_list')

    def list(request):
        context = {
            'suppliers': Supplier.objects.all(),
            'products': Product.objects.all(),
        }
        return render(request, 'ProductAdmin/list.html', context)

    def store(request):
        if request.method == 'POST':
            
            name = request.POST.get('name')
            supplier_id = request.POST.get('supplier')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            is_discontinued = request.POST.get('is_discontinued') == 'false'

            print(f"Received POST data: name={name}, supplier_id={supplier_id}, price={price}, stock={stock}, is_discontinued={is_discontinued}")
            if name and supplier_id and price and stock:
                if int(request.POST.get('id')) > 0:
                    product_id = request.POST.get('id')
                    edited_item = Product.objects.filter(id=product_id).first()
                    edited_item.name = name
                    edited_item.supplier = Supplier.objects.filter(id=supplier_id).first()
                    edited_item.price = price
                    edited_item.stock = stock
                    edited_item.is_discontinued = is_discontinued
                    edited_item.save()
                else:
                    Product.objects.create(name=name,
                                           price=price,
                                           supplier=Supplier.objects.filter(id=supplier_id).first(),
                                           stock=stock,
                                           is_discontinued=is_discontinued)

        return redirect('inventory:ProductAdmin_list')
    
    def delete(request):
        if request.method == 'POST':
            id = request.POST.get('id')
            item = Product.objects.filter(id=id).first()
            if item:
                item.delete()
        return redirect('inventory:ProductAdmin_list')

class OrderAdmin:
    def index(request):
        return redirect('inventory:OrderAdmin_list')

    def list(request):
        context = {
            'orders': Order.objects.all(),
            'products': Product.objects.all(),
        }
        return render(request, 'OrderAdmin/list.html', context)
    
    def store(request):
        if request.method == 'POST':
            
            product_id = request.POST.get('product')
            quantity = request.POST.get('quantity')
            status = request.POST.get('status')
            print(f"Received POST data: product_id={product_id}, quantity={quantity}, status={status}")

            if product_id and quantity and status:
                productObject = Product.objects.filter(id=product_id).first()
                Order.objects.create(product=Product.objects.filter(id=product_id).first(),
                                        quantity=int(quantity),
                                        status=status)
                productObject.stock -= int(quantity)
                productObject.save()

        return redirect('inventory:OrderAdmin_list')
    
    def delete(request):
        if request.method == 'POST':
            id = request.POST.get('id')
            item = Order.objects.filter(id=id).first()
            if item:
                item.delete()
        return redirect('inventory:OrderAdmin_list')