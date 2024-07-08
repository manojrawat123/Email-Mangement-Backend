"""emailmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from emailrouteschedule.views import EmailSheduleViews,SendScheduleEmail
from companycustomer.views import CustomerViews, SearchPageApiView, CustomerStatmentOfAmount, TransferCustomerView
from emailtemplate.views import EmailTemplateView
from rate.views import RateTableViews, RateSearchViewOrUpdate
from emaillog.views import EmailLogView 
from toproutes.views import AddTopRoutes, GetTopRouteTable
from invoice.views import InvoiceDetailCustomView
from dispute.views import DisputeDetailsViews
from myusersession.views import CustomTokenObtainPairView,VerifySessionView, UserRegisterView, GetAllUserView, ResetPassword, ForgotPassword
from countrycode.views import CountryEntryView
from payments.views import PaymentView
from vendorrate.views import VendorRateTableViews,VendorRateSearchViewOrUpdate, VendorRateByCountryCode,VendorTargetSheetByCountryCode
from vendorratetabel.views import VendorRateTabelView
from useripaddress.views import AddUserIpAddress
from menuaccess.views import MenuAccessApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('session/', VerifySessionView.as_view(), name='token_obtain_pair'),
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('myuser/', GetAllUserView.as_view(), name='my_user'),
    path('myuser/<int:id>/', GetAllUserView.as_view(), name='my_user'),
    path('reset-password/<userid_encode>/<token>/', ResetPassword.as_view(), name="Reset Password"),
    path('forgetpassword/', ForgotPassword.as_view(), name="forgot password email"),

    path('emailshedule/',EmailSheduleViews.as_view(),name=''),
    path('emailshedule/<int:pk>/', EmailSheduleViews.as_view(), name='email_schedule_detail'),
    path('customer/',CustomerViews.as_view(),name='customer_get'),
    path('customer/<int:pk>/', CustomerViews.as_view(), name='customer'),
    path('emailtemplate/',EmailTemplateView.as_view(),name=''),
    path('countrycode/',CountryEntryView.as_view(),name='country_code_view'),
    path('emailtemplate/<int:pk>/', EmailTemplateView.as_view(), name='email_template'),

    path('rate/',RateTableViews.as_view(),name=''),
    path('rate-search/',RateSearchViewOrUpdate.as_view(),name='rate-search'),
    path('rate-update-delete/<int:id>/',RateSearchViewOrUpdate.as_view(),name='rate-update-delete'),
    path('searchpage/', SearchPageApiView.as_view(), name='search_page'),
    path('searchpage/<int:id>/', SearchPageApiView.as_view(), name='search_page'),
    path('emaillog/',EmailLogView.as_view(),name='get_customer_email_templates'),
    path('toproute/',GetTopRouteTable.as_view(),name='get_customer_email_templates'),
    path('addroute/', AddTopRoutes.as_view(), name='add_top_route'),
    path('addroute/<int:id>/', AddTopRoutes.as_view(), name='add_top_route'),
    path('emaillog/<int:pk>/', EmailLogView.as_view(), name='email_log'),
    path('sendemailschedule/', SendScheduleEmail.as_view(), name='email_log'),

    path('invoices/', InvoiceDetailCustomView.as_view(), name='invoice-list-create'),
    path('getinvoices/', InvoiceDetailCustomView.as_view(), name='invoice-list-create'),
    path('getinvoices/<int:id>/', InvoiceDetailCustomView.as_view(), name='invoice-list-create'),
    path('dispute/', DisputeDetailsViews.as_view(), name='invoice-list-create'),
    path('payment/', PaymentView.as_view(), name='invoice-list-create'),
    path('payment/<int:id>/', PaymentView.as_view(), name='invoice-list-create'),

    path('dispute/<int:id>/', DisputeDetailsViews.as_view(), name='invoice-list-create'),
    path('invoices/<int:id>/', InvoiceDetailCustomView.as_view(), name='invoice-detail'),
    path('statementofamount/', CustomerStatmentOfAmount.as_view(), name='invoice-detail'),
    path('vendorrate/', VendorRateTableViews.as_view(), name='vendor-rate'),
    path('vendorrate/<int:id>/', VendorRateTableViews.as_view(), name='vendor-rate'),
    path('vendorratesearch/', VendorRateSearchViewOrUpdate.as_view(), name='vendor-rate'),
    path('vendorratesearch/<int:id>/', VendorRateSearchViewOrUpdate.as_view(), name='vendor-rate'),
    path('addvendorratepage/', VendorRateTabelView.as_view(), name='vendor-rate-tabel'),
    path('vendorratebycountrycode/', VendorRateByCountryCode.as_view(), name='vendor-rate-country-code'),
    path('vendortargetsheet/', VendorTargetSheetByCountryCode.as_view(), name='vendor-rate-country-code'),
    path('transfercustomer/', TransferCustomerView.as_view(), name='transfer-customer-view'),
    path('userip/', AddUserIpAddress.as_view(), name='add-user-ip'),
    path('userip/<int:id>/', AddUserIpAddress.as_view(), name='update-user-ip'),
    path('menuaccess/<int:id>/', MenuAccessApiView.as_view(), name='menu-access-api'),
]
