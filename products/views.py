from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import Http404
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .models import Product, Category
from .forms import ProductForm

# Create your views here.
def show_products(request):
    '''
    View to display the products in shop
    Only active products are shown, unless user is superuser.
    Products are then filtered if there is a get request with 'q'
    Or filtered by category if get request with category
    And sorted if there is a get request with sort in it
    '''
    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(is_active=True)

    search_term = None
    category = None
    sort = None
    sort_direction = None

    # GET requests for search, categories and sorting
    if request.GET:
        # handles sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            # if sorting by product name, add lowercase name to model to sort
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            # if direction is descending then reverse the sorting
            if 'direction' in request.GET:
                sort_direction = request.GET['direction']
                if sort_direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # handles filtering by category
        if 'category' in request.GET:
            category = request.GET['category']
            category = get_object_or_404(Category, name=category)
            products = products.filter(category=category)

        # handles searches
        if 'q' in request.GET:
            search_term = request.GET['q']
            if not search_term:
                messages.error(
                    request,
                    "You didn't enter anything in the search box! Try again."
                    )
                return redirect(reverse('products'))
            matches_search = Q(
                name__icontains=search_term
                ) | Q(
                    description__icontains=search_term
                    )
            products = products.filter(matches_search)
    # used in context for select box to show the selected option
    current_sorting = f'{sort}_{sort_direction}'
    context = {
        'products': products,
        'search_term': search_term,
        'current_category': category,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    '''
    View to show individual product details from shop page
    Superuser can access the view for any products
    Other users can only access the view for active products
    '''
    product = get_object_or_404(Product, pk=product_id)
    if not product.is_active and not request.user.is_superuser:
        raise Http404
    else:
        context = {
            'product': product,
        }
        return render(request, 'products/product_details.html', context)


@login_required
def add_product(request):
    """
    View for admin user to add product from front end. Raise 403 if not admin.
    Post request: handle posting of the form, show success/errors messages.
    Get request: render the form
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'New product: { product.name } added!')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(
                request,
                'Product not added. Please check the form for errors and '
                're-submit.'
                )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    '''
    View for admin user to edit product from front end. Raise 403 if not admin.
    Post request: handle posting of the form, show success/errors messages,
    (check if category matches sku, if not generate sku before saving).
    Get request: render the form with the existing product details.
    '''
    if not request.user.is_superuser:
        raise PermissionDenied()
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if product.sku[:3] != product.category.name[:3].upper():
                product.sku = product.generate_sku()
            product.save()
            messages.success(
                request, f'Updates made to product: { product.name }!'
                )
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(
                request,
                'Product NOT updated. Please check the form for errors and '
                're-submit.'
                )
    else:
        form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'product': product,
        'form': form,
    }
    return render(request, template, context)

@require_POST
@login_required
def delete_product(request, product_id):
    """
    View for admin user to delete product from front end.
    Raise 403 if not admin.
    Post request only: delete product, show success message.
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(
        request, f'Product: "{ product.name }" deleted!'
        )
    return redirect(reverse('products'))


@require_POST
@login_required
def toggle_product_active_status(request, product_id):
    """
    View for admin user to amend active status on product from front end.
    Raise 403 if not admin.
    Post request only: delete product, show success message.
    Form is on products and product_details pages, so using hidden input
    to send request.path, and redirecting to this so user stays on same page
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    redirect_url = request.POST.get('redirect_url')
    product = get_object_or_404(Product, pk=product_id)
    product.is_active = not product.is_active
    product.save()
    messages.success(
        request,
        f'Status for product: "{ product.name }" updated to '
        f'{"Active" if product.is_active else "Not Active"}!'
        )
    return redirect(redirect_url)
